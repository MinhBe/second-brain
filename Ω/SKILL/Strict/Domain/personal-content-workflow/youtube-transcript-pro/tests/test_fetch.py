from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from fetch import choose_subtitle,extract_video_id,clean_text,download_transcript

class FetchTests(unittest.TestCase):
    def test_requested_language_and_manual_priority(self):
        info={'subtitles':{'vi':[{}],'en':[{}]},'automatic_captions':{'vi':[{}]}}
        self.assertEqual(choose_subtitle(info,'vi'),('vi',False))
        self.assertEqual(choose_subtitle(info,'vi',True),('vi',True))
        self.assertEqual(choose_subtitle({'subtitles':{'vi-orig':[{}]},'automatic_captions':{'vi':[{}]}},'vi'),('vi-orig',False))
        with self.assertRaises(ValueError): choose_subtitle(info,'ja')

    def test_url_variants_and_impostor_host(self):
        ident='abcdefghijk'
        for url in [ident,'https://youtu.be/'+ident,'https://youtube.com/shorts/'+ident,'https://www.youtube.com/watch?x=1&v='+ident]:
            self.assertEqual(extract_video_id(url),ident)
        with self.assertRaises(ValueError): extract_video_id('https://youtube.com.evil.example/watch?v='+ident)

    def test_rolling_caption_and_later_repetition(self):
        text='WEBVTT\n\n00:00:01.000 --> 00:00:03.000\nXin chào\n\n00:00:02.000 --> 00:00:04.000\nXin chào mọi người\n\n00:00:10.000 --> 00:00:12.000\nXin chào\n'
        self.assertEqual(clean_text(text),'Xin chào\nmọi người\nXin chào')

    def test_does_not_take_unrelated_vtt(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp)/'unrelated.vtt').write_text('unrelated',encoding='utf-8')
            with patch('fetch.yt.YoutubeDL') as mock:
                mock.return_value.__enter__.return_value.extract_info.side_effect=[{'subtitles':{'vi':[{}]}},{'requested_subtitles':{}}]
                result,error=download_transcript('abcdefghijk','vi',output_dir=tmp)
            self.assertIsNone(result)
            self.assertIn('not downloaded',error)

if __name__=='__main__': unittest.main()
