import { createClient } from "@/lib/supabase/server";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import Link from "next/link";

export default async function StudentHomePage() {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();

  const { data: profile } = await supabase
    .from("profiles")
    .select("nickname")
    .eq("id", user!.id)
    .single();

  return (
    <div className="space-y-5 pt-2">
      <div className="text-center animate-pop-in">
        <p className="text-4xl mb-2 animate-bounce-gentle">👋</p>
        <h1 className="text-2xl font-bold">
          안녕, {profile?.nickname ?? "수지"}!
        </h1>
        <p className="text-sm text-muted-foreground mt-1">오늘도 화이팅!</p>
      </div>

      <Card className="bg-gradient-to-br from-pastel-lavender/50 to-pastel-pink/30 border-primary/20 animate-pop-in">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <span className="text-2xl">🎯</span> 오늘의 미션
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">5문제 풀고 오늘 미션 클리어!</p>
          <Button asChild className="w-full" size="lg">
            <Link href="/session">시작하기 🚀</Link>
          </Button>
        </CardContent>
      </Card>

      <Card className="bg-gradient-to-br from-pastel-mint/40 to-pastel-blue/30 border-secondary/30 animate-pop-in">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <span className="text-2xl">📚</span> 자유 연습
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">원하는 만큼 더 풀어보자!</p>
          <Button asChild variant="outline" className="w-full" size="lg">
            <Link href="/session">연습하기 💪</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
