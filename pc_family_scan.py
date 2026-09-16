import os, time, json, collections, re

scan_root = "C:/Users/Admin"
cutoff = 30  # more than 1 month

skip_dirs = {'$Recycle.Bin', 'System Volume Information', 'node_modules', '.git',
             '__pycache__', '.cache'}

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

for dirpath, dirnames, filenames in os.walk(scan_root):
    dirnames[:] = [d for d in dirnames if d not in skip_dirs]
    parts = [p for p in dirpath.replace('\\','/').split('/') if p]
    top1 = parts[3] if len(parts) > 3 else '/'.join(parts[-2:])
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
        if ext in SUS_EXT and any(d in parts for d in
                                  ['Downloads', 'Desktop', 'Temp', 'AppData']):
            reasons.append('exe-in-user-area')
        for p in SUS_PATTERNS:
            if p in name_l:
                reasons.append(p)
        if reasons and len(suspicious) < 20000:
            suspicious.append({'p': fpath, 's': size, 'age_days': round(agedays),
                               'r': reasons})
        if size > 200 * 1024 * 1024:  # 200MB+
            big_old.append({'p': fpath, 's': size, 'age_days': round(agedays),
                            'ext': ext})

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
