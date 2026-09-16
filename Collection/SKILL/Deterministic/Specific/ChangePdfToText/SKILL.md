---
name: change-pdf-to-text
description: Convert PDF files or folders of PDFs into Markdown and plain text, with direct text extraction first and OCR fallback for scanned documents when OCR dependencies are available.
---

# Change PDF To Text

Use this skill when the user wants PDFs converted into `.md` or `.txt`, especially batch conversion of language-learning PDFs under `C:\Users\Admin\Documents\Collection\Data\Language`.

## Workflow

- Use `pdf_to_text.py` for conversion. It accepts a single PDF or a folder and writes outputs without modifying source PDFs.
- Default input is `C:\Users\Admin\Documents\Collection\Data\Language`.
- Default output is `C:\Users\Admin\Documents\Collection\Data\Language\_converted_pdf_text`.
- Default output formats are both Markdown and plain text.
- The converter tries `PyMuPDF/fitz` first for fast Unicode text extraction, then `pdfplumber`, then OCR when `--ocr auto` or `--ocr always` and the OCR dependencies are available.
- Failed PDFs are recorded in `conversion_report.json`; a failed file must not stop the rest of a batch.

## Commands

Convert the default Language folder:

```powershell
python "C:\Users\Admin\Documents\Collection\Skills\Domain\personal\ChangePdfToText\run_convert.py"
```

Convert a specific file or folder:

```powershell
python "C:\Users\Admin\Documents\Collection\Skills\Domain\personal\ChangePdfToText\pdf_to_text.py" --input "C:\path\to\file-or-folder" --output "C:\path\to\output"
```

Useful options:

- `--formats md,txt` chooses Markdown, text, or both.
- `--ocr auto|never|always` controls OCR fallback.
- `--ocr-lang vie+eng+chi_sim+jpn+kor` changes Tesseract languages.
- `--no-recursive` limits folder conversion to top-level PDFs.

## Environment Notes

The direct extraction path needs `PyMuPDF` and/or `pdfplumber`. OCR also needs `pdf2image`, `pytesseract`, Tesseract in `PATH`, Poppler support for `pdf2image`, and installed Tesseract language data matching `--ocr-lang`.
