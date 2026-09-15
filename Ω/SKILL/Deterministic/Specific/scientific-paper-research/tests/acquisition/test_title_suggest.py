import unittest

from lib.providers import resolve_title_chain, suggest_doi
from tests.helpers import http_fake_factory

FULL = "Enhancing Financial Fraud Detection through Addressing Class Imbalance Using Hybrid SMOTE-GAN Techniques"
SHORT = "Enhancing Financial Fraud Detection through Addressing Class Imbalance Using Hybrid SMOTE-GAN"


def cand(title, doi, year="2023"):
    return {"title": title, "doi": doi, "year": year}


class SuggestTests(unittest.TestCase):
    def test_prefix_rule(self):
        s = suggest_doi(SHORT, [cand(FULL, "10.3390/ijfs11030110"), cand("Enhancing Medicare Fraud Detection", "10.1109/x")])
        self.assertEqual(s, {"doi": "10.3390/ijfs11030110", "title": FULL, "year": "2023", "rule": "prefix"})

    def test_ratio_rule(self):
        s = suggest_doi("Modeling Tabular Data using Conditional GAN", [cand("Modelling Tabular Data using a Conditional GAN", "10.1000/a")])
        self.assertEqual(s["rule"], "ratio")
        self.assertIsNone(suggest_doi("Modeling Tabular Data using Conditional GAN", [cand("Modeling Image Data using Diffusion Models", "10.1000/b")]))

    def test_two_matches_means_none(self):
        self.assertIsNone(suggest_doi(SHORT, [cand(FULL, "10.1/a"), cand(FULL + " (Preprint)", "10.1/b")]))

    def test_short_input_means_none(self):
        self.assertIsNone(suggest_doi("SMOTE-GAN", [cand("SMOTE-GAN Techniques", "10.1/a")]))

    def test_candidate_without_doi_ignored(self):
        self.assertIsNone(suggest_doi(SHORT, [cand(FULL, None)]))


class ChainSuggestionTests(unittest.TestCase):
    def test_ambiguous_result_carries_suggestion(self):
        http = http_fake_factory([(r"api\.crossref\.org", {"message": {"items": [
            {"DOI": "10.3390/ijfs11030110", "title": [FULL], "issued": {"date-parts": [[2023]]}},
            {"DOI": "10.1109/access.2024.3385781", "title": ["Enhancing Medicare Fraud Detection Through Machine Learning"], "issued": {"date-parts": [[2024]]}},
        ]}})])
        res = resolve_title_chain(SHORT, {}, {"http_get": http})
        self.assertEqual(res["resolution"], "ambiguous")
        self.assertEqual(res["suggestion"]["doi"], "10.3390/ijfs11030110")
        self.assertIsNone(res["resolved_doi"])  # never auto-selected


if __name__ == "__main__":
    unittest.main()
