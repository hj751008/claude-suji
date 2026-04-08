import { createClient } from "@/lib/supabase/server";
import { NextResponse } from "next/server";
import { gradeConceptIdentification } from "@/lib/session/grading";
import { evaluateMastery, type MasteryState } from "@/lib/session/mastery";

export async function POST(
  request: Request,
  { params }: { params: { id: string } },
) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await request.json();
  const { problemId, selectedConceptIds, timeMs } = body as {
    problemId: string;
    selectedConceptIds: string[];
    timeMs: number;
  };

  // Load correct concept IDs
  const { data: pcRows, error: pcError } = await supabase
    .from("problem_concepts")
    .select("concept_id")
    .eq("problem_id", problemId);

  if (pcError || !pcRows) {
    return NextResponse.json({ error: "problem not found" }, { status: 404 });
  }

  const correctConceptIds = pcRows.map((r) => r.concept_id);
  const { isCorrect } = gradeConceptIdentification({
    selectedConceptIds,
    correctConceptIds,
  });

  // Record attempt
  const { error: attemptError } = await supabase.from("attempts").insert({
    session_id: params.id,
    user_id: user.id,
    problem_id: problemId,
    selected_concepts: selectedConceptIds,
    is_correct: isCorrect,
    time_ms: timeMs,
  });
  if (attemptError) {
    return NextResponse.json({ error: attemptError.message }, { status: 500 });
  }

  // Load webtoon script
  const { data: webtoon } = await supabase
    .from("webtoon_scripts")
    .select("script")
    .eq("problem_id", problemId)
    .single();

  // Update concept mastery for the primary concept
  const { data: problem } = await supabase
    .from("problems")
    .select("concept_primary_id, difficulty")
    .eq("id", problemId)
    .single();

  let masteryChange: "up" | "down" | null = null;

  if (problem?.concept_primary_id) {
    const conceptId = problem.concept_primary_id;

    // Get or create mastery record
    const { data: mastery } = await supabase
      .from("concept_mastery")
      .select("level, accuracy_recent_10, attempts_total, downgrade_warnings")
      .eq("user_id", user.id)
      .eq("concept_id", conceptId)
      .single();

    const currentState: MasteryState = mastery
      ? {
          level: mastery.level,
          accuracyRecent10: mastery.accuracy_recent_10,
          attemptsTotal: mastery.attempts_total,
          downgradeWarnings: mastery.downgrade_warnings,
        }
      : { level: 1, accuracyRecent10: 0, attemptsTotal: 0, downgradeWarnings: 0 };

    // Load recent attempts for this user+concept (newest first)
    const { data: recentRows } = await supabase
      .from("attempts")
      .select("is_correct, problem_id")
      .eq("user_id", user.id)
      .order("attempted_at", { ascending: false })
      .limit(10);

    // Filter attempts related to this concept
    const conceptProblemIds = new Set<string>();
    if (recentRows) {
      const problemIds = [...new Set(recentRows.map((r) => r.problem_id))];
      const { data: relatedPc } = await supabase
        .from("problem_concepts")
        .select("problem_id")
        .eq("concept_id", conceptId)
        .in("problem_id", problemIds);
      (relatedPc ?? []).forEach((r) => conceptProblemIds.add(r.problem_id));
    }

    const conceptAttempts = (recentRows ?? [])
      .filter((r) => conceptProblemIds.has(r.problem_id))
      .map((r) => r.is_correct);

    // Get recent attempts at current level
    const { data: levelProblems } = await supabase
      .from("problems")
      .select("id")
      .eq("concept_primary_id", conceptId)
      .eq("difficulty", currentState.level);

    const levelProblemIds = new Set((levelProblems ?? []).map((p) => p.id));
    const recentAtCurrentLevel = (recentRows ?? [])
      .filter((r) => levelProblemIds.has(r.problem_id))
      .map((r) => r.is_correct);

    const evalResult = evaluateMastery({
      current: currentState,
      recentAttempts: conceptAttempts,
      recentAtCurrentLevel,
    });

    masteryChange = evalResult.levelChanged;

    // Upsert mastery
    await supabase.from("concept_mastery").upsert({
      user_id: user.id,
      concept_id: conceptId,
      level: evalResult.newState.level,
      accuracy_recent_10: evalResult.newState.accuracyRecent10,
      attempts_total: evalResult.newState.attemptsTotal,
      downgrade_warnings: evalResult.newState.downgradeWarnings,
      last_updated: new Date().toISOString(),
    });
  }

  return NextResponse.json({
    isCorrect,
    webtoonScript: webtoon?.script ?? null,
    masteryChange,
  });
}
