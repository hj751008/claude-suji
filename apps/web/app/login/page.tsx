import { LoginForm } from "./login-form";

export default function LoginPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8 bg-gradient-to-b from-pastel-lavender/40 via-background to-pastel-pink/20">
      <div className="text-center mb-8 animate-pop-in">
        <p className="text-5xl mb-4">📐✨</p>
        <h1 className="text-2xl font-bold text-foreground">수지의 수학 파트너</h1>
        <p className="text-sm text-muted-foreground mt-2">오늘도 같이 공부하자!</p>
      </div>
      <LoginForm />
    </main>
  );
}
