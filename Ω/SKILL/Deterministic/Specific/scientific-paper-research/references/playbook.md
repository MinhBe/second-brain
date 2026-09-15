# Playbook: what to do after every run

Read `status` in the JSON output. Do exactly the row that matches. Copy values from the output; never invent,
rephrase, or "improve" them. Never switch to a different strategy, source, DOI, or title.

## 1. Status table

| status | exit | do exactly this |
|---|---|---|
| ok | 0 | Relay `result` to the user (for downloads: the report file). Stop. |
| partial | 0 | Relay `result`. Then follow section 2. |
| clarification_required | 3 | Send the user `clarification.relay_verbatim` word for word. Stop until they answer. Then write a new request with their answer and run again. |
| needs_evidence | 4 | Open `result.evidence_template_path`, fill it per `references/evidence-fields.md`, run `next_command` verbatim. |
| invalid_request | 2 | Fix only the field named in `error.message`, run the same command again. |
| error | 1 | Tell the user `error.message` and `error.setup_hint`. Stop. Do not retry with a different request. |

## 2. Download modes with failures (status partial)

1. If the run had no `--report`, run the exact same command again with `--report <outdir>/report.md`. Cached files are not re-downloaded.
2. Open the report. Relay to the user, verbatim: the `## Summary` table, the `## Manual download` table, and the sentence about subscription-only papers if present.
3. Say which downloaded files are marked `(preprint)`: they are arXiv preprints, not the published version.
4. Then apply section 3 for each failure class present. Do not search for other sources yourself.

## 3. Failure class table

| failure_class | meaning | who acts | what happens next |
|---|---|---|---|
| blocked_403 | publisher CDN rejects every HTTP client | user (browser) | manual download loop (section 4) |
| blocked_challenge | publisher shows a JavaScript check page | user (browser) | manual download loop (section 4) |
| ssl_error | TLS certificate invalid even after retry | user (browser) | manual download loop (section 4) |
| invalid_pdf | every URL returned a web page | user (browser) | manual download loop (section 4) |
| network | timeout or 5xx | nobody now | tell the user to rerun later |
| subscription_only | no open-access copy anywhere | user (library / authors) | nothing automatic; say so once |
| no_oa | no OA location found | user (browser) | manual download loop (section 4) |
| not_found | DOI unknown to Unpaywall and OpenAlex | user | ask the user to check the DOI; do not guess a replacement |

## 4. Manual download loop

For each row of the report's `## Manual download` table:

1. Give the user the `open` link and the exact `save as` file name. Tell them to save the PDF into `outdir` under that name.
2. If you have a browser tool: open the link, download the PDF, save it into `outdir` under exactly the `save as` name. Do not rename it.
3. When the user says the files are saved (or after your own browser step), run the same command once more. Saved files are verified and adopted (`method: cache`); only remaining failures are retried.
4. Stop when every item is `downloaded`, or when the only remaining classes are `subscription_only` or `not_found`.

Run the rerun at most once per round of saved files. Never delete or move files in `outdir`.

## 5. TITLE_DOWNLOAD specifics

- `resolution: ambiguous` with a `suggestion`: show the user the suggested DOI and its rule. Ask whether it is the right paper.
  Only if they confirm, run a DOI_DOWNLOAD request with that DOI. Never download a suggestion on your own.
- `resolution: not_found`: ask the user for the DOI or the exact full title. Do not search the web for it.

## 6. Words to use when relaying

- `downloaded` + `version: published` → "downloaded (published version)"
- `downloaded` + `version: preprint` → "downloaded as arXiv preprint (not the published version)"
- `metadata_only` → "not downloaded; title known; see manual download"
- `failed` → "not downloaded; nothing found for this DOI"
