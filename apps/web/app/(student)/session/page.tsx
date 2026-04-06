"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

export default function SessionStartPage() {
  const router = useRouter();

  useEffect(() => {
    let cancelled = false;
    (async () => {
      const res = await fetch("/api/session/start", { method: "POST" });
      if (!res.ok) {
        alert("세션 시작 실패");
        router.push("/home");
        return;
      }
      const { sessionId } = await res.json();
      if (!cancelled) router.push(`/session/${sessionId}`);
    })();
    return () => { cancelled = true; };
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-[200px]">
      <p className="text-sm text-muted-foreground">세션 준비 중...</p>
    </div>
  );
}
