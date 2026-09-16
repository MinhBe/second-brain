# Changelog

All notable changes to this project will be documented in this file.

## [1.3.0] - 2026-09-11

### Added
- Resolvers `semantic_scholar` (open-access URL + arXiv id, no key) and `arxiv_preprint` (exact-title arXiv
  preprint of an unreachable paper) before the scihub fallback. Items carry `version: published|preprint`;
  preprint files get the `_preprint` suffix and the report marks them.
- `failure_class: blocked_challenge` for publisher JavaScript check pages (e.g. MDPI), routed to the manual download table.
- `references/playbook.md`: status and failure-class decision tables for the model, manual download loop, wording rules.

### Changed
- `contract_version` 1.3; `acquisition_item` gains `version`; chain order updated in `config/acquisition.yaml`.
- SKILL.md: always run download modes with `--report`, follow the playbook, name preprints.

## [1.2.0] - 2026-09-11

### Added
- `scripts/lib/env.py`: `UNPAYWALL_EMAIL` / `ELSEVIER_API_KEY` fall back to the Windows registry (User, then Machine)
  when missing from the process environment, so `setx` alone is enough.
- Deterministic URL expansion (`config/acquisition.yaml`): IEEE `stampPDF` rewrite for `ielx*/...pdf` and
  `document/<id>` links; figshare landing pages resolved through the public figshare API.
- Richer HTML -> PDF link extraction (iframe, download anchors, stampPDF, `?download=true`, `/pdf?`).
- Optional browser impersonation on 403 via `curl_cffi` when installed (`warnings: impersonated_client`).
- arXiv titles from the export API so arXiv files are named by title; scihub fallback files too.
- Acquisition item `expected_filename` and a `## Manual download` report section (open link, save as, rerun to adopt).
- Title suggestion for ambiguous TITLE_DOWNLOAD results (`suggestion`, prefix/ratio rule) - proposed, never downloaded.

### Changed
- `contract_version` 1.2; `acquisition_item` gains `expected_filename`, `title_item` gains `suggestion`.
- Analysis notes moved to `references/analysis-2026-09-11.md`.

## [1.1.0] - 2026-09-11

### Added
- No-key providers: Crossref and OpenAlex resolve titles; OpenAlex runs TOPIC/KEYWORD_SEARCH when
  `ELSEVIER_API_KEY` is absent (`config/providers.yaml`, `scripts/lib/providers.py`).
- Acquisition chain `arxiv_direct -> unpaywall -> europe_pmc -> openalex -> scihub_fallback -> metadata_only`
  (`scripts/lib/resolvers.py`), with per-item `attempts`, `failure_class`, `warnings`, `manual_urls`.
- HTTP policy (`scripts/lib/http.py`): browser User-Agent retry on 403, one unverified-TLS retry on
  certificate failures (recorded as `ssl_unverified`), HTML -> citation_pdf_url follow.
- Resume via `<outdir>/.acquired.json` (`method: cache`), and `--report <path.md>` Markdown report.

### Changed
- `contract_version` 1.1: search results carry `provider`; title items carry `provider`; acquisition item keys extended.
- Missing `UNPAYWALL_EMAIL` is a warning, not an error. scihub-cli arguments (incl. `--no-fast-fail`) moved to config.

### Removed
- `process_doi` / `attempt_download` from `scripts/lib/unpaywall.py` (replaced by the chain driver in `acquire.py`).

## [1.0.0] - 2026-09-11

### Changed
- Rebuilt as `scientific-paper-research`, a strict deterministic skill: six fixed modes
  (TOPIC_SEARCH, KEYWORD_SEARCH, DOI_DOWNLOAD, TITLE_DOWNLOAD, PAPER_ANALYSIS, BATCH_ANALYSIS),
  one entrypoint `scripts/run.py --request request.json`, fixed JSON envelope and exit codes.
- Query compilation moved out of the model: concept slots + approved synonym whitelist (`config/synonyms.yaml`),
  fixed PUBYEAR/LANGUAGE/DOCTYPE filters, declared defaults (`config/defaults.yaml`).
- Acquisition chain declared in `config/acquisition.yaml` (unpaywall -> scihub_fallback -> metadata_only) with PDF verification and sha256.
- Two-step paper analysis with provenance-checked evidence (`schemas/evidence.schema.json`, quote-in-text validation).
- English-only SKILL.md under 80 lines; Chinese README and per-mode CLI scripts removed.

### Added
- `config/`, `schemas/`, `references/`, offline `tests/` suite.

## [0.1.0] - 2026-02-09

### Added
- Initial public release of `sci-papers-downloder` as an academic paper download Skill.
- Scopus search workflow (`scripts/search_scopus.py`) for DOI/title metadata retrieval.
- DOI download workflow (`scripts/download_open_access.py`) with Unpaywall-first strategy.
- Optional Sci-Hub fallback integration via `scihub-cli`.
- End-to-end quantity and freshness runner (`scripts/topic_batch_download.py`).
- Intent mapping policy for terms like "some", "batch", "as many as possible", and "latest".
- Bilingual documentation: English `README.md` and Chinese `README.zh-CN.md`.
- MIT license and public GitHub repository packaging.
