#!/usr/bin/env python3
"""One-shot Ubuntu application-state recovery bundle; Python 3.10+ and GnuPG."""
import datetime as dt
import getpass
import hashlib
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tarfile
import tempfile

HOME = Path.home().resolve()
BRAIN = HOME / 'Documents/second-brain'
TARGET = BRAIN / 'setting/system-recovery'
ARCHIVES = TARGET / 'archives'
NOW = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%SZ')
ARCHIVE = ARCHIVES / ('ubuntu-recovery-' + NOW + '.tar.gz.gpg')

README = '''# Ubuntu / Hermes / 9Router — Disaster Recovery

## Read this first
This folder is a **portable, encrypted application-setup backup**; it is **NOT** a bootable image of Ubuntu, and it is NOT proof that every browser login can be migrated. `archives/` contains encrypted secrets and must be copied OFF this VM (encrypted external storage or an appropriately managed private backup). A directory on the same VM is not disaster recovery. The Second Brain itself is EXCLUDED from the application archive to avoid recursively backing up this folder: back up / sync the entire Second Brain separately and verify that your remote copy contains it.

## Contents
- `backup.py`: rerunnable snapshot script. Use `python3 setting/system-recovery/backup.py` from any directory, or run it by absolute path.
- `restore.py`: decrypts and **extracts into a new staging directory** without overwriting an existing Ubuntu installation. Use `python3 restore.py /path/to/ubuntu-recovery-*.tar.gz.gpg`.
- `archives/ubuntu-recovery-<UTC>.tar.gz.gpg`: AES-256 OpenPGP symmetric encrypted archive. **Passphrase is NEVER stored here.** Lose the passphrase = lose this backup. If you upload this file to GitHub, you risk its file-size limit; use a separate encrypted-backup destination or Git LFS explicitly. This folder does not automatically push Git commits.

## Captured
- Almost all of `/home/<username>` (Hermes config/profiles/skills/agents/cron/sessions/projects, 9Router state including provider/combo/credential database, installed source, BrowserSkill, Chrome profile, SSH/GnuPG, shell config, other apps). Exclusions: entire `Documents/second-brain`, `.cache` and Trash, runtime Chromium crash dumps, the temporary recovery build. Keep the Second Brain separately backed up.
- SQLite online snapshots for `~/.9router/db/data.sqlite` and `~/.hermes/browser-parallel-queue/jobs.sqlite3`, stored separately under `snapshots/` in archive and intended to be copied over their corresponding extracted home paths before restoration. Live DB originals and WAL/SHM files are skipped to avoid inconsistent copies.
- If passwordless cached sudo was authorized: `/etc`, `/opt`, `/srv`, `/usr/local`, `/var/lib/9router`, `/var/lib/hermes`, cron spool (where present) in `system-files.tar`, including systemd services (sensitive; archive is encrypted).
- `manifest/`: OS details, package versions and manual apt packages, global npm packages, Python packages in Hermes venv, service definitions/enablement, crontabs, storage inventory, repository remotes and HEAD commits when available, backup warnings. Treat plain manifest as sensitive if sharing.
- 9Router global npm binary is NOT required inside the backup when npm global list has a version: reinstall with `npm i -g 9router@<RECORDED_VERSION>` then restore DB. Likewise, rebuilding Python venv is often safer than copying an old interpreter environment into a new OS.

## Recovery on fresh Ubuntu (not in-place overwrite)
1. Restore Second Brain first from your separate offsite backup, and bring the encrypted archive and its passphrase to the new machine. Install `sudo apt update && sudo apt install -y gnupg python3 python3-venv tar git nodejs npm` (Node and npm versions should match manifest; use your normal Node version manager if present).
2. Run `python3 restore.py archives/ubuntu-recovery-YYYY...tar.gz.gpg`. Enter passphrase. It extracts under `~/ubuntu-recovery-staging-...` without modifying `~/.hermes` or any live services. Check `manifest/`, `home/<username>`, and `system-files.tar` (if present). Source machine username may differ.
3. If user/path agree, STOP old services before data replacement: `systemctl --user stop hermes-gateway`; `sudo systemctl stop 9router` if configured. For exact restore of user state from STAGING, after reviewing: `rsync -a --exclude=.cache --exclude=Documents/second-brain STAGING/home/<olduser>/ "$HOME/"`. Rsync overlays files and may change existing config: run `rsync -ani` FIRST. If rsync is missing `sudo apt install rsync`.
4. Restore the online DB snapshots AFTER overlay and BEFORE service start: copy `STAGING/snapshots/home/<olduser>/.9router/db/data.sqlite` to `~/.9router/db/data.sqlite`, and BrowserSkill jobs SQLite similarly, if present. Set permissions to your new user. Keep any original files backed up rather than deleting them.
5. Review `system-files.tar` using `tar -tf STAGING/system-files.tar`; restore only needed `/etc/systemd/system/...` and `/etc/...` entries with appropriate sudo, do NOT blindly replace new Ubuntu `/etc`, SSH host keys, machine IDs, passwd/group or kernel config. Run `systemctl daemon-reload` and `systemctl --user daemon-reload` after services are reviewed. Reinstall exact package versions from manifest where possible; Python wheels/browser native dependencies may need rebuilding.
6. Verify `9router` and `hermes` executables, check 9Router `:20128` and its model aliases (`medium`, `reasoning`), inspect Telegram tokens without printing them, test `bskq doctor`, `bskq status`, and ensure only ONE polling gateway per Telegram bot token. Browser login cookies may be encrypted against the old desktop keyring and require sign-in again.
7. Restart only one gateway after verification: `systemctl --user start hermes-gateway`. Inspect `journalctl --user -u hermes-gateway -n 100 --no-pager` and corresponding 9Router log. Resume missions from verified state; do not blindly retry already-sent BrowserSkill tasks.

## Operational warnings
- This is a point-in-time backup while apps may be running. SQLite critical DBs use online backup; other changing files may not form an atomic image. For a perfect system-level restore, ALSO make a powered-off VMware/Hyper-V/Proxmox VM snapshot or full-disk image and keep it off the affected disk.
- Password-protect and restrict archive: it can contain API keys, Telegram bot tokens, SSH private keys, cookies, 9Router credentials and personal files. NEVER commit decrypted content, `.env` or raw SQLite to a repository. Rotating credentials may be necessary if a backup leaks.
- Archive passphrase is entered via hidden TTY input and passed to GPG via a private FD. No encryption password is saved in a script, README or shell history.
- `backup.py` will not silently claim success if key snapshot/encryption fails. Read `manifest/backup-report.json` after extracting; missing root snapshot is reported and root-files restore is incomplete.
'''

RESTORE = r'''#!/usr/bin/env python3
import datetime as dt, getpass, os, pathlib, subprocess, sys, tarfile, tempfile, shutil
if len(sys.argv)!=2: raise SystemExit('Usage: python3 restore.py /path/to/ubuntu-recovery-YYYY.tar.gz.gpg')
f=pathlib.Path(sys.argv[1]).expanduser().resolve()
if not f.is_file(): raise SystemExit('Archive not found: '+str(f))
if not shutil.which('gpg'): raise SystemExit('Install GnuPG: sudo apt install gnupg')
out=pathlib.Path.home()/('ubuntu-recovery-staging-'+dt.datetime.now().strftime('%Y%m%d-%H%M%S'))
if out.exists(): raise SystemExit('Destination exists: '+str(out))
out.mkdir(mode=0o700)
pw=getpass.getpass('Recovery passphrase (hidden): ')
r,w=os.pipe()
try:
 with tempfile.TemporaryFile() as plain:
  p=subprocess.Popen(['gpg','--batch','--yes','--pinentry-mode','loopback','--passphrase-fd',str(r),'--decrypt',str(f)],stdin=subprocess.DEVNULL,stdout=plain,stderr=subprocess.PIPE,pass_fds=(r,))
  os.close(r);r=-1;os.write(w,pw.encode()+b'\n');os.close(w);w=-1
  err=p.communicate()[1]
  if p.returncode: raise RuntimeError('GPG decrypt FAILED: '+err.decode(errors='replace')[-1600:])
  plain.seek(0)
  with tarfile.open(fileobj=plain,mode='r:gz') as t:
   # Prevent any archive path from escaping the designated staging directory.
   t.extractall(out,filter='data')
 print('RESTORED TO:',out,'(STAGING ONLY; no live files overwritten)')
 print('READ FIRST:',out/'manifest/backup-report.json')
 print('Copy SQLite snapshots only AFTER reviewing README; system-files.tar MUST NOT be blindly extracted over /etc.')
except Exception:
 shutil.rmtree(out,ignore_errors=True)
 raise
finally:
 if r>=0: os.close(r)
 if w>=0: os.close(w)
'''

def run_capture(args, timeout=100):
    try:
        p = subprocess.run(args, capture_output=True, text=True, timeout=timeout, check=False)
        return {'exit': p.returncode, 'stdout': p.stdout[-100000:], 'stderr': p.stderr[-12000:]}
    except Exception as e:
        return {'error': type(e).__name__ + ': ' + str(e)}

def main():
    if not BRAIN.is_dir():
        sys.exit('Second Brain not found at ' + str(BRAIN) + '; no backup written. Adjust BRAIN in script if moved.')
    if not shutil.which('gpg'):
        sys.exit('GnuPG required: sudo apt install gnupg; no backup written.')
    TARGET.mkdir(parents=True, exist_ok=True)
    ARCHIVES.mkdir(parents=True, exist_ok=True)
    os.chmod(TARGET, 0o700)
    os.chmod(ARCHIVES, 0o700)
    (TARGET/'backup.py').write_text(Path(__file__).read_text(encoding='utf-8'),encoding='utf-8')
    (TARGET/'restore.py').write_text(RESTORE,encoding='utf-8')
    (TARGET/'README.md').write_text(README,encoding='utf-8')
    (TARGET/'.gitignore').write_text('archives/\n*.tar.gz\n*.sqlite\n*.sqlite3\n',encoding='utf-8')
    print('DESTINATION:', TARGET, flush=True)
    print('NOTE: second-brain content is excluded from the application archive; back it up separately.', flush=True)
    pass1=getpass.getpass('NEW archive passphrase (hidden; SAVE IT OUTSIDE THIS VM): ')
    if len(pass1)<12: sys.exit('Passphrase must be at least 12 characters; not creating archive.')
    pass2=getpass.getpass('Repeat archive passphrase: ')
    if pass1!=pass2: sys.exit('Passphrases do not match; not creating archive.')
    warnings=[]
    with tempfile.TemporaryDirectory(prefix='ubuntu-recovery-',dir='/tmp') as temp:
        work=Path(temp)
        os.chmod(work,0o700)
        manifest=work/'manifest'; manifest.mkdir()
        snapshots=work/'snapshots'; snapshots.mkdir()
        m = {'timestamp_utc': NOW, 'home': str(HOME), 'second_brain': str(BRAIN), 'excluded': [str(BRAIN),'~/.cache','~/.local/share/Trash'], 'sqlite_snapshots': [], 'warnings':warnings, 'system_archive_included':False}
        probes={
            'os-release': ['bash','-lc','cat /etc/os-release'],
            'uname': ['uname','-a'],
            'dpkg-packages': ['dpkg-query','-W','-f=${binary:Package} ${Version}\n'],
            'apt-manual': ['apt-mark','showmanual'],
            'snap-list': ['snap','list'],
            'npm-global': ['npm','list','-g','--depth=0','--json'],
            'node-version': ['node','--version'],
            'npm-version': ['npm','--version'],
            'python-version': [sys.executable,'--version'],
            'hermes-venv-pip': [str(HOME/'.hermes/hermes-agent/venv/bin/python'),'-m','pip','freeze'],
            'systemd-user-services': ['systemctl','--user','list-unit-files','--no-pager'],
            'systemd-system-services': ['systemctl','list-unit-files','--no-pager'],
            'user-crontab': ['crontab','-l'],
            'git-remotes-second-brain': ['git','-C',str(BRAIN),'remote','-v'],
            'git-commit-second-brain': ['git','-C',str(BRAIN),'rev-parse','HEAD'],
            'disk-usage': ['df','-h'],
            '9router-service': ['systemctl','cat','9router'],
            'hermes-gateway-service': ['systemctl','--user','cat','hermes-gateway'],
        }
        for name,cmd in probes.items():
            result=run_capture(cmd)
            # Remotes can carry username/password; do not include their raw value.
            if name=='git-remotes-second-brain':
                result['stdout']='[REDACTED: remotes may embed credentials; run git remote -v on restored repo]'
            (manifest/(name+'.json')).write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding='utf-8')
        dbs=[HOME/'.9router/db/data.sqlite',HOME/'.hermes/browser-parallel-queue/jobs.sqlite3']
        skip_sqlite=set()
        for db in dbs:
            if not db.exists():
                warnings.append('DB not found: '+str(db))
                continue
            relative=db.relative_to(HOME)
            dest=snapshots/'home'/HOME.name/relative
            dest.parent.mkdir(parents=True,exist_ok=True)
            try:
                src=sqlite3.connect('file:'+str(db)+'?mode=ro',uri=True,timeout=35)
                dst=sqlite3.connect(str(dest),timeout=35)
                try: src.backup(dst,pages=256,sleep=0.1)
                finally: src.close();dst.close()
                probe=sqlite3.connect(str(dest))
                try:
                    check=probe.execute('PRAGMA quick_check').fetchone()[0]
                    if check!='ok': raise RuntimeError('SQLite quick_check: '+str(check))
                finally:probe.close()
                m['sqlite_snapshots'].append(str(dest.relative_to(work)))
                skip_sqlite.update({db,Path(str(db)+'-wal'),Path(str(db)+'-shm')})
                print('SQLITE OK:',relative,flush=True)
            except Exception as exc:
                raise RuntimeError('CRITICAL DB SNAPSHOT FAILED for '+str(db)+': '+str(exc)) from exc
        # This sudo archive captures root-level config/service dirs when -v has been authorized.
        if shutil.which('sudo') and subprocess.run(['sudo','-n','true'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:
            root_candidates=['/etc','/opt','/srv','/usr/local','/var/lib/9router','/var/lib/hermes','/var/spool/cron/crontabs']
            root_entries=[x.lstrip('/') for x in root_candidates if Path(x).exists()]
            if root_entries:
                rt=work/'system-files.tar'
                cmd=['sudo','-n','tar','-C','/','-cpf',str(rt),'--warning=no-file-changed',*root_entries]
                run=subprocess.run(cmd,capture_output=True,text=True)
                if run.returncode!=0:
                    raise RuntimeError('Root archive failed; not claiming full backup: '+run.stderr[-1600:])
                subprocess.run(['sudo','-n','chown',str(os.getuid())+':'+str(os.getgid()),str(rt)],check=True)
                m['system_archive_included']=True
                m['root_entries']=root_entries
                print('ROOT CONFIG SNAPSHOT OK:',', '.join(root_entries),flush=True)
        else:
            warnings.append('NO ROOT ARCHIVE: run sudo -v before backup.py, then rerun; only home state is backed up.')
        (manifest/'backup-report.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
        tarpath=work/'payload.tar.gz'
        count=[0]
        def filter_entry(info):
            p=Path('/'+info.name)
            if p == BRAIN or BRAIN in p.parents: return None
            if p == TARGET/'archives' or TARGET/'archives' in p.parents:return None
            if p == HOME/'.cache' or HOME/'.cache' in p.parents:return None
            if p == HOME/'.local/share/Trash' or HOME/'.local/share/Trash' in p.parents:return None
            if p in skip_sqlite:return None
            if p.name in ('core','core.dump') and info.size>50000000:return None
            count[0]+=1
            return info
        print('PACKING HOME, manifests, SQLite snapshots and root config; may take time...',flush=True)
        with tarfile.open(tarpath,'w:gz',dereference=False) as arc:
            arc.add(HOME,arcname=str(HOME).lstrip('/'),filter=filter_entry,recursive=True)
            arc.add(manifest,arcname='manifest')
            arc.add(snapshots,arcname='snapshots')
            if m['system_archive_included']:arc.add(work/'system-files.tar',arcname='system-files.tar')
        m['home_entry_count']=count[0]
        m['payload_size_bytes']=tarpath.stat().st_size
        (manifest/'backup-report.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
        # Also write an updated report outside the archive for immediate inspection.
        (TARGET/'LAST_BACKUP_REPORT.json').write_text(json.dumps(m,indent=2,ensure_ascii=False),encoding='utf-8')
        with tarfile.open(tarpath,'r:gz') as t:
            assert 'snapshots' in t.getnames() and 'manifest' in t.getnames()
        partial=ARCHIVES/(ARCHIVE.name+'.partial')
        with open(tarpath,'rb') as src:
            r,w=os.pipe()
            try:
                proc=subprocess.Popen(['gpg','--batch','--yes','--pinentry-mode','loopback','--passphrase-fd',str(r),'--symmetric','--cipher-algo','AES256','--compress-algo','none','--output',str(partial)],stdin=src,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,pass_fds=(r,))
                os.close(r);r=-1;os.write(w,pass1.encode()+b'\n');os.close(w);w=-1
                stderr=proc.communicate()[1]
                if proc.returncode:raise RuntimeError('GPG encryption failed: '+stderr.decode(errors='replace')[-1000:])
            finally:
                if r>=0:os.close(r)
                if w>=0:os.close(w)
        os.chmod(partial,0o600)
        os.replace(partial,ARCHIVE)
        sha=hashlib.sha256()
        with ARCHIVE.open('rb') as f:
            for chunk in iter(lambda:f.read(1024*1024),b''):sha.update(chunk)
        (TARGET/'LATEST_SHA256.txt').write_text(sha.hexdigest()+'  '+ARCHIVE.name+'\n',encoding='utf-8')
    print('SUCCESS ENCRYPTED ARCHIVE:',ARCHIVE,flush=True)
    print('ARCHIVE MB:',round(ARCHIVE.stat().st_size/1024**2,1),'SHA256:',sha.hexdigest(),flush=True)
    print('README:',TARGET/'README.md',flush=True)
    if warnings:print('WARNINGS:',*warnings,sep='\n- ',flush=True)
    print('NEXT: copy archive AND Second Brain to offsite storage; keeping them only on this Ubuntu VM will NOT protect from disk/VM loss.',flush=True)

if __name__=='__main__':main()
