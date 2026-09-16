import tempfile
import unittest
from pathlib import Path

from lib.acquire import acquire_dois, build_http_policy
from lib.config import load_yaml
from lib.resolvers import ResolveContext, resolve_arxiv_preprint, resolve_semantic_scholar
from lib.unpaywall import FallbackConfig
from tests.helpers import HttpResponse, http_error, http_fake_factory, pdf_response, scihub_fake_factory

CFG = load_yaml("acquisition")
TITLE = "ModSec-Learn: Boosting ModSecurity with Machine Learning"


def atom(*entries):
    body = "".join(f"<entry><id>http://arxiv.org/abs/{i}v1</id><title>{t}</title></entry>" for i, t in entries)
    return HttpResponse(200, f'<?xml version="1.0"?><feed><title>q</title>{body}</feed>'.encode(), "application/atom+xml", "u")


def ctx(http=None, title=None, arxiv_id=None):
    c = ResolveContext(doi="10.1007/978-3-031-76459-2_3", email=None, contact_email="t@example.org", policy=build_http_policy(CFG, "t@example.org", 5), cfg=CFG, http_get=http)
    c.meta["title"] = title
    c.meta["arxiv_id"] = arxiv_id
    return c


class SemanticScholarTests(unittest.TestCase):
    def test_sets_arxiv_id_and_title(self):
        http = http_fake_factory([(r"semanticscholar", {"title": TITLE, "openAccessPdf": {"url": "https://hdl.handle.net/11584/440487"}, "externalIds": {"ArXiv": "2406.13547"}})])
        c = ctx(http)
        self.assertEqual(resolve_semantic_scholar(c.doi, c), ["https://hdl.handle.net/11584/440487"])
        self.assertEqual(c.meta["arxiv_id"], "2406.13547")
        self.assertEqual(c.meta["title"], TITLE)

    def test_404_is_swallowed(self):
        c = ctx(http_fake_factory([(r"semanticscholar", http_error("s", 404))]))
        self.assertEqual(resolve_semantic_scholar(c.doi, c), [])
        self.assertIn("semantic_scholar", c.meta["lookup_404"])


class ArxivPreprintTests(unittest.TestCase):
    def test_uses_known_arxiv_id_without_search(self):
        http = http_fake_factory([])
        c = ctx(http, title=TITLE, arxiv_id="2406.13547")
        self.assertEqual(resolve_arxiv_preprint(c.doi, c), ["https://arxiv.org/pdf/2406.13547"])
        self.assertEqual(c.meta["version"], "preprint")
        self.assertIn("https://arxiv.org/abs/2406.13547", c.meta["landing_urls"])
        self.assertEqual(http.calls, [])

    def test_title_search_exact_match(self):
        http = http_fake_factory([(r"export\.arxiv\.org/api/query\?search_query=ti", atom(("2406.13547", "ModSec-Learn: Boosting ModSecurity\n with Machine Learning"), ("1111.1111", "Something else")))])
        c = ctx(http, title=TITLE)
        self.assertEqual(resolve_arxiv_preprint(c.doi, c), ["https://arxiv.org/pdf/2406.13547"])
        self.assertIn("ti%3A%22ModSec-Learn", http.calls[0][0])

    def test_no_exact_match_returns_nothing(self):
        http = http_fake_factory([(r"export\.arxiv\.org", atom(("1111.1111", "ModSec-Learn: Boosting ModSecurity with Machine Learning and More")))])
        c = ctx(http, title=TITLE)
        self.assertEqual(resolve_arxiv_preprint(c.doi, c), [])
        self.assertIsNone(c.meta["version"])

    def test_two_exact_matches_is_ambiguous(self):
        http = http_fake_factory([(r"export\.arxiv\.org", atom(("1111.1111", TITLE), ("2222.2222", TITLE)))])
        self.assertEqual(resolve_arxiv_preprint("10.1/x", ctx(http, title=TITLE)), [])

    def test_arxiv_doi_and_missing_title_skip(self):
        http = http_fake_factory([])
        self.assertEqual(resolve_arxiv_preprint("10.48550/arXiv.2406.13547", ctx(http, title=TITLE)), [])
        self.assertEqual(resolve_arxiv_preprint("10.1/x", ctx(http, title=None)), [])
        self.assertEqual(http.calls, [])


class EndToEndPreprintTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.fallback = FallbackConfig(mode="off", command=None, email=None, timeout=60)

    def tearDown(self):
        self.tmp.cleanup()

    def test_blocked_repository_falls_back_to_preprint(self):
        http = http_fake_factory([
            (r"europepmc/webservices", {"resultList": {"result": []}}),
            (r"api\.openalex\.org/works/", {"display_name": TITLE, "open_access": {"is_oa": True, "oa_url": "https://hdl.handle.net/11584/440487"},
                                            "best_oa_location": {"pdf_url": None, "landing_page_url": "https://hdl.handle.net/11584/440487"}, "locations": []}),
            (r"hdl\.handle\.net", http_error("h", 403)),
            (r"semanticscholar", {"title": TITLE, "openAccessPdf": {"url": "https://hdl.handle.net/11584/440487"}, "externalIds": {"ArXiv": "2406.13547"}}),
            (r"arxiv\.org/pdf/2406\.13547", pdf_response("https://arxiv.org/pdf/2406.13547")),
        ])
        items = acquire_dois(["10.1007/978-3-031-76459-2_3"], self.tmp.name, None, cfg=CFG, http_get=http, scihub_fn=scihub_fake_factory([]), fallback=self.fallback)
        item = items[0]
        self.assertEqual(item["status"], "downloaded")
        self.assertEqual(item["method"], "arxiv_preprint")
        self.assertEqual(item["version"], "preprint")
        self.assertTrue(Path(item["path"]).name.endswith("_preprint.pdf"))
        self.assertEqual(item["expected_filename"], Path(item["path"]).name)
        self.assertEqual(list(item), load_yaml("output-contracts")["acquisition_item"])
        outcomes = {a["resolver"]: a["outcome"] for a in item["attempts"]}
        self.assertEqual(outcomes["openalex"], "failed")
        self.assertEqual(outcomes["semantic_scholar"], "no_candidates")  # its hdl URL was already tried by openalex
        self.assertEqual(outcomes["arxiv_preprint"], "downloaded")
        # rerun -> cache keeps the preprint version
        items2 = acquire_dois(["10.1007/978-3-031-76459-2_3"], self.tmp.name, None, cfg=CFG, http_get=http, scihub_fn=scihub_fake_factory([]), fallback=self.fallback)
        self.assertEqual((items2[0]["method"], items2[0]["version"]), ("cache", "preprint"))

    def test_published_version_is_default(self):
        http = http_fake_factory([(r"arxiv\.org/pdf/2312\.13041", pdf_response("https://arxiv.org/pdf/2312.13041"))])
        items = acquire_dois(["10.48550/arXiv.2312.13041"], self.tmp.name, None, cfg=CFG, http_get=http, scihub_fn=scihub_fake_factory([]), fallback=self.fallback)
        self.assertEqual(items[0]["version"], "published")


if __name__ == "__main__":
    unittest.main()
