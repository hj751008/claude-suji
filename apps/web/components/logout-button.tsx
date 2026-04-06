"use client";

import { Button } from "@/components/ui/button";
import { logout } from "@/app/logout/actions";

export function LogoutButton() {
  return (
    <form action={logout}>
      <Button variant="ghost" size="sm" type="submit">로그아웃</Button>
    </form>
  );
}
