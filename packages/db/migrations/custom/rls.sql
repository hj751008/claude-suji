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

-- Helper: check admin role without RLS recursion
CREATE OR REPLACE FUNCTION is_admin()
RETURNS boolean AS $$
  SELECT EXISTS (
    SELECT 1 FROM profiles
    WHERE id = auth.uid() AND role = 'admin'
  );
$$ LANGUAGE sql SECURITY DEFINER;

-- Profiles: users can read/update own profile; admin can read all
CREATE POLICY "profiles_self_read" ON profiles FOR SELECT
  USING (auth.uid() = id);
CREATE POLICY "profiles_self_update" ON profiles FOR UPDATE
  USING (auth.uid() = id);
CREATE POLICY "profiles_admin_read_all" ON profiles FOR SELECT
  USING (is_admin());
CREATE POLICY "profiles_self_insert" ON profiles FOR INSERT
  WITH CHECK (auth.uid() = id);

-- Sessions: students see own; admin sees all
CREATE POLICY "sessions_own" ON sessions FOR ALL
  USING (auth.uid() = user_id);
CREATE POLICY "sessions_admin_read" ON sessions FOR SELECT
  USING (is_admin());

-- Attempts: students see own; admin sees all
CREATE POLICY "attempts_own" ON attempts FOR ALL
  USING (auth.uid() = user_id);
CREATE POLICY "attempts_admin_read" ON attempts FOR SELECT
  USING (is_admin());

-- Concept mastery: students see own; admin sees all
CREATE POLICY "concept_mastery_own" ON concept_mastery FOR ALL
  USING (auth.uid() = user_id);
CREATE POLICY "concept_mastery_admin_read" ON concept_mastery FOR SELECT
  USING (is_admin());

-- Rewards: students read own; admin writes
CREATE POLICY "rewards_own_read" ON rewards FOR SELECT
  USING (auth.uid() = user_id);
CREATE POLICY "rewards_admin_insert" ON rewards FOR INSERT
  WITH CHECK (is_admin());

-- Problem reports: students create/read own; admin reads all
CREATE POLICY "problem_reports_own" ON problem_reports FOR ALL
  USING (auth.uid() = user_id);
CREATE POLICY "problem_reports_admin_read" ON problem_reports FOR SELECT
  USING (is_admin());

-- Content tables: everyone authenticated can read published; admin writes
CREATE POLICY "content_read_subjects" ON subjects FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "content_read_grades" ON grades FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "content_read_units" ON units FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "content_read_sub_units" ON sub_units FOR SELECT USING (auth.role() = 'authenticated');
CREATE POLICY "content_read_concepts" ON concepts FOR SELECT USING (auth.role() = 'authenticated');

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
  USING (is_admin());
CREATE POLICY "admin_write_concepts" ON concepts FOR ALL
  USING (is_admin());
