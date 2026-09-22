#!/usr/bin/env python3
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
