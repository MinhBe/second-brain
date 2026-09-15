import json
import tempfile
import unittest
from pathlib import Path

from lib.acquire import acquire_dois
from lib.config import load_yaml
from lib.manifest import load_manifest, manifest_path
from lib.unpaywall import FallbackConfig
from tests.helpers import default_routes, http_fake_factory, scihub_fake_factory


class ManifestTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = load_yaml("acquisition")
        self.fallback = FallbackConfig(mode="off", command=None, email="e", timeout=60)

    def tearDown(self):
        self.tmp.cleanup()

    def run_once(self):
        http = http_fake_factory(default_routes())
        items = acquire_dois(["10.1000/aaa", "10.1000/bbb"], self.tmp.name, "e", cfg=self.cfg, http_get=http, scihub_fn=scihub_fake_factory([]), fallback=self.fallback)
        return items, http

    def test_rerun_uses_cache_without_http(self):
        first, _ = self.run_once()
        self.assertEqual(first[0]["method"], "unpaywall")
        manifest = load_manifest(Path(self.tmp.name), self.cfg)
        self.assertIn("10.1000/aaa", manifest["items"])
        self.assertNotIn("10.1000/bbb", manifest["items"])

        second, http = self.run_once()
        self.assertEqual(second[0]["method"], "cache")
        self.assertEqual(second[0]["status"], "downloaded")
        self.assertEqual(second[0]["chain_attempted"], ["cache"])
        self.assertEqual(second[0]["sha256"], first[0]["sha256"])
        self.assertFalse(any("10.1000/aaa" in c[0] or "10.1000%2Faaa" in c[0] for c in http.calls))
        self.assertEqual(second[1]["failure_class"], "subscription_only")  # failures are retried

    def test_changed_file_is_readopted_with_new_sha(self):
        first, _ = self.run_once()
        Path(first[0]["path"]).write_bytes(b"%PDF-1.4\n" + b"9" * 3000)  # sha changes but still a valid PDF
        second, _ = self.run_once()
        self.assertEqual(second[0]["method"], "cache")
        self.assertNotEqual(second[0]["sha256"], first[0]["sha256"])
        self.assertEqual(load_manifest(Path(self.tmp.name), self.cfg)["items"]["10.1000/aaa"]["sha256"], second[0]["sha256"])

    def test_corrupted_file_is_redownloaded(self):
        first, _ = self.run_once()
        Path(first[0]["path"]).write_bytes(b"<html>not a pdf")
        second, _ = self.run_once()
        self.assertEqual(second[0]["method"], "unpaywall")
        self.assertEqual(second[0]["status"], "downloaded")

    def test_missing_file_is_redownloaded(self):
        first, _ = self.run_once()
        Path(first[0]["path"]).unlink()
        second, _ = self.run_once()
        self.assertEqual(second[0]["method"], "unpaywall")

    def test_existing_file_from_older_run_is_adopted(self):
        from tests.helpers import PDF_BYTES

        (Path(self.tmp.name) / "Alpha_Paper.pdf").write_bytes(PDF_BYTES)  # v1.0 naming, no manifest yet
        items, http = self.run_once()
        self.assertEqual(items[0]["method"], "cache")
        self.assertTrue(items[0]["path"].endswith("Alpha_Paper.pdf"))
        self.assertFalse(any("example.org/pdf" in c[0] for c in http.calls))
        self.assertEqual(len(list(Path(self.tmp.name).glob("*.pdf"))), 1)  # no duplicate written
        self.assertIn("10.1000/aaa", load_manifest(Path(self.tmp.name), self.cfg)["items"])

    def test_corrupt_manifest_is_tolerated(self):
        manifest_path(Path(self.tmp.name), self.cfg).write_text("{not json", encoding="utf-8")
        items, _ = self.run_once()
        self.assertEqual(items[0]["status"], "downloaded")
        data = json.loads(manifest_path(Path(self.tmp.name), self.cfg).read_text(encoding="utf-8"))
        self.assertEqual(data["version"], 1)


if __name__ == "__main__":
    unittest.main()
