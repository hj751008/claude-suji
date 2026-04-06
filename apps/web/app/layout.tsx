import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "수지의 수학 학습 파트너",
  description: "개념 식별 훈련으로 수학 기초를 다지자",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
      <body>{children}</body>
    </html>
  );
}
