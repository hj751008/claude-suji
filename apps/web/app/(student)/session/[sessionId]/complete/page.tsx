import { createClient } from "@/lib/supabase/server";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";

const praises = [
  "오늘도 멋졌어!",
  "수고했어, 최고야!",
  "역시 수지! 잘했어!",
  "대단해, 오늘도 해냈다!",
  "완벽한 하루!",
];

function getPraise(correct: number, total: number) {
  if (total === 0) return praises[0];
  const ratio = correct / total;
  if (ratio >= 0.8) return "완벽에 가까워! 🌟🌟🌟";
  if (ratio >= 0.6) return "잘하고 있어! 🌟🌟";
  if (ratio >= 0.4) return "좋은 시작이야! 🌟";
  return "도전한 것 자체가 대단해! 💪";
}

function getEmoji(correct: number, total: number) {
  if (total === 0) return "🎉";
  const ratio = correct / total;
  if (ratio >= 0.8) return "🏆";
  if (ratio >= 0.6) return "🎉";
  if (ratio >= 0.4) return "✨";
  return "💪";
}

export default async function SessionCompletePage({
  params,
}: {
  params: { sessionId: string };
}) {
  const supabase = createClient();

  await supabase
    .from("sessions")
    .update({ ended_at: new Date().toISOString() })
    .eq("id", params.sessionId);

  const { data: attempts } = await supabase
    .from("attempts")
    .select("is_correct, time_ms")
    .eq("session_id", params.sessionId);

  const total = attempts?.length ?? 0;
  const correct = attempts?.filter((a) => a.is_correct).length ?? 0;
  const emoji = getEmoji(correct, total);
  const praise = getPraise(correct, total);

  return (
    <div className="space-y-6 text-center py-6 animate-pop-in">
      <div>
        <p className="text-6xl mb-3 animate-bounce-gentle">{emoji}</p>
        <h1 className="text-2xl font-bold">미션 완료!</h1>
      </div>

      <Card className="bg-gradient-to-br from-pastel-yellow/40 to-pastel-mint/30">
        <CardContent className="p-6 space-y-3">
          <p className="text-lg font-bold text-foreground">{praise}</p>
          <p className="text-sm text-muted-foreground">
            오늘 {total}문제에 도전했어
          </p>
        </CardContent>
      </Card>

      <div className="space-y-3">
        <Button asChild size="lg" className="w-full">
          <Link href="/home">홈으로 🏠</Link>
        </Button>
        <Button asChild variant="outline" size="lg" className="w-full">
          <Link href="/session">한 세트 더! 💪</Link>
        </Button>
      </div>
    </div>
  );
}
