import os, time, json, collections, re

# Target only the directories that matter for cleanup
scan_dirs = [
    "C:/Users/Admin/Downloads",
    "C:/Users/Admin/Desktop",
    "C:/Users/Admin/Documents",
    "C:/Users/Admin/Pictures",
    "C:/Users/Admin/Videos",
    "C:/Users/Admin/Music",
    "C:/Users/Admin/AppData/Local/Temp",
    "C:/Users/Admin/AppData/Roaming",
]

cutoff = 30  # more than 1 month

SUS_EXT = {'.exe','.dll','.scr','.bat','.cmd','.vbs','.ps1','.js','.jar','.msi',
           '.lnk','.iso','.dmp','.log','.bin','.sys','.drv','.cpl','.com','.pif',
           '.hta','.wsf','.jse','.apk','.deb','.rpm','.torrent','.crdownload',
           '.part','.dat','.reg','.html','.htm'}
SUS_PATTERNS = ['crack','keygen','patch','hack','activation','free','setup','install']
DOUBLE_EXT = re.compile(r'\.(exe|scr|bat|vbs|js|jar|msi|cmd)\.')

ext_counter = collections.defaultdict(lambda: [0, 0])
dir_counter = collections.defaultdict(lambda: [0, 0])
suspicious = []
big_old = []

now = time.time()

for scan_root in scan_dirs:
    if not os.path.isdir(scan_root):
        continue
    for dirpath, dirnames, filenames in os.walk(scan_root):
        dirnames[:] = [d for d in dirnames if d not in ('node_modules','.git','__pycache__','.cache')]
        parts = [p for p in dirpath.replace('\\','/').split('/') if p]
        # identify which target dir this is
        top1 = "Other"
        for t in scan_dirs:
            if dirpath.startswith(t):
                top1 = os.path.basename(t)
                break
        for fname in filenames:
            fpath = os.path.join(dirpath, fname)
            try:
                st = os.stat(fpath)
            except Exception:
                continue
            agedays = (now - st.st_atime) / 86400
            size = st.st_size
            if agedays < cutoff:
                continue
            ext = os.path.splitext(fname)[1].lower()
            ec = ext_counter[(top1, ext)]
            ec[0] += 1
            ec[1] += size
            dc = dir_counter[top1]
            dc[0] += 1
            dc[1] += size

            name_l = fname.lower()
            reasons = []
            if DOUBLE_EXT.search(name_l):
                reasons.append('double-extension')
            if ext in SUS_EXT and top1 in ['Downloads', 'Desktop', 'Temp', 'AppData']:
                reasons.append(f'exe-in-{top1}')
            for p in SUS_PATTERNS:
                if p in name_l:
                    reasons.append(p)
            if reasons and len(suspicious) < 20000:
                suspicious.append({'p': fpath, 's': size, 'age_days': round(agedays),
                                   'r': reasons, 'dir': top1})
            if size > 200 * 1024 * 1024:  # 200MB+
                big_old.append({'p': fpath, 's': size, 'age_days': round(agedays),
                                'ext': ext, 'dir': top1})

out = {
    'ext_families': [{'dir': d, 'ext': e, 'count': c[0], 'size': c[1]}
                     for (d, e), c in sorted(ext_counter.items(), key=lambda x: -x[1][1])[:120]],
    'dir_totals': [{'dir': d, 'count': c[0], 'size': c[1]}
                   for d, c in sorted(dir_counter.items(), key=lambda x: -x[1][1])],
    'suspicious_count': len(suspicious),
    'suspicious': sorted(suspicious, key=lambda x: -x['s'])[:8000],
    'big_old_count': len(big_old),
    'big_old': sorted(big_old, key=lambda x: -x['s']),
}

with open('C:/Users/Admin/Documents/Second Brain/pc_families.json', 'w') as f:
    json.dump(out, f)
print('written', len(suspicious), 'suspicious,', len(big_old), 'big,',
      len(ext_counter), 'families')