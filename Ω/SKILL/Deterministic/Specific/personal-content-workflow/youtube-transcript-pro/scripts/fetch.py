"""Fetch one video's subtitles; preserve language, provenance and legitimate repetition."""
import argparse
import html
import json
from pathlib import Path
import re
from urllib.parse import parse_qs, urlparse
import yt_dlp as yt

def extract_video_id(value):
    if re.fullmatch(r'[\w-]{11}',value,re.ASCII):
        return value
    p=urlparse(value)
    host=(p.hostname or '').lower()
    parts=p.path.strip('/').split('/')
    ident=''
    if host in {'youtu.be','www.youtu.be'}:
        ident=parts[0]
    elif host in {'youtube.com','www.youtube.com','m.youtube.com','music.youtube.com'}:
        ident=parse_qs(p.query).get('v',[''])[0] if p.path=='/watch' else (parts[1] if len(parts)>1 and parts[0] in ['embed','shorts','v','live'] else '')
    if not re.fullmatch(r'[\w-]{11}',ident,re.ASCII):
        raise ValueError('Invalid YouTube URL or video ID')
    return ident

def choose_subtitle(info,lang=None,auto=False):
    manual=info.get('subtitles') or {}
    automatic=info.get('automatic_captions') or {}
    available=list(dict.fromkeys(([] if auto else list(manual))+list(automatic)))
    preferred=[lang,lang+'-orig'] if lang else ['vi-orig','vi','en-orig','en']+available
    if lang:
        for source,is_auto in ([(automatic,True)] if auto else [(manual,False),(automatic,True)]):
            for language in preferred:
                if source.get(language): return language,is_auto
    else:
        for language in preferred:
            if not auto and manual.get(language): return language,False
            if automatic.get(language): return language,True
    raise ValueError(f'No subtitles for requested language {lang}' if lang else 'No subtitles available')

def download_transcript(url,lang=None,auto=False,output_dir='.'):
    try:
        ident=extract_video_id(url)
        canonical=f'https://www.youtube.com/watch?v={ident}'
        directory=Path(output_dir).resolve()
        directory.mkdir(parents=True,exist_ok=True)
        with yt.YoutubeDL({'quiet':True,'noplaylist':True}) as ydl:
            info=ydl.extract_info(canonical,download=False)
        language,automatic=choose_subtitle(info,lang,auto)
        options={'quiet':True,'noplaylist':True,'skip_download':True,'writesubtitles':not automatic,
            'writeautomaticsub':automatic,'subtitleslangs':[language],'subtitlesformat':'vtt',
            'outtmpl':str(directory/f'transcript_{ident}.%(ext)s')}
        with yt.YoutubeDL(options) as ydl:
            data=ydl.extract_info(canonical,download=True)
        subtitle=(data.get('requested_subtitles') or {}).get(language,{})
        candidate=Path(subtitle.get('filepath') or directory/f'transcript_{ident}.{language}.vtt').resolve()
        if not candidate.is_relative_to(directory) or not candidate.name.startswith(f'transcript_{ident}.') or not candidate.is_file():
            raise FileNotFoundError('The selected video/language subtitle was not downloaded')
        translated='tlang' in parse_qs(urlparse(subtitle.get('url','')).query)
        meta={'id':ident,'title':info.get('title'),'url':canonical,'language':language,
            'source':'auto_translated' if translated else 'auto_native' if automatic else 'manual'}
        candidate.with_suffix('.meta.json').write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')
        return str(candidate),None
    except Exception as exc:
        return None,str(exc)

def timestamp(value):
    result=0.
    for part in value.replace(',','.').split(':'): result=result*60+float(part)
    return result

def clean_text(text):
    previous_tokens,previous_end,lines=[],-1,[]
    timing=re.compile(r'(?P<start>(?:\d+:)?\d{2}:\d{2}[.,]\d{3})\s*-->\s*(?P<end>(?:\d+:)?\d{2}:\d{2}[.,]\d{3})')
    for block in re.split(r'\n\s*\n',text.replace('\r\n','\n')):
        match=timing.search(block)
        if not match: continue
        body=block[match.end():].split('\n',1)
        body=html.unescape(re.sub(r'<[^>]*>','',body[1] if len(body)>1 else ''))
        tokens=re.sub(r'\s+',' ',body).strip().split()
        original=tokens[:]
        start,end=timestamp(match['start']),timestamp(match['end'])
        # Only overlapping cues are rolling captions, not repetitions later in speech.
        if start<previous_end:
            for n in range(min(len(previous_tokens),len(tokens)),0,-1):
                if previous_tokens[-n:]==tokens[:n]:
                    tokens=tokens[n:]
                    break
        if tokens: lines.append(' '.join(tokens))
        previous_tokens,previous_end=original,end
    return '\n'.join(lines)

def clean_transcript(vtt_file,output_file=None):
    source=Path(vtt_file)
    target=Path(output_file) if output_file else source.with_suffix('.txt')
    body=clean_text(source.read_text(encoding='utf-8-sig'))
    if not body.strip(): raise ValueError('No subtitle text after parsing')
    target.write_text(body+'\n',encoding='utf-8')
    return str(target)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('video')
    p.add_argument('--lang','-l')
    p.add_argument('--auto','-a',action='store_true')
    p.add_argument('--clean','-c',action='store_true')
    p.add_argument('--output-dir',default='.')
    args=p.parse_args()
    output,error=download_transcript(args.video,args.lang,args.auto,args.output_dir)
    if error: p.exit(1,error+'\n')
    print(clean_transcript(output) if args.clean else output)

if __name__=='__main__': main()
