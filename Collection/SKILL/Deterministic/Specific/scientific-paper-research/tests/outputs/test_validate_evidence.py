import copy
import unittest

from lib.parse_paper import detect_sections, evidence_template
from lib.validate_evidence import validate_evidence
from tests.helpers import FIXTURES

TEXT = (FIXTURES / "sample_paper.txt").read_text(encoding="utf-8")
SECTIONS = detect_sections(TEXT)


def found(value, section, quote, source="full_text"):
    return {"value": value, "source": source, "location": {"section": section, "quote": quote}, "status": "found"}


def codes(errors):
    return [e["code"] for e in errors]


class ValidateEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.ev = evidence_template()

    def check(self, level="full_text"):
        return validate_evidence(self.ev, SECTIONS, TEXT, level)

    def test_untouched_template_is_valid(self):
        self.assertEqual(self.check(), [])

    def test_valid_found_fields(self):
        self.ev["study_design"] = found("randomized controlled trial", "methods", "This was a randomized controlled trial conducted at two academic hospitals.")
        self.ev["sample_size"] = found(240, "2. Methods", "We  enrolled 240 adult\nparticipants referred")  # whitespace differs
        self.ev["outcomes"] = found(["sensitivity"], "results", "sensitivity increased from 81% to 93%")  # case differs
        self.ev["conclusions"] = found(["AI helps"], "abstract", "The system improved sensitivity", source="abstract")
        self.assertEqual(self.check(), [])

    def test_model_inferred_rejected(self):
        self.ev["population"] = found("adults", "methods", "We enrolled 240 adult participants", source="model_inferred")
        self.assertEqual(codes(self.check()), ["source_forbidden"])

    def test_found_without_value(self):
        self.ev["population"] = found(None, "methods", "We enrolled 240 adult participants")
        self.assertEqual(codes(self.check()), ["found_without_value"])

    def test_not_found_with_value(self):
        self.ev["population"]["value"] = "adults"
        self.assertEqual(codes(self.check()), ["not_found_with_value"])

    def test_quote_not_in_text(self):
        self.ev["comparator"] = found("placebo", "methods", "the control arm received placebo tablets daily")
        self.assertEqual(codes(self.check()), ["quote_not_in_text"])

    def test_quote_in_other_section_is_rejected(self):
        self.ev["comparator"] = found("double reading", "results", "the control arm used standard double reading")
        self.assertEqual(codes(self.check()), ["quote_not_in_text"])

    def test_body_section_accepts_any_verbatim_quote(self):
        self.ev["comparator"] = found("double reading", "body", "the control arm used standard double reading")
        self.assertEqual(self.check(), [])

    def test_short_quote_rejected(self):
        self.ev["comparator"] = found("x", "methods", "This was a")
        self.assertEqual(codes(self.check()), ["quote_not_in_text"])

    def test_section_unknown(self):
        self.ev["comparator"] = found("double reading", "appendix", "the control arm used standard double reading")
        self.assertEqual(codes(self.check()), ["section_unknown"])

    def test_full_text_source_needs_full_text_level(self):
        self.ev["comparator"] = found("double reading", "methods", "the control arm used standard double reading")
        self.assertEqual(codes(self.check(level="none")), ["source_exceeds_evidence_level"])

    def test_abstract_source_needs_abstract_section(self):
        no_abstract = [s for s in SECTIONS if s["canonical"] != "abstract"]
        self.ev["conclusions"] = found(["x"], "body", "The system improved sensitivity", source="abstract")
        self.assertEqual(codes(validate_evidence(self.ev, no_abstract, TEXT, "full_text")), ["source_exceeds_evidence_level"])

    def test_missing_and_extra_fields(self):
        del self.ev["limitations"]
        self.ev["funding"] = copy.deepcopy(self.ev["methods"])
        self.assertEqual(sorted(codes(self.check())), ["extra_field", "missing_field"])

    def test_schema_and_semantic_errors_reported_together(self):
        self.ev["sample_size"] = found("two hundred", "methods", "We enrolled 240 adult participants")  # wrong type
        self.ev["comparator"] = found("placebo", "methods", "the control arm received placebo tablets daily")
        self.assertEqual(sorted(codes(self.check())), ["quote_not_in_text", "schema_violation"])

    def test_not_a_dict(self):
        self.assertEqual(codes(validate_evidence([], SECTIONS, TEXT, "full_text")), ["schema_violation"])


if __name__ == "__main__":
    unittest.main()
