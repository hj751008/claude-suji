import { createClient } from "@/lib/supabase/server";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";

export default async function SessionCompletePage({
  params,
}: {
  params: { sessionId: string };
}) {
  const supabase = createClient();

  // Mark session ended
  await supabase
    .from("sessions")
    .update({ ended_at: new Date().toISOString() })
    .eq("id", params.sessionId);

  // Load attempts for this session
  const { data: attempts } = await supabase
    .from("attempts")
    .select("is_correct, time_ms")
    .eq("session_id", params.sessionId);

  const total = attempts?.length ?? 0;
  const correct = attempts?.filter((a) => a.is_correct).length ?? 0;
  const totalTimeSec = Math.round(
    (attempts ?? []).reduce((s, a) => s + (a.time_ms ?? 0), 0) / 1000,
  );

  return (
    <div className="space-y-6 text-center py-8">
      <h1 className="text-2xl font-bold">🎉 오늘 미션 완료!</h1>
      <Card>
        <CardContent className="p-6 space-y-3">
          <p className="text-lg">정답: {correct}/{total}</p>
          <p className="text-sm text-muted-foreground">
            시간: {Math.floor(totalTimeSec / 60)}분 {totalTimeSec % 60}초
          </p>
        </CardContent>
      </Card>
      <Button asChild size="lg" className="w-full">
        <Link href="/home">홈으로</Link>
      </Button>
    </div>
  );
}
