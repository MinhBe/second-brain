import tempfile
import unittest

from lib.acquire import acquire_dois, build_http_policy
from lib.config import load_yaml
from lib.resolvers import ResolveContext, expand_candidates, resolve_arxiv_direct, rewrite_candidates
from lib.unpaywall import FallbackConfig, maybe_extract_pdf_url_from_html
from tests.helpers import HttpResponse, http_error, http_fake_factory, json_response, pdf_response, scihub_fake_factory

CFG = load_yaml("acquisition")
ARXIV_ATOM = b'<?xml version="1.0"?><feed><title>ArXiv Query</title><entry><id>x</id><title>Advancing SQL Injection\n Detection</title></entry></feed>'


def ctx(http=None):
    return ResolveContext(doi="10.1/x", email=None, contact_email="t@example.org", policy=build_http_policy(CFG, "t@example.org", 5), cfg=CFG, http_get=http)


class RewriteTests(unittest.TestCase):
    def test_ieee_stamp_from_ielx_and_document(self):
        out = rewrite_candidates(["https://ieeexplore.ieee.org/ielx7/6287639/6514899/10187144.pdf", "https://ieeexplore.ieee.org/document/8395015/"], CFG)
        self.assertEqual(out, ["https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=10187144",
                               "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=8395015"])

    def test_originals_first_then_rewrites_then_landing_expansions(self):
        c = ctx(http_fake_factory([(r"api\.figshare\.com/v2/articles/25697922", {"files": [{"name": "x.docx", "download_url": "https://nd/1"}, {"name": "paper.pdf", "download_url": "https://nd/2"}]})]))
        c.landing("https://figshare.com/articles/journal_contribution/Some_Title/25697922")
        c.landing("https://ieeexplore.ieee.org/document/1")
        out = expand_candidates(["https://a/1.pdf", "https://a/1.pdf"], c)
        self.assertEqual(out, ["https://a/1.pdf", "https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=1", "https://nd/2", "https://nd/1"])
        self.assertEqual(expand_candidates([], c), ["https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=1"])  # figshare expanded only once

    def test_figshare_api_error_is_swallowed(self):
        c = ctx(http_fake_factory([(r"api\.figshare\.com", http_error("f", 500))]))
        c.landing("https://figshare.com/articles/journal_contribution/T/1")
        self.assertEqual(expand_candidates([], c), [])
        self.assertIn("figshare", c.meta["lookup_errors"])


class HtmlExtractionTests(unittest.TestCase):
    def test_patterns_in_fixed_order(self):
        self.assertEqual(maybe_extract_pdf_url_from_html('<meta name="citation_pdf_url" content="https://p/a.pdf"><a href="https://p/b.pdf">'), "https://p/a.pdf")
        self.assertEqual(maybe_extract_pdf_url_from_html('<meta content="https://p/a.pdf" name="citation_pdf_url">'), "https://p/a.pdf")
        self.assertEqual(maybe_extract_pdf_url_from_html('<iframe src="/stamp/x.pdf?arnumber=1"></iframe>'), "/stamp/x.pdf?arnumber=1")
        self.assertEqual(maybe_extract_pdf_url_from_html('<a class="btn" download href="/files/123">Download</a>'), "/files/123")
        self.assertEqual(maybe_extract_pdf_url_from_html('<a href="/stampPDF/getPDF.jsp?tp=&arnumber=9">PDF</a>'), "/stampPDF/getPDF.jsp?tp=&arnumber=9")
        self.assertEqual(maybe_extract_pdf_url_from_html('<a href="/content/pdf/1.pdf?download=true">get</a>'), "/content/pdf/1.pdf?download=true")
        self.assertEqual(maybe_extract_pdf_url_from_html('<a href="/x/y/pdf?version=3">pdf</a>'), "/x/y/pdf?version=3")
        self.assertIsNone(maybe_extract_pdf_url_from_html("<html><body>nothing</body></html>"))


class ArxivTitleTests(unittest.TestCase):
    def test_title_from_export_api(self):
        c = ctx(http_fake_factory([(r"export\.arxiv\.org/api/query", HttpResponse(200, ARXIV_ATOM, "application/atom+xml", "u"))]))
        urls = resolve_arxiv_direct("10.48550/arXiv.2312.13041", c)
        self.assertEqual(urls, ["https://arxiv.org/pdf/2312.13041"])
        self.assertEqual(c.meta["title"], "Advancing SQL Injection Detection")

    def test_api_failure_does_not_block(self):
        c = ctx(http_fake_factory([(r"export\.arxiv\.org", http_error("a", 503))]))
        self.assertEqual(resolve_arxiv_direct("10.48550/arXiv.2312.13041", c), ["https://arxiv.org/pdf/2312.13041"])
        self.assertIsNone(c.meta["title"])


class EndToEndExpanderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.fallback = FallbackConfig(mode="off", command=None, email=None, timeout=60)

    def tearDown(self):
        self.tmp.cleanup()

    def acquire(self, routes):
        http = http_fake_factory(routes)
        items = acquire_dois(["10.1109/ACCESS.2023.3296707"], self.tmp.name, None, cfg=CFG, http_get=http, scihub_fn=scihub_fake_factory([]), fallback=self.fallback)
        return items[0], http

    def test_ieee_stamp_rescues_dead_ielx_link(self):
        item, http = self.acquire([
            (r"europepmc/webservices", {"resultList": {"result": []}}),
            (r"api\.openalex\.org/works/", {"display_name": "GAN Survey", "open_access": {"is_oa": True, "oa_url": None},
                                            "best_oa_location": {"pdf_url": "https://ieeexplore.ieee.org/ielx7/6287639/6514899/10187144.pdf", "landing_page_url": "https://doi.org/10.1109/access.2023.3296707"},
                                            "locations": []}),
            (r"ielx7", http_error("i", 404)),
            (r"stampPDF/getPDF\.jsp\?tp=&arnumber=10187144", pdf_response("https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=10187144")),
        ])
        self.assertEqual(item["status"], "downloaded")
        self.assertEqual(item["method"], "openalex")
        self.assertEqual(item["expected_filename"], "GAN_Survey.pdf")
        openalex_attempt = [a for a in item["attempts"] if a["resolver"] == "openalex"][0]
        self.assertIn("https://ieeexplore.ieee.org/stampPDF/getPDF.jsp?tp=&arnumber=10187144", openalex_attempt["candidates"])

    def test_figshare_landing_rescues(self):
        item, http = self.acquire([
            (r"europepmc/webservices", {"resultList": {"result": []}}),
            (r"api\.openalex\.org/works/", {"display_name": "GAN Survey", "open_access": {"is_oa": True, "oa_url": None}, "best_oa_location": None,
                                            "locations": [{"is_oa": True, "pdf_url": None, "landing_page_url": "https://figshare.com/articles/journal_contribution/A_Survey/25697922"}]}),
            (r"api\.figshare\.com/v2/articles/25697922", {"files": [{"name": "A_Survey.pdf", "download_url": "https://ndownloader.figshare.com/files/45869847"}]}),
            (r"ndownloader\.figshare\.com/files/45869847", pdf_response("https://s3/x.pdf")),
        ])
        self.assertEqual(item["status"], "downloaded")
        self.assertEqual(item["method"], "openalex")
        self.assertIn("https://figshare.com/articles/journal_contribution/A_Survey/25697922", item.get("manual_urls") or ["https://figshare.com/articles/journal_contribution/A_Survey/25697922"])

    def test_failed_item_reports_expected_filename(self):
        item, _ = self.acquire([
            (r"europepmc/webservices", {"resultList": {"result": []}}),
            (r"api\.openalex\.org/works/", {"display_name": "GAN Survey", "open_access": {"is_oa": True, "oa_url": "https://www.mdpi.com/x/pdf"}, "locations": []}),
            (r"mdpi\.com", http_error("m", 403)),
        ])
        self.assertEqual(item["status"], "metadata_only")
        self.assertEqual(item["expected_filename"], "GAN_Survey.pdf")
        self.assertEqual(item["failure_class"], "blocked_403")


if __name__ == "__main__":
    unittest.main()
