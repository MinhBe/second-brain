# Book Insight Verification

Date: 2026-09-08. Workspace: `C:/Users/Admin/Documents/Collection`.

## Completed Checks

- `python -m unittest discover -s tests -v`: 27 tests passed.
- Skill creator `quick_validate.py`, with Python UTF-8 mode: valid skill.
- Live YouTube collection: 7 accepted videos in `amusing_live/manifest.json`.
- Existing seven-review Amusing dataset: 32 validated extractions, 6 glossary terms, 12 Q&A entries, zero schema errors and unverified snippets.
- Existing five-review Attached dataset: 32 validated extractions, 7 glossary terms, 12 Q&A entries, zero schema errors and unverified snippets.
- Final assembly: zero warnings and unknown labels for both reports; summary word counts 956 and 953 respectively.
- Both outputs have sections 0 through 12. Section 0 is the source inventory, followed by twelve content sections.
- Optional Anki CSVs generated in each working directory; stable-ID behavior covered by regression tests.
- Workspace junctions exist for book-insight and learn-this in both `.agents/skills` and `.claude/skills`.
- Original transcript files and prior analysis reports were not overwritten.

## Evidence Boundaries

- The reports use manually curated, source-backed claims. They are selective reconstructions, not exhaustive semantic extraction of every transcript sentence and not direct readings of either book.
- Subtitle kinds were checked against live metadata. The two ambiguous Vietnamese Amusing sources were resolved by comparing parsed cues against freshly downloaded manual subtitles.
- Citation validation establishes that a snippet exists in the cited paragraph, not that a paraphrase logically follows or a reviewer is factually correct. Semantic attribution still requires human/agent review.
- Full-read and BOOK/NOTE integration were tested with synthetic fixtures only; no complete book text was available in this workspace.
- Actual import into the Anki desktop application was not tested. CSVs use a stable first-field ID, not a fabricated internal Anki GUID.
- Fresh-session agent skill discovery and automatic learn-this routing were not exercised end to end. Filesystem registration and routing instructions were checked.
- Live collection is separate from the fixed review datasets used for the two example reports. It does not change their source IDs.
- Wrong-book and audiobook rejection have deterministic tests; the live search is not guaranteed to return those specific rejected examples.
