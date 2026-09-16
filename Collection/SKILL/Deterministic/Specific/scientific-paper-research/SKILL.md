---
name: scientific-paper-research
description: Strict, deterministic scientific paper search, download and structured PDF analysis via Scopus, Unpaywall and a fixed evidence schema. Use when the user asks to find, search, download, or analyze scientific papers by topic, keywords, DOI, title, or PDF file.
---

# Scientific Paper Research (strict)

You are a parser, not a research strategist. Do exactly four things:
1. Pick ONE mode from the table.
2. Write `request.json` with only the fields listed.
3. Run the command.
4. Relay `result` to the user as-is (or `clarification.relay_verbatim` / `error.message`).

Never add papers, keywords, synonyms, filters, years, or analysis the user did not state.
Never claim a paper was read unless its `evidence_level` is `full_text`.
Never retry with a different strategy after an error; report `error.message`.
A downloaded item with `version: preprint` is an arXiv preprint, not the published version: say so.

## Mode table

| User supplies | mode | required field |
|---|---|---|
| one or more PDF file paths (2+) | BATCH_ANALYSIS | `pdf_paths: []` |
| one PDF file path | PAPER_ANALYSIS | `pdf_path` |
| DOI(s) like `10.xxxx/...` | DOI_DOWNLOAD | `dois: []` |
| exact paper title(s) to download | TITLE_DOWNLOAD | `titles: []` |
| exact keywords or a boolean query | KEYWORD_SEARCH | `query` |
| a topic, research title, or question | TOPIC_SEARCH | `concepts: [{slot, term}]` |

If several apply, the higher row wins. Copy DOIs, titles, and queries verbatim.
For TOPIC_SEARCH use the user's own words as `term`; `slot` is one of
`technology, disease, modality, population, intervention, comparator, outcome, geography, study_type, other`.

## Optional fields (search modes only; copy what the user said, otherwise omit)

`result_count` (number, or `few` | `batch` | `max`), `freshness` (`latest` | `recent`),
`year_from`, `years_back`, `language` (`english` | `any`),
`document_type` (`article` | `review` | `article_or_review` | `any`), `download` (true | false), `outdir`.
KEYWORD_SEARCH: `query_is_scopus_syntax: true` when the query already uses Scopus field codes.
If the user mentions a population, place, intervention, comparator, or study type WITHOUT a value,
list the slot name in `unresolved_filters` and the script will ask.

## Command

```powershell
python -X utf8 scripts/run.py --request request.json
```

Download modes: always append `--report <outdir>/report.md`; the report lists failed items with the link to open and the exact file name to save.
After every run follow `references/playbook.md` (status and failure_class tables). When status is `partial`, relay the report's Manual download table verbatim.
Exit codes: `0` done, relay `result`. `2` fix `request.json` using `error.message`.
`3` ask the user `clarification.relay_verbatim`, then stop. `4` PAPER/BATCH_ANALYSIS step 1 done:
fill the evidence file (see `references/evidence-fields.md`), then run `next_command` verbatim.
`1` report `error.message`; do not retry.

## Examples

```json
{"mode": "DOI_DOWNLOAD", "dois": ["10.1016/j.cell.2020.01.001", "10.1038/s41586-020-2012-7"]}
```

```json
{"mode": "TOPIC_SEARCH", "result_count": 8, "freshness": "latest",
 "concepts": [{"slot": "technology", "term": "artificial intelligence"},
              {"slot": "disease", "term": "lung cancer"}, {"slot": "modality", "term": "CT"}]}
```

## References (read only when the command or this file says so)

`references/playbook.md` (what to do after each run), `references/request-examples.md`, `references/output-contracts.md`,
`references/evidence-fields.md`, `references/setup.md` (API keys, dependencies).
No API key is required: without `ELSEVIER_API_KEY` the script uses OpenAlex and Crossref automatically.
