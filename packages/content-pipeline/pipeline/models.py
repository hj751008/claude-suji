"""Pydantic 모델 — 파이프라인 데이터 스키마"""

from __future__ import annotations
from pydantic import BaseModel, Field
from enum import Enum


class Difficulty(int, Enum):
    BASIC = 1       # Lv1: 기본 인식
    VARIANT = 2     # Lv2: 변형 표현
    MIXED = 3       # Lv3: 혼합 (미래)
    APPLIED = 4     # Lv4: 응용 (미래)


class ExtractedConcept(BaseModel):
    """PDF에서 추출된 개념"""
    name: str = Field(description="개념 이름 (예: 절댓값)")
    description: str = Field(description="개념 설명")
    sub_unit: str = Field(description="소단원 이름")
    examples: list[str] = Field(default_factory=list, description="대표 예시 문제")


class SolutionStep(BaseModel):
    step: int
    explanation: str
    expression: str = ""


class CreatedProblem(BaseModel):
    """AI가 생성한 문제"""
    body: str = Field(description="문제 본문")
    answer: str = Field(description="정답")
    difficulty: Difficulty
    concept_tags: list[str] = Field(description="관련 개념 이름 리스트")
    solution_steps: list[SolutionStep] = Field(default_factory=list)
    source_trace: dict = Field(default_factory=dict, description="참고 메타 (원문 X)")


class ReviewVerdict(str, Enum):
    PASS = "pass"
    FAIL = "fail"


class ReviewResult(BaseModel):
    """페르소나 검증 결과"""
    persona: str
    verdict: ReviewVerdict
    reason: str


class WebtoonLine(BaseModel):
    """웹툰 스크립트 한 줄"""
    speaker: str | None = None  # None이면 scene description
    text: str
    type: str = "dialogue"  # "dialogue" | "scene"


class WebtoonScript(BaseModel):
    """문제별 웹툰 해설 스크립트"""
    lines: list[WebtoonLine]
