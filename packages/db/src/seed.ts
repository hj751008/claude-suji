import "dotenv/config";
import { db, schema } from "./index";
import { eq } from "drizzle-orm";

async function seed() {
  console.log("🌱 Seeding database...");

  // SUBJECT → GRADE → UNIT → SUB_UNIT
  const [subject] = await db.insert(schema.subjects).values({ name: "수학" })
    .onConflictDoNothing().returning();
  const actualSubject = subject ??
    (await db.select().from(schema.subjects).where(eq(schema.subjects.name, "수학")))[0];

  const [grade] = await db.insert(schema.grades).values({
    subjectId: actualSubject.id, name: "중1", order: 1,
  }).returning();

  const [unit] = await db.insert(schema.units).values({
    gradeId: grade.id, name: "수와 연산", order: 1,
  }).returning();

  const [subUnit] = await db.insert(schema.subUnits).values({
    unitId: unit.id, name: "정수와 유리수", order: 1,
  }).returning();

  // CONCEPTS (3개)
  const conceptRows = await db.insert(schema.concepts).values([
    { subUnitId: subUnit.id, name: "자연수", description: "1, 2, 3, ... 양의 정수", order: 1 },
    { subUnitId: subUnit.id, name: "정수", description: "..., -2, -1, 0, 1, 2, ...", order: 2 },
    { subUnitId: subUnit.id, name: "수의 범위", description: "'~보다 크고 ~보다 작은' 형태", order: 3 },
  ]).returning();

  const [자연수, 정수, 수의범위] = conceptRows;
  console.log(`  ✓ ${conceptRows.length} concepts inserted`);

  // PROBLEMS (5개, Lv1)
  const problemRows = await db.insert(schema.problems).values([
    {
      conceptPrimaryId: 자연수.id, difficulty: 1,
      body: "1부터 10까지의 자연수 중 5보다 큰 수는 몇 개입니까?",
      answer: "5",
      status: "published" as const, sympyVerified: true,
    },
    {
      conceptPrimaryId: 정수.id, difficulty: 1,
      body: "다음 중 정수가 아닌 것은? ① -3 ② 0 ③ 1/2 ④ 7",
      answer: "3",
      status: "published" as const, sympyVerified: true,
    },
    {
      conceptPrimaryId: 수의범위.id, difficulty: 1,
      body: "2보다 크고 7보다 작은 자연수의 개수는?",
      answer: "4",
      status: "published" as const, sympyVerified: true,
    },
    {
      conceptPrimaryId: 자연수.id, difficulty: 1,
      body: "0은 자연수입니까? (예/아니오)",
      answer: "아니오",
      status: "published" as const, sympyVerified: true,
    },
    {
      conceptPrimaryId: 정수.id, difficulty: 1,
      body: "-5와 3 사이의 정수는 모두 몇 개입니까? (양 끝 포함 안 함)",
      answer: "7",
      status: "published" as const, sympyVerified: true,
    },
  ]).returning();

  console.log(`  ✓ ${problemRows.length} problems inserted`);

  // problem_concepts (다중 태깅)
  await db.insert(schema.problemConcepts).values([
    { problemId: problemRows[0].id, conceptId: 자연수.id },
    { problemId: problemRows[0].id, conceptId: 수의범위.id },
    { problemId: problemRows[1].id, conceptId: 정수.id },
    { problemId: problemRows[2].id, conceptId: 자연수.id },
    { problemId: problemRows[2].id, conceptId: 수의범위.id },
    { problemId: problemRows[3].id, conceptId: 자연수.id },
    { problemId: problemRows[4].id, conceptId: 정수.id },
    { problemId: problemRows[4].id, conceptId: 수의범위.id },
  ]);

  // WEBTOON SCRIPTS
  await db.insert(schema.webtoonScripts).values([
    {
      problemId: problemRows[0].id,
      script: [
        { type: "scene", text: "수지가 문제를 보며 고민 중" },
        { speaker: "수지", text: "자연수가 뭐더라... 1부터 시작하는 거 맞지?" },
        { speaker: "AI튜터", text: "맞아. 1, 2, 3, ... 이렇게 가는 수야. 0이나 음수는 아니야." },
        { speaker: "AI튜터", text: "그리고 '5보다 큰'은 범위 시그널. 6부터 세면 돼." },
      ],
    },
    {
      problemId: problemRows[1].id,
      script: [
        { speaker: "수지", text: "정수? 음수도 정수라 했지?" },
        { speaker: "AI튜터", text: "맞아. ..., -3, -2, -1, 0, 1, 2, 3, ...이 정수야." },
        { speaker: "AI튜터", text: "1/2처럼 **분수 형태**는 정수가 아니야. 유리수지." },
      ],
    },
    {
      problemId: problemRows[2].id,
      script: [
        { speaker: "AI튜터", text: "'~보다 크고 ~보다 작은'은 범위 표현 시그널이야." },
        { speaker: "AI튜터", text: "2보다 크니까 3부터, 7보다 작으니까 6까지. 3,4,5,6 = 4개." },
      ],
    },
    {
      problemId: problemRows[3].id,
      script: [
        { speaker: "AI튜터", text: "자연수는 '물건 개수 셀 때' 쓰는 수야. 1부터 시작." },
        { speaker: "AI튜터", text: "0은 '없음'이라서 자연수가 아니야." },
      ],
    },
    {
      problemId: problemRows[4].id,
      script: [
        { speaker: "AI튜터", text: "-5와 3 사이, 양 끝 포함 안 함 → -4, -3, -2, -1, 0, 1, 2" },
        { speaker: "AI튜터", text: "세어보면 7개." },
      ],
    },
  ]);

  console.log("✅ Seed complete");
  process.exit(0);
}

seed().catch((e) => {
  console.error(e);
  process.exit(1);
});
