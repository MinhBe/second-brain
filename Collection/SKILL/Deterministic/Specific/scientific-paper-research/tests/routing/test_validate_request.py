import unittest

from lib.validate_request import validate
from tests.helpers import TODAY, request


class ValidateRequestTests(unittest.TestCase):
    def test_each_mode_fixture_is_ok(self):
        for name in ("topic_search", "keyword_search", "doi_download", "title_download", "paper_analysis", "batch_analysis"):
            with self.subTest(name=name):
                res = validate(request(name), today=TODAY)
                self.assertEqual(res.status, "ok", res.error or res.clarification)
                self.assertIn("defaults_applied", res.normalized)

    def test_search_defaults_are_recorded(self):
        res = validate({"mode": "KEYWORD_SEARCH", "query": "x"}, today=TODAY)
        self.assertEqual(res.normalized["result_count"], 20)
        self.assertEqual(res.normalized["language"], "english")
        self.assertEqual(res.normalized["document_type"], "article_or_review")
        self.assertFalse(res.normalized["download"])
        for key in ("result_count", "language", "document_type", "download", "outdir"):
            self.assertIn(key, res.normalized["defaults_applied"])

    def test_result_count_words(self):
        self.assertEqual(validate({"mode": "KEYWORD_SEARCH", "query": "x", "result_count": "few"}).normalized["result_count"], 5)
        self.assertEqual(validate({"mode": "KEYWORD_SEARCH", "query": "x", "result_count": "many"}).normalized["result_count"], 50)
        self.assertEqual(validate({"mode": "KEYWORD_SEARCH", "query": "x", "result_count": 7}).normalized["result_count"], 7)
        self.assertNotIn("result_count", validate({"mode": "KEYWORD_SEARCH", "query": "x", "result_count": 7}).normalized["defaults_applied"])

    def test_unknown_quantity_word_is_schema_error(self):
        res = validate({"mode": "KEYWORD_SEARCH", "query": "x", "result_count": "lots"})
        self.assertEqual(res.status, "invalid_request")

    def test_missing_required_field(self):
        res = validate(request("doi_download_invalid"))
        self.assertEqual(res.status, "invalid_request")
        self.assertEqual(res.error["message"], "unknown field 'doi' is not allowed in DOI_DOWNLOAD")
        res = validate({"mode": "DOI_DOWNLOAD"})
        self.assertEqual(res.error["message"], "field 'dois' is required for DOI_DOWNLOAD")

    def test_unknown_key_rejected(self):
        res = validate({"mode": "KEYWORD_SEARCH", "query": "x", "synonyms": ["y"]})
        self.assertEqual(res.status, "invalid_request")
        self.assertIn("unknown field 'synonyms'", res.error["message"])

    def test_bad_mode(self):
        self.assertEqual(validate({"mode": "LIT_REVIEW"}).status, "invalid_request")
        self.assertEqual(validate({}).status, "invalid_request")
        self.assertEqual(validate("nope").status, "invalid_request")

    def test_clarification_empty_concepts(self):
        res = validate(request("topic_search_missing_concepts"), today=TODAY)
        self.assertEqual(res.status, "clarification_required")
        self.assertEqual(res.clarification["missing"][0]["field"], "concepts")
        self.assertTrue(res.clarification["relay_verbatim"].startswith("Please provide the core concept"))

    def test_clarification_future_year(self):
        res = validate({"mode": "KEYWORD_SEARCH", "query": "x", "year_from": 2031}, today=TODAY)
        self.assertEqual(res.status, "clarification_required")
        self.assertEqual(res.clarification["missing"][0]["field"], "year_from")

    def test_clarification_unresolved_filter(self):
        res = validate({"mode": "TOPIC_SEARCH", "concepts": [{"slot": "disease", "term": "asthma"}], "unresolved_filters": ["population", "geography"]}, today=TODAY)
        self.assertEqual(res.status, "clarification_required")
        self.assertEqual([m["field"] for m in res.clarification["missing"]], ["population", "geography"])

    def test_never_default_slots_are_not_defaulted(self):
        res = validate({"mode": "TOPIC_SEARCH", "concepts": [{"slot": "disease", "term": "asthma"}]}, today=TODAY)
        for slot in ("population", "geography", "intervention", "comparator", "study_type"):
            self.assertNotIn(slot, res.normalized)
            self.assertNotIn(slot, res.normalized["defaults_applied"])

    def test_doi_normalization_and_dedupe(self):
        res = validate({"mode": "DOI_DOWNLOAD", "dois": ["https://doi.org/10.1000/AAA.", "10.1000/aaa", "junk", "doi:10.1000/bbb)"]})
        self.assertEqual(res.status, "ok")
        self.assertEqual(res.normalized["dois"], ["10.1000/AAA", "10.1000/bbb"])
        self.assertEqual(res.normalized["invalid_dois"][0]["input"], "junk")

    def test_too_many_dois(self):
        res = validate({"mode": "DOI_DOWNLOAD", "dois": [f"10.1000/{i}" for i in range(51)]})
        self.assertEqual(res.status, "invalid_request")

    def test_all_invalid_dois_is_clarification(self):
        res = validate({"mode": "DOI_DOWNLOAD", "dois": ["junk"]})
        self.assertEqual(res.status, "clarification_required")


if __name__ == "__main__":
    unittest.main()
