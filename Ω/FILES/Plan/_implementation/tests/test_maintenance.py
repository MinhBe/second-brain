import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

HERE=Path(__file__).resolve().parents[1]
ROOT=HERE.parents[2]

class MaintenanceTests(unittest.TestCase):
    def fixture(self, root, source='Skills/sample', destination='Reference/sample'):
        p=root/'Skills/sample'
        p.mkdir(parents=True)
        (p/'data.txt').write_text('Nội dung không đổi',encoding='utf-8')
        manifest=root/'moves.json'
        manifest.write_text(json.dumps({'root':str(root),'moves':[{'source':source,'destination':destination}]}),encoding='utf-8')
        return manifest

    def run_move(self, manifest, mode):
        return subprocess.run(['powershell.exe','-NoProfile','-ExecutionPolicy','Bypass','-File',str(HERE/'reorganize.ps1'),
            '-Manifest',str(manifest),'-Mode',mode],capture_output=True)

    def test_dry_run_apply_resume_rollback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            manifest=self.fixture(root)
            self.assertEqual(self.run_move(manifest,'DryRun').returncode,0)
            self.assertTrue((root/'Skills/sample/data.txt').exists())
            for mode in ['Apply','Apply']:
                result=self.run_move(manifest,mode)
                self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual((root/'Reference/sample/data.txt').read_text(encoding='utf-8'),'Nội dung không đổi')
            self.assertEqual(self.run_move(manifest,'Rollback').returncode,0)
            self.assertTrue((root/'Skills/sample/data.txt').exists())

    def test_conflicting_destination_does_not_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            manifest=self.fixture(root)
            (root/'Reference/sample').mkdir(parents=True)
            self.assertNotEqual(self.run_move(manifest,'Apply').returncode,0)
            self.assertTrue((root/'Skills/sample/data.txt').exists())

    def test_escape_does_not_move(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            manifest=self.fixture(root,destination='../outside')
            self.assertNotEqual(self.run_move(manifest,'Apply').returncode,0)
            self.assertTrue((root/'Skills/sample/data.txt').exists())

    def test_junction_destination_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            manifest=self.fixture(root)
            (root/'actual').mkdir()
            # The target and junction are both explicitly inside the temporary workspace.
            command="New-Item -ItemType Junction -Path '"+str(root/'Reference')+"' -Target '"+str(root/'actual')+"' | Out-Null"
            result=subprocess.run(['powershell.exe','-NoProfile','-Command',command],capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertNotEqual(self.run_move(manifest,'Apply').returncode,0)
            # Remove only the junction through the Directory API; never recurse through it.
            import os
            os.rmdir(root/'Reference')

    def test_pdf_cli_keeps_source_and_extracts_text(self):
        import fitz
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)
            source=root/'sample.pdf'
            document=fitz.open()
            page=document.new_page()
            text='Evidence-based learning preserves conditions, checks sources and records uncertainty. This is a deterministic PDF conversion fixture.'
            page.insert_textbox(fitz.Rect(40,40,550,150),text)
            document.save(source)
            document.close()
            before=hashlib.sha256(source.read_bytes()).hexdigest()
            script=ROOT/'Skills/Domain/personal/ChangePdfToText/pdf_to_text.py'
            result=subprocess.run([sys.executable,'-X','utf8','-B',str(script),'--input',str(source),'--output',str(root/'out'),'--ocr','never'],capture_output=True)
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertIn('preserves conditions',(root/'out/sample.txt').read_text(encoding='utf-8'))
            self.assertTrue((root/'out/sample.md').exists())
            self.assertEqual(before,hashlib.sha256(source.read_bytes()).hexdigest())

if __name__=='__main__': unittest.main()
