"""수지 콘텐츠 파이프라인 CLI"""

from __future__ import annotations
from pathlib import Path
import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(help="수지 수학 콘텐츠 파이프라인")
console = Console()


@app.command()
def extract_concepts(
    pdf_path: Path = typer.Argument(..., help="PDF 파일 또는 디렉토리 경로"),
    unit: str = typer.Option(..., "--unit", "-u", help="단원명"),
    sub_unit: str = typer.Option(..., "--sub-unit", "-s", help="소단원명"),
    output: Path = typer.Option("concepts.json", "--output", "-o", help="출력 JSON 경로"),
):
    """PDF에서 수학 개념 추출"""
    import json
    from pipeline.pdf_parser import extract_text_from_pdf, extract_all_pdfs
    from pipeline.concept_extractor import extract_concepts as _extract

    console.print(Panel(f"📖 개념 추출: {pdf_path}", style="blue"))

    if pdf_path.is_dir():
        docs = extract_all_pdfs(pdf_path)
        pages = [p for doc in docs for p in doc["pages"]]
    else:
        pages = extract_text_from_pdf(pdf_path)

    concepts = _extract(pages, unit, sub_unit)
    data = [c.model_dump() for c in concepts]

    output.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    console.print(f"[green]✓[/] {len(concepts)}개 개념 → {output}")


@app.command()
def review_concepts(
    concepts_file: Path = typer.Argument(..., help="concepts.json 경로"),
):
    """추출된 개념 목록 확인 및 편집 안내"""
    import json
    from pipeline.models import ExtractedConcept

    data = json.loads(concepts_file.read_text(encoding="utf-8"))
    concepts = [ExtractedConcept(**c) for c in data]

    console.print(Panel(f"📋 개념 목록 ({len(concepts)}개)", style="blue"))
    for i, c in enumerate(concepts, 1):
        console.print(f"  {i}. [bold]{c.name}[/] — {c.description}")
        if c.examples:
            for ex in c.examples:
                console.print(f"     예) {ex}")

    console.print(f"\n[yellow]💡[/] 수정이 필요하면 {concepts_file}을 직접 편집하세요.")


@app.command()
def generate(
    concepts_file: Path = typer.Argument(..., help="concepts.json 경로"),
    difficulty: int = typer.Option(1, "--difficulty", "-d", help="난이도 (1=기본, 2=변형)"),
    count: int = typer.Option(2, "--count", "-c", help="페르소나당 문제 수"),
    skip_review: bool = typer.Option(False, "--skip-review", help="검증 단계 건너뛰기"),
    skip_webtoon: bool = typer.Option(False, "--skip-webtoon", help="웹툰 스크립트 건너뛰기"),
    dry_run: bool = typer.Option(False, "--dry-run", help="DB 저장 없이 결과만 출력"),
    output: Path = typer.Option("problems.json", "--output", "-o", help="출력 JSON 경로"),
):
    """개념 기반으로 문제 생성 → 검증 → 웹툰 → DB 저장"""
    import json
    from pipeline.models import ExtractedConcept, Difficulty
    from pipeline.problem_creator import create_problems
    from pipeline.sympy_verifier import verify_problems
    from pipeline.reviewer import review_problems
    from pipeline.webtoon_generator import generate_webtoon_scripts

    data = json.loads(concepts_file.read_text(encoding="utf-8"))
    concepts = [ExtractedConcept(**c) for c in data]
    diff = Difficulty(difficulty)

    console.print(Panel(
        f"🧮 문제 생성: {len(concepts)}개 개념, Lv{difficulty}, "
        f"{count}개/페르소나",
        style="blue",
    ))

    all_results = []

    for concept in concepts:
        console.print(f"\n[bold blue]▶[/] 개념: {concept.name}")

        # 1. 문제 생성
        problems = create_problems(concept.name, concept.description, diff, count)
        if not problems:
            console.print("  [red]✗[/] 문제 생성 실패, 건너뜀")
            continue

        # 2. SymPy 검증
        console.print("  [blue]🔢[/] SymPy 검증...")
        verify_results = verify_problems(problems)

        # 3. 페르소나 검증
        if not skip_review:
            console.print("  [blue]🔍[/] 페르소나 검증...")
            review_results = review_problems(problems, concept.name)
            # 통과한 문제만 남김
            problems = [p for p, _, passed in review_results if passed]
            console.print(f"  [green]✓[/] 검증 통과: {len(problems)}개")
        else:
            console.print("  [yellow]⏭[/] 검증 건너뜀")

        # 4. 웹툰 스크립트
        scripts = []
        if not skip_webtoon and problems:
            console.print("  [blue]🎬[/] 웹툰 스크립트 생성...")
            scripts = generate_webtoon_scripts(problems, concept.name)

        # 결과 수집
        for i, problem in enumerate(problems):
            entry = {
                "concept": concept.name,
                "problem": problem.model_dump(),
                "sympy_verified": verify_results[i]["verified"] if i < len(verify_results) else None,
            }
            if i < len(scripts):
                entry["webtoon"] = scripts[i].model_dump()
            all_results.append(entry)

    # 결과 저장
    output.write_text(
        json.dumps(all_results, ensure_ascii=False, indent=2, default=str),
        encoding="utf-8",
    )
    console.print(f"\n[green]✓[/] {len(all_results)}개 문제 → {output}")

    # DB 저장
    if not dry_run and all_results:
        _save_to_db(all_results, concepts)
    elif dry_run:
        console.print("[yellow]💡[/] --dry-run: DB 저장 건너뜀")


def _save_to_db(results: list[dict], concepts):
    """결과를 Supabase에 저장"""
    from pipeline.db import (
        get_client, get_or_create_hierarchy, upsert_concept,
        insert_problem, insert_webtoon_script,
    )
    from pipeline.models import CreatedProblem, WebtoonScript, ExtractedConcept

    console.print("\n[blue]💾[/] DB 저장 중...")
    client = get_client()

    # 계층 생성 (기본값: 중1 수학)
    ids = get_or_create_hierarchy(client, "수학", "중1", "기본", "기본")

    saved = 0
    for entry in results:
        try:
            # 개념 upsert
            concept = ExtractedConcept(
                name=entry["concept"],
                description="",
                sub_unit="기본",
            )
            concept_id = upsert_concept(client, ids["sub_unit_id"], concept)

            # 문제 저장
            problem = CreatedProblem(**entry["problem"])
            problem_id = insert_problem(client, concept_id, problem)

            # 웹툰 저장
            if "webtoon" in entry:
                script = WebtoonScript(**entry["webtoon"])
                if script.lines:
                    insert_webtoon_script(client, problem_id, script)

            saved += 1
        except Exception as e:
            console.print(f"  [red]✗[/] 저장 실패: {e}")

    console.print(f"[green]✓[/] DB 저장 완료: {saved}/{len(results)}개")


@app.command()
def run_pipeline(
    pdf_path: Path = typer.Argument(..., help="PDF 파일 경로"),
    unit: str = typer.Option(..., "--unit", "-u", help="단원명"),
    sub_unit: str = typer.Option(..., "--sub-unit", "-s", help="소단원명"),
    difficulty: int = typer.Option(1, "--difficulty", "-d", help="난이도"),
    count: int = typer.Option(2, "--count", "-c", help="페르소나당 문제 수"),
    dry_run: bool = typer.Option(False, "--dry-run", help="DB 저장 없이"),
):
    """전체 파이프라인 한 번에 실행: PDF → 개념추출 → 문제생성 → 검증 → DB"""
    import json
    import tempfile
    from pipeline.pdf_parser import extract_text_from_pdf
    from pipeline.concept_extractor import extract_concepts as _extract

    console.print(Panel("🚀 전체 파이프라인 실행", style="bold blue"))

    # 1. PDF 파싱
    console.print("\n[bold]1/2[/] 개념 추출")
    pages = extract_text_from_pdf(pdf_path)
    concepts = _extract(pages, unit, sub_unit)

    if not concepts:
        console.print("[red]✗[/] 추출된 개념이 없습니다")
        raise typer.Exit(1)

    # concepts.json 임시 저장
    tmp = Path(tempfile.mkdtemp()) / "concepts.json"
    tmp.write_text(
        json.dumps([c.model_dump() for c in concepts], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # 2. 문제 생성 (generate 명령 재활용)
    console.print("\n[bold]2/2[/] 문제 생성 + 검증")
    generate(
        concepts_file=tmp,
        difficulty=difficulty,
        count=count,
        skip_review=False,
        skip_webtoon=False,
        dry_run=dry_run,
        output=Path("problems.json"),
    )

    console.print(Panel("✅ 파이프라인 완료!", style="bold green"))


if __name__ == "__main__":
    app()
