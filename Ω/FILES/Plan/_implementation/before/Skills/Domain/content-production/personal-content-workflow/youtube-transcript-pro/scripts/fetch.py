#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.10"
# dependencies = ["yt-dlp>=2024.01.01"]
# ///

"""
Download and clean YouTube transcript.

Usage:
    uv run fetch.py "YOUTUBE_URL"
    uv run fetch.py "YOUTUBE_URL" --clean
    uv run fetch.py "YOUTUBE_URL" --lang vi
"""

import sys
import re
import argparse
from pathlib import Path

try:
    import yt_dlp as yt
except ImportError:
    print("ERROR: yt-dlp not installed. Run: pip install yt-dlp")
    sys.exit(1)


def extract_video_id(url_or_id: str) -> str:
    """Extract video ID from various YouTube URL formats."""
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/)([a-zA-Z0-9_-]{11})',
        r'^([a-zA-Z0-9_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    raise ValueError(f"Could not extract video ID from: {url_or_id}")


def get_video_title(url: str) -> str:
    """Get video title for filename."""
    ydl = yt.YoutubeDL({'quiet': True})
    info = ydl.extract_info(url, download=False)
    title = info.get('title', 'untitled')
    # Clean for filesystem
    title = re.sub(r'[/\\:?*"<>|]', '-', title)
    title = re.sub(r'-+', '-', title)
    title = title[:60].strip('-')
    return title


def list_available_subs(url: str) -> list:
    """List available subtitle languages."""
    ydl = yt.YoutubeDL({'quiet': True})
    try:
        info = ydl.extract_info(url, download=False)
        subs = info.get('subtitles', {}) or {}
        auto_subs = info.get('automatic_captions', {}) or {}
        all_subs = {**subs, **auto_subs}
        return list(all_subs.keys()) if all_subs else []
    except Exception:
        return []


def download_transcript(url: str, lang: str = None, auto: bool = False) -> tuple:
    """Download transcript to file. Returns (filepath, error)."""
    video_id = extract_video_id(url)
    video_title = get_video_title(url)
    
    output_name = f"transcript_{video_id}"
    output_file = f"{output_name}.vtt"
    
    ydl_opts = {
        'writesubtitles': True,
        'writeautosubtitle': True,
        'skipdownload': True,
        'outtmpl': output_name,
        'quiet': True,
        'no_warnings': True,
    }
    
    if auto:
        ydl_opts['writesubtitles'] = False
        ydl_opts['writeautosubtitle'] = True
    
    try:
        ydl = yt.YoutubeDL(ydl_opts)
        ydl.download([url])
        
        # Find the VTT file
        vtt_files = list(Path('.').glob('*.vtt'))
        if not vtt_files:
            return None, "No subtitle file created"
            
        return str(vtt_files[0]), None
    except Exception as e:
        return None, str(e)


def clean_transcript(vtt_file: str, output_file: str = None) -> str:
    """Clean and deduplicate VTT transcript."""
    if output_file is None:
        output_file = vtt_file.replace('.vtt', '.txt')
    
    seen = set()
    cleaned_lines = []
    
    with open(vtt_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip VTT headers and timestamps
            if (line and 
                not line.startswith('WEBVTT') and 
                not line.startswith('Kind:') and 
                not line.startswith('Language:') and 
                '-->' not in line and
                not line.isdigit()):
                # Clean HTML tags
                clean = re.sub(r'<[^>]*>', '', line)
                clean = clean.replace('&amp;', '&').replace('&gt;', '>').replace('&lt;', '<')
                clean = clean.strip()
                
                if clean and clean not in seen:
                    seen.add(clean)
                    cleaned_lines.append(clean)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cleaned_lines))
    
    return output_file


def main():
    parser = argparse.ArgumentParser(description='Download YouTube transcript')
    parser.add_argument('video', help='YouTube URL or video ID')
    parser.add_argument('--lang', '-l', default=None, help='Language code (e.g., vi, en)')
    parser.add_argument('--clean', '-c', action='store_true', help='Clean and deduplicate output')
    parser.add_argument('--auto', '-a', action='store_true', help='Force auto-generated subs')
    args = parser.parse_args()
    
    url = args.video
    if not url.startswith('http'):
        url = f"https://www.youtube.com/watch?v={url}"
    
    print(f"Processing: {url}")
    
    # Step 1: List subs
    available = list_available_subs(url)
    if available:
        print(f"Available languages: {', '.join(available[:5])}{'...' if len(available) > 5 else ''}")
    else:
        print("No subtitles available, trying auto...")
    
    # Step 2: Download
    vtt_file, error = download_transcript(url, auto=args.auto)
    if error:
        print(f"Error: {error}")
        sys.exit(1)
    
    print(f"Downloaded: {vtt_file}")
    
    # Step 3: Clean
    if args.clean:
        output_file = clean_transcript(vtt_file)
        print(f"Cleaned: {output_file}")
        
        # Show preview
        with open(output_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()[:20]
            print("\n--- Preview (first 20 lines) ---")
            print(''.join(lines))
    else:
        print(f"Output: {vtt_file}")
        print("Run with --clean to deduplicate and get plain text")


if __name__ == '__main__':
    main()