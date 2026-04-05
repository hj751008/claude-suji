# Plan 1: Walking Skeleton Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 수지가 로그인해서 시드 문제 3-5개로 개념 식별 세션을 완료할 수 있는 end-to-end 웹앱을 Vercel에 배포한다.

**Architecture:** pnpm 모노레포 안에 Next.js 14 App Router 웹앱. Supabase(Postgres+Auth+RLS)가 DB/인증 담당. Drizzle ORM으로 타입 세이프 스키마. 시드 데이터 3 concepts + 5 problems로 세션 흐름 end-to-end 검증.

**Tech Stack:** Next.js 14, TypeScript 5, pnpm workspaces, Tailwind CSS, shadcn/ui, Drizzle ORM, Supabase (Auth + Postgres + RLS), Vercel

---

## File Structure

**신규 생성 파일:**

```
claude-suji/
├── package.json                          # 루트 workspace 설정
├── pnpm-workspace.yaml                   # workspace 정의
├── .gitignore                            # Node/Next/env 무시
├── .env.example                          # 환경변수 템플릿
├── biome.json                            # 린트/포맷 설정
├── apps/
│   └── web/
│       ├── package.json
│       ├── next.config.mjs
│       ├── tsconfig.json
│       ├── tailwind.config.ts
│       ├── postcss.config.mjs
│       ├── components.json               # shadcn/ui 설정
│       ├── app/
│       │   ├── layout.tsx
│       │   ├── page.tsx                  # 랜딩(로그인으로 리다이렉트)
│       │   ├── globals.css
│       │   ├── login/page.tsx
│       │   ├── (student)/
│       │   │   ├── layout.tsx
│       │   │   ├── home/page.tsx
│       │   │   └── session/
│       │   │       ├── page.tsx          # 세션 시작
│       │   │       └── [sessionId]/
│       │   │           ├── page.tsx      # 세션 진행
│       │   │           └── complete/page.tsx
│       │   ├── (admin)/
│       │   │   ├── layout.tsx
│       │   │   └── dashboard/page.tsx    # 스텁만
│       │   ├── api/
│       │   │   ├── session/start/route.ts
│       │   │   └── session/[id]/submit/route.ts
│       │   └── auth/
│       │       └── callback/route.ts
│       ├── components/
│       │   ├── ui/                       # shadcn 생성 컴포넌트
│       │   ├── problem-card.tsx
│       │   ├── concept-multiselect.tsx
│       │   └── feedback-panel.tsx
│       ├── lib/
│       │   ├── supabase/
│       │   │   ├── client.ts             # 브라우저 클라이언트
│       │   │   ├── server.ts             # 서버 컴포넌트 클라이언트
│       │   │   └── middleware.ts         # 미들웨어 헬퍼
│       │   ├── db/
│       │   │   ├── schema.ts             # Drizzle 스키마
│       │   │   └── index.ts              # DB 클라이언트
│       │   ├── session/
│       │   │   ├── grading.ts            # 정답 판정 순수함수
│       │   │   └── grading.test.ts
│       │   └── utils.ts
│       └── middleware.ts                 # Next.js 미들웨어(auth 체크)
├── packages/
│   └── db/
│       ├── package.json
│       ├── drizzle.config.ts
│       ├── src/
│       │   ├── schema.ts                 # 마스터 스키마(apps/web이 재export)
│       │   └── seed.ts                   # 시드 스크립트
│       └── migrations/
│           └── (Drizzle 자동생성)
└── docs/
    └── superpowers/
        ├── specs/2026-04-06-suji-math-app-design.md (이미 존재)
        └── plans/2026-04-06-plan1-walking-skeleton.md (이 파일)
```

**수정 파일:** 없음 (빈 레포에서 시작)

---

## 사전 요구사항

시작하기 전에 다음이 준비되어 있어야 한다:

1. **Supabase 프로젝트**: https://supabase.com 에서 무료 프로젝트 1개 생성 완료
   - 프로젝트 URL, anon key, service_role key 확보
   - Postgres 연결 문자열(Connection String) 확보
2. **Vercel 계정**: 기존 무료 계정 사용
3. **로컬 도구**:
   - Node.js 20+
   - pnpm 9+ (`npm install -g pnpm`)
   - Git

---

## Task 1: pnpm 모노레포 초기화

**Files:**
- Create: `package.json`
- Create: `pnpm-workspace.yaml`
- Create: `.gitignore`
- Create: `.env.example`

- [ ] **Step 1: 루트 package.json 생성**

Create `package.json`:
```json
{
  "name": "claude-suji",
  "version": "0.1.0",
  "private": true,
  "packageManager": "pnpm@9.0.0",
  "scripts": {
    "dev": "pnpm --filter web dev",
    "build": "pnpm --filter web build",
    "lint": "pnpm -r lint",
    "db:generate": "pnpm --filter @suji/db generate",
    "db:migrate": "pnpm --filter @suji/db migrate",
    "db:seed": "pnpm --filter @suji/db seed"
  },
  "devDependencies": {
    "@biomejs/biome": "^1.9.0"
  }
}
```

- [ ] **Step 2: pnpm-workspace.yaml 생성**

Create `pnpm-workspace.yaml`:
```yaml
packages:
  - "apps/*"
  - "packages/*"
```

- [ ] **Step 3: .gitignore 생성**

Create `.gitignore`:
```
node_modules/
.next/
.turbo/
dist/
.env
.env.local
*.log
.DS_Store
.vercel/
.vscode/
.idea/
coverage/
.swc/
next-env.d.ts
```

- [ ] **Step 4: .env.example 생성**

Create `.env.example`:
```
# Supabase
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=

# Database (Drizzle/서버)
DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@[YOUR-HOST]:5432/postgres
```

- [ ] **Step 5: 디렉터리 구조 생성 후 커밋**

Run:
```bash
mkdir -p apps/web packages/db
pnpm install
git add package.json pnpm-workspace.yaml pnpm-lock.yaml .gitignore .env.example
git commit -m "chore: initialize pnpm monorepo workspace"
```

---

## Task 2: Next.js 14 앱 생성 (apps/web)

**Files:**
- Create: `apps/web/package.json`
- Create: `apps/web/next.config.mjs`
- Create: `apps/web/tsconfig.json`
- Create: `apps/web/app/layout.tsx`
- Create: `apps/web/app/page.tsx`
- Create: `apps/web/app/globals.css`

- [ ] **Step 1: apps/web/package.json 생성**

Create `apps/web/package.json`:
```json
{
  "name": "web",
  "version": "0.1.0",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "biome check ."
  },
  "dependencies": {
    "next": "14.2.16",
    "react": "18.3.1",
    "react-dom": "18.3.1"
  },
  "devDependencies": {
    "@types/node": "20.16.10",
    "@types/react": "18.3.11",
    "@types/react-dom": "18.3.0",
    "typescript": "5.6.2"
  }
}
```

- [ ] **Step 2: next.config.mjs 생성**

Create `apps/web/next.config.mjs`:
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    typedRoutes: true,
  },
};

export default nextConfig;
```

- [ ] **Step 3: tsconfig.json 생성**

Create `apps/web/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [{ "name": "next" }],
    "paths": { "@/*": ["./*"] }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 4: 기본 layout과 page 생성**

Create `apps/web/app/layout.tsx`:
```tsx
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
```

Create `apps/web/app/page.tsx`:
```tsx
import { redirect } from "next/navigation";

export default function HomePage() {
  redirect("/login");
}
```

Create `apps/web/app/globals.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;
```

- [ ] **Step 5: 의존성 설치 후 dev 서버 확인**

Run:
```bash
pnpm install
pnpm dev
```
Expected: `http://localhost:3000` 접속 시 `/login`으로 리다이렉트 (아직 404 예상. 정상).
Stop the dev server (Ctrl+C).

- [ ] **Step 6: 커밋**

```bash
git add apps/web
git commit -m "feat(web): scaffold Next.js 14 app with TypeScript"
```

---

## Task 3: Tailwind CSS + shadcn/ui 설치

**Files:**
- Create: `apps/web/tailwind.config.ts`
- Create: `apps/web/postcss.config.mjs`
- Create: `apps/web/components.json`
- Modify: `apps/web/app/globals.css`
- Modify: `apps/web/package.json`

- [ ] **Step 1: Tailwind + shadcn/ui 의존성 설치**

Run from `apps/web`:
```bash
cd apps/web
pnpm add -D tailwindcss@3.4.13 postcss@8.4.47 autoprefixer@10.4.20
pnpm add class-variance-authority@0.7.0 clsx@2.1.1 tailwind-merge@2.5.2 lucide-react@0.446.0 tailwindcss-animate@1.0.7
cd ../..
```

- [ ] **Step 2: tailwind.config.ts 생성**

Create `apps/web/tailwind.config.ts`:
```typescript
import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ["class"],
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    container: { center: true, padding: "2rem", screens: { "2xl": "1400px" } },
    extend: {
      colors: {
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
      },
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
    },
  },
  plugins: [require("tailwindcss-animate")],
};
export default config;
```

- [ ] **Step 3: postcss.config.mjs 생성**

Create `apps/web/postcss.config.mjs`:
```javascript
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
};
```

- [ ] **Step 4: globals.css에 CSS 변수 추가**

Modify `apps/web/app/globals.css`:
```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --card: 0 0% 100%;
    --card-foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --secondary: 210 40% 96.1%;
    --secondary-foreground: 222.2 47.4% 11.2%;
    --muted: 210 40% 96.1%;
    --muted-foreground: 215.4 16.3% 46.9%;
    --accent: 210 40% 96.1%;
    --accent-foreground: 222.2 47.4% 11.2%;
    --destructive: 0 84.2% 60.2%;
    --destructive-foreground: 210 40% 98%;
    --border: 214.3 31.8% 91.4%;
    --input: 214.3 31.8% 91.4%;
    --ring: 222.2 84% 4.9%;
    --radius: 0.5rem;
  }
}

@layer base {
  * { @apply border-border; }
  body { @apply bg-background text-foreground; }
}
```

- [ ] **Step 5: components.json 생성 (shadcn/ui 설정)**

Create `apps/web/components.json`:
```json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

- [ ] **Step 6: lib/utils.ts 생성**

Create `apps/web/lib/utils.ts`:
```typescript
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}
```

- [ ] **Step 7: shadcn/ui 기본 컴포넌트 설치**

Run from `apps/web`:
```bash
cd apps/web
pnpm dlx shadcn@latest add button card checkbox label input
cd ../..
```
(프롬프트가 나오면 기본값 선택)

- [ ] **Step 8: dev 서버에서 Tailwind 적용 확인**

Modify `apps/web/app/page.tsx`:
```tsx
import { redirect } from "next/navigation";

export default function HomePage() {
  redirect("/login");
}
```

(파일은 이미 생성됨. 그대로 둠.)

Run `pnpm dev`, 접속해서 에러 없는지 확인. Stop server.

- [ ] **Step 9: 커밋**

```bash
git add apps/web
git commit -m "feat(web): add Tailwind CSS and shadcn/ui components"
```

---

## Task 4: packages/db 셋업 + Drizzle 스키마

**Files:**
- Create: `packages/db/package.json`
- Create: `packages/db/drizzle.config.ts`
- Create: `packages/db/src/schema.ts`
- Create: `packages/db/src/index.ts`
- Create: `packages/db/tsconfig.json`

- [ ] **Step 1: packages/db/package.json 생성**

Create `packages/db/package.json`:
```json
{
  "name": "@suji/db",
  "version": "0.1.0",
  "private": true,
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "scripts": {
    "generate": "drizzle-kit generate",
    "migrate": "drizzle-kit migrate",
    "push": "drizzle-kit push",
    "seed": "tsx src/seed.ts"
  },
  "dependencies": {
    "drizzle-orm": "0.34.0",
    "postgres": "3.4.4"
  },
  "devDependencies": {
    "@types/node": "20.16.10",
    "drizzle-kit": "0.25.0",
    "tsx": "4.19.1",
    "dotenv": "16.4.5",
    "typescript": "5.6.2"
  }
}
```

- [ ] **Step 2: packages/db/tsconfig.json 생성**

Create `packages/db/tsconfig.json`:
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "types": ["node"]
  },
  "include": ["src/**/*.ts"]
}
```

- [ ] **Step 3: drizzle.config.ts 생성**

Create `packages/db/drizzle.config.ts`:
```typescript
import "dotenv/config";
import type { Config } from "drizzle-kit";

export default {
  schema: "./src/schema.ts",
  out: "./migrations",
  dialect: "postgresql",
  dbCredentials: {
    url: process.env.DATABASE_URL!,
  },
  verbose: true,
  strict: true,
} satisfies Config;
```

- [ ] **Step 4: Drizzle 스키마 생성**

Create `packages/db/src/schema.ts`:
```typescript
import {
  pgTable, uuid, text, integer, boolean, timestamp, jsonb, pgEnum, primaryKey, index,
} from "drizzle-orm/pg-core";

// ENUMS
export const userRoleEnum = pgEnum("user_role", ["student", "admin"]);
export const problemStatusEnum = pgEnum("problem_status", ["published", "draft", "rejected"]);
export const sessionModeEnum = pgEnum("session_mode", ["daily", "free"]);

// CORE CONTENT
export const subjects = pgTable("subjects", {
  id: uuid("id").primaryKey().defaultRandom(),
  name: text("name").notNull().unique(),
  createdAt: timestamp("created_at").notNull().defaultNow(),
});

export const grades = pgTable("grades", {
  id: uuid("id").primaryKey().defaultRandom(),
  subjectId: uuid("subject_id").notNull().references(() => subjects.id),
  name: text("name").notNull(),
  order: integer("order").notNull(),
});

export const units = pgTable("units", {
  id: uuid("id").primaryKey().defaultRandom(),
  gradeId: uuid("grade_id").notNull().references(() => grades.id),
  name: text("name").notNull(),
  order: integer("order").notNull(),
});

export const subUnits = pgTable("sub_units", {
  id: uuid("id").primaryKey().defaultRandom(),
  unitId: uuid("unit_id").notNull().references(() => units.id),
  name: text("name").notNull(),
  order: integer("order").notNull(),
});

export const concepts = pgTable("concepts", {
  id: uuid("id").primaryKey().defaultRandom(),
  subUnitId: uuid("sub_unit_id").notNull().references(() => subUnits.id),
  name: text("name").notNull(),
  description: text("description"),
  order: integer("order").notNull(),
});

export const problems = pgTable("problems", {
  id: uuid("id").primaryKey().defaultRandom(),
  conceptPrimaryId: uuid("concept_primary_id").notNull().references(() => concepts.id),
  difficulty: integer("difficulty").notNull(), // 1-4
  body: text("body").notNull(),
  answer: text("answer").notNull(),
  status: problemStatusEnum("status").notNull().default("draft"),
  sympyVerified: boolean("sympy_verified").notNull().default(false),
  sourceTrace: jsonb("source_trace"),
  createdAt: timestamp("created_at").notNull().defaultNow(),
});

export const problemConcepts = pgTable(
  "problem_concepts",
  {
    problemId: uuid("problem_id").notNull().references(() => problems.id, { onDelete: "cascade" }),
    conceptId: uuid("concept_id").notNull().references(() => concepts.id),
  },
  (t) => ({ pk: primaryKey({ columns: [t.problemId, t.conceptId] }) })
);

export const solutions = pgTable("solutions", {
  problemId: uuid("problem_id").primaryKey().references(() => problems.id, { onDelete: "cascade" }),
  steps: jsonb("steps").notNull(),
});

export const webtoonScripts = pgTable("webtoon_scripts", {
  problemId: uuid("problem_id").primaryKey().references(() => problems.id, { onDelete: "cascade" }),
  script: jsonb("script").notNull(),
});

// USERS & LEARNING
export const profiles = pgTable("profiles", {
  id: uuid("id").primaryKey(), // matches auth.users.id
  role: userRoleEnum("role").notNull().default("student"),
  nickname: text("nickname"),
  createdAt: timestamp("created_at").notNull().defaultNow(),
});

export const sessions = pgTable("sessions", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").notNull().references(() => profiles.id, { onDelete: "cascade" }),
  mode: sessionModeEnum("mode").notNull(),
  startedAt: timestamp("started_at").notNull().defaultNow(),
  endedAt: timestamp("ended_at"),
});

export const attempts = pgTable(
  "attempts",
  {
    id: uuid("id").primaryKey().defaultRandom(),
    sessionId: uuid("session_id").notNull().references(() => sessions.id, { onDelete: "cascade" }),
    userId: uuid("user_id").notNull().references(() => profiles.id, { onDelete: "cascade" }),
    problemId: uuid("problem_id").notNull().references(() => problems.id),
    selectedConcepts: jsonb("selected_concepts").notNull(), // uuid[]
    isCorrect: boolean("is_correct").notNull(),
    timeMs: integer("time_ms").notNull(),
    attemptedAt: timestamp("attempted_at").notNull().defaultNow(),
  },
  (t) => ({ userIdx: index("attempts_user_idx").on(t.userId) })
);

export const conceptMastery = pgTable(
  "concept_mastery",
  {
    userId: uuid("user_id").notNull().references(() => profiles.id, { onDelete: "cascade" }),
    conceptId: uuid("concept_id").notNull().references(() => concepts.id),
    level: integer("level").notNull().default(1),
    accuracyRecent10: integer("accuracy_recent_10").notNull().default(0), // percent 0-100
    attemptsTotal: integer("attempts_total").notNull().default(0),
    downgradeWarnings: integer("downgrade_warnings").notNull().default(0),
    lastUpdated: timestamp("last_updated").notNull().defaultNow(),
  },
  (t) => ({ pk: primaryKey({ columns: [t.userId, t.conceptId] }) })
);

// OPERATIONAL
export const rewards = pgTable("rewards", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").notNull().references(() => profiles.id, { onDelete: "cascade" }),
  kind: text("kind").notNull(), // "sticker" | "praise"
  content: text("content").notNull(),
  grantedAt: timestamp("granted_at").notNull().defaultNow(),
  grantedBy: uuid("granted_by").notNull().references(() => profiles.id),
});

export const problemReports = pgTable("problem_reports", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").notNull().references(() => profiles.id, { onDelete: "cascade" }),
  problemId: uuid("problem_id").notNull().references(() => problems.id),
  note: text("note"),
  status: text("status").notNull().default("open"), // open | resolved
  reportedAt: timestamp("reported_at").notNull().defaultNow(),
});

export const problemReviews = pgTable("problem_reviews", {
  id: uuid("id").primaryKey().defaultRandom(),
  problemId: uuid("problem_id").notNull().references(() => problems.id),
  stage: text("stage").notNull(), // "sympy" | "persona"
  personaName: text("persona_name"),
  verdict: text("verdict").notNull(), // "pass" | "fail"
  reason: text("reason"),
  reviewedAt: timestamp("reviewed_at").notNull().defaultNow(),
});
```

- [ ] **Step 5: DB 클라이언트 엔트리 생성**

Create `packages/db/src/index.ts`:
```typescript
import postgres from "postgres";
import { drizzle } from "drizzle-orm/postgres-js";
import * as schema from "./schema";

const connectionString = process.env.DATABASE_URL;
if (!connectionString) throw new Error("DATABASE_URL is not set");

const queryClient = postgres(connectionString, { prepare: false });
export const db = drizzle(queryClient, { schema });
export * from "./schema";
export { schema };
```

- [ ] **Step 6: 의존성 설치 후 커밋**

```bash
pnpm install
git add packages/db
git commit -m "feat(db): add Drizzle schema for MVP tables"
```

---

## Task 5: DB 마이그레이션 생성 및 Supabase에 적용

**Files:**
- Create: `.env` (gitignored)
- Create: `packages/db/migrations/` (drizzle-kit 자동생성)

- [ ] **Step 1: .env 파일 생성 (루트)**

Create `.env` (이 파일은 gitignored):
```
NEXT_PUBLIC_SUPABASE_URL=https://YOUR-PROJECT-REF.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=YOUR_ANON_KEY
SUPABASE_SERVICE_ROLE_KEY=YOUR_SERVICE_ROLE_KEY
DATABASE_URL=postgresql://postgres.YOUR-REF:[YOUR-PASSWORD]@aws-0-ap-northeast-2.pooler.supabase.com:5432/postgres
```

> **중요**: Supabase 대시보드 → Project Settings → Database → Connection String(Session Pooler) 복사해서 넣기. `[YOUR-PASSWORD]`는 실제 DB 비밀번호.

- [ ] **Step 2: packages/db에도 .env 심볼릭 링크 또는 복사**

Run:
```bash
cp .env packages/db/.env
```

- [ ] **Step 3: 마이그레이션 파일 생성**

Run:
```bash
pnpm db:generate
```
Expected: `packages/db/migrations/0000_xxxxx.sql` 파일 생성됨.

- [ ] **Step 4: 마이그레이션 DB에 적용**

Run:
```bash
pnpm db:migrate
```
Expected: "Migrations applied" 메시지. Supabase 대시보드 Table Editor에서 생성된 테이블 확인.

- [ ] **Step 5: 커밋**

```bash
git add packages/db/migrations
git commit -m "feat(db): generate and apply initial migration"
```

---

## Task 6: Supabase Auth 클라이언트 셋업

**Files:**
- Create: `apps/web/lib/supabase/client.ts`
- Create: `apps/web/lib/supabase/server.ts`
- Create: `apps/web/lib/supabase/middleware.ts`
- Create: `apps/web/middleware.ts`
- Modify: `apps/web/package.json`

- [ ] **Step 1: Supabase 의존성 설치**

Run from `apps/web`:
```bash
cd apps/web
pnpm add @supabase/ssr@0.5.1 @supabase/supabase-js@2.45.4
cd ../..
```

- [ ] **Step 2: 브라우저 클라이언트 생성**

Create `apps/web/lib/supabase/client.ts`:
```typescript
import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  return createBrowserClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
  );
}
```

- [ ] **Step 3: 서버 클라이언트 생성**

Create `apps/web/lib/supabase/server.ts`:
```typescript
import { createServerClient } from "@supabase/ssr";
import { cookies } from "next/headers";

export function createClient() {
  const cookieStore = cookies();
  return createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return cookieStore.getAll();
        },
        setAll(cookiesToSet) {
          try {
            cookiesToSet.forEach(({ name, value, options }) =>
              cookieStore.set(name, value, options),
            );
          } catch {
            // Called from Server Component: safe to ignore
          }
        },
      },
    },
  );
}
```

- [ ] **Step 4: 미들웨어 헬퍼 생성**

Create `apps/web/lib/supabase/middleware.ts`:
```typescript
import { createServerClient } from "@supabase/ssr";
import { NextResponse, type NextRequest } from "next/server";

export async function updateSession(request: NextRequest) {
  let supabaseResponse = NextResponse.next({ request });

  const supabase = createServerClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,
    {
      cookies: {
        getAll() {
          return request.cookies.getAll();
        },
        setAll(cookiesToSet) {
          cookiesToSet.forEach(({ name, value }) =>
            request.cookies.set(name, value),
          );
          supabaseResponse = NextResponse.next({ request });
          cookiesToSet.forEach(({ name, value, options }) =>
            supabaseResponse.cookies.set(name, value, options),
          );
        },
      },
    },
  );

  const { data: { user } } = await supabase.auth.getUser();

  const protectedPaths = ["/home", "/session", "/dashboard"];
  const isProtected = protectedPaths.some((p) => request.nextUrl.pathname.startsWith(p));

  if (isProtected && !user) {
    const url = request.nextUrl.clone();
    url.pathname = "/login";
    return NextResponse.redirect(url);
  }

  return supabaseResponse;
}
```

- [ ] **Step 5: Next.js middleware 파일 생성**

Create `apps/web/middleware.ts`:
```typescript
import { type NextRequest } from "next/server";
import { updateSession } from "@/lib/supabase/middleware";

export async function middleware(request: NextRequest) {
  return await updateSession(request);
}

export const config = {
  matcher: [
    "/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)",
  ],
};
```

- [ ] **Step 6: 커밋**

```bash
git add apps/web
git commit -m "feat(auth): add Supabase SSR client and auth middleware"
```

---

## Task 7: 로그인 페이지

**Files:**
- Create: `apps/web/app/login/page.tsx`
- Create: `apps/web/app/login/login-form.tsx`
- Create: `apps/web/app/login/actions.ts`

- [ ] **Step 1: 로그인 Server Action 생성**

Create `apps/web/app/login/actions.ts`:
```typescript
"use server";

import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

export async function login(formData: FormData) {
  const supabase = createClient();
  const email = formData.get("email") as string;
  const password = formData.get("password") as string;

  const { error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) {
    return { error: error.message };
  }
  redirect("/home");
}
```

- [ ] **Step 2: 로그인 폼 클라이언트 컴포넌트**

Create `apps/web/app/login/login-form.tsx`:
```tsx
"use client";

import { useState } from "react";
import { login } from "./actions";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function LoginForm() {
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  async function handleSubmit(formData: FormData) {
    setPending(true);
    setError(null);
    const result = await login(formData);
    if (result?.error) {
      setError(result.error);
      setPending(false);
    }
  }

  return (
    <form action={handleSubmit} className="space-y-4 max-w-sm w-full">
      <div className="space-y-2">
        <Label htmlFor="email">이메일</Label>
        <Input id="email" name="email" type="email" required autoComplete="email" />
      </div>
      <div className="space-y-2">
        <Label htmlFor="password">비밀번호</Label>
        <Input id="password" name="password" type="password" required autoComplete="current-password" />
      </div>
      {error && <p className="text-sm text-destructive">{error}</p>}
      <Button type="submit" className="w-full" disabled={pending}>
        {pending ? "로그인 중..." : "로그인"}
      </Button>
    </form>
  );
}
```

- [ ] **Step 3: 로그인 페이지**

Create `apps/web/app/login/page.tsx`:
```tsx
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
```

- [ ] **Step 4: 로컬 dev 서버로 로그인 페이지 확인**

Run `pnpm dev`, `http://localhost:3000/login` 접속 → 폼 렌더링 확인. Stop.

- [ ] **Step 5: 커밋**

```bash
git add apps/web/app/login
git commit -m "feat(auth): add login page with email/password form"
```

---

## Task 8: 시드 데이터 스크립트 (3 concepts + 5 problems)

**Files:**
- Create: `packages/db/src/seed.ts`

- [ ] **Step 1: 시드 스크립트 작성**

Create `packages/db/src/seed.ts`:
```typescript
import "dotenv/config";
import { db, schema } from "./index";
import { eq } from "drizzle-orm";

async function seed() {
  console.log("🌱 Seeding database...");

  // SUBJECT → GRADE → UNIT → SUB_UNIT
  const [subject] = await db.insert(schema.subjects).values({ name: "수학" })
    .onConflictDoNothing().returning();
  const actualSubject = subject ??
    (await db.select().from(schema.subjects).where(eq(schema.subjects.name, "수학")))[0];

  const [grade] = await db.insert(schema.grades).values({
    subjectId: actualSubject.id, name: "중1", order: 1,
  }).returning();

  const [unit] = await db.insert(schema.units).values({
    gradeId: grade.id, name: "수와 연산", order: 1,
  }).returning();

  const [subUnit] = await db.insert(schema.subUnits).values({
    unitId: unit.id, name: "정수와 유리수", order: 1,
  }).returning();

  // CONCEPTS (3개)
  const conceptRows = await db.insert(schema.concepts).values([
    { subUnitId: subUnit.id, name: "자연수", description: "1, 2, 3, ... 양의 정수", order: 1 },
    { subUnitId: subUnit.id, name: "정수", description: "..., -2, -1, 0, 1, 2, ...", order: 2 },
    { subUnitId: subUnit.id, name: "수의 범위", description: "'~보다 크고 ~보다 작은' 형태", order: 3 },
  ]).returning();

  const [자연수, 정수, 수의범위] = conceptRows;
  console.log(`  ✓ ${conceptRows.length} concepts inserted`);

  // PROBLEMS (5개, Lv1)
  const problemRows = await db.insert(schema.problems).values([
    {
      conceptPrimaryId: 자연수.id, difficulty: 1,
      body: "1부터 10까지의 자연수 중 5보다 큰 수는 몇 개입니까?",
      answer: "5",
      status: "published", sympyVerified: true,
    },
    {
      conceptPrimaryId: 정수.id, difficulty: 1,
      body: "다음 중 정수가 아닌 것은? ① -3 ② 0 ③ 1/2 ④ 7",
      answer: "3",
      status: "published", sympyVerified: true,
    },
    {
      conceptPrimaryId: 수의범위.id, difficulty: 1,
      body: "2보다 크고 7보다 작은 자연수의 개수는?",
      answer: "4",
      status: "published", sympyVerified: true,
    },
    {
      conceptPrimaryId: 자연수.id, difficulty: 1,
      body: "0은 자연수입니까? (예/아니오)",
      answer: "아니오",
      status: "published", sympyVerified: true,
    },
    {
      conceptPrimaryId: 정수.id, difficulty: 1,
      body: "-5와 3 사이의 정수는 모두 몇 개입니까? (양 끝 포함 안 함)",
      answer: "7",
      status: "published", sympyVerified: true,
    },
  ]).returning();

  console.log(`  ✓ ${problemRows.length} problems inserted`);

  // problem_concepts (다중 태깅)
  await db.insert(schema.problemConcepts).values([
    { problemId: problemRows[0].id, conceptId: 자연수.id },
    { problemId: problemRows[0].id, conceptId: 수의범위.id },
    { problemId: problemRows[1].id, conceptId: 정수.id },
    { problemId: problemRows[2].id, conceptId: 자연수.id },
    { problemId: problemRows[2].id, conceptId: 수의범위.id },
    { problemId: problemRows[3].id, conceptId: 자연수.id },
    { problemId: problemRows[4].id, conceptId: 정수.id },
    { problemId: problemRows[4].id, conceptId: 수의범위.id },
  ]);

  // WEBTOON SCRIPTS (간단한 대화체)
  await db.insert(schema.webtoonScripts).values([
    {
      problemId: problemRows[0].id,
      script: [
        { type: "scene", text: "수지가 문제를 보며 고민 중" },
        { speaker: "수지", text: "자연수가 뭐더라... 1부터 시작하는 거 맞지?" },
        { speaker: "AI튜터", text: "맞아. 1, 2, 3, ... 이렇게 가는 수야. 0이나 음수는 아니야." },
        { speaker: "AI튜터", text: "그리고 '5보다 큰'은 범위 시그널. 6부터 세면 돼." },
      ],
    },
    {
      problemId: problemRows[1].id,
      script: [
        { speaker: "수지", text: "정수? 음수도 정수라 했지?" },
        { speaker: "AI튜터", text: "맞아. ..., -3, -2, -1, 0, 1, 2, 3, ...이 정수야." },
        { speaker: "AI튜터", text: "1/2처럼 **분수 형태**는 정수가 아니야. 유리수지." },
      ],
    },
    {
      problemId: problemRows[2].id,
      script: [
        { speaker: "AI튜터", text: "'~보다 크고 ~보다 작은'은 범위 표현 시그널이야." },
        { speaker: "AI튜터", text: "2보다 크니까 3부터, 7보다 작으니까 6까지. 3,4,5,6 = 4개." },
      ],
    },
    {
      problemId: problemRows[3].id,
      script: [
        { speaker: "AI튜터", text: "자연수는 '물건 개수 셀 때' 쓰는 수야. 1부터 시작." },
        { speaker: "AI튜터", text: "0은 '없음'이라서 자연수가 아니야." },
      ],
    },
    {
      problemId: problemRows[4].id,
      script: [
        { speaker: "AI튜터", text: "-5와 3 사이, 양 끝 포함 안 함 → -4, -3, -2, -1, 0, 1, 2" },
        { speaker: "AI튜터", text: "세어보면 7개." },
      ],
    },
  ]);

  console.log("✅ Seed complete");
  process.exit(0);
}

seed().catch((e) => {
  console.error(e);
  process.exit(1);
});
```

- [ ] **Step 2: 시드 실행**

Run:
```bash
pnpm db:seed
```
Expected: `✅ Seed complete`. Supabase 대시보드에서 concepts/problems 테이블 확인.

- [ ] **Step 3: 커밋**

```bash
git add packages/db/src/seed.ts
git commit -m "feat(db): add seed script with 3 concepts and 5 problems"
```

---

## Task 9: 수지/아빠 계정 수동 생성 + 프로필 RLS

**Files:**
- Create: `packages/db/migrations/custom/rls.sql`
- Create: `packages/db/src/rls-setup.md`

- [ ] **Step 1: RLS 정책 SQL 파일 생성**

Create `packages/db/migrations/custom/rls.sql`:
```sql
-- Enable RLS on all tables
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE concept_mastery ENABLE ROW LEVEL SECURITY;
ALTER TABLE rewards ENABLE ROW LEVEL SECURITY;
ALTER TABLE problem_reports ENABLE ROW LEVEL SECURITY;

ALTER TABLE subjects ENABLE ROW LEVEL SECURITY;
ALTER TABLE grades ENABLE ROW LEVEL SECURITY;
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE sub_units ENABLE ROW LEVEL SECURITY;
ALTER TABLE concepts ENABLE ROW LEVEL SECURITY;
ALTER TABLE problems ENABLE ROW LEVEL SECURITY;
ALTER TABLE problem_concepts ENABLE ROW LEVEL SECURITY;
ALTER TABLE solutions ENABLE ROW LEVEL SECURITY;
ALTER TABLE webtoon_scripts ENABLE ROW LEVEL SECURITY;
ALTER TABLE problem_reviews ENABLE ROW LEVEL SECURITY;

-- Profiles: users can read/update own profile; admin can read all
CREATE POLICY "profiles_self_read" ON profiles FOR SELECT
  USING (auth.uid() = id);
CREATE POLICY "profiles_self_update" ON profiles FOR UPDATE
  USING (auth.uid() = id);
CREATE POLICY "profiles_admin_read_all" ON profiles FOR SELECT
  USING (EXISTS(SELECT 1 FROM profiles p WHERE p.id = auth.uid() AND p.role = 'admin'));
CREATE POLICY "profiles_self_insert" ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Sessions: students see own; admin sees all
CREATE POLICY "sessions_own" ON sessions FOR ALL
  USING (auth.uid() = user_id);
CREATE POLICY "sessions_admin_read" ON sessions FOR SELECT
  USING (EXISTS(SELECT 1 FROM profiles p WHERE p.id = auth.uid() AND p.role = 'admin'));

-- Attempts: students see own; admin sees all
CREATE POLICY "attempts_own" ON attempts FOR ALL
  USING (auth.uid() = user_id);
CREATE POLICY "attempts_admin_read" ON attempts FOR SELECT
  USING (EXISTS(SELECT 1 FROM profiles p WHERE p.id = auth.uid() AND p.role = 'admin'));

-- Concept mastery: students see own; admin sees all
CREATE POLICY "concept_mastery_own" ON concept_mastery FOR ALL
  USING (auth.uid() = user_id);
CREATE POLICY "concept_mastery_admin_read" ON concept_mastery FOR SELECT
  USING (EXISTS(SELECT 1 FROM profiles p WHERE p.id = auth.uid() AND p.role = 'admin'));

-- Rewards: students read own; admin writes
CREATE POLICY "rewards_own_read" ON rewards FOR SELECT
  USING (auth.uid() = user_id);
CREATE POLICY "rewards_admin_insert" ON rewards FOR INSERT
  WITH CHECK (EXISTS(SELECT 1 FROM profiles p WHERE p.id = auth.uid() AND p.role = 'admin'));

-- Problem reports: students create/read own; admin reads all
CREATE POLICY "problem_reports_own" ON problem_reports FOR ALL
  USING (auth.uid() = user_id);
CREATE POLICY "problem_reports_admin_read" ON problem_reports FOR SELECT
  USING (EXISTS(SELECT 1 FROM profiles p WHERE p.id = auth.uid() AND p.role = 'admin'));

-- Content tables: everyone authenticated can read published; admin writes
CREATE POLICY "content_read_all" ON subjects FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "content_read_all" ON grades FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "content_read_all" ON units FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "content_read_all" ON sub_units FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "content_read_all" ON concepts FOR SELECT USING (auth.role() = 'authenticated');

CREATE POLICY "problems_read_published" ON problems FOR SELECT
  USING (auth.role() = 'authenticated' AND status = 'published');
CREATE POLICY "problem_concepts_read" ON problem_concepts FOR SELECT
  USING (auth.role() = 'authenticated');
CREATE POLICY "webtoon_scripts_read" ON webtoon_scripts FOR SELECT
  USING (auth.role() = 'authenticated');
CREATE POLICY "solutions_read" ON solutions FOR SELECT
  USING (auth.role() = 'authenticated');

-- Admin can write content
CREATE POLICY "admin_write_problems" ON problems FOR ALL
  USING (EXISTS(SELECT 1 FROM profiles p WHERE p.id = auth.uid() AND p.role = 'admin'));
CREATE POLICY "admin_write_concepts" ON concepts FOR ALL
  USING (EXISTS(SELECT 1 FROM profiles p WHERE p.id = auth.uid() AND p.role = 'admin'));
```

- [ ] **Step 2: RLS SQL을 Supabase SQL Editor에서 실행**

Supabase 대시보드 → SQL Editor → 위 SQL 전체 붙여넣기 → Run.
Expected: "Success. No rows returned".

- [ ] **Step 3: 수동 계정 생성 안내서 작성**

Create `packages/db/src/rls-setup.md`:
```markdown
# 초기 계정 설정 가이드

## 1. Supabase Auth 에서 계정 2개 생성
Supabase 대시보드 → Authentication → Users → "Add user" → "Create new user"
1. 아빠 계정: admin@suji.local, 비밀번호 설정
2. 수지 계정: suji@suji.local, 비밀번호 설정

## 2. profiles 테이블에 role 설정
SQL Editor에서:
\`\`\`sql
-- 아빠를 admin으로
INSERT INTO profiles (id, role, nickname)
SELECT id, 'admin', '아빠'
FROM auth.users WHERE email = 'admin@suji.local';

-- 수지를 student로
INSERT INTO profiles (id, role, nickname)
SELECT id, 'student', '수지'
FROM auth.users WHERE email = 'suji@suji.local';
\`\`\`

## 3. 초기 비밀번호 전달 후 수지가 로그인 → 비번 변경 유도
```

- [ ] **Step 4: 계정 생성 실제 수행**

위 `rls-setup.md` 따라 Supabase 대시보드에서:
1. Authentication → Add user → 2개 생성
2. SQL Editor에서 profiles INSERT 2개 실행

- [ ] **Step 5: 커밋**

```bash
git add packages/db/migrations/custom packages/db/src/rls-setup.md
git commit -m "feat(db): add RLS policies and initial account setup guide"
```

---

## Task 10: 학생 home 페이지 (읽기 전용)

**Files:**
- Create: `apps/web/app/(student)/layout.tsx`
- Create: `apps/web/app/(student)/home/page.tsx`
- Modify: `apps/web/package.json` (add @suji/db)

- [ ] **Step 1: apps/web에서 @suji/db 의존성 추가**

Modify `apps/web/package.json` → `dependencies`에 추가:
```json
"@suji/db": "workspace:*",
"drizzle-orm": "0.34.0",
"postgres": "3.4.4"
```

Run:
```bash
pnpm install
```

- [ ] **Step 2: 학생 레이아웃 (역할 확인)**

Create `apps/web/app/(student)/layout.tsx`:
```tsx
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

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
    <div className="min-h-screen bg-background">
      <header className="border-b px-4 py-3">
        <h1 className="text-sm text-muted-foreground">수지의 수학 학습</h1>
      </header>
      <main className="p-4 max-w-md mx-auto">{children}</main>
    </div>
  );
}
```

- [ ] **Step 3: 홈 페이지 작성**

Create `apps/web/app/(student)/home/page.tsx`:
```tsx
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
```

- [ ] **Step 4: 로컬에서 확인**

Run `pnpm dev`. `http://localhost:3000/login` → 수지 계정으로 로그인 → `/home` 리다이렉트 → 환영 카드 확인.

- [ ] **Step 5: 커밋**

```bash
git add apps/web
git commit -m "feat(student): add home page with greeting and start button"
```

---

## Task 11: 정답 판정 순수함수 (TDD)

**Files:**
- Create: `apps/web/lib/session/grading.ts`
- Create: `apps/web/lib/session/grading.test.ts`
- Modify: `apps/web/package.json` (vitest)

- [ ] **Step 1: vitest 설치**

Run from `apps/web`:
```bash
cd apps/web
pnpm add -D vitest@2.1.1 @vitest/ui@2.1.1
cd ../..
```

- [ ] **Step 2: 실패하는 테스트 작성**

Create `apps/web/lib/session/grading.test.ts`:
```typescript
import { describe, it, expect } from "vitest";
import { gradeConceptIdentification } from "./grading";

describe("gradeConceptIdentification", () => {
  it("returns correct=true when selected concepts match exactly", () => {
    const result = gradeConceptIdentification({
      selectedConceptIds: ["a", "b"],
      correctConceptIds: ["a", "b"],
    });
    expect(result.isCorrect).toBe(true);
  });

  it("returns correct=true regardless of order", () => {
    const result = gradeConceptIdentification({
      selectedConceptIds: ["b", "a"],
      correctConceptIds: ["a", "b"],
    });
    expect(result.isCorrect).toBe(true);
  });

  it("returns correct=false when selection missing a concept", () => {
    const result = gradeConceptIdentification({
      selectedConceptIds: ["a"],
      correctConceptIds: ["a", "b"],
    });
    expect(result.isCorrect).toBe(false);
  });

  it("returns correct=false when selection has extra concept", () => {
    const result = gradeConceptIdentification({
      selectedConceptIds: ["a", "b", "c"],
      correctConceptIds: ["a", "b"],
    });
    expect(result.isCorrect).toBe(false);
  });

  it("returns correct=false when selection is empty", () => {
    const result = gradeConceptIdentification({
      selectedConceptIds: [],
      correctConceptIds: ["a"],
    });
    expect(result.isCorrect).toBe(false);
  });
});
```

- [ ] **Step 3: 테스트 실행하여 실패 확인**

Run from `apps/web`:
```bash
cd apps/web
pnpm exec vitest run lib/session/grading.test.ts
cd ../..
```
Expected: FAIL with "Cannot find module './grading'"

- [ ] **Step 4: 최소 구현 작성**

Create `apps/web/lib/session/grading.ts`:
```typescript
export type GradingInput = {
  selectedConceptIds: string[];
  correctConceptIds: string[];
};

export type GradingResult = {
  isCorrect: boolean;
};

export function gradeConceptIdentification(input: GradingInput): GradingResult {
  const selected = new Set(input.selectedConceptIds);
  const correct = new Set(input.correctConceptIds);
  if (selected.size !== correct.size) return { isCorrect: false };
  for (const id of correct) {
    if (!selected.has(id)) return { isCorrect: false };
  }
  return { isCorrect: true };
}
```

- [ ] **Step 5: 테스트 통과 확인**

Run from `apps/web`:
```bash
cd apps/web
pnpm exec vitest run lib/session/grading.test.ts
cd ../..
```
Expected: PASS (5 tests passing).

- [ ] **Step 6: 커밋**

```bash
git add apps/web
git commit -m "feat(session): add concept identification grading logic with tests"
```

---

## Task 12: 세션 시작 API + 세션 진행 페이지

**Files:**
- Create: `apps/web/app/api/session/start/route.ts`
- Create: `apps/web/app/(student)/session/page.tsx`
- Create: `apps/web/app/(student)/session/[sessionId]/page.tsx`

- [ ] **Step 1: 세션 시작 API Route**

Create `apps/web/app/api/session/start/route.ts`:
```typescript
import { createClient } from "@/lib/supabase/server";
import { NextResponse } from "next/server";

export async function POST() {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const { data: session, error } = await supabase
    .from("sessions")
    .insert({ user_id: user.id, mode: "daily" })
    .select("id")
    .single();

  if (error || !session) {
    return NextResponse.json({ error: error?.message ?? "insert failed" }, { status: 500 });
  }

  return NextResponse.json({ sessionId: session.id });
}
```

- [ ] **Step 2: /session 페이지 (세션 생성 + 리다이렉트)**

Create `apps/web/app/(student)/session/page.tsx`:
```tsx
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
```

- [ ] **Step 3: 세션 진행 페이지 (서버 컴포넌트, 문제 5개 로드)**

Create `apps/web/app/(student)/session/[sessionId]/page.tsx`:
```tsx
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";
import { SessionRunner } from "./session-runner";

export default async function SessionPage({
  params,
}: {
  params: { sessionId: string };
}) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  // Load 5 published problems + their correct concepts + all concepts for multiselect
  const { data: problems } = await supabase
    .from("problems")
    .select(`
      id, body, difficulty,
      problem_concepts(concept_id)
    `)
    .eq("status", "published")
    .limit(5);

  const { data: allConcepts } = await supabase
    .from("concepts")
    .select("id, name");

  if (!problems || problems.length === 0 || !allConcepts) {
    return <p className="text-sm text-muted-foreground">문제가 준비되지 않았어요.</p>;
  }

  const problemsWithConcepts = problems.map((p) => ({
    id: p.id,
    body: p.body,
    difficulty: p.difficulty,
    correctConceptIds: (p.problem_concepts ?? []).map((pc: { concept_id: string }) => pc.concept_id),
  }));

  return (
    <SessionRunner
      sessionId={params.sessionId}
      problems={problemsWithConcepts}
      allConcepts={allConcepts}
    />
  );
}
```

- [ ] **Step 4: 커밋 (세션 진행 runner는 다음 태스크)**

```bash
git add apps/web/app/api apps/web/app/\(student\)/session
git commit -m "feat(session): add session start API and problem loading"
```

---

## Task 13: 세션 진행 클라이언트 컴포넌트 (문제 풀이 UX)

**Files:**
- Create: `apps/web/app/(student)/session/[sessionId]/session-runner.tsx`
- Create: `apps/web/components/problem-card.tsx`
- Create: `apps/web/components/concept-multiselect.tsx`
- Create: `apps/web/components/feedback-panel.tsx`

- [ ] **Step 1: 문제 카드 컴포넌트**

Create `apps/web/components/problem-card.tsx`:
```tsx
import { Card, CardContent } from "@/components/ui/card";

export function ProblemCard({
  body,
  index,
  total,
}: { body: string; index: number; total: number }) {
  return (
    <Card>
      <CardContent className="p-6 space-y-4">
        <p className="text-xs text-muted-foreground">문제 {index + 1}/{total}</p>
        <p className="text-base leading-relaxed">{body}</p>
      </CardContent>
    </Card>
  );
}
```

- [ ] **Step 2: 개념 멀티셀렉트 컴포넌트**

Create `apps/web/components/concept-multiselect.tsx`:
```tsx
"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

export function ConceptMultiselect({
  concepts,
  selectedIds,
  onChange,
  disabled,
}: {
  concepts: { id: string; name: string }[];
  selectedIds: string[];
  onChange: (ids: string[]) => void;
  disabled?: boolean;
}) {
  function toggle(id: string) {
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((x) => x !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  }

  return (
    <div className="space-y-3">
      <p className="text-sm font-medium">💡 이 문제는 어떤 개념?</p>
      <div className="space-y-2">
        {concepts.map((c) => (
          <div key={c.id} className="flex items-center space-x-3 py-1">
            <Checkbox
              id={`concept-${c.id}`}
              checked={selectedIds.includes(c.id)}
              onCheckedChange={() => toggle(c.id)}
              disabled={disabled}
            />
            <Label htmlFor={`concept-${c.id}`} className="cursor-pointer text-base">
              {c.name}
            </Label>
          </div>
        ))}
      </div>
    </div>
  );
}
```

- [ ] **Step 3: 피드백 패널 컴포넌트**

Create `apps/web/components/feedback-panel.tsx`:
```tsx
import { Card, CardContent } from "@/components/ui/card";

type WebtoonLine =
  | { type: "scene"; text: string }
  | { speaker: string; text: string };

export function FeedbackPanel({
  isCorrect,
  selectedNames,
  correctNames,
  webtoonScript,
}: {
  isCorrect: boolean;
  selectedNames: string[];
  correctNames: string[];
  webtoonScript: WebtoonLine[] | null;
}) {
  return (
    <div className="space-y-4">
      <div
        className={`text-center p-4 rounded-lg ${
          isCorrect ? "bg-green-50 text-green-900" : "bg-amber-50 text-amber-900"
        }`}
      >
        <p className="text-lg font-bold">
          {isCorrect ? "✅ 맞았어!" : "❌ 아쉬워, 다시 볼까?"}
        </p>
        {!isCorrect && (
          <p className="text-sm mt-2">
            네가 고른: {selectedNames.join(", ") || "없음"}<br />
            정답: {correctNames.join(", ")}
          </p>
        )}
        {isCorrect && (
          <p className="text-sm mt-2">개념: {correctNames.join(", ")}</p>
        )}
      </div>

      {webtoonScript && webtoonScript.length > 0 && (
        <Card>
          <CardContent className="p-4 space-y-3">
            <p className="text-sm font-medium">📖 웹툰 설명</p>
            {webtoonScript.map((line, i) => (
              <div key={i} className="text-sm">
                {"type" in line ? (
                  <p className="italic text-muted-foreground">[{line.text}]</p>
                ) : (
                  <p>
                    <span className="font-semibold">{line.speaker}: </span>
                    {line.text}
                  </p>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
```

- [ ] **Step 4: 세션 Runner 클라이언트 컴포넌트**

Create `apps/web/app/(student)/session/[sessionId]/session-runner.tsx`:
```tsx
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { Button } from "@/components/ui/button";
import { ProblemCard } from "@/components/problem-card";
import { ConceptMultiselect } from "@/components/concept-multiselect";
import { FeedbackPanel } from "@/components/feedback-panel";

type Problem = {
  id: string;
  body: string;
  difficulty: number;
  correctConceptIds: string[];
};

type Concept = { id: string; name: string };

type SubmitResult = {
  isCorrect: boolean;
  webtoonScript: unknown;
};

export function SessionRunner({
  sessionId,
  problems,
  allConcepts,
}: {
  sessionId: string;
  problems: Problem[];
  allConcepts: Concept[];
}) {
  const router = useRouter();
  const [index, setIndex] = useState(0);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [startTime, setStartTime] = useState<number>(Date.now());
  const [feedback, setFeedback] = useState<SubmitResult | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const current = problems[index];

  async function handleSubmit() {
    setSubmitting(true);
    const timeMs = Date.now() - startTime;
    const res = await fetch(`/api/session/${sessionId}/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        problemId: current.id,
        selectedConceptIds: selectedIds,
        timeMs,
      }),
    });
    const result: SubmitResult = await res.json();
    setFeedback(result);
    setSubmitting(false);
  }

  function handleNext() {
    if (index + 1 >= problems.length) {
      router.push(`/session/${sessionId}/complete`);
      return;
    }
    setIndex(index + 1);
    setSelectedIds([]);
    setStartTime(Date.now());
    setFeedback(null);
  }

  if (feedback) {
    const correctNames = current.correctConceptIds
      .map((id) => allConcepts.find((c) => c.id === id)?.name)
      .filter(Boolean) as string[];
    const selectedNames = selectedIds
      .map((id) => allConcepts.find((c) => c.id === id)?.name)
      .filter(Boolean) as string[];

    return (
      <div className="space-y-6">
        <FeedbackPanel
          isCorrect={feedback.isCorrect}
          selectedNames={selectedNames}
          correctNames={correctNames}
          webtoonScript={feedback.webtoonScript as never}
        />
        <Button onClick={handleNext} className="w-full" size="lg">
          {index + 1 >= problems.length ? "세션 완료" : "다음 문제"}
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <ProblemCard body={current.body} index={index} total={problems.length} />
      <ConceptMultiselect
        concepts={allConcepts}
        selectedIds={selectedIds}
        onChange={setSelectedIds}
      />
      <Button
        onClick={handleSubmit}
        disabled={selectedIds.length === 0 || submitting}
        className="w-full"
        size="lg"
      >
        {submitting ? "제출 중..." : "제출"}
      </Button>
    </div>
  );
}
```

- [ ] **Step 5: 커밋**

```bash
git add apps/web/app/\(student\)/session apps/web/components
git commit -m "feat(session): add problem solving UI components and runner"
```

---

## Task 14: 답안 제출 API (채점 + attempts 기록 + 웹툰 조회)

**Files:**
- Create: `apps/web/app/api/session/[id]/submit/route.ts`

- [ ] **Step 1: 제출 API Route**

Create `apps/web/app/api/session/[id]/submit/route.ts`:
```typescript
import { createClient } from "@/lib/supabase/server";
import { NextResponse } from "next/server";
import { gradeConceptIdentification } from "@/lib/session/grading";

export async function POST(
  request: Request,
  { params }: { params: { id: string } },
) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) return NextResponse.json({ error: "unauthorized" }, { status: 401 });

  const body = await request.json();
  const { problemId, selectedConceptIds, timeMs } = body as {
    problemId: string;
    selectedConceptIds: string[];
    timeMs: number;
  };

  // Load correct concept IDs
  const { data: pcRows, error: pcError } = await supabase
    .from("problem_concepts")
    .select("concept_id")
    .eq("problem_id", problemId);

  if (pcError || !pcRows) {
    return NextResponse.json({ error: "problem not found" }, { status: 404 });
  }

  const correctConceptIds = pcRows.map((r) => r.concept_id);
  const { isCorrect } = gradeConceptIdentification({
    selectedConceptIds,
    correctConceptIds,
  });

  // Record attempt
  const { error: attemptError } = await supabase.from("attempts").insert({
    session_id: params.id,
    user_id: user.id,
    problem_id: problemId,
    selected_concepts: selectedConceptIds,
    is_correct: isCorrect,
    time_ms: timeMs,
  });
  if (attemptError) {
    return NextResponse.json({ error: attemptError.message }, { status: 500 });
  }

  // Load webtoon script
  const { data: webtoon } = await supabase
    .from("webtoon_scripts")
    .select("script")
    .eq("problem_id", problemId)
    .single();

  return NextResponse.json({
    isCorrect,
    webtoonScript: webtoon?.script ?? null,
  });
}
```

- [ ] **Step 2: 커밋**

```bash
git add apps/web/app/api/session
git commit -m "feat(session): add answer submission API with grading and attempt record"
```

---

## Task 15: 세션 완료 페이지

**Files:**
- Create: `apps/web/app/(student)/session/[sessionId]/complete/page.tsx`

- [ ] **Step 1: 세션 완료 페이지 (요약 조회)**

Create `apps/web/app/(student)/session/[sessionId]/complete/page.tsx`:
```tsx
import { createClient } from "@/lib/supabase/server";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import Link from "next/link";

export default async function SessionCompletePage({
  params,
}: {
  params: { sessionId: string };
}) {
  const supabase = createClient();

  // Mark session ended
  await supabase
    .from("sessions")
    .update({ ended_at: new Date().toISOString() })
    .eq("id", params.sessionId);

  // Load attempts for this session
  const { data: attempts } = await supabase
    .from("attempts")
    .select("is_correct, time_ms")
    .eq("session_id", params.sessionId);

  const total = attempts?.length ?? 0;
  const correct = attempts?.filter((a) => a.is_correct).length ?? 0;
  const totalTimeSec = Math.round(
    (attempts ?? []).reduce((s, a) => s + (a.time_ms ?? 0), 0) / 1000,
  );

  return (
    <div className="space-y-6 text-center py-8">
      <h1 className="text-2xl font-bold">🎉 오늘 미션 완료!</h1>
      <Card>
        <CardContent className="p-6 space-y-3">
          <p className="text-lg">정답: {correct}/{total}</p>
          <p className="text-sm text-muted-foreground">
            시간: {Math.floor(totalTimeSec / 60)}분 {totalTimeSec % 60}초
          </p>
        </CardContent>
      </Card>
      <Button asChild size="lg" className="w-full">
        <Link href="/home">홈으로</Link>
      </Button>
    </div>
  );
}
```

- [ ] **Step 2: 로컬 전체 흐름 확인**

Run `pnpm dev`:
1. `/login` 수지 로그인
2. `/home` → "시작하기" 클릭
3. 문제 5개 풀이 → 각 제출 → 피드백 → 다음
4. 5번째 문제 후 "세션 완료" → `/session/[id]/complete` 확인
5. "홈으로" → `/home`

- [ ] **Step 3: 커밋**

```bash
git add apps/web/app/\(student\)/session
git commit -m "feat(session): add completion page with session summary"
```

---

## Task 16: 관리자 대시보드 스텁

**Files:**
- Create: `apps/web/app/(admin)/layout.tsx`
- Create: `apps/web/app/(admin)/dashboard/page.tsx`

- [ ] **Step 1: 관리자 레이아웃 (role 체크)**

Create `apps/web/app/(admin)/layout.tsx`:
```tsx
import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

export default async function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const supabase = createClient();
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) redirect("/login");

  const { data: profile } = await supabase
    .from("profiles")
    .select("role")
    .eq("id", user.id)
    .single();

  if (!profile) redirect("/login");
  if (profile.role !== "admin") redirect("/home");

  return (
    <div className="min-h-screen bg-background">
      <header className="border-b px-4 py-3">
        <h1 className="text-sm text-muted-foreground">관리자</h1>
      </header>
      <main className="p-4 max-w-4xl mx-auto">{children}</main>
    </div>
  );
}
```

- [ ] **Step 2: 관리자 대시보드 스텁**

Create `apps/web/app/(admin)/dashboard/page.tsx`:
```tsx
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
```

- [ ] **Step 3: 로컬에서 확인**

`pnpm dev`, 아빠 계정 로그인 → `/dashboard` 접속 → 숫자 확인.

- [ ] **Step 4: 커밋**

```bash
git add apps/web/app/\(admin\)
git commit -m "feat(admin): add minimal admin dashboard stub"
```

---

## Task 17: Vercel 배포

**Files:**
- Modify: `apps/web/next.config.mjs` (if needed)
- Create: `vercel.json` (루트)

- [ ] **Step 1: vercel.json 생성 (monorepo 설정)**

Create `vercel.json`:
```json
{
  "buildCommand": "pnpm --filter web build",
  "installCommand": "pnpm install --frozen-lockfile",
  "framework": "nextjs",
  "outputDirectory": "apps/web/.next"
}
```

- [ ] **Step 2: Vercel 프로젝트 연결**

수동 작업:
1. https://vercel.com/new 접속
2. GitHub 저장소 import (claude-suji)
3. Framework Preset: Next.js
4. Root Directory: `./` (루트)
5. Environment Variables 추가:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `SUPABASE_SERVICE_ROLE_KEY`
   - `DATABASE_URL`

- [ ] **Step 3: 첫 배포**

Vercel 대시보드에서 "Deploy" 버튼 클릭. 빌드 로그 확인.

- [ ] **Step 4: 배포 URL 접속하여 end-to-end 확인**

`https://claude-suji-xxx.vercel.app/login` →
1. 수지 계정 로그인
2. 홈 → 시작하기 → 문제 5개 풀이 → 완료 페이지
3. 로그아웃 (브라우저 쿠키 삭제)
4. 아빠 계정 로그인 → `/dashboard` 통계 확인

- [ ] **Step 5: vercel.json 커밋**

```bash
git add vercel.json
git commit -m "chore: add Vercel deployment configuration"
git push origin main
```

---

## Task 18: 로그아웃 버튼 추가

**Files:**
- Modify: `apps/web/app/(student)/layout.tsx`
- Create: `apps/web/components/logout-button.tsx`
- Create: `apps/web/app/logout/actions.ts`

- [ ] **Step 1: 로그아웃 Server Action**

Create `apps/web/app/logout/actions.ts`:
```typescript
"use server";

import { createClient } from "@/lib/supabase/server";
import { redirect } from "next/navigation";

export async function logout() {
  const supabase = createClient();
  await supabase.auth.signOut();
  redirect("/login");
}
```

- [ ] **Step 2: 로그아웃 버튼 컴포넌트**

Create `apps/web/components/logout-button.tsx`:
```tsx
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
```

- [ ] **Step 3: 학생 레이아웃에 로그아웃 추가**

Modify `apps/web/app/(student)/layout.tsx`:
```tsx
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
    <div className="min-h-screen bg-background">
      <header className="border-b px-4 py-3 flex items-center justify-between">
        <h1 className="text-sm text-muted-foreground">수지의 수학 학습</h1>
        <LogoutButton />
      </header>
      <main className="p-4 max-w-md mx-auto">{children}</main>
    </div>
  );
}
```

- [ ] **Step 4: 관리자 레이아웃에도 추가**

Modify `apps/web/app/(admin)/layout.tsx` header 부분:
```tsx
      <header className="border-b px-4 py-3 flex items-center justify-between">
        <h1 className="text-sm text-muted-foreground">관리자</h1>
        <LogoutButton />
      </header>
```

Import 추가: `import { LogoutButton } from "@/components/logout-button";`

- [ ] **Step 5: 로컬 확인 + 배포**

```bash
pnpm dev  # 확인 후 Ctrl+C
git add apps/web
git commit -m "feat(auth): add logout button to student and admin layouts"
git push origin main
```

Vercel이 자동 재배포. 배포 URL에서 로그아웃 테스트.

---

## Self-Review 결과

**스펙 커버리지 체크** (spec vs plan):
- ✅ 로그인 (수지+아빠, role 분리): Task 6, 7, 9, 10, 16
- ✅ 수지 홈 화면: Task 10
- ✅ 세션 시작+진행+완료: Task 12, 13, 14, 15
- ✅ 개념 식별 UI (멀티셀렉트): Task 13
- ✅ 정답/오답 피드백 + 웹툰: Task 13, 14
- ✅ 관리자 대시보드 스텁: Task 16
- ✅ Supabase RLS: Task 9
- ✅ Drizzle 스키마 전체 테이블: Task 4
- ✅ 시드 데이터 3 concepts + 5 problems: Task 8
- ✅ Vercel 배포: Task 17
- ✅ 로그아웃: Task 18
- ⏭️ 콘텐츠 파이프라인: **Plan 2** (의도적 제외)
- ⏭️ 스티커/신고/CSV/숙달도 다운그레이드: **Plan 3** (의도적 제외)
- ⏭️ E2E 테스트 Playwright: Plan 3 (MVP는 수동 테스트로 충분)

**Placeholder 스캔**: 각 태스크는 완전한 코드 포함. TBD/TODO 없음.

**타입 일관성**: `GradingInput`, `GradingResult`, `Problem`, `Concept`, `WebtoonLine` 모두 일관.

---

**Plan 1 완료 시 결과물**:
수지가 Vercel URL에 로그인해서 시드 문제 5개로 개념 식별 훈련 세션을 완료할 수 있다. 모든 시도는 DB에 기록되며 아빠는 관리자 대시보드에서 통계 확인 가능.

**다음 단계**: Plan 2 (Content Pipeline)에서 실제 400개 문제를 LLM으로 생성.
