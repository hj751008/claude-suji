import { LoginForm } from "./login-form";

export default function LoginPage() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center p-8">
      <div className="text-center mb-8">
        <h1 className="text-2xl font-bold">수지의 수학 학습 파트너</h1>
        <p className="text-sm text-muted-foreground mt-2">로그인하고 시작해요</p>
      </div>
      <LoginForm />
    </main>
  );
}
