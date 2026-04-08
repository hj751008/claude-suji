"""Supabase DB 연결 및 CRUD"""

from __future__ import annotations
from supabase import create_client, Client
from .config import SUPABASE_URL, SUPABASE_SERVICE_KEY
from .models import CreatedProblem, WebtoonScript, ExtractedConcept


def get_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)


def get_or_create_hierarchy(client: Client, subject: str, grade: str, unit: str, sub_unit: str) -> dict:
    """콘텐츠 계층 구조 조회/생성, 각 ID 반환"""
    # Subject
    res = client.table("subjects").select("id").eq("name", subject).execute()
    if res.data:
        subject_id = res.data[0]["id"]
    else:
        subject_id = client.table("subjects").insert({"name": subject}).execute().data[0]["id"]

    # Grade
    res = client.table("grades").select("id").eq("subject_id", subject_id).eq("name", grade).execute()
    if res.data:
        grade_id = res.data[0]["id"]
    else:
        grade_id = client.table("grades").insert({
            "subject_id": subject_id, "name": grade, "order": 1
        }).execute().data[0]["id"]

    # Unit
    res = client.table("units").select("id").eq("grade_id", grade_id).eq("name", unit).execute()
    if res.data:
        unit_id = res.data[0]["id"]
    else:
        count = client.table("units").select("id", count="exact").eq("grade_id", grade_id).execute()
        unit_id = client.table("units").insert({
            "grade_id": grade_id, "name": unit, "order": (count.count or 0) + 1
        }).execute().data[0]["id"]

    # Sub-unit
    res = client.table("sub_units").select("id").eq("unit_id", unit_id).eq("name", sub_unit).execute()
    if res.data:
        sub_unit_id = res.data[0]["id"]
    else:
        count = client.table("sub_units").select("id", count="exact").eq("unit_id", unit_id).execute()
        sub_unit_id = client.table("sub_units").insert({
            "unit_id": unit_id, "name": sub_unit, "order": (count.count or 0) + 1
        }).execute().data[0]["id"]

    return {
        "subject_id": subject_id,
        "grade_id": grade_id,
        "unit_id": unit_id,
        "sub_unit_id": sub_unit_id,
    }


def upsert_concept(client: Client, sub_unit_id: str, concept: ExtractedConcept) -> str:
    """개념 upsert, concept_id 반환"""
    res = client.table("concepts").select("id").eq("sub_unit_id", sub_unit_id).eq("name", concept.name).execute()
    if res.data:
        return res.data[0]["id"]
    count = client.table("concepts").select("id", count="exact").eq("sub_unit_id", sub_unit_id).execute()
    inserted = client.table("concepts").insert({
        "sub_unit_id": sub_unit_id,
        "name": concept.name,
        "description": concept.description,
        "order": (count.count or 0) + 1,
    }).execute()
    return inserted.data[0]["id"]


def insert_problem(client: Client, concept_id: str, problem: CreatedProblem) -> str:
    """문제 삽입, problem_id 반환"""
    inserted = client.table("problems").insert({
        "concept_primary_id": concept_id,
        "difficulty": problem.difficulty.value,
        "body": problem.body,
        "answer": problem.answer,
        "status": "published",
        "sympy_verified": False,
        "source_trace": problem.source_trace,
    }).execute()
    problem_id = inserted.data[0]["id"]

    # problem_concepts M:N
    client.table("problem_concepts").insert({
        "problem_id": problem_id,
        "concept_id": concept_id,
    }).execute()

    # solutions
    if problem.solution_steps:
        client.table("solutions").insert({
            "problem_id": problem_id,
            "steps": [s.model_dump() for s in problem.solution_steps],
        }).execute()

    return problem_id


def insert_webtoon_script(client: Client, problem_id: str, script: WebtoonScript) -> None:
    """웹툰 스크립트 삽입"""
    client.table("webtoon_scripts").upsert({
        "problem_id": problem_id,
        "script": [line.model_dump() for line in script.lines],
    }).execute()


def insert_review(client: Client, problem_id: str, stage: str, persona: str, verdict: str, reason: str) -> None:
    """검증 결과 기록"""
    client.table("problem_reviews").insert({
        "problem_id": problem_id,
        "stage": stage,
        "persona_name": persona,
        "verdict": verdict,
        "reason": reason,
    }).execute()
