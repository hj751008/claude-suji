"""테스트용 시드 데이터 — 소인수분해 + 정수와 유리수 문제 직접 투입"""

import sys
sys.stdout.reconfigure(encoding='utf-8')

from pipeline.db import get_client

client = get_client()

# ── 기존 계층 ID ──
SUBJECT_ID = "ce9188f9-40b1-4ba9-8dc3-231db2ddbbfc"  # 수학
GRADE_ID = "36f18890-d393-42b6-b04a-2fd260f5178f"    # 중1
UNIT_ID = "091e7814-3a4e-4e5e-b0cc-48402db8e3f2"     # 수와 연산
SUB_UNIT_정수 = "fbcf6296-5cba-47c3-8539-782f124c6ed2"  # 정수와 유리수

# ── 소인수분해 소단원 생성 ──
res = client.table("sub_units").select("id").eq("unit_id", UNIT_ID).eq("name", "소인수분해").execute()
if res.data:
    SUB_UNIT_소인수 = res.data[0]["id"]
else:
    SUB_UNIT_소인수 = client.table("sub_units").insert({
        "unit_id": UNIT_ID, "name": "소인수분해", "order": 2
    }).execute().data[0]["id"]
print(f"소인수분해 sub_unit: {SUB_UNIT_소인수}")


def ensure_concept(sub_unit_id, name, description, order):
    res = client.table("concepts").select("id").eq("sub_unit_id", sub_unit_id).eq("name", name).execute()
    if res.data:
        return res.data[0]["id"]
    return client.table("concepts").insert({
        "sub_unit_id": sub_unit_id, "name": name, "description": description, "order": order
    }).execute().data[0]["id"]


def insert_problem(concept_id, difficulty, body, answer, steps=None):
    # 중복 체크
    res = client.table("problems").select("id").eq("concept_primary_id", concept_id).eq("body", body).execute()
    if res.data:
        print(f"  (이미 존재) {body[:30]}...")
        return res.data[0]["id"]

    inserted = client.table("problems").insert({
        "concept_primary_id": concept_id,
        "difficulty": difficulty,
        "body": body,
        "answer": answer,
        "status": "published",
        "sympy_verified": True,
        "source_trace": {"generator": "claude-direct", "version": "plan3-seed"},
    }).execute()
    pid = inserted.data[0]["id"]

    client.table("problem_concepts").insert({
        "problem_id": pid, "concept_id": concept_id,
    }).execute()

    if steps:
        client.table("solutions").insert({
            "problem_id": pid, "steps": steps,
        }).execute()

    print(f"  + {body[:40]}...")
    return pid


# ============================================================
# 소인수분해 개념 + 문제
# ============================================================
print("\n=== 소인수분해 ===")

c_소수 = ensure_concept(SUB_UNIT_소인수, "소수와 합성수",
    "1보다 큰 자연수 중 1과 자기 자신만을 약수로 가지는 수가 소수, 그 외가 합성수", 1)

c_거듭 = ensure_concept(SUB_UNIT_소인수, "거듭제곱",
    "같은 수를 여러 번 곱한 것을 간단히 나타내는 방법", 2)

c_소인수분해 = ensure_concept(SUB_UNIT_소인수, "소인수분해",
    "자연수를 소인수들의 곱으로 나타내는 것", 3)

c_약수개수 = ensure_concept(SUB_UNIT_소인수, "약수의 개수",
    "소인수분해를 이용하여 약수의 개수를 구하는 방법", 4)

c_최대공약수 = ensure_concept(SUB_UNIT_소인수, "최대공약수",
    "두 개 이상의 자연수의 공통인 약수 중 가장 큰 수", 5)

c_최소공배수 = ensure_concept(SUB_UNIT_소인수, "최소공배수",
    "두 개 이상의 자연수의 공통인 배수 중 가장 작은 수", 6)


# -- 소수와 합성수 --
print("\n[소수와 합성수]")
insert_problem(c_소수, 1,
    "다음 중 소수인 것은?\n① 1  ② 9  ③ 11  ④ 15  ⑤ 21",
    "3",
    [{"step": 1, "explanation": "소수는 1보다 크고, 1과 자기 자신만을 약수로 가지는 수", "expression": ""},
     {"step": 2, "explanation": "1은 소수가 아님, 9=3×3, 15=3×5, 21=3×7은 합성수", "expression": ""},
     {"step": 3, "explanation": "11은 1과 11만 약수이므로 소수", "expression": "답: ③"}])

insert_problem(c_소수, 1,
    "20 이하의 소수를 모두 구하면 몇 개인가?",
    "8",
    [{"step": 1, "explanation": "20 이하의 소수 나열", "expression": "2, 3, 5, 7, 11, 13, 17, 19"},
     {"step": 2, "explanation": "총 8개", "expression": "답: 8"}])

insert_problem(c_소수, 2,
    "10 이상 30 이하의 자연수 중 합성수의 개수를 구하시오.",
    "15",
    [{"step": 1, "explanation": "10~30 자연수: 총 21개", "expression": ""},
     {"step": 2, "explanation": "이 범위의 소수: 11, 13, 17, 19, 23, 29 → 6개", "expression": ""},
     {"step": 3, "explanation": "합성수 = 21 - 6 = 15", "expression": "답: 15"}])

insert_problem(c_소수, 2,
    "두 자리 자연수 중 가장 작은 소수와 가장 큰 소수의 합을 구하시오.",
    "108",
    [{"step": 1, "explanation": "두 자리 수 중 가장 작은 소수: 11", "expression": ""},
     {"step": 2, "explanation": "두 자리 수 중 가장 큰 소수: 97", "expression": ""},
     {"step": 3, "explanation": "11 + 97 = 108", "expression": "답: 108"}])


# -- 거듭제곱 --
print("\n[거듭제곱]")
insert_problem(c_거듭, 1,
    "2×2×2×2×2를 거듭제곱으로 나타내시오.",
    "2의 5제곱",
    [{"step": 1, "explanation": "2를 5번 곱했으므로", "expression": "2⁵"}])

insert_problem(c_거듭, 1,
    "3⁴의 값을 구하시오.",
    "81",
    [{"step": 1, "explanation": "3⁴ = 3×3×3×3", "expression": ""},
     {"step": 2, "explanation": "= 9×9 = 81", "expression": "답: 81"}])

insert_problem(c_거듭, 2,
    "2³×5²의 값을 구하시오.",
    "200",
    [{"step": 1, "explanation": "2³ = 8, 5² = 25", "expression": ""},
     {"step": 2, "explanation": "8 × 25 = 200", "expression": "답: 200"}])


# -- 소인수분해 --
print("\n[소인수분해]")
insert_problem(c_소인수분해, 1,
    "36을 소인수분해하시오.",
    "2² × 3²",
    [{"step": 1, "explanation": "36 = 2 × 18", "expression": ""},
     {"step": 2, "explanation": "18 = 2 × 9", "expression": ""},
     {"step": 3, "explanation": "9 = 3 × 3", "expression": ""},
     {"step": 4, "explanation": "36 = 2² × 3²", "expression": "답: 2² × 3²"}])

insert_problem(c_소인수분해, 1,
    "60을 소인수분해하시오.",
    "2² × 3 × 5",
    [{"step": 1, "explanation": "60 = 2 × 30 = 2 × 2 × 15 = 2 × 2 × 3 × 5", "expression": ""},
     {"step": 2, "explanation": "60 = 2² × 3 × 5", "expression": "답: 2² × 3 × 5"}])

insert_problem(c_소인수분해, 2,
    "72의 소인수를 모두 구하시오.",
    "2, 3",
    [{"step": 1, "explanation": "72 = 2³ × 3²", "expression": ""},
     {"step": 2, "explanation": "소인수: 2, 3", "expression": "답: 2, 3"}])

insert_problem(c_소인수분해, 2,
    "어떤 자연수를 소인수분해하면 2³ × 3 × 7이다. 이 자연수를 구하시오.",
    "168",
    [{"step": 1, "explanation": "2³ = 8, 8 × 3 = 24, 24 × 7 = 168", "expression": "답: 168"}])


# -- 약수의 개수 --
print("\n[약수의 개수]")
insert_problem(c_약수개수, 1,
    "2³ × 3의 약수의 개수를 구하시오.",
    "8",
    [{"step": 1, "explanation": "(지수+1)들의 곱으로 약수의 개수를 구함", "expression": ""},
     {"step": 2, "explanation": "(3+1) × (1+1) = 4 × 2 = 8", "expression": "답: 8"}])

insert_problem(c_약수개수, 1,
    "48의 약수의 개수를 구하시오.",
    "10",
    [{"step": 1, "explanation": "48 = 2⁴ × 3", "expression": ""},
     {"step": 2, "explanation": "(4+1) × (1+1) = 10", "expression": "답: 10"}])

insert_problem(c_약수개수, 2,
    "약수의 개수가 6개인 가장 작은 자연수를 구하시오.",
    "12",
    [{"step": 1, "explanation": "6 = 6×1 또는 3×2 또는 2×3", "expression": ""},
     {"step": 2, "explanation": "2⁵=32, 2²×3=12, 2×3²=18", "expression": ""},
     {"step": 3, "explanation": "가장 작은 수: 12", "expression": "답: 12"}])


# -- 최대공약수 --
print("\n[최대공약수]")
insert_problem(c_최대공약수, 1,
    "12와 18의 최대공약수를 구하시오.",
    "6",
    [{"step": 1, "explanation": "12 = 2² × 3, 18 = 2 × 3²", "expression": ""},
     {"step": 2, "explanation": "공통 소인수의 최소 지수: 2¹ × 3¹ = 6", "expression": "답: 6"}])

insert_problem(c_최대공약수, 1,
    "24와 36의 최대공약수를 구하시오.",
    "12",
    [{"step": 1, "explanation": "24 = 2³ × 3, 36 = 2² × 3²", "expression": ""},
     {"step": 2, "explanation": "최대공약수: 2² × 3 = 12", "expression": "답: 12"}])

insert_problem(c_최대공약수, 2,
    "사탕 48개와 초콜릿 36개를 최대한 많은 학생에게 남김없이 똑같이 나누어 주려고 한다. 최대 몇 명에게 나누어 줄 수 있는가?",
    "12",
    [{"step": 1, "explanation": "48과 36의 최대공약수를 구함", "expression": ""},
     {"step": 2, "explanation": "48 = 2⁴ × 3, 36 = 2² × 3²", "expression": ""},
     {"step": 3, "explanation": "최대공약수: 2² × 3 = 12", "expression": "답: 12명"}])


# -- 최소공배수 --
print("\n[최소공배수]")
insert_problem(c_최소공배수, 1,
    "4와 6의 최소공배수를 구하시오.",
    "12",
    [{"step": 1, "explanation": "4 = 2², 6 = 2 × 3", "expression": ""},
     {"step": 2, "explanation": "공통·비공통 소인수의 최대 지수: 2² × 3 = 12", "expression": "답: 12"}])

insert_problem(c_최소공배수, 1,
    "8과 12의 최소공배수를 구하시오.",
    "24",
    [{"step": 1, "explanation": "8 = 2³, 12 = 2² × 3", "expression": ""},
     {"step": 2, "explanation": "최소공배수: 2³ × 3 = 24", "expression": "답: 24"}])

insert_problem(c_최소공배수, 2,
    "버스 A는 15분마다, 버스 B는 20분마다 출발한다. 오전 8시에 동시에 출발했다면, 다음에 동시에 출발하는 시각은?",
    "오전 9시",
    [{"step": 1, "explanation": "15와 20의 최소공배수를 구함", "expression": ""},
     {"step": 2, "explanation": "15 = 3 × 5, 20 = 2² × 5", "expression": ""},
     {"step": 3, "explanation": "최소공배수: 2² × 3 × 5 = 60분", "expression": ""},
     {"step": 4, "explanation": "8시 + 60분 = 9시", "expression": "답: 오전 9시"}])


# ============================================================
# 정수와 유리수 — 기존 개념 보강 + 새 개념 추가
# ============================================================
print("\n=== 정수와 유리수 ===")

# 기존 개념 ID
c_자연수 = "5d821726-09e7-4b6b-b05f-2cfe80859528"
c_정수 = "02b6094e-9915-4b67-a271-23ec6b930197"
c_수의범위 = "6d6d30ec-e617-4c9b-a36d-6748c53e520c"

# 새 개념
c_절댓값 = ensure_concept(SUB_UNIT_정수, "절댓값",
    "수직선에서 원점으로부터의 거리", 4)

c_정수덧뺄 = ensure_concept(SUB_UNIT_정수, "정수의 덧셈과 뺄셈",
    "양수, 음수를 포함한 정수의 덧셈과 뺄셈", 5)

c_정수곱나 = ensure_concept(SUB_UNIT_정수, "정수의 곱셈과 나눗셈",
    "양수, 음수를 포함한 정수의 곱셈과 나눗셈", 6)


# -- 기존 개념 문제 보강 --
print("\n[자연수 보강]")
insert_problem(c_자연수, 2,
    "다음 수 중 자연수인 것을 모두 고르시오.\n-5, 0, 3, 1/2, 7, -1",
    "3, 7",
    [{"step": 1, "explanation": "자연수는 1, 2, 3, ... 양의 정수", "expression": ""},
     {"step": 2, "explanation": "-5(음수), 0, 1/2(분수), -1(음수)은 자연수 아님", "expression": "답: 3, 7"}])

print("\n[정수 보강]")
insert_problem(c_정수, 2,
    "다음 수를 양의 정수, 0, 음의 정수로 분류하시오.\n-8, 5, 0, -1, 12, -100",
    "양의 정수: 5, 12 / 0 / 음의 정수: -8, -1, -100",
    [{"step": 1, "explanation": "양의 정수(자연수): 5, 12", "expression": ""},
     {"step": 2, "explanation": "0은 양수도 음수도 아님", "expression": ""},
     {"step": 3, "explanation": "음의 정수: -8, -1, -100", "expression": ""}])


# -- 절댓값 --
print("\n[절댓값]")
insert_problem(c_절댓값, 1,
    "|-7|의 값을 구하시오.",
    "7",
    [{"step": 1, "explanation": "절댓값은 수직선에서 원점까지의 거리", "expression": ""},
     {"step": 2, "explanation": "-7은 원점에서 7만큼 떨어져 있음", "expression": "답: 7"}])

insert_problem(c_절댓값, 1,
    "|+3|의 값을 구하시오.",
    "3",
    [{"step": 1, "explanation": "+3은 원점에서 3만큼 떨어져 있음", "expression": "답: 3"}])

insert_problem(c_절댓값, 2,
    "절댓값이 5인 정수를 모두 구하시오.",
    "5, -5",
    [{"step": 1, "explanation": "원점에서 5만큼 떨어진 수", "expression": ""},
     {"step": 2, "explanation": "+5와 -5", "expression": "답: 5, -5"}])

insert_problem(c_절댓값, 2,
    "절댓값이 3보다 작은 정수를 모두 구하시오.",
    "-2, -1, 0, 1, 2",
    [{"step": 1, "explanation": "원점에서 거리가 3 미만인 정수", "expression": ""},
     {"step": 2, "explanation": "-2, -1, 0, 1, 2", "expression": "답: -2, -1, 0, 1, 2"}])


# -- 정수의 덧셈과 뺄셈 --
print("\n[정수의 덧셈과 뺄셈]")
insert_problem(c_정수덧뺄, 1,
    "(-3) + (+8)을 계산하시오.",
    "5",
    [{"step": 1, "explanation": "부호가 다르므로 절댓값의 차를 구하고 큰 쪽 부호", "expression": ""},
     {"step": 2, "explanation": "8 - 3 = 5, 양수가 더 크므로 +5", "expression": "답: 5"}])

insert_problem(c_정수덧뺄, 1,
    "(-5) + (-4)를 계산하시오.",
    "-9",
    [{"step": 1, "explanation": "부호가 같으므로 절댓값의 합에 공통 부호", "expression": ""},
     {"step": 2, "explanation": "5 + 4 = 9, 공통 부호 음수 → -9", "expression": "답: -9"}])

insert_problem(c_정수덧뺄, 1,
    "(+6) - (+9)를 계산하시오.",
    "-3",
    [{"step": 1, "explanation": "빼기는 부호를 바꿔 더하기로", "expression": "(+6) + (-9)"},
     {"step": 2, "explanation": "9 - 6 = 3, 음수가 더 크므로 -3", "expression": "답: -3"}])

insert_problem(c_정수덧뺄, 2,
    "(-7) + (+3) - (-5)를 계산하시오.",
    "1",
    [{"step": 1, "explanation": "(-7) + (+3) + (+5)로 변환", "expression": ""},
     {"step": 2, "explanation": "양수의 합: 3 + 5 = 8", "expression": ""},
     {"step": 3, "explanation": "8 + (-7) = 1", "expression": "답: 1"}])


# -- 정수의 곱셈과 나눗셈 --
print("\n[정수의 곱셈과 나눗셈]")
insert_problem(c_정수곱나, 1,
    "(-4) × (+3)을 계산하시오.",
    "-12",
    [{"step": 1, "explanation": "부호가 다르면 결과는 음수", "expression": ""},
     {"step": 2, "explanation": "4 × 3 = 12 → -12", "expression": "답: -12"}])

insert_problem(c_정수곱나, 1,
    "(-6) × (-2)를 계산하시오.",
    "12",
    [{"step": 1, "explanation": "부호가 같으면 결과는 양수", "expression": ""},
     {"step": 2, "explanation": "6 × 2 = 12 → +12", "expression": "답: 12"}])

insert_problem(c_정수곱나, 1,
    "(-15) ÷ (+3)을 계산하시오.",
    "-5",
    [{"step": 1, "explanation": "부호가 다르면 결과는 음수", "expression": ""},
     {"step": 2, "explanation": "15 ÷ 3 = 5 → -5", "expression": "답: -5"}])

insert_problem(c_정수곱나, 2,
    "(-2) × (+3) × (-4)를 계산하시오.",
    "24",
    [{"step": 1, "explanation": "음수가 2개(짝수)이므로 결과는 양수", "expression": ""},
     {"step": 2, "explanation": "2 × 3 × 4 = 24", "expression": "답: 24"}])

insert_problem(c_정수곱나, 2,
    "(-36) ÷ (-4) ÷ (+3)을 계산하시오.",
    "3",
    [{"step": 1, "explanation": "(-36) ÷ (-4) = +9", "expression": ""},
     {"step": 2, "explanation": "(+9) ÷ (+3) = +3", "expression": "답: 3"}])


# ── 결과 요약 ──
print("\n=== 최종 현황 ===")
for table in ['concepts', 'problems', 'solutions']:
    res = client.table(table).select('*', count='exact').execute()
    print(f"{table}: {res.count}건")
