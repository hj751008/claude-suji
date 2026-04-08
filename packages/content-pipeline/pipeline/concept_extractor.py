"""PDF 텍스트에서 개념 추출 — Claude API"""

from __future__ import annotations
import json
from anthropic import Anthropic
from rich.console import Console

from .config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_RETRIES
from .models import ExtractedConcept
from .prompts.concept_extraction import SYSTEM, USER_TEMPLATE

console = Console(force_terminal=True)
_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def extract_concepts(
    pdf_pages: list[dict],
    unit_name: str,
    sub_unit_name: str,
) -> list[ExtractedConcept]:
    """PDF 페이지 텍스트에서 개념 추출

    Args:
        pdf_pages: [{"page": 1, "text": "..."}]
        unit_name: 단원명
        sub_unit_name: 소단원명

    Returns:
        추출된 개념 리스트
    """
    combined_text = "\n\n".join(
        f"[페이지 {p['page']}]\n{p['text']}" for p in pdf_pages
    )

    # 텍스트가 너무 길면 청크 분할
    max_chars = 12000
    if len(combined_text) > max_chars:
        console.print(f"[yellow]⚠[/] 텍스트가 길어 {max_chars}자로 잘라냅니다")
        combined_text = combined_text[:max_chars]

    user_msg = USER_TEMPLATE.format(
        unit_name=unit_name,
        sub_unit_name=sub_unit_name,
        pdf_text=combined_text,
    )

    client = _get_client()

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=4096,
                system=SYSTEM,
                messages=[{"role": "user", "content": user_msg}],
            )
            raw = response.content[0].text
            # JSON 블록 추출
            raw = _extract_json(raw)
            data = json.loads(raw)
            concepts = [ExtractedConcept(**item) for item in data]
            console.print(f"[green]✓[/] {len(concepts)}개 개념 추출 완료")
            return concepts
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            console.print(f"[yellow]⚠[/] 파싱 실패 (시도 {attempt}/{MAX_RETRIES}): {e}")
            if attempt == MAX_RETRIES:
                raise
        except Exception as e:
            console.print(f"[red]✗[/] API 오류 (시도 {attempt}/{MAX_RETRIES}): {e}")
            if attempt == MAX_RETRIES:
                raise

    return []  # unreachable


def _extract_json(text: str) -> str:
    """마크다운 코드 블록에서 JSON 추출"""
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        return text[start:end].strip()
    if "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        return text[start:end].strip()
    # 코드 블록 없으면 [ ] 범위 추출
    start = text.index("[")
    end = text.rindex("]") + 1
    return text[start:end]
