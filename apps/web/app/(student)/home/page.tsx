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
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold">안녕, {profile?.nickname ?? "수지"} 👋</h1>
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-lg">📊 오늘의 미션</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-sm text-muted-foreground">5문제 · 개념 식별 훈련</p>
          <Button asChild className="w-full">
            <Link href="/session">시작하기</Link>
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
