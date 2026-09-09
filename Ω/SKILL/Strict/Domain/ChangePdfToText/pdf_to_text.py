import argparse
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


DEFAULT_INPUT = Path(__file__).resolve().parents[4] / 'Data' / 'Language'
DEFAULT_OUTPUT = DEFAULT_INPUT / "_converted_pdf_text"
MIN_TEXT_THRESHOLD = 100


@dataclass
class PageText:
    page: int
    text: str


@dataclass
class ConversionResult:
    pdf_path: Path
    output_txt: Path | None
    output_md: Path | None
    status: str
    engine: str
    page_count: int
    char_count: int
    error: str | None = None


def import_optional(module_name: str):
    try:
        return __import__(module_name)
    except ImportError:
        return None


def discover_pdfs(input_path: Path, recursive: bool) -> list[Path]:
    if input_path.is_file():
        return [input_path] if input_path.suffix.lower() == ".pdf" else []

    pattern = "**/*.pdf" if recursive else "*.pdf"
    return sorted(input_path.glob(pattern))


def relative_output_stem(pdf_path: Path, input_path: Path, output_dir: Path) -> Path:
    if input_path.is_file():
        relative = Path(pdf_path.stem)
    else:
        try:
            relative = pdf_path.relative_to(input_path).with_suffix("")
        except ValueError:
            relative = Path(pdf_path.stem)

    return output_dir / relative


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


def render_text(pages: list[PageText]) -> str:
    return "\n\n".join(page.text.strip() for page in pages if page.text.strip()).strip() + "\n"


def render_markdown(pdf_path: Path, pages: list[PageText]) -> str:
    lines = [f"# {pdf_path.stem}", "", f"Source: `{pdf_path.name}`", ""]
    for page in pages:
        text = page.text.strip()
        if not text:
            continue
        lines.extend([f"## Page {page.page}", "", text, ""])
    return "\n".join(lines).rstrip() + "\n"


def write_outputs(
    pdf_path: Path,
    input_path: Path,
    output_dir: Path,
    pages: list[PageText],
    formats: set[str],
) -> tuple[Path | None, Path | None]:
    stem = relative_output_stem(pdf_path, input_path, output_dir)
    stem.parent.mkdir(parents=True, exist_ok=True)

    txt_path = Path(f"{stem}.txt") if "txt" in formats else None
    md_path = Path(f"{stem}.md") if "md" in formats else None

    if txt_path is not None:
        txt_path.write_text(render_text(pages), encoding="utf-8")
    if md_path is not None:
        md_path.write_text(render_markdown(pdf_path, pages), encoding="utf-8")

    return txt_path, md_path


def convert_one(
    pdf_path: Path,
    input_path: Path,
    output_dir: Path,
    formats: set[str],
    ocr_mode: str,
    ocr_lang: str,
) -> ConversionResult:
    try:
        pages, page_count, engine = extract_pdf(pdf_path, ocr_mode, ocr_lang)
        txt_path, md_path = write_outputs(pdf_path, input_path, output_dir, pages, formats)
        return ConversionResult(
            pdf_path=pdf_path,
            output_txt=txt_path,
            output_md=md_path,
            status="ok",
            engine=engine,
            page_count=page_count,
            char_count=page_chars(pages),
        )
    except Exception as exc:
        return ConversionResult(
            pdf_path=pdf_path,
            output_txt=None,
            output_md=None,
            status="failed",
            engine="none",
            page_count=0,
            char_count=0,
            error=str(exc),
        )


def report_record(result: ConversionResult, root: Path) -> dict[str, object]:
    def display(path: Path | None) -> str | None:
        if path is None:
            return None
        try:
            return str(path.relative_to(root))
        except ValueError:
            return str(path)

    return {
        "pdf": display(result.pdf_path),
        "status": result.status,
        "engine": result.engine,
        "pages": result.page_count,
        "chars": result.char_count,
        "txt": display(result.output_txt),
        "md": display(result.output_md),
        "error": result.error,
    }


def parse_formats(value: str) -> set[str]:
    formats = {item.strip().lower() for item in value.split(",") if item.strip()}
    invalid = formats - {"md", "txt"}
    if invalid:
        raise argparse.ArgumentTypeError(f"Unsupported format(s): {', '.join(sorted(invalid))}")
    if not formats:
        raise argparse.ArgumentTypeError("At least one output format is required")
    return formats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Convert PDF files to Markdown and/or plain text with direct extraction and OCR fallback."
    )
    parser.add_argument(
        "--input",
        default=str(DEFAULT_INPUT),
        help=f"Input PDF file or folder. Default: {DEFAULT_INPUT}",
    )
    parser.add_argument(
        "--output",
        default=None,
        help=f"Output folder. Default: {DEFAULT_OUTPUT} for the default Language folder.",
    )
    parser.add_argument(
        "--formats",
        type=parse_formats,
        default=parse_formats("md,txt"),
        help="Comma-separated output formats: md,txt. Default: md,txt",
    )
    parser.add_argument(
        "--ocr",
        choices=["auto", "never", "always"],
        default="auto",
        help="OCR mode. Default: auto",
    )
    parser.add_argument(
        "--ocr-lang",
        default="vie+eng+chi_sim+jpn+kor",
        help="Tesseract language list. Default: vie+eng+chi_sim+jpn+kor",
    )
    parser.add_argument(
        "--recursive",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Search folders recursively. Default: true",
    )
    return parser


def main(argv: Iterable[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    input_path = Path(args.input).expanduser().resolve()
    output_dir = Path(args.output).expanduser().resolve() if args.output else DEFAULT_OUTPUT

    if not input_path.exists():
        print(f"Input not found: {input_path}", file=sys.stderr)
        return 2

    pdfs = discover_pdfs(input_path, args.recursive)
    if not pdfs:
        print(f"No PDF files found in: {input_path}", file=sys.stderr)
        return 2

    output_dir.mkdir(parents=True, exist_ok=True)
    results: list[ConversionResult] = []

    for index, pdf_path in enumerate(pdfs, 1):
        print(f"[{index}/{len(pdfs)}] {pdf_path}")
        result = convert_one(pdf_path, input_path, output_dir, args.formats, args.ocr, args.ocr_lang)
        results.append(result)
        if result.status == "ok":
            print(f"  ok: {result.engine}, pages={result.page_count}, chars={result.char_count}")
        else:
            print(f"  failed: {result.error}")

    report = {
        "input": str(input_path),
        "output": str(output_dir),
        "total": len(results),
        "ok": sum(1 for result in results if result.status == "ok"),
        "failed": sum(1 for result in results if result.status != "ok"),
        "results": [report_record(result, output_dir) for result in results],
    }
    report_path = output_dir / "conversion_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Report saved to: {report_path}")

    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
