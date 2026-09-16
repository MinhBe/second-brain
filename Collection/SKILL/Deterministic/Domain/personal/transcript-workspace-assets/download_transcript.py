import os
import time
from youtube_transcript_api import YouTubeTranscriptApi

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

URLS = [
    "https://www.youtube.com/watch?v=uGouKEuej4k",
    "https://www.youtube.com/watch?v=m9yayKNK7yw",
    "https://www.youtube.com/watch?v=VIyK8Tq3YRw",
    "https://www.youtube.com/watch?v=qkATC8JO3lM",
    "https://www.youtube.com/watch?v=TbCTOBKv1P4",
    "https://www.youtube.com/watch?v=lqkocF3j2f0",
    "https://www.youtube.com/watch?v=0O0iHqK2fh4",
    "https://www.youtube.com/watch?v=CoY8145FxFE",
]


def get_video_id(url):
    return url.split("v=")[1].split("&")[0]


def download_transcript(video_url, lang="vi"):
    video_id = get_video_id(video_url)
    try:
        api = YouTubeTranscriptApi()
        transcript_list = api.list(video_id)
        transcript = transcript_list.find_transcript([lang])
        fetched = transcript.fetch()
        text = "\n".join([entry.text for entry in fetched.snippets])
        return text, None
    except Exception as e:
        return None, str(e)


if __name__ == "__main__":
    all_text = []
    for i, url in enumerate(URLS):
        video_id = get_video_id(url)
        print(f"Dang tai {i+1}/{len(URLS)}: {video_id}")
        text, error = download_transcript(url)
        if text:
            all_text.append(f"=== Transcript: {video_id} ===\n{text}\n")
            print(f"Da tai: {video_id} ({len(text)} ky tu)")
        else:
            print(f"Loi {video_id}: {error}")
        if i < len(URLS) - 1:
            time.sleep(3)

    output_file = os.path.join(OUTPUT_DIR, "all_transcripts.txt")
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n\n".join(all_text))
    print(f"\nDa luu tat ca vao: {output_file}")
    print(f"Tong so ky tu: {len('\n\n'.join(all_text))}")
