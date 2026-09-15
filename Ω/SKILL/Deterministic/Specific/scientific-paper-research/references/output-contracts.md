# Output contracts (contract_version 1.3)

Source of truth: `config/output-contracts.yaml` (tests assert exact key order).

## Envelope (every run)

```
mode, status, request, result, clarification, error, next_command, contract_version
```

| status | exit | meaning |
|---|---|---|
| ok | 0 | pipeline completed |
| partial | 0 | completed; some items failed (see per-item `status`/`failure_class`) |
| clarification_required | 3 | ask `clarification.relay_verbatim`, stop |
| needs_evidence | 4 | analysis step 1 done; fill evidence file, run `next_command` |
| invalid_request | 2 | fix `request.json` per `error.message` |
| error | 1 | report `error.message`; do not retry |

`request` is the normalized request; `request.defaults_applied` lists every field filled from
`config/defaults.yaml`; `request.providers_used` (search and title modes) lists the providers that ran.

`error.code` is one of: `invalid_request`, `missing_env_ELSEVIER_API_KEY`, `scopus_syntax_requires_key`,
`missing_dependency`, `scopus_http_<n>`, `network_error`, `pdf_not_found`, `pdf_unreadable`,
`evidence_invalid`, `internal_error`. Missing `UNPAYWALL_EMAIL` is never an error (see warnings).

`evidence_level` (everywhere): `full_text` | `abstract_only` | `metadata_only` | `none`.

## result keys by mode

**TOPIC_SEARCH**: `compiled_query, provider, sort, filters, concept_blocks, total_hits, returned_count, papers, acquisition`
`provider` is `scopus` or `openalex`. For OpenAlex, `compiled_query` reads `search=... | filter=... | sort=...`.
`concept_blocks[]`: `slot, input_term, matched_key, terms, expansion` (`synonyms` only when the term is in `config/synonyms.yaml`).

**KEYWORD_SEARCH**: same without `concept_blocks`.

`papers[]`: `title, doi, year, source, cited_by, authors, eid, full_text_available, evidence_level`.
OpenAlex: `authors` joins all authors with `; `, `eid` is the OpenAlex work id (`W...`); Scopus gives the first author and EID.
`acquisition` is `null` unless `download: true`; then `attempted_count, downloaded_count, items[]`.

**DOI_DOWNLOAD**: `requested_count, valid_dois, invalid_dois[{input, reason}], downloaded_count, failed_count, items[]`

**Acquisition item** (`items[]` everywhere a download happens):
```
doi, status, method, path, expected_filename, sha256, title, is_oa, full_text_available, evidence_level, version,
chain_attempted, attempts, failure_class, warnings, manual_urls, error
```
- `status`: `downloaded` | `metadata_only` (title known, no PDF) | `failed` (nothing known).
- `version`: `published` | `preprint` (arXiv preprint found via `arxiv_preprint`; file name ends in `_preprint.pdf`) | `null` when not downloaded.
- `method`: `arxiv_direct` | `unpaywall` | `europe_pmc` | `openalex` | `semantic_scholar` | `arxiv_preprint` | `scihub_fallback` | `cache` (verified file already in `outdir`, from a previous run or saved manually) | `null`.
- `expected_filename`: the file name this run uses or would use (`<title>.pdf`, else `<doi>.pdf`). Save a manual download under this name in `outdir` and rerun to have it adopted.
- `chain_attempted[]`: resolver names in the order they ran. `attempts[]`: `{resolver, candidates[], outcome, error}` with outcome `downloaded` | `no_candidates` | `failed` | `skipped`. Candidates include deterministic expansions (IEEE stampPDF rewrite, figshare API files).
- `warnings[]`: `ssl_unverified` (TLS verification was skipped on retry), `impersonated_client` (curl_cffi browser impersonation was used), `no_unpaywall_email`.
- `manual_urls[]`: `https://doi.org/<doi>` first, then landing pages seen; open these in a real browser.
- `error`: last fetch error, else lookup errors, else the failure class.

| failure_class | meaning | action |
|---|---|---|
| none | downloaded | — |
| blocked_403 | publisher CDN rejected every client | open a manual URL in a browser |
| blocked_challenge | publisher returned a JavaScript check page (small HTML with challenge/verify markers) | open a manual URL in a browser |
| ssl_error | TLS verification failed and the retry failed too | open a manual URL in a browser |
| invalid_pdf | every URL returned a web page, not a PDF | open a manual URL in a browser |
| network | timeouts / 5xx | rerun later; verified files are skipped |
| subscription_only | Unpaywall/OpenAlex say `is_oa: false` | library access, VPN, or ask the authors |
| no_oa | no open-access location found, OA status unknown | check manual URLs |
| not_found | DOI unknown to Unpaywall and OpenAlex | check the DOI |

**TITLE_DOWNLOAD**: `requested_count, resolved_count, downloaded_count, items[]`
`items[]`: `input_title, resolution (exact|ambiguous|not_found), provider (crossref|openalex|scopus), resolved_doi, candidates[{title, doi, year}], suggestion, acquisition`.
Only `exact` titles are downloaded; ambiguous ones list candidates and are never guessed. `suggestion` is `null` or
`{doi, title, year, rule}` when exactly one candidate matches a fixed rule (`prefix`: one title is a prefix of the other;
`ratio`: difflib similarity >= 0.9; input must be >= 30 normalized characters). It is a proposal only: put the DOI in a
DOI_DOWNLOAD request to fetch it.

**PAPER_ANALYSIS step 1** (`needs_evidence`): `paper_id, pdf_path, sha256, engine, page_count, char_count, evidence_level, full_text_available, detected_doi, sections[{name, canonical, page_start, char_start, char_end}], sections_path, text_path, evidence_template_path, instructions_ref`

**PAPER_ANALYSIS step 2** (`ok`): `paper_id, pdf_path, doi, title, evidence_level, full_text_available, fields, validation{ok, error_count, errors[{code, field, message}]}`

**BATCH_ANALYSIS**: `papers[]` (each as PAPER_ANALYSIS, or `{pdf_path, error}`), `summary{total, parsed, failed, validated}`.

## Report (`--report path.md`)

Deterministic Markdown: `# Acquisition report` → `## Summary` (counts, failures by class) → `## Downloaded` →
`## Failed` (grouped by class in the table order above, each with error, warnings, manual URLs) →
`## Manual download` (table: DOI, save as, open; plus the three fixed steps; subscription-only papers excluded) →
`## Unresolved titles` (TITLE_DOWNLOAD, with `suggested:` lines) → `## Invalid DOIs`.
