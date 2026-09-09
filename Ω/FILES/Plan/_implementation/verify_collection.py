"""Save reproducible checks without treating pending ASR/listening as completed."""
import argparse
import ast
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote
from datetime import datetime, timezone
ROOT=Path(__file__).resolve().parents[3]
HERE=Path(__file__).resolve().parent
SCRIPTS=ROOT/'Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/scripts'
sys.path.insert(0,str(SCRIPTS))
from common import digest, read_json, write_json, fingerprint
from assemble import validate_editorial

def main(tests=False, final=False):
    results={'checked_at':datetime.now(timezone.utc).isoformat(),'errors':[],'test_suites':[], 'artifacts':[]}
    if tests:
        suites=[('audio','Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/tests'),
            ('youtube','Skills/Domain/content-production/personal-content-workflow/youtube-transcript-pro/tests'),
            ('maintenance','Data/Plan/_implementation/tests'),('book-insight','Skills/Domain/content-production/personal-content-workflow/book-insight/tests')]
        env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONUTF8':'1'}
        for name,path in suites:
            result=subprocess.run([sys.executable,'-X','utf8','-B','-m','unittest','discover','-s',str(ROOT/path),'-v'],
                cwd=ROOT,env=env,capture_output=True,text=True,encoding='utf-8',errors='replace')
            (HERE/f'test_{name}.log').write_text(result.stdout+result.stderr,encoding='utf-8')
            results['test_suites'].append({'name':name,'exit_code':result.returncode})
            if result.returncode: results['errors'].append('test failed: '+name)
    for path in list(SCRIPTS.glob('*.py'))+list(HERE.glob('*.py')):
        try: ast.parse(path.read_text(encoding='utf-8'))
        except SyntaxError as exc: results['errors'].append(str(exc))
    for base in ['.agents/skills','.claude/skills']:
        for name in ['book-insight','learn-this','audio-transcribe-local']:
            path=ROOT/base/name
            if not (path/'SKILL.md').is_file(): results['errors'].append('broken registration: '+str(path))
    for name in ['learn-this','audio-transcribe-local','youtube-transcript-pro']:
        base=ROOT/'Skills/Domain/content-production/personal-content-workflow'/name
        for path in [base/'SKILL.md']+list((base/'references').glob('*.md')):
            for match in re.finditer(r'\]\(([^)]+)\)',path.read_text(encoding='utf-8')):
                target=match[1].split('#')[0]
                if target and not re.match(r'\w+://',target) and not (path.parent/target).exists():
                    results['errors'].append('broken skill link: '+str(path)+': '+target)
    output=ROOT/'Data/Transcripts'
    rows=read_json(output/'_reports/inventory.json',[])
    results['sources']=len(rows)
    results['duplicates']=sum(bool(r['duplicate_of']) for r in rows)
    results['source_hash_errors']=[]
    for row in rows:
        if digest(row['path'])!=row['sha256']:
            results['source_hash_errors'].append(row['file'])
        if row['duplicate_of']: continue
        work=output/'_work'/row['slug']
        raw=read_json(work/'raw.json')
        status={'slug':row['slug'],'asr':bool(raw),'editorial':False,'listening':'pending'}
        if raw:
            if raw['source_sha256']!=row['sha256'] or raw['content_hash']!=fingerprint(raw['segments']):
                results['errors'].append('raw provenance: '+row['slug'])
            for name in ['raw.json','raw.txt','raw.srt','quality_report.md','quality.json']:
                if not (work/name).is_file(): results['errors'].append('missing '+str(work/name))
            editorial,knowledge=read_json(work/'editorial.json'),read_json(work/'knowledge.json')
            if editorial is not None and knowledge is not None:
                try:
                    validate_editorial(raw,editorial,knowledge)
                    status['editorial']=True
                    status['segments']=len(raw['segments'])
                    status['claims']=len(knowledge['claims'])
                    assembly=read_json(work/'assembly.json',{})
                    if (assembly.get('raw_content_hash')!=raw['content_hash']
                        or assembly.get('editorial_sha256')!=digest(work/'editorial.json')
                        or assembly.get('knowledge_sha256')!=digest(work/'knowledge.json')):
                        results['errors'].append('stale assembly: '+row['slug'])
                    for suffix in ['TRANSCRIPT','KNOWLEDGE']:
                        if not (output/f'{row["slug"]}_{suffix}.md').is_file():
                            results['errors'].append('missing final artifact: '+row['slug']+suffix)
                except Exception as exc: results['errors'].append(row['slug']+': '+str(exc))
        if final and not status['editorial']: results['errors'].append('incomplete: '+row['slug'])
        results['artifacts'].append(status)
    results['errors']+=results['source_hash_errors']
    if final:
        if len(rows)!=13 or results['duplicates']!=1: results['errors'].append('inventory count mismatch')
        moves=read_json(HERE/'move_verification.json')
        if not moves or moves['errors']: results['errors'].append('move verification incomplete')
        for source_status in results['artifacts']:
            state=read_json(output/'_reports/checkpoint.json',{}).get('files',{}).get(source_status['slug'],{})
            if state.get('status')!='asr_complete': results['errors'].append('checkpoint incomplete: '+source_status['slug'])
        documents=list(output.glob('*.md'))+list((output/'_review').glob('*.md'))+list((output/'_reports').glob('*.md'))
        documents+=list((ROOT/'Data/Plan').glob('*.md'))+[ROOT/'Skills/README.md']
        for document in documents:
            for match in re.finditer(r'\]\(([^)]+)\)',document.read_text(encoding='utf-8')):
                link=match[1]
                if re.match(r'\w+://',link): continue
                target,_,fragment=link.partition('#')
                path=document.parent/unquote(target) if target else document
                if not path.exists(): results['errors'].append('broken output link: '+str(document)+': '+link)
                elif fragment and path.is_file() and path.suffix=='.md' and fragment.startswith(('S0','N')):
                    if f'id="{fragment}"' not in path.read_text(encoding='utf-8'):
                        results['errors'].append('broken anchor: '+str(document)+': '+link)
        samples=read_json(output/'_review/samples.json',[])
        if len(samples)!=4: results['errors'].append('listening samples missing')
        for sample in samples:
            if digest(output/'_review'/sample['file'])!=sample['clip_sha256']:
                results['errors'].append('listening sample changed: '+sample['file'])
    write_json(HERE/('FINAL_VERIFICATION.json' if final else 'verification.json'),results)
    print(json.dumps({'errors':results['errors'],'test_suites':results['test_suites'],
        'sources':len(rows),'asr_complete':sum(r['asr'] for r in results['artifacts']),
        'editorial_complete':sum(r['editorial'] for r in results['artifacts'])},ensure_ascii=False))
    return bool(results['errors'])

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--tests',action='store_true')
    p.add_argument('--final',action='store_true')
    args=p.parse_args()
    raise SystemExit(int(main(args.tests,args.final)))
