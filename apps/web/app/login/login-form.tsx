"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { login } from "./actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent } from "@/components/ui/card";

export function LoginForm() {
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);
  const router = useRouter();

  async function handleSubmit(formData: FormData) {
    setPending(true);
    setError(null);
    const result = await login(formData);
    if (result?.error) {
      setError(result.error);
      setPending(false);
    } else {
      window.location.href = "/home";
    }
  }

  return (
    <Card className="w-full max-w-sm animate-pop-in">
      <CardContent className="p-6">
        <form action={handleSubmit} className="space-y-5">
          <div className="space-y-2">
            <Label htmlFor="email">이메일</Label>
            <Input id="email" name="email" type="email" required autoComplete="email" placeholder="suji@suji.app" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">비밀번호</Label>
            <Input id="password" name="password" type="password" required autoComplete="current-password" placeholder="비밀번호 입력" />
          </div>
          {error && (
            <p className="text-sm text-destructive bg-destructive/10 rounded-lg p-2 text-center">{error}</p>
          )}
          <Button type="submit" className="w-full" size="lg" disabled={pending}>
            {pending ? "로그인 중... ⏳" : "시작하기 🚀"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
