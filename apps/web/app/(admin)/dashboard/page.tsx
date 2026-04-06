import { createClient } from "@/lib/supabase/server";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

export default async function AdminDashboardPage() {
  const supabase = createClient();

  const { count: totalAttempts } = await supabase
    .from("attempts")
    .select("*", { count: "exact", head: true });

  const { count: totalSessions } = await supabase
    .from("sessions")
    .select("*", { count: "exact", head: true });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold">관리자 대시보드</h1>
      <div className="grid grid-cols-2 gap-4">
        <Card>
          <CardHeader><CardTitle className="text-sm">총 시도</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold">{totalAttempts ?? 0}</p></CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="text-sm">총 세션</CardTitle></CardHeader>
          <CardContent><p className="text-3xl font-bold">{totalSessions ?? 0}</p></CardContent>
        </Card>
      </div>
      <p className="text-sm text-muted-foreground">상세 대시보드는 Plan 3에서 확장됩니다.</p>
    </div>
  );
}
