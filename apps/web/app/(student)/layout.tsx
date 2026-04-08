import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import { LogoutButton } from "@/components/logout-button";

export default async function StudentLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: profile } = await supabase
    .from("profiles")
    .select("role, nickname")
    .eq("id", user.id)
    .single();

  if (!profile) redirect("/login");
  if (profile.role !== "student") redirect("/dashboard");

  return (
    <div className="min-h-screen bg-gradient-to-b from-pastel-lavender/30 via-background to-pastel-mint/20">
      <header className="sticky top-0 z-10 backdrop-blur-sm bg-white/70 border-b border-border/50 px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="text-lg">📐</span>
          <h1 className="text-sm font-semibold text-primary">수지의 수학</h1>
        </div>
        <LogoutButton />
      </header>
      <main className="p-4 pb-8 max-w-md mx-auto">{children}</main>
    </div>
  );
}
