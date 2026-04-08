"""4-페르소나 문제 창작 — Claude API"""

from __future__ import annotations
import json
from anthropic import Anthropic
from rich.console import Console

from .config import ANTHROPIC_API_KEY, MODEL_NAME, MAX_RETRIES
from .models import CreatedProblem, Difficulty, SolutionStep
from .prompts.problem_creation import PERSONAS, USER_TEMPLATE, DIFFICULTY_GUIDES

console = Console(force_terminal=True)
_client: Anthropic | None = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=ANTHROPIC_API_KEY)
    return _client


def create_problems(
    concept_name: str,
    concept_description: str,
    difficulty: Difficulty,
    count_per_persona: int = 2,
) -> list[CreatedProblem]:
    """4명의 페르소나가 각각 문제를 생성한 뒤 합산

    Args:
        concept_name: 개념 이름
        concept_description: 개념 설명
        difficulty: 난이도
        count_per_persona: 페르소나당 생성 문제 수

    Returns:
        전체 생성 문제 리스트
    """
    all_problems: list[CreatedProblem] = []
    client = _get_client()

    difficulty_guide = DIFFICULTY_GUIDES.get(difficulty.value, "")

    for persona_name, persona_system in PERSONAS.items():
        console.print(f"  [blue]🎭[/] {persona_name} 페르소나 문제 생성 중...")

        user_msg = USER_TEMPLATE.format(
            concept_name=concept_name,
            concept_description=concept_description,
            difficulty=difficulty.value,
            difficulty_name=difficulty.name,
            count=count_per_persona,
            difficulty_guide=difficulty_guide,
        )

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                response = client.messages.create(
                    model=MODEL_NAME,
                    max_tokens=4096,
                    system=persona_system,
                    messages=[{"role": "user", "content": user_msg}],
                )
                raw = _extract_json(response.content[0].text)
                data = json.loads(raw)

                for item in data:
                    steps = [
                        SolutionStep(**s) for s in item.get("solution_steps", [])
                    ]
                    problem = CreatedProblem(
                        body=item["body"],
                        answer=item["answer"],
                        difficulty=difficulty,
                        concept_tags=item.get("concept_tags", [concept_name]),
                        solution_steps=steps,
                        source_trace={"persona": persona_name},
                    )
                    all_problems.append(problem)

                console.print(
                    f"    [green]✓[/] {persona_name}: {len(data)}개 생성"
                )
                break
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                console.print(
                    f"    [yellow]⚠[/] 파싱 실패 (시도 {attempt}/{MAX_RETRIES}): {e}"
                )
                if attempt == MAX_RETRIES:
                    console.print(f"    [red]✗[/] {persona_name} 건너뜀")
            except Exception as e:
                console.print(
                    f"    [red]✗[/] API 오류 (시도 {attempt}/{MAX_RETRIES}): {e}"
                )
                if attempt == MAX_RETRIES:
                    console.print(f"    [red]✗[/] {persona_name} 건너뜀")

    console.print(f"[green]✓[/] 총 {len(all_problems)}개 문제 생성 완료")
    return all_problems


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
    start = text.index("[")
    end = text.rindex("]") + 1
    return text[start:end]
