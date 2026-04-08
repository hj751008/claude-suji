"""3-페르소나 독립 검증 — Claude API"""

from __future__ import annotations
import json
from anthropic import Anthropic
from rich.console import Console

from .config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_RETRIES
from .models import CreatedProblem, ReviewResult, ReviewVerdict
from .prompts.review import PERSONAS, USER_TEMPLATE

console = Console()
_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def review_problem(
    problem: CreatedProblem,
    concept_name: str,
) -> list[ReviewResult]:
    """3명의 페르소나가 독립적으로 문제를 검증

    Returns:
        3개의 ReviewResult (각 페르소나별)
    """
    client = _get_client()
    results: list[ReviewResult] = []

    solution_text = ""
    if problem.solution_steps:
        solution_text = " → ".join(
            f"({s.step}) {s.explanation} {s.expression}".strip()
            for s in problem.solution_steps
        )

    user_msg = USER_TEMPLATE.format(
        concept_name=concept_name,
        difficulty=problem.difficulty.value,
        problem_body=problem.body,
        problem_answer=problem.answer,
        solution_steps=solution_text or "(풀이 없음)",
    )

    for persona_name, persona_system in PERSONAS.items():
        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = client.messages.create(
                    model=MODEL_NAME,
                    max_tokens=1024,
                    system=persona_system,
                    messages=[{"role": "user", "content": user_msg}],
                )
                raw = _extract_json(response.content[0].text)
                data = json.loads(raw)

                result = ReviewResult(
                    persona=persona_name,
                    verdict=ReviewVerdict(data["verdict"]),
                    reason=data["reason"],
                )
                results.append(result)

                icon = "✓" if result.verdict == ReviewVerdict.PASS else "✗"
                color = "green" if result.verdict == ReviewVerdict.PASS else "red"
                console.print(
                    f"    [{color}]{icon}[/] {persona_name}: {result.verdict.value}"
                )
                break
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                console.print(
                    f"    [yellow]⚠[/] {persona_name} 파싱 실패 "
                    f"(시도 {attempt}/{MAX_RETRIES}): {e}"
                )
                if attempt == MAX_RETRIES:
                    results.append(ReviewResult(
                        persona=persona_name,
                        verdict=ReviewVerdict.FAIL,
                        reason=f"파싱 오류: {e}",
                    ))
            except Exception as e:
                console.print(
                    f"    [red]✗[/] {persona_name} API 오류 "
                    f"(시도 {attempt}/{MAX_RETRIES}): {e}"
                )
                if attempt == MAX_RETRIES:
                    results.append(ReviewResult(
                        persona=persona_name,
                        verdict=ReviewVerdict.FAIL,
                        reason=f"API 오류: {e}",
                    ))

    return results


def review_problems(
    problems: list[CreatedProblem],
    concept_name: str,
    min_pass: int = 2,
) -> list[tuple[CreatedProblem, list[ReviewResult], bool]]:
    """문제 리스트 전체 검증

    Args:
        min_pass: 통과 판정에 필요한 최소 pass 수 (기본 2/3)

    Returns:
        [(problem, reviews, passed)]
    """
    results = []
    for i, problem in enumerate(problems):
        console.print(f"  [blue]📝[/] 문제 {i+1}/{len(problems)} 검증 중...")
        reviews = review_problem(problem, concept_name)
        pass_count = sum(1 for r in reviews if r.verdict == ReviewVerdict.PASS)
        passed = pass_count >= min_pass
        results.append((problem, reviews, passed))

    total_passed = sum(1 for _, _, p in results if p)
    console.print(
        f"[green]✓[/] 검증 완료: {total_passed}/{len(problems)}개 통과 "
        f"(기준: {min_pass}/{len(PERSONAS)}명 pass)"
    )
    return results


def _extract_json(text: str) -> str:
    """JSON 오브젝트 추출"""
    if "```json" in text:
        start = text.index("```json") + 7
        end = text.index("```", start)
        return text[start:end].strip()
    if "```" in text:
        start = text.index("```") + 3
        end = text.index("```", start)
        return text[start:end].strip()
    start = text.index("{")
    end = text.rindex("}") + 1
    return text[start:end]
