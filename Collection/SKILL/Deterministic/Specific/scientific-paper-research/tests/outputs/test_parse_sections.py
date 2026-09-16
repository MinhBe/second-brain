import unittest

from lib.parse_paper import build_text, detect_sections, evidence_template
from lib.pdf_text import PageText
from tests.helpers import FIXTURES

TEXT = (FIXTURES / "sample_paper.txt").read_text(encoding="utf-8")


class SectionTests(unittest.TestCase):
    def test_detects_headings_in_order(self):
        sections = detect_sections(TEXT)
        canon = [s["canonical"] for s in sections]
        self.assertEqual(canon, ["body", "abstract", "introduction", "methods", "results", "discussion", "limitations", "conclusion", "references"])

    def test_numbered_heading_and_offsets(self):
        sections = {s["canonical"]: s for s in detect_sections(TEXT)}
        methods = sections["methods"]
        self.assertEqual(methods["name"], "2. Methods")
        span = TEXT[methods["char_start"]:methods["char_end"]]
        self.assertTrue(span.startswith("2. Methods"))
        self.assertIn("240 adult participants", span)
        self.assertNotIn("Sensitivity increased", span)
        self.assertEqual(sections["body"]["char_end"], len(TEXT))

    def test_long_lines_are_not_headings(self):
        text = "Results of the study show that the introduction of the new methods and discussion\nResults\nfoo"
        canon = [s["canonical"] for s in detect_sections(text)]
        self.assertEqual(canon, ["body", "results"])

    def test_page_offsets(self):
        text, offsets = build_text([PageText(1, "Abstract\nfoo"), PageText(2, "Methods\nbar")])
        self.assertEqual(offsets, [0, 14])
        pages = [s["page_start"] for s in detect_sections(text, offsets)]
        self.assertEqual(pages, [1, 1, 2])

    def test_template_fields(self):
        template = evidence_template()
        self.assertEqual(len(template), 13)
        self.assertEqual(template["sample_size"], {"value": None, "source": None, "location": None, "status": "not_found"})


if __name__ == "__main__":
    unittest.main()
