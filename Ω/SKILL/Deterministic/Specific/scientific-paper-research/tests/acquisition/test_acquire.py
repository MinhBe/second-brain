import tempfile
import unittest
from pathlib import Path

from lib.acquire import acquire_dois, verify_pdf
from lib.config import load_yaml
from lib.doi import find_dois, is_valid_doi, normalize_doi
from lib.search import resolve_title, run_search
from lib.unpaywall import FallbackConfig
from tests.helpers import (
    HTML_NO_LINK,
    default_routes,
    http_error,
    http_fake_factory,
    json_response,
    pdf_response,
    scihub_fake_factory,
    scopus_fake,
    ssl_error,
    unpaywall_record,
)
from lib.http import HttpResponse


class DoiTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize_doi("https://doi.org/10.1000/abc."), "10.1000/abc")
        self.assertEqual(normalize_doi("doi:10.1000/abc)"), "10.1000/abc")
        self.assertEqual(normalize_doi("  DOI: 10.1000/x;"), "10.1000/x")

    def test_validity(self):
        self.assertTrue(is_valid_doi("10.1016/j.cell.2020.01.001"))
        self.assertFalse(is_valid_doi("10.1/x"))
        self.assertFalse(is_valid_doi("abc"))

    def test_find_dois(self):
        text = "see https://doi.org/10.1000/AAA. and 10.1000/aaa and 10.2000/b."
        self.assertEqual(find_dois(text), ["10.1000/AAA", "10.2000/b"])


class AcquireTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.cfg = load_yaml("acquisition")
        self.fallback = FallbackConfig(mode="auto", command=None, email="e", timeout=60, setup_error="scihub_cli_not_found")

    def tearDown(self):
        self.tmp.cleanup()

    def acquire(self, dois, routes, email="e", scihub=None, fallback=None):
        http = http_fake_factory(routes)
        items = acquire_dois(dois, self.tmp.name, email, cfg=self.cfg, http_get=http,
                             scihub_fn=scihub or scihub_fake_factory([]), fallback=fallback or self.fallback)
        return items, http

    def test_chain_config_is_fixed(self):
        self.assertEqual(self.cfg["chain"], ["arxiv_direct", "unpaywall", "europe_pmc", "openalex", "semantic_scholar", "arxiv_preprint", "scihub_fallback", "metadata_only"])
        self.assertEqual(self.cfg["scihub_fallback"]["mode"], "auto")
        self.assertIn("--no-fast-fail", self.cfg["scihub_fallback"]["extra_args"])

    def test_item_key_order(self):
        items, _ = self.acquire(["10.1000/aaa"], default_routes())
        self.assertEqual(list(items[0]), load_yaml("output-contracts")["acquisition_item"])

    def test_arxiv_direct(self):
        items, http = self.acquire(["10.48550/arXiv.2312.13041"], [(r"arxiv\.org/pdf/2312\.13041", pdf_response("https://arxiv.org/pdf/2312.13041"))])
        item = items[0]
        self.assertEqual(item["status"], "downloaded")
        self.assertEqual(item["method"], "arxiv_direct")
        self.assertEqual(item["chain_attempted"], ["arxiv_direct"])
        self.assertEqual(item["evidence_level"], "full_text")
        self.assertEqual(len(item["sha256"]), 64)
        self.assertEqual([("export.arxiv.org" in c[0], "arxiv.org/pdf" in c[0]) for c in http.calls], [(True, False), (False, True)])
        self.assertTrue(Path(item["path"]).name.startswith("10.48550_arXiv"))  # title API 404s in this fake -> DOI name

    def test_unpaywall_download(self):
        items, _ = self.acquire(["10.1000/aaa"], default_routes())
        item = items[0]
        self.assertEqual(item["method"], "unpaywall")
        self.assertEqual(item["title"], "Alpha Paper")
        self.assertEqual(item["chain_attempted"], ["arxiv_direct", "unpaywall"])
        self.assertEqual([a["outcome"] for a in item["attempts"]], ["no_candidates", "downloaded"])
        self.assertEqual(item["failure_class"], "none")
        self.assertTrue(Path(item["path"]).name.startswith("Alpha_Paper"))

    def test_403_then_europe_pmc(self):
        routes = [
            (r"api\.unpaywall\.org", json_response("u", unpaywall_record("10.3390/x", pdf_url="https://www.mdpi.com/x/pdf", title="MDPI paper"))),
            (r"mdpi\.com", http_error("m", 403)),
            (r"europepmc/webservices", {"resultList": {"result": [{"pmcid": "PMC123", "title": "MDPI paper"}]}}),
            (r"europepmc\.org/articles/PMC123", pdf_response("https://europepmc.org/articles/PMC123?pdf=render")),
        ]
        items, _ = self.acquire(["10.3390/x"], routes)
        item = items[0]
        self.assertEqual(item["status"], "downloaded")
        self.assertEqual(item["method"], "europe_pmc")
        self.assertEqual([(a["resolver"], a["outcome"]) for a in item["attempts"]],
                         [("arxiv_direct", "no_candidates"), ("unpaywall", "failed"), ("europe_pmc", "downloaded")])
        self.assertEqual(item["attempts"][1]["error"], "http_403")

    def test_blocked_403_everywhere(self):
        routes = [
            (r"api\.unpaywall\.org", json_response("u", unpaywall_record("10.3390/x", pdf_url="https://www.mdpi.com/x/pdf"))),
            (r"mdpi\.com", http_error("m", 403)),
            (r"europepmc/webservices", {"resultList": {"result": []}}),
            (r"api\.openalex\.org/works/", {"display_name": "X", "open_access": {"is_oa": True, "oa_url": "https://www.mdpi.com/x/pdf"}, "locations": []}),
        ]
        items, _ = self.acquire(["10.3390/x"], routes)
        item = items[0]
        self.assertEqual(item["status"], "metadata_only")
        self.assertEqual(item["failure_class"], "blocked_403")
        self.assertEqual(item["manual_urls"][0], "https://doi.org/10.3390/x")
        self.assertIn("https://example.org/landing", item["manual_urls"])
        self.assertEqual(item["chain_attempted"][-1], "metadata_only")

    def test_ssl_error_class_when_retry_fails(self):
        routes = [
            (r"api\.unpaywall\.org", json_response("u", unpaywall_record("10.1/x", pdf_url="https://repo.example/x.pdf"))),
            (r"repo\.example", ssl_error()),
            (r"europepmc/webservices", {"resultList": {"result": []}}),
            (r"api\.openalex\.org/works/", http_error("o", 404)),
        ]
        items, http = self.acquire(["10.1/x"], routes)
        self.assertEqual(items[0]["failure_class"], "ssl_error")
        self.assertEqual([c[2] for c in http.calls if "repo.example" in c[0]], [True, False])

    def test_ssl_retry_success_records_warning(self):
        def repo(url, headers, verify_ssl):
            return pdf_response(url) if not verify_ssl else ssl_error()

        routes = [
            (r"api\.unpaywall\.org", json_response("u", unpaywall_record("10.1/x", pdf_url="https://repo.example/x.pdf"))),
            (r"repo\.example", repo),
        ]
        items, _ = self.acquire(["10.1/x"], routes)
        self.assertEqual(items[0]["status"], "downloaded")
        self.assertEqual(items[0]["warnings"], ["ssl_unverified"])

    def test_invalid_pdf_class(self):
        routes = [
            (r"api\.unpaywall\.org", json_response("u", unpaywall_record("10.1/x", pdf_url="https://pub.example/landing"))),
            (r"pub\.example", HttpResponse(200, HTML_NO_LINK, "text/html", "https://pub.example/landing")),
            (r"europepmc/webservices", {"resultList": {"result": []}}),
            (r"api\.openalex\.org/works/", http_error("o", 404)),
        ]
        items, _ = self.acquire(["10.1/x"], routes)
        self.assertEqual(items[0]["failure_class"], "invalid_pdf")

    def test_subscription_only(self):
        items, _ = self.acquire(["10.1000/bbb"], default_routes())
        item = items[0]
        self.assertEqual(item["status"], "metadata_only")
        self.assertEqual(item["failure_class"], "subscription_only")
        self.assertIs(item["is_oa"], False)
        self.assertEqual(item["title"], "Beta Paper")
        self.assertEqual([a["outcome"] for a in item["attempts"]][:4], ["no_candidates"] * 4)

    def test_not_found(self):
        items, _ = self.acquire(["10.9999/nope"], default_routes())
        item = items[0]
        self.assertEqual(item["status"], "failed")
        self.assertEqual(item["failure_class"], "not_found")
        self.assertEqual(item["evidence_level"], "none")

    def test_no_email_skips_unpaywall_with_warning(self):
        items, http = self.acquire(["10.1000/aaa"], default_routes(), email=None)
        item = items[0]
        self.assertIn("no_unpaywall_email", item["warnings"])
        self.assertFalse(any("unpaywall.org" in c[0] for c in http.calls))
        self.assertEqual(item["attempts"][1]["outcome"], "skipped")

    def test_openalex_provides_pmc_and_repository(self):
        routes = [
            (r"api\.unpaywall\.org", http_error("u", 404)),
            (r"europepmc/webservices", {"resultList": {"result": []}}),
            (r"api\.openalex\.org/works/", {"display_name": "Repo paper", "open_access": {"is_oa": True, "oa_url": "https://repo.example/x.pdf"},
                                            "best_oa_location": {"pdf_url": "https://repo.example/x.pdf", "landing_page_url": "https://repo.example/x"},
                                            "locations": [], "ids": {"pmcid": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC77"}}),
            (r"repo\.example/x\.pdf", pdf_response("https://repo.example/x.pdf")),
        ]
        items, _ = self.acquire(["10.1/x"], routes)
        self.assertEqual(items[0]["method"], "openalex")
        self.assertEqual(items[0]["title"], "Repo paper")
        self.assertIn("https://europepmc.org/articles/PMC77?pdf=render", items[0]["attempts"][3]["candidates"])

    def test_scihub_fallback_used_last(self):
        items, _ = self.acquire(["10.1000/bbb"], default_routes(), scihub=scihub_fake_factory(["10.1000/bbb"]))
        self.assertEqual(items[0]["method"], "scihub_fallback")
        self.assertEqual(items[0]["chain_attempted"][-1], "scihub_fallback")

    def test_scihub_off_is_skipped(self):
        off = FallbackConfig(mode="off", command=None, email="e", timeout=60)
        items, _ = self.acquire(["10.1000/bbb"], default_routes(), scihub=scihub_fake_factory(["10.1000/bbb"]), fallback=off)
        self.assertEqual(items[0]["status"], "metadata_only")
        self.assertEqual([a for a in items[0]["attempts"] if a["resolver"] == "scihub_fallback"][0]["outcome"], "skipped")

    def test_order_preserved(self):
        dois = ["10.1000/bbb", "10.1000/aaa", "10.9999/nope"]
        items, _ = self.acquire(dois, default_routes())
        self.assertEqual([i["doi"] for i in items], dois)

    def test_verify_rejects_non_pdf(self):
        bad = Path(self.tmp.name) / "bad.pdf"
        bad.write_bytes(b"<html>" + b"0" * 5000)
        self.assertEqual(verify_pdf(str(bad), self.cfg)["error"], "not_a_pdf")
        small = Path(self.tmp.name) / "small.pdf"
        small.write_bytes(b"%PDF-1.4")
        self.assertEqual(verify_pdf(str(small), self.cfg)["error"], "file_too_small")


class SearchTests(unittest.TestCase):
    def test_run_search_collects_and_flags_metadata_only(self):
        found = run_search("q", "-coverDate", 2, "k", page_size=25, request_fn=scopus_fake)
        self.assertEqual(found["total_hits"], 3)
        self.assertEqual(len(found["papers"]), 2)
        self.assertEqual(found["papers"][0]["doi"], "10.1000/aaa")
        self.assertEqual(found["papers"][0]["evidence_level"], "metadata_only")

    def test_missing_doi_counted(self):
        found = run_search("q", "-coverDate", 10, "k", request_fn=scopus_fake)
        self.assertEqual(found["missing_doi"], 1)
        self.assertIsNone(found["papers"][2]["doi"])

    def test_resolve_title_exact_ambiguous_not_found(self):
        self.assertEqual(resolve_title("alpha paper", "k", request_fn=scopus_fake)["resolution"], "exact")
        amb = resolve_title("Paper", "k", request_fn=scopus_fake)
        self.assertEqual(amb["resolution"], "ambiguous")
        self.assertIsNone(amb["resolved_doi"])
        self.assertEqual(len(amb["candidates"]), 3)
        empty = resolve_title("x", "k", request_fn=lambda **kw: {"search-results": {"opensearch:totalResults": "0", "entry": []}})
        self.assertEqual(empty["resolution"], "not_found")

    def test_title_without_doi_is_not_exact(self):
        self.assertEqual(resolve_title("Gamma Paper", "k", request_fn=scopus_fake)["resolution"], "ambiguous")


if __name__ == "__main__":
    unittest.main()
