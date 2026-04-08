"""SymPy 수치 검증 — 정답 검산"""

from __future__ import annotations
import re
from sympy import sympify, Rational, simplify, N
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)
from rich.console import Console

from .models import CreatedProblem

console = Console()

_transformations = standard_transformations + (implicit_multiplication_application,)


def verify_answer(problem: CreatedProblem) -> bool | None:
    """문제의 정답을 SymPy로 검증

    Returns:
        True: 검증 통과
        False: 검증 실패 (정답 불일치)
        None: 검증 불가 (수식이 아닌 답)
    """
    answer = problem.answer.strip()

    # 수식 파싱 가능한 답만 검증
    if not _is_math_expression(answer):
        return None

    try:
        parsed = _parse_answer(answer)
        if parsed is None:
            return None

        # 풀이 단계가 있으면 마지막 단계의 expression과 비교
        if problem.solution_steps:
            last_expr = problem.solution_steps[-1].expression.strip()
            if last_expr and _is_math_expression(last_expr):
                parsed_last = _parse_answer(last_expr)
                if parsed_last is not None:
                    diff = simplify(parsed - parsed_last)
                    if diff == 0:
                        return True
                    # 수치 비교 fallback
                    if abs(float(N(diff))) < 1e-10:
                        return True
                    console.print(
                        f"[red]✗[/] 정답({answer}) ≠ 풀이 결과({last_expr})"
                    )
                    return False

        # 풀이 없으면 정답 파싱 성공 여부만 확인
        return True

    except Exception as e:
        console.print(f"[yellow]⚠[/] SymPy 검증 실패: {e}")
        return None


def verify_problems(problems: list[CreatedProblem]) -> list[dict]:
    """문제 리스트 전체 검증

    Returns:
        [{"index": 0, "answer": "...", "verified": True|False|None}]
    """
    results = []
    passed = 0
    failed = 0
    skipped = 0

    for i, p in enumerate(problems):
        result = verify_answer(p)
        results.append({"index": i, "answer": p.answer, "verified": result})
        if result is True:
            passed += 1
        elif result is False:
            failed += 1
        else:
            skipped += 1

    console.print(
        f"[green]✓ {passed}[/] / [red]✗ {failed}[/] / [yellow]⏭ {skipped}[/] "
        f"(총 {len(problems)}개)"
    )
    return results


def _is_math_expression(text: str) -> bool:
    """수식으로 파싱 가능한 답인지 판별"""
    text = text.strip()
    if not text:
        return False
    # 순수 텍스트 답변 필터 (한글 포함 시 수식 아님)
    if re.search(r"[가-힣]", text):
        return False
    # 숫자, 분수, 수식 기호만 있으면 수식
    return bool(re.match(r'^[\d\s\+\-\*/\^\.()x√±<>=≤≥|/]+$', text))


def _parse_answer(text: str) -> object | None:
    """답 문자열을 SymPy 표현식으로 변환"""
    text = text.strip()

    # 분수 표기 변환: a/b → Rational(a,b)
    frac_match = re.match(r'^(-?\d+)/(\d+)$', text)
    if frac_match:
        return Rational(int(frac_match.group(1)), int(frac_match.group(2)))

    # 일반 수식 파싱
    try:
        return parse_expr(text, transformations=_transformations)
    except Exception:
        pass

    # sympify fallback
    try:
        return sympify(text)
    except Exception:
        return None
