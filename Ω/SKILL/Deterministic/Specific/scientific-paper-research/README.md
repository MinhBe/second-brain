# scientific-paper-research

A strict, deterministic skill for scientific paper search, download, and structured PDF analysis.
The model classifies intent and fills a small JSON request; everything else is code and config.

```
MODEL DECIDES LESS. CODE DECIDES MORE.
user input -> fixed mode -> validated request -> fixed pipeline -> fixed output
```

- `SKILL.md`: the only file the model needs (mode table, fields, one command).
- `scripts/run.py`: single entrypoint. `scripts/lib/`: validation, query compiler, Scopus, Unpaywall, PDF parsing, evidence validation.
- `config/`: defaults, mode rules, synonym whitelist, acquisition chain, section patterns, output contracts.
- `schemas/`: request, evidence, output JSON schemas.
- `references/`: setup, request examples, output contracts, evidence-field guide, design spec.
- `tests/`: offline unittest suite (no network).

Modes: `TOPIC_SEARCH`, `KEYWORD_SEARCH`, `DOI_DOWNLOAD`, `TITLE_DOWNLOAD`, `PAPER_ANALYSIS`, `BATCH_ANALYSIS`.
No API key required: OpenAlex and Crossref are used when Scopus credentials are absent; downloads chain arXiv, Unpaywall, Europe PMC, OpenAlex, Semantic Scholar, arXiv preprints, then optional scihub-cli. `references/playbook.md` tells the model what to do after each run.

```powershell
python -X utf8 scripts/run.py --request request.json
python -X utf8 -m unittest discover -s tests -t .
```

See `references/setup.md` for credentials. Scopus/Unpaywall client code derives from
[sci-papers-downloder](https://github.com/wdc63/sci-papers-downloder) (MIT).
