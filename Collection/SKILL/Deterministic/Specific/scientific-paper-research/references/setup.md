# Setup

## Python packages

```powershell
pip install pyyaml jsonschema pymupdf
```

`pdfplumber` is an optional second extractor. OCR for scanned PDFs additionally needs
`pdf2image`, `pytesseract`, Poppler, and Tesseract in `PATH`; without them the run reports `pdf_unreadable`.

## No-key path (default)

Everything runs without any API key:

| Mode | Without keys | With `ELSEVIER_API_KEY` |
|---|---|---|
| TOPIC_SEARCH / KEYWORD_SEARCH | OpenAlex (`result.provider: openalex`) | Scopus first |
| TITLE_DOWNLOAD | Crossref, then OpenAlex | Scopus as third fallback |
| DOI_DOWNLOAD | arXiv direct, Europe PMC, OpenAlex, scihub-cli | same |
| PAPER/BATCH_ANALYSIS | local only | same |

`UNPAYWALL_EMAIL` is optional but recommended: it enables the Unpaywall resolver (more open-access
locations) and is used as the contact email for OpenAlex, Crossref and Europe PMC. Without it the item
carries `warnings: ["no_unpaywall_email"]` and a fixed placeholder contact is sent (`config/providers.yaml`).

`query_is_scopus_syntax: true` is the one request that needs `ELSEVIER_API_KEY` (error `scopus_syntax_requires_key`).
For OpenAlex, boolean operators in `query` must be uppercase `AND` / `OR` / `NOT`; phrases go in double quotes.

## Credentials (persistent, Windows)

```powershell
setx ELSEVIER_API_KEY "your_elsevier_key"
setx UNPAYWALL_EMAIL "you@example.com"
```

`setx` alone is enough: when a variable is missing from the process environment the script reads it from the
Windows registry (User level, then Machine level). No `$env:` prefix is needed per command. Scopus access depends
on your institution's entitlement (<https://dev.elsevier.com/>).

## Acquisition chain and network policy (`config/acquisition.yaml`)

Order is fixed: `arxiv_direct → unpaywall → europe_pmc → openalex → semantic_scholar → arxiv_preprint → scihub_fallback → metadata_only`.
`arxiv_preprint` only fires when the arXiv id is known (Semantic Scholar) or an arXiv entry has exactly the same normalized title; such files are marked `version: preprint` and named `*_preprint.pdf`.
For each candidate URL the downloader: sends a descriptive User-Agent; on HTTP 403 retries once with a
browser User-Agent; on `CERTIFICATE_VERIFY_FAILED` retries once without TLS verification and records
`warnings: ["ssl_unverified"]` (set `http.ssl.retry_unverified: false` to disable); follows one HTML →
`citation_pdf_url` hop. Every saved file must start with `%PDF`, be at least 1024 bytes, and gets a sha256.

Candidate URLs are expanded deterministically (`candidate_rewrites`, `landing_expanders`): IEEE `ielx*/...pdf` and
`document/<id>` links also try `stampPDF/getPDF.jsp?arnumber=<id>` (returns the PDF for open-access IEEE articles),
and figshare landing pages are resolved through the public figshare API to their file URLs.

Publisher CDNs that block scripts (e.g. MDPI) are usually reachable through their PubMed Central copy via
Europe PMC; subscription-only papers are reported as `failure_class: subscription_only` with `manual_urls`.

Optional: `pip install curl_cffi` enables one extra retry with a real browser TLS fingerprint after a 403
(`http.impersonate_on_403`, warning `impersonated_client`). Tested against MDPI from this network it passes the 403 but then receives a JavaScript challenge page (`failure_class: blocked_challenge`); only a real browser can pass it, so the manual download flow below covers that case.

## Manual download loop

When a run ends with `blocked_403` / `invalid_pdf` / `ssl_error` items, the report's `## Manual download` table lists,
per paper, the link to open and the exact file name to save as (`expected_filename`). Save the PDF into the request's
`outdir` under that name and rerun the same command: the file is verified and adopted (`method: cache`), and only the
remaining failures are retried.

## Resume

`<outdir>/.acquired.json` records every verified download. Rerunning the same request skips those DOIs
(`method: cache`) and retries only failures, so you can rerun after switching network or VPN.

## Report

```powershell
python -X utf8 scripts/run.py --request request.json --report report.md
```

Writes a deterministic Markdown summary: downloaded table, failures grouped by `failure_class` with the
links to open in a real browser, unresolved titles, invalid DOIs.

## Optional scihub-cli fallback

`scihub_fallback.mode: auto`: when no open-access copy was found, the script calls `scihub-cli` if installed
(with `extra_args` from config), otherwise records `scihub_cli_not_found`. Install:

```powershell
uv tool install git+https://github.com/Oxidane-bot/scihub-cli.git
```

Set `mode: off` to disable. Using this source may violate publisher terms or local law; that is the operator's decision.

## Verify

```powershell
python -X utf8 -m unittest discover -s tests -t .
```
