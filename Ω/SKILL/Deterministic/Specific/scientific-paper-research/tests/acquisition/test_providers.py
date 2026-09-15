import unittest

from lib.compile_query import OpenAlexPlan
from lib.providers import (
    available_search_providers,
    contact_email,
    openalex_paper_item,
    resolve_title_chain,
    resolve_title_crossref,
    search_openalex,
)
from tests.helpers import http_fake_factory, scopus_fake

TITLE = "Black-Box Adversarial Attacks Against SQL Injection Detection Model"


def crossref_items(*rows):
    return {"message": {"items": [{"DOI": doi, "title": [title], "issued": {"date-parts": [[year]]}} for doi, title, year in rows]}}


def openalex_work(i, title, doi, year=2024):
    return {"id": f"https://openalex.org/W{i}", "display_name": title, "doi": f"https://doi.org/{doi}" if doi else None,
            "publication_year": year, "cited_by_count": i, "authorships": [{"author": {"display_name": "Ann A"}}, {"author": {"display_name": "Bob B"}}],
            "primary_location": {"source": {"display_name": "Journal X"}}}


class ProviderAvailabilityTests(unittest.TestCase):
    def test_no_key_means_openalex_only(self):
        self.assertEqual(available_search_providers({}), ["openalex"])
        self.assertEqual(available_search_providers({"ELSEVIER_API_KEY": "k"}), ["scopus", "openalex"])

    def test_contact_email(self):
        self.assertEqual(contact_email({"UNPAYWALL_EMAIL": "me@x.org"}), "me@x.org")
        self.assertTrue(contact_email({}).endswith("@users.noreply.github.com"))


class TitleResolutionTests(unittest.TestCase):
    def test_crossref_exact(self):
        http = http_fake_factory([(r"api\.crossref\.org", crossref_items(("10.37256/cm.5420245292", TITLE, 2024), ("10.1/other", "Other", 2023)))])
        res = resolve_title_crossref(TITLE, {}, http_get=http)
        self.assertEqual(res["resolution"], "exact")
        self.assertEqual(res["resolved_doi"], "10.37256/cm.5420245292")
        self.assertIn("query.bibliographic=", http.calls[0][0])
        self.assertIn("mailto=", http.calls[0][0])

    def test_crossref_ambiguous_and_not_found(self):
        http = http_fake_factory([(r"api\.crossref\.org", crossref_items(("10.1/a", TITLE, 2024), ("10.1/b", TITLE, 2020)))])
        self.assertEqual(resolve_title_crossref(TITLE, {}, http_get=http)["resolution"], "ambiguous")
        http = http_fake_factory([(r"api\.crossref\.org", crossref_items())])
        self.assertEqual(resolve_title_crossref(TITLE, {}, http_get=http)["resolution"], "not_found")

    def test_chain_stops_at_first_exact(self):
        http = http_fake_factory([
            (r"api\.crossref\.org", crossref_items(("10.1/a", "Something else", 2024))),
            (r"api\.openalex\.org/works\?", {"meta": {"count": 1}, "results": [openalex_work(1, TITLE, "10.37256/cm.5420245292")]}),
        ])
        res = resolve_title_chain(TITLE, {}, {"http_get": http})
        self.assertEqual(res["resolution"], "exact")
        self.assertEqual(res["provider"], "openalex")
        self.assertEqual(res["providers_used"], ["crossref", "openalex"])

    def test_chain_uses_scopus_only_with_key(self):
        http = http_fake_factory([(r"api\.crossref\.org", crossref_items()), (r"api\.openalex\.org/works\?", {"meta": {"count": 0}, "results": []})])
        res = resolve_title_chain("Alpha Paper", {}, {"http_get": http, "request_fn": scopus_fake})
        self.assertEqual(res["resolution"], "not_found")
        self.assertEqual(res["providers_used"], ["crossref", "openalex"])
        res = resolve_title_chain("Alpha Paper", {"ELSEVIER_API_KEY": "k"}, {"http_get": http, "request_fn": scopus_fake})
        self.assertEqual(res["resolution"], "exact")
        self.assertEqual(res["provider"], "scopus")

    def test_provider_outage_is_skipped(self):
        http = http_fake_factory([(r"api\.openalex\.org/works\?", {"meta": {"count": 1}, "results": [openalex_work(1, TITLE, "10.1000/x")]})])  # crossref 404s
        res = resolve_title_chain(TITLE, {}, {"http_get": http})
        self.assertEqual(res["resolution"], "exact")
        self.assertEqual(res["providers_used"], ["openalex"])


class OpenAlexSearchTests(unittest.TestCase):
    def test_paper_item_mapping(self):
        item = openalex_paper_item(openalex_work(7, "T", "10.1000/AAA"))
        self.assertEqual(item["doi"], "10.1000/AAA")
        self.assertEqual(item["year"], "2024")
        self.assertEqual(item["cited_by"], 7)
        self.assertEqual(item["authors"], "Ann A; Bob B")
        self.assertEqual(item["eid"], "W7")
        self.assertEqual(item["source"], "Journal X")
        self.assertEqual(item["evidence_level"], "metadata_only")

    def test_search_pages_and_dedupes(self):
        pages = {
            "page=1": {"meta": {"count": 3}, "results": [openalex_work(1, "A", "10.1000/a"), openalex_work(2, "B", "10.1000/b")]},
            "page=2": {"meta": {"count": 3}, "results": [openalex_work(2, "B", "10.1000/b"), openalex_work(3, "C", None)]},
        }

        def responder(url, headers, verify_ssl):
            from tests.helpers import json_response

            for key, payload in pages.items():
                if key in url:
                    return json_response(url, payload)
            return json_response(url, {"meta": {"count": 3}, "results": []})

        http = http_fake_factory([(r"api\.openalex\.org/works\?", responder)])
        plan = OpenAlexPlan(search='("x")', filters=["language:en"], sort="cited_by_count:desc", from_year=None)
        found = search_openalex(plan, 3, {}, http_get=http)
        self.assertEqual(found["provider"], "openalex")
        self.assertEqual(found["total_hits"], 3)
        self.assertEqual([p["title"] for p in found["papers"]], ["A", "B", "C"])
        self.assertEqual(found["missing_doi"], 1)
        self.assertIn("filter=language%3Aen", http.calls[0][0])
        self.assertIn("per-page=3", http.calls[0][0])


if __name__ == "__main__":
    unittest.main()
