"""웹툰 스크립트 생성 — Claude API"""

from __future__ import annotations
import json
from anthropic import Anthropic
from rich.console import Console

from .config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_RETRIES
from .models import CreatedProblem, WebtoonScript, WebtoonLine
from .prompts.webtoon import SYSTEM, USER_TEMPLATE

console = Console()
_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def generate_webtoon_script(
    problem: CreatedProblem,
    concept_name: str,
) -> WebtoonScript:
    """문제에 대한 웹툰 해설 스크립트 생성"""
    client = _get_client()

    solution_summary = ""
    if problem.solution_steps:
        solution_summary = " → ".join(
            f"{s.explanation}" for s in problem.solution_steps
        )

    user_msg = USER_TEMPLATE.format(
        problem_body=problem.body,
        problem_answer=problem.answer,
        concept_name=concept_name,
        solution_summary=solution_summary or "(풀이 없음)",
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.messages.create(
                model=MODEL_NAME,
                max_tokens=2048,
                system=SYSTEM,
                messages=[{"role": "user", "content": user_msg}],
            )
            raw = _extract_json(response.content[0].text)
            data = json.loads(raw)

            lines = [WebtoonLine(**item) for item in data]
            console.print(f"    [green]✓[/] 웹툰 스크립트 {len(lines)}줄 생성")
            return WebtoonScript(lines=lines)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            console.print(
                f"    [yellow]⚠[/] 파싱 실패 (시도 {attempt}/{MAX_RETRIES}): {e}"
            )
            if attempt == MAX_RETRIES:
                raise
        except Exception as e:
            console.print(
                f"    [red]✗[/] API 오류 (시도 {attempt}/{MAX_RETRIES}): {e}"
            )
            if attempt == MAX_RETRIES:
                raise

    return WebtoonScript(lines=[])  # unreachable


def generate_webtoon_scripts(
    problems: list[CreatedProblem],
    concept_name: str,
) -> list[WebtoonScript]:
    """문제 리스트에 대한 웹툰 스크립트 일괄 생성"""
    scripts = []
    for i, problem in enumerate(problems):
        console.print(f"  [blue]🎬[/] 문제 {i+1}/{len(problems)} 웹툰 스크립트...")
        try:
            script = generate_webtoon_script(problem, concept_name)
            scripts.append(script)
        except Exception as e:
            console.print(f"    [red]✗[/] 건너뜀: {e}")
            scripts.append(WebtoonScript(lines=[]))

    console.print(f"[green]✓[/] 웹툰 스크립트 {len(scripts)}개 완료")
    return scripts


def _extract_json(text: str) -> str:
    """JSON 배열 추출"""
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        return text[start:end].strip()
    if "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        return text[start:end].strip()
    start = text.index("[")
    end = text.rindex("]") + 1
    return text[start:end]
