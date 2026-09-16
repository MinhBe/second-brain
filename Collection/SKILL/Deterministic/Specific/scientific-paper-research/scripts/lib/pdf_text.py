"""PDF text extraction (fitz -> pdfplumber -> optional OCR). Vendored from ChangePdfToText/pdf_to_text.py."""

import shutil
from dataclasses import dataclass
from pathlib import Path

MIN_TEXT_THRESHOLD = 100


@dataclass
class PageText:
    page: int
    text: str


def import_optional(module_name: str):
    try:
        return __import__(module_name)
    except ImportError:
        return None


def extract_with_pdfplumber(pdf_path: Path) -> tuple[list[PageText], int]:
    pdfplumber = import_optional("pdfplumber")
    if pdfplumber is None:
        raise RuntimeError("Missing Python package: pdfplumber")

    pages: list[PageText] = []
    with pdfplumber.open(str(pdf_path)) as pdf:
        for index, page in enumerate(pdf.pages, 1):
            pages.append(PageText(index, page.extract_text() or ""))
        return pages, len(pdf.pages)


def extract_with_fitz(pdf_path: Path) -> tuple[list[PageText], int]:
    fitz = import_optional("fitz")
    if fitz is None:
        raise RuntimeError("Missing Python package: PyMuPDF")

    pages: list[PageText] = []
    with fitz.open(str(pdf_path)) as doc:
        for index, page in enumerate(doc, 1):
            pages.append(PageText(index, page.get_text() or ""))
        return pages, doc.page_count


def extract_with_ocr(pdf_path: Path, lang: str) -> tuple[list[PageText], int]:
    pdf2image = import_optional("pdf2image")
    pytesseract = import_optional("pytesseract")
    if pdf2image is None:
        raise RuntimeError("Missing Python package: pdf2image")
    if pytesseract is None:
        raise RuntimeError("Missing Python package: pytesseract")
    if shutil.which("tesseract") is None:
        raise RuntimeError("Missing tesseract executable in PATH")

    images = pdf2image.convert_from_path(str(pdf_path))
    pages = [
        PageText(index, pytesseract.image_to_string(image, lang=lang) or "")
        for index, image in enumerate(images, 1)
    ]
    return pages, len(images)


def page_chars(pages: list[PageText]) -> int:
    return len("\n".join(page.text for page in pages).strip())


def text_quality_score(pages: list[PageText]) -> int:
    text = "\n".join(page.text for page in pages)
    cjk_chars = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    mojibake_markers = sum(text.count(marker) for marker in ("Ã", "Â", "â€", "æ", "ç", "è", "å"))
    return len(text.strip()) + (cjk_chars * 10) - (mojibake_markers * 50)


def looks_mojibake(pages: list[PageText]) -> bool:
    text = "\n".join(page.text for page in pages)
    cjk_chars = sum(1 for char in text if "\u4e00" <= char <= "\u9fff")
    mojibake_markers = sum(text.count(marker) for marker in ("Ã", "Â", "â€", "æ", "ç", "è", "å"))
    return mojibake_markers >= 20 and cjk_chars < mojibake_markers


def extract_pdf(pdf_path: Path, ocr_mode: str, ocr_lang: str) -> tuple[list[PageText], int, str]:
    errors: list[str] = []
    best_direct: tuple[list[PageText], int, str] | None = None

    for engine, extractor in (
        ("fitz", extract_with_fitz),
        ("pdfplumber", extract_with_pdfplumber),
    ):
        try:
            pages, page_count = extractor(pdf_path)
            if best_direct is None or text_quality_score(pages) > text_quality_score(best_direct[0]):
                best_direct = (pages, page_count, engine)
            if page_count > 0 and page_chars(pages) >= MIN_TEXT_THRESHOLD and not looks_mojibake(pages):
                return pages, page_count, engine
            if looks_mojibake(pages):
                errors.append(f"{engine}: extracted mojibake-looking text")
            elif page_chars(pages) < MIN_TEXT_THRESHOLD:
                errors.append(f"{engine}: extracted less than {MIN_TEXT_THRESHOLD} chars")
        except Exception as exc:
            errors.append(f"{engine}: {exc}")

    if best_direct is not None:
        best_chars = page_chars(best_direct[0])
        best_page_count = best_direct[1]
        if best_page_count > 0 and (best_chars >= MIN_TEXT_THRESHOLD or (ocr_mode == "never" and best_chars > 0)):
            return best_direct

        if best_page_count == 0:
            errors.append(f"{best_direct[2]}: PDF has 0 readable pages")
        elif best_chars == 0:
            errors.append(f"{best_direct[2]}: extracted no text")

    if best_direct is not None and ocr_mode == "never":
        raise RuntimeError("; ".join(errors) if errors else "No text extracted")

    if best_direct is not None and page_chars(best_direct[0]) >= MIN_TEXT_THRESHOLD:
        return best_direct

    if ocr_mode in {"auto", "always"}:
        try:
            pages, page_count = extract_with_ocr(pdf_path, ocr_lang)
            if page_chars(pages) > 0:
                return pages, page_count, "ocr"
            errors.append("ocr: extracted no text")
        except Exception as exc:
            errors.append(f"ocr: {exc}")

    raise RuntimeError("; ".join(errors) if errors else "No text extracted")
