# 초기 계정 설정 가이드

## 1. Supabase Auth 에서 계정 2개 생성
Supabase 대시보드 → Authentication → Users → "Add user" → "Create new user"
1. 아빠 계정: admin@suji.local, 비밀번호 설정
2. 수지 계정: suji@suji.local, 비밀번호 설정

## 2. profiles 테이블에 role 설정
SQL Editor에서:
```sql
-- 아빠를 admin으로
INSERT INTO profiles (id, role, nickname)
SELECT id, 'admin', '아빠'
FROM auth.users WHERE email = 'admin@suji.local';

-- 수지를 student로
INSERT INTO profiles (id, role, nickname)
SELECT id, 'student', '수지'
FROM auth.users WHERE email = 'suji@suji.local';
```

## 3. 초기 비밀번호 전달 후 수지가 로그인 → 비번 변경 유도
