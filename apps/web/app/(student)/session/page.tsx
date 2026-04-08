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
    <div className="flex flex-col items-center justify-center min-h-[300px] animate-pop-in">
      <p className="text-4xl mb-4 animate-bounce-gentle">📐</p>
      <p className="text-sm text-muted-foreground font-medium">문제 준비 중...</p>
    </div>
  );
}
