"""PDF 텍스트 추출 — pypdf 사용"""

from __future__ import annotations
from pathlib import Path
from pypdf import PdfReader
from rich.console import Console

console = Console()


def extract_text_from_pdf(pdf_path: str | Path) -> list[dict]:
    """PDF에서 페이지별 텍스트 추출

    Returns:
        [{"page": 1, "text": "..."}, ...]
    """
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF 파일 없음: {path}")

    reader = PdfReader(str(path))
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"page": i + 1, "text": text.strip()})

    console.print(f"[green]✓[/] {path.name}: {len(pages)}페이지 추출 완료")
    return pages


def extract_all_pdfs(directory: str | Path, pattern: str = "*.pdf") -> list[dict]:
    """디렉토리 내 모든 PDF에서 텍스트 추출

    Returns:
        [{"file": "filename.pdf", "pages": [{"page": 1, "text": "..."}]}]
    """
    dir_path = Path(directory)
    if not dir_path.is_dir():
        raise NotADirectoryError(f"디렉토리 없음: {dir_path}")

    results = []
    pdf_files = sorted(dir_path.glob(pattern))
    console.print(f"[blue]📁[/] {len(pdf_files)}개 PDF 발견: {dir_path}")

    for pdf_file in pdf_files:
        try:
            pages = extract_text_from_pdf(pdf_file)
            results.append({"file": pdf_file.name, "pages": pages})
        except Exception as e:
            console.print(f"[red]✗[/] {pdf_file.name}: {e}")

    return results
