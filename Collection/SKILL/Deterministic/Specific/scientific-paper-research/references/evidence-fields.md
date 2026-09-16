# Evidence fields (PAPER_ANALYSIS / BATCH_ANALYSIS step 2)

Step 1 wrote three files per paper into `workdir`: `<id>.text.txt` (full extracted text),
`<id>.sections.json` (section spans), `<id>.evidence.json` (template). Edit ONLY the evidence file.

## Rule

```
NOT FOUND != INFER
```

Every field is a provenance object:

```json
{"value": ..., "source": "full_text", "location": {"section": "methods", "quote": "verbatim text"}, "status": "found"}
```

- `status: "found"` requires `value`, `source`, and `location`.
- `status: "not_found"` requires `value: null`, `source: null`, `location: null`. Leave the template line untouched.
- `source` is one of `metadata`, `abstract`, `full_text`. There is no `model_inferred`; the validator rejects it.
- `location.section` must be a `canonical` or `name` from `<id>.sections.json` (`body` always exists).
- `location.quote` is copied verbatim from that section of `<id>.text.txt`, 15 to 300 characters.
  Whitespace and letter case are ignored; wording is not.
- `source: "full_text"` is allowed only when step 1 reported `evidence_level: full_text`.
- `source: "abstract"` is allowed only when an `abstract` section was detected.

## Fields

| field | value type | look in |
|---|---|---|
| study_design | string (e.g. "randomized controlled trial") | methods, abstract |
| population | string | methods |
| sample_size | integer | methods, results |
| intervention | string | methods |
| comparator | string | methods |
| outcomes | list of strings | methods, results |
| inclusion_criteria | list of strings | methods |
| exclusion_criteria | list of strings | methods |
| methods | list of strings (procedures) | methods |
| statistical_methods | list of strings | methods |
| key_results | list of strings | results, abstract |
| conclusions | list of strings | conclusion, abstract |
| limitations | list of strings | limitations, discussion |

## Procedure

1. Read `<id>.text.txt` once.
2. For each field, if the paper states it, fill the four keys. Otherwise leave `not_found`.
3. Run `next_command` from the step-1 output. If `status` is `error` with `evidence_invalid`,
   fix exactly the fields listed in `result.validation.errors` and run the same command again.
