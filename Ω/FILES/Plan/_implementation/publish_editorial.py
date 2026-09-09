"""Expand manually authored review notes; never invent or automatically review ASR content."""
import argparse
from pathlib import Path
import sys
from datetime import date
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'Skills/Domain/content-production/personal-content-workflow/audio-transcribe-local/scripts'))
from common import read_json, write_json, fingerprint
from assemble import assemble, index

def publish(slug):
    output=ROOT/'Data/Transcripts'
    spec=read_json(output/'_editorial'/f'{slug}.json')
    work=output/'_work'/slug
    raw=read_json(work/'raw.json')
    if spec['raw_hash']!=fingerprint(raw['segments']) or spec['segments']!=len(raw['segments']):
        raise ValueError('Manual review notes do not match this raw transcript')
    unclear=set(spec.get('unclear',[]))
    segment_ids=[s['id'] for s in raw['segments']]
    for first,last in spec.get('unclear_ranges',[]):
        start,end=segment_ids.index(first),segment_ids.index(last)
        if end<start: raise ValueError('Reversed manual uncertainty range')
        unclear.update(segment_ids[start:end+1])
    for segment in raw['segments']:
        if any(term.casefold() in segment['text'].casefold() for term in spec.get('flag_terms',[])):
            unclear.add(segment['id'])
    editorial={'title':spec['title'],'raw_content_hash':spec['raw_hash'],
        'reviewed_segment_ids':[s['id'] for s in raw['segments']],
        'corrections':spec.get('corrections',{}),'unclear_segments':sorted(unclear),
        'chapters':[{'start_id':sid,'title':title} for sid,title in spec.get('chapters',[])]}
    claims=[]
    for claim in spec.get('claims',[]):
        claims.append({'id':claim['id'],'text':claim['text'],'confidence':claim.get('confidence','vừa'),
            'confidence_reason':claim.get('why','Có lời trực tiếp trong văn bản; chưa nghe duyệt hoặc kiểm chứng bên ngoài.'),
            'evidence':[{'segment_id':sid,'quote':quote} for sid,quote in claim['quotes']],
            'verification':'chưa kiểm chứng'})
    created=spec.get('created',read_json(work/'knowledge.json',{}).get('created',date.today().isoformat()))
    knowledge={'created':created,'claims':claims,'nodes':spec.get('nodes',[]),
        'open_questions':spec.get('open_questions',[]),'practice':spec.get('practice',[])}
    write_json(work/'editorial.json',editorial)
    write_json(work/'knowledge.json',knowledge)
    assemble(work,output)
    index(output)
    print(f'Published {slug}: {len(raw["segments"])} reviewed segments, {len(claims)} claims')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('slugs',nargs='+')
    args=p.parse_args()
    for slug in args.slugs: publish(slug)
