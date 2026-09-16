import re
import unittest

from lib.compile_query import (
    attach_filters,
    attach_filters_openalex,
    build_synonym_index,
    compile_keyword_query_openalex,
    compile_topic_query_openalex,
    openalex_compiled_string,
    compile_keyword_query,
    compile_title_query,
    compile_topic_query,
    resolve_concept,
    resolve_from_year,
)
from lib.config import load_yaml
from tests.helpers import TODAY


class SynonymTableTests(unittest.TestCase):
    def test_no_alias_collisions_and_key_format(self):
        table = load_yaml("synonyms")
        build_synonym_index(table)  # raises on collision
        for key in table["concepts"]:
            self.assertRegex(key, r"^[a-z0-9_]+$")

    def test_collision_detected(self):
        bad = {"concepts": {"a": {"canonical": "x", "synonyms": ["y"]}, "b": {"canonical": "y", "synonyms": []}}}
        with self.assertRaises(ValueError):
            build_synonym_index(bad)


class ResolveConceptTests(unittest.TestCase):
    def test_hit_expands_in_file_order(self):
        block = resolve_concept("technology", "Artificial Intelligence.")
        self.assertEqual(block.matched_key, "artificial_intelligence")
        self.assertEqual(block.expansion, "synonyms")
        self.assertEqual(block.terms[0], "artificial intelligence")
        self.assertIn("deep learning", block.terms)

    def test_alias_resolves(self):
        self.assertEqual(resolve_concept("modality", "CT").matched_key, "computed_tomography")
        self.assertEqual(resolve_concept("modality", "ct  scan").matched_key, "computed_tomography")

    def test_miss_is_verbatim_and_unexpanded(self):
        block = resolve_concept("disease", "lung cancers")
        self.assertIsNone(block.matched_key)
        self.assertEqual(block.terms, ["lung cancers"])
        self.assertEqual(block.expansion, "none")


class CompileTests(unittest.TestCase):
    def test_topic_query_shape(self):
        blocks = [resolve_concept("technology", "artificial intelligence"), resolve_concept("disease", "lung cancer"), resolve_concept("modality", "CT")]
        q = compile_topic_query(blocks)
        self.assertTrue(q.startswith('TITLE-ABS-KEY("artificial intelligence" OR '))
        self.assertEqual(q.count(" AND "), 2)
        self.assertIn('TITLE-ABS-KEY("computed tomography" OR "CT" OR "CT scan")', q)

    def test_escaping(self):
        block = resolve_concept("other", 'say "hi"')
        self.assertEqual(compile_topic_query([block]), 'TITLE-ABS-KEY("say \\"hi\\"")')

    def test_keyword_preserved(self):
        raw = '  ("lung cancer") AND ("computed tomography")  '
        self.assertEqual(compile_keyword_query(raw, True), raw.strip())
        self.assertEqual(compile_keyword_query("lung cancer", False), 'TITLE-ABS-KEY("lung cancer")')

    def test_title_query(self):
        self.assertEqual(compile_title_query(" A Title "), 'TITLE("A Title")')


class FilterTests(unittest.TestCase):
    def test_year_precedence(self):
        self.assertEqual(resolve_from_year(2020, 2, "latest", today=TODAY), 2020)
        self.assertEqual(resolve_from_year(None, 2, "latest", today=TODAY), 2025)
        self.assertEqual(resolve_from_year(None, None, "latest", today=TODAY), 2024)
        self.assertEqual(resolve_from_year(None, None, "recent", today=TODAY), 2022)
        self.assertIsNone(resolve_from_year(None, None, None, today=TODAY))

    def test_attach_filters_exact_string(self):
        plan = attach_filters('TITLE-ABS-KEY("x")', 2024, "english", "article_or_review")
        self.assertEqual(plan.query, '(TITLE-ABS-KEY("x")) AND PUBYEAR > 2023 AND LANGUAGE(english) AND (DOCTYPE(ar) OR DOCTYPE(re))')
        self.assertEqual(plan.sort, "-coverDate")
        self.assertEqual(plan.filters, {"from_year": 2024, "language": "english", "document_type": "article_or_review"})

    def test_any_filters_add_nothing(self):
        plan = attach_filters('TITLE-ABS-KEY("x")', None, "any", "any")
        self.assertEqual(plan.query, 'TITLE-ABS-KEY("x")')
        self.assertEqual(plan.sort, "-citedby-count")
        self.assertNotRegex(plan.query, re.compile(r"LANGUAGE|DOCTYPE|PUBYEAR"))


class OpenAlexCompileTests(unittest.TestCase):
    def test_topic_query(self):
        blocks = [resolve_concept("technology", "artificial intelligence"), resolve_concept("disease", "lung cancer")]
        q = compile_topic_query_openalex(blocks)
        self.assertTrue(q.startswith('("artificial intelligence" OR "AI" OR '))
        self.assertIn(') AND ("lung cancer" OR ', q)

    def test_inner_quotes_dropped(self):
        self.assertEqual(compile_topic_query_openalex([resolve_concept("other", 'say "hi"')]), '("say hi")')

    def test_keyword_verbatim(self):
        self.assertEqual(compile_keyword_query_openalex('  "lung cancer" AND "CT"  '), '"lung cancer" AND "CT"')

    def test_filters_and_sort(self):
        plan = attach_filters_openalex('("x")', 2024, "english", "article_or_review")
        self.assertEqual(plan.filters, ["publication_year:>2023", "language:en", "type:article|review"])
        self.assertEqual(plan.sort, "publication_date:desc")
        self.assertEqual(openalex_compiled_string(plan), 'search=("x") | filter=publication_year:>2023,language:en,type:article|review | sort=publication_date:desc')

    def test_any_adds_nothing(self):
        plan = attach_filters_openalex('("x")', None, "any", "any")
        self.assertEqual(plan.filters, [])
        self.assertEqual(plan.sort, "cited_by_count:desc")
        self.assertEqual(openalex_compiled_string(plan), 'search=("x") | sort=cited_by_count:desc')


if __name__ == "__main__":
    unittest.main()
