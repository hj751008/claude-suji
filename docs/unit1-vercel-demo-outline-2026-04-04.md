# Unit 1 Vercel Demo Outline (2026-04-04)

## Scope

- This document covers only:
  - landing page outline
  - component list
- It does not decide:
  - separate repo vs same repo
  - live remote tutoring exposure

## Route Plan

### `/`

- Purpose:
  - the main visible result page
  - explain what the project already does today
  - convert curiosity into `Unit 1` exploration
- Audience:
  - stakeholder
  - collaborator
  - pilot tutor
  - reviewer

### `/unit1`

- Purpose:
  - a focused Unit 1 detail page
  - explain concept scope, tutoring flow, and what the demo proves

### `/unit1/proof`

- Purpose:
  - show proof without turning the hero page into a developer console
  - document the current evidence and current limits honestly

## Landing Page Outline

### Section 1. Hero Poster

- Goal:
  - tell the user in one screen what is real today
- Content:
  - eyebrow: `Suji Math AI`
  - headline: `소인수분해를 실제 tutoring flow로 보여주는 Unit 1 데모`
  - support copy:
    - `문서만 정리한 프로젝트가 아니라, Unit 1에서 replay, handoff, next-step planning이 실제로 이어지는 결과를 보여준다.`
  - primary CTA:
    - `Unit 1 데모 보기`
  - secondary CTA:
    - `검증 근거 보기`
  - side proof chips:
    - `Unit 1 first`
    - `runtime-complete`
    - `pilot-compared`

### Section 2. What Is Real Today

- Goal:
  - replace vague claims with concrete capability statements
- Layout:
  - three proof blocks in one row on desktop
- Content blocks:
  - `Transcript Replay`
    - `검증된 Unit 1 흐름을 같은 구조로 다시 재생할 수 있다.`
  - `Blocker-First Handoff`
    - `완료 후 다음 세션이 보수적으로 다시 계획된다.`
  - `One-Turn Tutor Loop`
    - `한 번의 관찰 입력으로 다음 action이 실제로 바뀐다.`

### Section 3. Why Unit 1 First

- Goal:
  - explain scope discipline before the user asks
- Content:
  - `Unit 1은 현재 저장소에서 가장 강하게 검증된 slice다.`
  - `그래서 첫 결과물은 전체 커리큘럼이 아니라 Unit 1 tutoring loop다.`
  - concise bullets:
    - `runtime-complete`
    - `pilot-log comparison exists`
    - `operator demo already works`

### Section 4. Demo Path

- Goal:
  - show how the demo flows in practice
- Layout:
  - four ordered steps with short captions
- Steps:
  - `1. transcript replay`
  - `2. next guided session`
  - `3. one tutor turn`
  - `4. raw operator log capture`

### Section 5. Screenshot Or Proof Visual

- Goal:
  - make the project feel concrete, not conceptual
- Content:
  - one main screenshot from the current operator demo
  - caption:
    - `현재 내부 데모 표면은 Unit 1 흐름을 먼저 보여주도록 정리돼 있다.`
- Candidate asset:
  - `output/playwright/unit1-first-screen-v2.png`

### Section 6. Honest Limits

- Goal:
  - protect trust by naming what is not done yet
- Content:
  - `이 페이지는 전체 제품 출시를 의미하지 않는다.`
  - `현재는 Unit 1이 첫 결과물이다.`
  - `Unit 2, Unit 3는 같은 검증 게이트를 통과한 뒤 붙는다.`

### Section 7. Final CTA

- Goal:
  - give the user one clear next action
- CTA set:
  - `Unit 1 상세 보기`
  - `검증 근거 보기`

## `/unit1` Page Outline

### Section 1. Unit 1 Intro

- headline:
  - `Unit 1: 소인수분해`
- support copy:
  - `수 하나를 기본 블록으로 나누고, 그 결과를 다시 사용하는 tutoring flow를 다룬다.`

### Section 2. Skill Scope

- list the current Unit 1 family in grouped form:
  - `U1-S1` to `U1-S4`
  - `U1-S5A` to `U1-S5D`

### Section 3. What The Tutor Can Do

- three or four short bullets:
  - identify concept confusion
  - reopen blocker-first practice
  - move from factorization to transfer tasks
  - keep operator evidence in a structured flow

### Section 4. Demo Flows

- cards for:
  - `Pilot A`
  - `Pilot B`
  - `Pilot C`

### Section 5. Evidence Summary

- short, user-facing summary:
  - `현재 기준에서 Unit 1은 runtime-complete 상태다.`
  - `다만 넓은 field validation은 아직 아니다.`

## `/unit1/proof` Page Outline

### Section 1. Proof Header

- headline:
  - `Unit 1 Proof`
- support copy:
  - `현재 저장소가 실제로 확인한 것과 아직 확인하지 않은 것을 분리해서 보여준다.`

### Section 2. Confirmed Facts

- `validate-content` pass
- `harness` pass
- transcript replay coverage
- blocker-first reopen verification
- local operator UI support
- real pilot-log comparison exists

### Section 3. Current Limits

- not broad classroom validation
- not finalized mastery scoring
- not full multi-unit product claim

### Section 4. Expansion Rule

- `다음 unit은 같은 validation gate를 통과해야 붙는다.`

## Component List

### Global

1. `SiteShell`
- wraps page width, background, header/footer spacing

2. `TopNav`
- minimal brand row
- links:
  - `/`
  - `/unit1`
  - `/unit1/proof`

### Landing Page Components

3. `HeroPoster`
- props:
  - `eyebrow`
  - `headline`
  - `body`
  - `primaryCta`
  - `secondaryCta`
  - `proofChips`

4. `ProofChipRow`
- small status tags
- should stay compact and not become badge clutter

5. `CapabilityTriptych`
- three-column proof block group
- items:
  - title
  - description

6. `ScopeReasonSection`
- explains why Unit 1 is first
- may use one large paragraph plus three short bullets

7. `DemoPathTimeline`
- ordered four-step visual
- each step:
  - number
  - title
  - one-line description

8. `ScreenshotShowcase`
- one large screenshot frame
- caption below

9. `HonestLimitsSection`
- two-column or stacked list of `done / not yet`

10. `FinalCtaBand`
- one strong CTA
- one secondary proof CTA

### Unit 1 Detail Page Components

11. `UnitHeader`
- title, subtitle, short summary

12. `SkillFamilyGrid`
- grouped skill overview for the Unit 1 range

13. `TutorCapabilityList`
- compact bullet section

14. `DemoFlowCards`
- cards for `Pilot A`, `Pilot B`, `Pilot C`

15. `EvidenceSummaryPanel`
- concise summary of what Unit 1 status means

### Proof Page Components

16. `ProofFactList`
- explicit `confirmed` facts only

17. `ProofLimitList`
- explicit limits only

18. `ExpansionGatePanel`
- explains when another unit is allowed onto the landing story

## Content Rules For Components

- Every component must answer one question only.
- No dashboard-card mosaic.
- No fake analytics numbers.
- No overclaiming copy.
- The first viewport must explain the result without requiring technical context.

## Copy Rules

- Use product language on `/` and `/unit1`.
- Use proof language on `/unit1/proof`.
- Avoid maintainer jargon on the landing page.
- Translate technical ideas into user-facing meaning whenever possible.

## MVP Build Order

1. `SiteShell`
2. `TopNav`
3. `HeroPoster`
4. `CapabilityTriptych`
5. `DemoPathTimeline`
6. `ScreenshotShowcase`
7. `HonestLimitsSection`
8. `FinalCtaBand`
9. `/unit1` detail page
10. `/unit1/proof` page

## Definition Of Done For This Design Stage

- The landing page can be sketched without open structural questions.
- Every planned section has one purpose.
- Every major component has a clear responsibility.
- The page can now move into implementation without reopening product scope.
