import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import { SessionRunner } from "./session-runner";

export default async function SessionPage({
  params,
}: {
  params: { sessionId: string };
}) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: problems } = await supabase
    .from("problems")
    .select(`
      id, body, difficulty,
      problem_concepts(concept_id)
    `)
    .eq("status", "published")
    .limit(5);

  const { data: allConcepts } = await supabase
    .from("concepts")
    .select("id, name");

  if (!problems || problems.length === 0 || !allConcepts) {
    return <p className="text-sm text-muted-foreground">문제가 준비되지 않았어요.</p>;
  }

  const problemsWithConcepts = problems.map((p) => ({
    id: p.id,
    body: p.body,
    difficulty: p.difficulty,
    correctConceptIds: (p.problem_concepts ?? []).map((pc: { concept_id: string }) => pc.concept_id),
  }));

  return (
    <SessionRunner
      sessionId={params.sessionId}
      problems={problemsWithConcepts}
      allConcepts={allConcepts}
    />
  );
}
