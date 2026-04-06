import { createClient } from "@/lib/supabase/server";
import { NextResponse } from "next/server";
import { gradeConceptIdentification } from "@/lib/session/grading";

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

  return NextResponse.json({
    isCorrect,
    webtoonScript: webtoon?.script ?? null,
  });
}
