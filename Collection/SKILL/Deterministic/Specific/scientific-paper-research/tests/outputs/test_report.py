import json
import tempfile
import unittest
from pathlib import Path

from lib.output import envelope
from lib.report import render_report
from run import main
from tests.helpers import default_routes, http_fake_factory, request, scihub_fake_factory


def item(doi, status, failure_class="none", method=None, title=None, manual=(), warnings=(), version=None):
    return {"doi": doi, "status": status, "method": method, "path": f"./d/{doi.replace('/', '_')}.pdf" if status == "downloaded" else None,
            "expected_filename": f"{doi.replace('/', '_')}.pdf",
            "sha256": "a" * 64 if status == "downloaded" else None, "title": title, "is_oa": None, "full_text_available": status == "downloaded",
            "evidence_level": "full_text" if status == "downloaded" else "metadata_only",
            "version": version or ("published" if status == "downloaded" else None), "chain_attempted": [], "attempts": [],
            "failure_class": failure_class, "warnings": list(warnings), "manual_urls": list(manual), "error": None if status == "downloaded" else failure_class}


class RenderReportTests(unittest.TestCase):
    def test_sections_and_grouping(self):
        result = {"requested_count": 4, "valid_dois": [], "invalid_dois": [{"input": "junk", "reason": "not a DOI"}], "downloaded_count": 2, "failed_count": 2,
                  "items": [item("10.1/a", "downloaded", method="arxiv_direct"), item("10.1/b", "downloaded", method="cache", title="Cached"),
                            item("10.3390/x", "metadata_only", "blocked_403", title="MDPI", manual=["https://doi.org/10.3390/x"], warnings=["ssl_unverified"]),
                            item("10.1016/y", "metadata_only", "subscription_only", title="Paywalled", manual=["https://doi.org/10.1016/y"])]}
        text = render_report(envelope("DOI_DOWNLOAD", "partial", result=result))
        self.assertTrue(text.startswith("# Acquisition report\n\n## Summary"))
        self.assertIn("| DOI_DOWNLOAD | partial | 4 | 2 | 1 | 2 |", text)
        self.assertIn("- `blocked_403`: 1", text)
        self.assertIn("| 2 | Cached | cache |", text)
        self.assertLess(text.index("### blocked_403 (1)"), text.index("### subscription_only (1)"))
        self.assertIn("  - <https://doi.org/10.3390/x>", text)
        self.assertIn("  - warnings: ssl_unverified", text)
        self.assertIn("## Invalid DOIs\n\n- `junk`: not a DOI", text)
        self.assertEqual(text, render_report(envelope("DOI_DOWNLOAD", "partial", result=result)))  # deterministic
        # manual download section lists only classes a browser can fix, with the exact file name to save as
        self.assertIn("## Manual download", text)
        self.assertIn("| 1 | `10.3390/x` | `10.3390_x.pdf` | <https://doi.org/10.3390/x> |", text)
        self.assertNotIn("| `10.1016/y` |", text)
        self.assertIn("1 paper(s) are subscription-only", text)
        self.assertIn("Save it into `./downloads`", text)

    def test_preprint_and_challenge_rendering(self):
        result = {"requested_count": 2, "valid_dois": [], "invalid_dois": [], "downloaded_count": 1, "failed_count": 1,
                  "items": [item("10.1007/x", "downloaded", method="arxiv_preprint", title="ModSec-Learn", version="preprint"),
                            item("10.3390/y", "metadata_only", "blocked_challenge", title="MDPI paper", manual=["https://doi.org/10.3390/y"])]}
        text = render_report(envelope("DOI_DOWNLOAD", "partial", result=result))
        self.assertIn("| 1 | ModSec-Learn (preprint) | arxiv_preprint |", text)
        self.assertIn("1 file(s) marked (preprint) are arXiv preprints", text)
        self.assertIn("### blocked_challenge (1)", text)
        self.assertIn("JavaScript challenge", text)
        self.assertIn("| 1 | `10.3390/y` | `10.3390_y.pdf` | <https://doi.org/10.3390/y> |", text)

    def test_title_download_unresolved_section(self):
        result = {"requested_count": 2, "resolved_count": 1, "downloaded_count": 1, "items": [
            {"input_title": "A", "resolution": "exact", "provider": "crossref", "resolved_doi": "10.1/a", "candidates": [], "suggestion": None, "acquisition": item("10.1/a", "downloaded", method="unpaywall")},
            {"input_title": "B", "resolution": "ambiguous", "provider": "openalex", "resolved_doi": None, "candidates": [{"title": "B1", "doi": "10.1/b1", "year": "2020"}],
             "suggestion": {"doi": "10.1/b1", "title": "B1", "year": "2020", "rule": "prefix"}, "acquisition": None},
        ]}
        text = render_report(envelope("TITLE_DOWNLOAD", "partial", result=result))
        self.assertIn("## Unresolved titles\n\n- B (ambiguous, provider: openalex)\n  - candidate: B1 | 10.1/b1 | 2020\n  - suggested: `10.1/b1` (prefix match)", text)


class ReportCliTests(unittest.TestCase):
    def test_report_written_via_run(self):
        import run as run_module

        with tempfile.TemporaryDirectory() as tmp:
            req = dict(request("doi_download"), outdir=tmp)
            req_path = Path(tmp) / "req.json"
            req_path.write_text(json.dumps(req), encoding="utf-8")
            report_path = Path(tmp) / "report.md"
            original = run_module.execute
            run_module.execute = lambda r: original(r, env={}, deps={"http_get": http_fake_factory(default_routes()), "scihub_fn": scihub_fake_factory([])})
            try:
                code = main(["--request", str(req_path), "--report", str(report_path)])
            finally:
                run_module.execute = original
            self.assertEqual(code, 0)
            text = report_path.read_text(encoding="utf-8")
            self.assertIn("## Downloaded", text)
            self.assertIn("10.1000/bbb", text)


if __name__ == "__main__":
    unittest.main()
