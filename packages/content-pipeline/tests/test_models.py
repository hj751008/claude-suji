"""Pydantic 모델 테스트"""

import pytest
from pipeline.models import (
    Difficulty,
    ExtractedConcept,
    SolutionStep,
    CreatedProblem,
    ReviewVerdict,
    ReviewResult,
    WebtoonLine,
    WebtoonScript,
)


class TestDifficulty:
    def test_basic_value(self):
        assert Difficulty.BASIC == 1

    def test_variant_value(self):
        assert Difficulty.VARIANT == 2

    def test_from_int(self):
        assert Difficulty(1) == Difficulty.BASIC
        assert Difficulty(2) == Difficulty.VARIANT


class TestExtractedConcept:
    def test_minimal(self):
        c = ExtractedConcept(
            name="절댓값",
            description="수직선 위에서 원점까지의 거리",
            sub_unit="정수와 유리수",
        )
        assert c.name == "절댓값"
        assert c.examples == []

    def test_with_examples(self):
        c = ExtractedConcept(
            name="절댓값",
            description="원점까지의 거리",
            sub_unit="정수와 유리수",
            examples=["|-3| = 3", "|5| = 5"],
        )
        assert len(c.examples) == 2

    def test_serialization(self):
        c = ExtractedConcept(
            name="절댓값",
            description="테스트",
            sub_unit="테스트",
        )
        data = c.model_dump()
        assert data["name"] == "절댓값"
        restored = ExtractedConcept(**data)
        assert restored == c


class TestSolutionStep:
    def test_minimal(self):
        s = SolutionStep(step=1, explanation="양변에 2를 더한다")
        assert s.expression == ""

    def test_with_expression(self):
        s = SolutionStep(step=1, explanation="계산", expression="3 + 5 = 8")
        assert s.expression == "3 + 5 = 8"


class TestCreatedProblem:
    def test_minimal(self):
        p = CreatedProblem(
            body="|-7|의 값은?",
            answer="7",
            difficulty=Difficulty.BASIC,
            concept_tags=["절댓값"],
        )
        assert p.difficulty == Difficulty.BASIC
        assert p.solution_steps == []
        assert p.source_trace == {}

    def test_full(self):
        p = CreatedProblem(
            body="|-7|의 값은?",
            answer="7",
            difficulty=Difficulty.VARIANT,
            concept_tags=["절댓값"],
            solution_steps=[
                SolutionStep(step=1, explanation="절댓값 정의 적용", expression="|-7| = 7"),
            ],
            source_trace={"persona": "교육학자"},
        )
        assert len(p.solution_steps) == 1
        assert p.source_trace["persona"] == "교육학자"

    def test_difficulty_enum(self):
        p = CreatedProblem(
            body="문제", answer="답", difficulty=1, concept_tags=["개념"],
        )
        assert p.difficulty == Difficulty.BASIC


class TestReviewResult:
    def test_pass(self):
        r = ReviewResult(persona="출판관계자", verdict=ReviewVerdict.PASS, reason="적절함")
        assert r.verdict == ReviewVerdict.PASS

    def test_fail(self):
        r = ReviewResult(persona="학습전문가", verdict=ReviewVerdict.FAIL, reason="난이도 초과")
        assert r.verdict == ReviewVerdict.FAIL

    def test_verdict_from_string(self):
        r = ReviewResult(persona="일타강사", verdict="pass", reason="OK")
        assert r.verdict == ReviewVerdict.PASS


class TestWebtoonScript:
    def test_empty(self):
        s = WebtoonScript(lines=[])
        assert len(s.lines) == 0

    def test_with_lines(self):
        s = WebtoonScript(lines=[
            WebtoonLine(type="scene", text="교실 장면"),
            WebtoonLine(speaker="마플", text="안녕! 오늘은 절댓값!", type="dialogue"),
            WebtoonLine(speaker="수지", text="절댓값이 뭐야?", type="dialogue"),
        ])
        assert len(s.lines) == 3
        assert s.lines[0].speaker is None
        assert s.lines[1].speaker == "마플"

    def test_serialization_roundtrip(self):
        original = WebtoonScript(lines=[
            WebtoonLine(speaker="마플", text="테스트", type="dialogue"),
        ])
        data = original.model_dump()
        restored = WebtoonScript(**data)
        assert restored == original
