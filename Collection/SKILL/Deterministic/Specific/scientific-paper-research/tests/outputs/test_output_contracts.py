import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

from lib.config import SKILL_ROOT, load_schema, load_yaml
from lib.output import exit_code_for
from run import execute
from tests.helpers import FIXTURES, TODAY, default_routes, fake_extract_factory, http_fake_factory, request, scihub_fake_factory, scopus_fake

CONTRACTS = load_yaml("output-contracts")
ENV = {"ELSEVIER_API_KEY": "k", "UNPAYWALL_EMAIL": "e"}
OPENALEX_SEARCH = {"meta": {"count": 1}, "results": [{"id": "https://openalex.org/W1", "display_name": "Alpha Paper", "doi": "https://doi.org/10.1000/aaa",
                                                       "publication_year": 2025, "cited_by_count": 12, "authorships": [], "primary_location": {"source": {"display_name": "Journal A"}}}]}


class OutputContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        from lib.unpaywall import FallbackConfig

        self.deps = {
            "request_fn": scopus_fake,
            "http_get": http_fake_factory(default_routes() + [(r"title\.search", {"meta": {"count": 0}, "results": []}),
                                                             (r"api\.openalex\.org/works\?", OPENALEX_SEARCH)]),
            "scihub_fn": scihub_fake_factory([]),
            "fallback": FallbackConfig(mode="auto", command=None, email="e", timeout=60),
            "today": TODAY,
        }

    def tearDown(self):
        self.tmp.cleanup()

    def assert_envelope(self, out):
        self.assertEqual(list(out), CONTRACTS["envelope"])
        jsonschema.Draft202012Validator(load_schema("output")).validate(out)
        if out["error"]:
            self.assertNotIn("Traceback", out["error"]["message"])
        self.assertEqual(out["contract_version"], "1.3")

    def run_mode(self, name, env=ENV, **extra):
        req = dict(request(name), outdir=self.tmp.name, **extra)
        out = execute(req, env=env, deps=self.deps)
        self.assert_envelope(out)
        return out

    def test_topic_search_scopus(self):
        out = self.run_mode("topic_search")
        self.assertEqual(out["status"], "ok")
        self.assertEqual(list(out["result"]), CONTRACTS["result"]["TOPIC_SEARCH"])
        self.assertEqual(out["result"]["provider"], "scopus")
        self.assertEqual(out["request"]["providers_used"], ["scopus"])
        self.assertEqual(list(out["result"]["papers"][0]), CONTRACTS["paper_item"])
        self.assertEqual(out["result"]["concept_blocks"][2]["matched_key"], "computed_tomography")
        self.assertIn("PUBYEAR > 2023", out["result"]["compiled_query"])
        self.assertIsNone(out["result"]["acquisition"])

    def test_topic_search_openalex_without_key(self):
        out = self.run_mode("topic_search", env={})
        self.assertEqual(out["status"], "ok")
        self.assertEqual(out["result"]["provider"], "openalex")
        self.assertTrue(out["result"]["compiled_query"].startswith('search=("artificial intelligence"'))
        self.assertIn("filter=publication_year:>2023,language:en,type:article|review", out["result"]["compiled_query"])
        self.assertEqual(out["result"]["sort"], "publication_date:desc")
        self.assertEqual(out["result"]["papers"][0]["doi"], "10.1000/aaa")

    def test_keyword_search_with_download(self):
        out = self.run_mode("keyword_search", download=True)
        self.assertEqual(list(out["result"]), CONTRACTS["result"]["KEYWORD_SEARCH"])
        self.assertIn('TITLE-ABS-KEY("(\\"lung cancer\\") AND (\\"computed tomography\\")")', out["result"]["compiled_query"])
        self.assertEqual(out["status"], "partial")
        self.assertEqual(out["result"]["acquisition"]["downloaded_count"], 1)
        self.assertEqual(out["result"]["papers"][0]["evidence_level"], "full_text")
        self.assertEqual(out["result"]["papers"][1]["evidence_level"], "metadata_only")

    def test_scopus_syntax_without_key_errors(self):
        out = self.run_mode("keyword_search", env={}, query_is_scopus_syntax=True)
        self.assertEqual(out["status"], "error")
        self.assertEqual(out["error"]["code"], "scopus_syntax_requires_key")

    def test_doi_download(self):
        out = self.run_mode("doi_download")
        self.assertEqual(list(out["result"]), CONTRACTS["result"]["DOI_DOWNLOAD"])
        self.assertEqual(list(out["result"]["items"][0]), CONTRACTS["acquisition_item"])
        self.assertEqual(list(out["result"]["items"][0]["attempts"][0]), CONTRACTS["attempt"])
        self.assertEqual(out["result"]["valid_dois"], ["10.1000/AAA", "10.1000/bbb"])
        self.assertEqual(out["result"]["downloaded_count"], 1)
        self.assertEqual(out["result"]["items"][1]["failure_class"], "subscription_only")
        self.assertEqual(out["status"], "partial")

    def test_doi_download_without_any_env(self):
        out = self.run_mode("doi_download", env={})
        self.assertEqual(out["status"], "partial")
        self.assertIn("no_unpaywall_email", out["result"]["items"][0]["warnings"])

    def test_title_download(self):
        out = self.run_mode("title_download")
        self.assertEqual(list(out["result"]), CONTRACTS["result"]["TITLE_DOWNLOAD"])
        items = out["result"]["items"]
        self.assertEqual(list(items[0]), CONTRACTS["title_item"])
        self.assertEqual([i["resolution"] for i in items], ["exact", "ambiguous", "ambiguous"])
        self.assertEqual(items[0]["provider"], "scopus")  # crossref fake 404s -> skipped; openalex empty; scopus exact
        self.assertEqual(items[0]["acquisition"]["status"], "downloaded")
        self.assertIsNone(items[1]["acquisition"])
        self.assertEqual(out["request"]["providers_used"], ["openalex", "scopus"])

    def test_invalid_and_clarification_envelopes(self):
        out = execute(request("doi_download_invalid"), env=ENV, deps=self.deps)
        self.assert_envelope(out)
        self.assertEqual(out["status"], "invalid_request")
        out = execute(request("topic_search_missing_concepts"), env=ENV, deps=self.deps)
        self.assert_envelope(out)
        self.assertEqual(out["status"], "clarification_required")

    def test_paper_analysis_two_steps(self):
        pdf = Path(self.tmp.name) / "sample.pdf"
        pdf.write_bytes(b"%PDF-1.4\n" + b"0" * 4096)
        text = (FIXTURES / "sample_paper.txt").read_text(encoding="utf-8")
        deps = dict(self.deps, extract_fn=fake_extract_factory(text))
        out = execute({"mode": "PAPER_ANALYSIS", "pdf_path": pdf.as_posix(), "workdir": self.tmp.name}, env={}, deps=deps)
        self.assert_envelope(out)
        self.assertEqual(out["status"], "needs_evidence")
        self.assertEqual(list(out["result"]), CONTRACTS["result"]["PAPER_ANALYSIS_STEP1"])
        self.assertEqual(out["result"]["detected_doi"], "10.1000/aaa")
        step2 = json.loads(Path(out["next_command"].split("--request ")[1]).read_text(encoding="utf-8"))
        out2 = execute(step2, env={}, deps=deps)
        self.assert_envelope(out2)
        self.assertEqual(out2["status"], "ok")
        self.assertEqual(list(out2["result"]), CONTRACTS["result"]["PAPER_ANALYSIS"])

    def test_batch_analysis(self):
        pdf = Path(self.tmp.name) / "sample.pdf"
        pdf.write_bytes(b"%PDF-1.4\n" + b"0" * 4096)
        text = (FIXTURES / "sample_paper.txt").read_text(encoding="utf-8")
        deps = dict(self.deps, extract_fn=fake_extract_factory(text))
        out = execute({"mode": "BATCH_ANALYSIS", "pdf_paths": [pdf.as_posix(), "missing.pdf"], "workdir": self.tmp.name}, env={}, deps=deps)
        self.assert_envelope(out)
        self.assertEqual(out["status"], "needs_evidence")
        self.assertEqual(out["result"]["summary"], {"total": 2, "parsed": 1, "failed": 1, "validated": 0})
        self.assertEqual(out["result"]["papers"][1]["error"]["code"], "pdf_not_found")

    def test_exit_codes(self):
        for status, code in CONTRACTS["exit_codes"].items():
            self.assertEqual(exit_code_for(status), code)

    def test_cli_invalid_request_exit_2(self):
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", str(SKILL_ROOT / "scripts" / "run.py"), "--request", str(FIXTURES / "requests" / "doi_download_invalid.json")],
            capture_output=True, text=True, cwd=str(SKILL_ROOT),
        )
        self.assertEqual(proc.returncode, 2)
        self.assertEqual(json.loads(proc.stdout)["status"], "invalid_request")

    def test_cli_unreadable_request_file(self):
        proc = subprocess.run(
            [sys.executable, "-X", "utf8", str(SKILL_ROOT / "scripts" / "run.py"), "--request", "does-not-exist.json"],
            capture_output=True, text=True, cwd=str(SKILL_ROOT),
        )
        self.assertEqual(proc.returncode, 2)


if __name__ == "__main__":
    unittest.main()
