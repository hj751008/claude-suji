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
  difficulty: integer("difficulty").notNull(),
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
  id: uuid("id").primaryKey(),
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
    selectedConcepts: jsonb("selected_concepts").notNull(),
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
    accuracyRecent10: integer("accuracy_recent_10").notNull().default(0),
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
  kind: text("kind").notNull(),
  content: text("content").notNull(),
  grantedAt: timestamp("granted_at").notNull().defaultNow(),
  grantedBy: uuid("granted_by").notNull().references(() => profiles.id),
});

export const problemReports = pgTable("problem_reports", {
  id: uuid("id").primaryKey().defaultRandom(),
  userId: uuid("user_id").notNull().references(() => profiles.id, { onDelete: "cascade" }),
  problemId: uuid("problem_id").notNull().references(() => problems.id),
  note: text("note"),
  status: text("status").notNull().default("open"),
  reportedAt: timestamp("reported_at").notNull().defaultNow(),
});

export const problemReviews = pgTable("problem_reviews", {
  id: uuid("id").primaryKey().defaultRandom(),
  problemId: uuid("problem_id").notNull().references(() => problems.id),
  stage: text("stage").notNull(),
  personaName: text("persona_name"),
  verdict: text("verdict").notNull(),
  reason: text("reason"),
  reviewedAt: timestamp("reviewed_at").notNull().defaultNow(),
});
