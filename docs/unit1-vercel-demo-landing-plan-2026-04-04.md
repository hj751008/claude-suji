# Unit 1 Vercel Demo Landing Plan (2026-04-04)

## Purpose

- This document defines the recommended Vercel-facing landing surface for the
  current `Unit 1` deliverable.
- The goal is not to deploy the full current repository as-is.
- The goal is to create one visible, external-facing demo surface that explains
  and launches the strongest working slice: `Unit 1 prime factorization`.

## PM Recommendation

- Ship a separate `Unit 1 demo landing` on Vercel.
- Keep the current Python runtime and local operator UI as the trusted tutoring
  engine and QA surface behind it.
- Do not market the first Vercel page as the full Suji Math AI product.
- Market it as:
  - `Unit 1 Tutor Flow Demo`
  - or `수지 수학 AI Unit 1 데모`

## Why A Separate Vercel Landing

- The current repository does not contain a Vercel-ready web app structure such
  as `package.json`, `next.config.*`, or `vercel.json`.
- The current app surface is Python CLI + local operator UI, not a public
  learner-facing website.
- Trying to deploy the current repo directly to Vercel would mix two concerns:
  - demo storytelling
  - internal runtime and QA behavior
- A thin Vercel landing reduces risk and gives the project a visible result
  faster.

## Product Positioning

- Product claim for the first Vercel page:
  - `수지의 수학 학습 도우미의 첫 결과물은 Unit 1 tutoring loop다.`
- This page should prove:
  - one learning unit is concretely modeled
  - one tutoring loop can be replayed and explained
  - blocker-first handoff and next-step planning already work
- This page should not claim:
  - all middle-school math is ready
  - mastery scoring is finalized
  - classroom deployment is complete

## Audience

- Primary:
  - project stakeholder
  - collaborator
  - reviewer
  - pilot tutor
- Secondary:
  - future partner who needs to see that the project is real and not only
    documents
- Not primary:
  - unsupervised student self-serve user

## Visual Thesis

- A calm, premium poster-like page that feels educational but not childish.
- One warm cream surface, one deep teal accent, one proof-driven structure.
- It should look like a product demo, not a QA console and not a curriculum
  wiki.

## Content Plan

### 1. Hero

- Product name
- one-sentence promise
- direct CTA
- secondary CTA for proof

Example direction:

- headline: `소인수분해를 실제 tutoring flow로 보여주는 Unit 1 데모`
- body: `문서만 정리한 프로젝트가 아니라, replay, handoff, next-step planning이 실제로 이어지는 첫 결과물을 보여준다.`
- CTA 1: `데모 보기`
- CTA 2: `검증 근거 보기`

### 2. What It Does

- Three short capability blocks:
  - transcript replay
  - blocker-first handoff
  - one-turn tutor simulation

### 3. Why Unit 1 First

- Explain why the first visible result is Unit 1:
  - strongest validated slice
  - runtime-complete
  - pilot comparison exists

### 4. Proof Section

- Show concrete evidence, not generic claims:
  - validate-content pass
  - harness pass
  - transcript-backed regression coverage
  - pilot-log comparison status

### 5. Demo Path

- One short, scannable flow:
  - replay transcript
  - open next guided session
  - refresh observation form
  - submit one tutor turn

### 6. Expansion Path

- Explain how Unit 2 and Unit 3 will be added later:
  - same validation gate
  - same conservative policy discipline
  - same replay and handoff contract

### 7. Final CTA

- `Unit 1 데모 시작`
- `운영/검증 구조 보기`

## Interaction Thesis

- Keep motion minimal and meaningful:
  - one hero reveal
  - one section fade/slide sequence
  - one CTA hover emphasis
- Avoid dashboard cards and fake app chrome in the first viewport.

## Recommended Information Architecture

The Vercel landing should have these routes:

1. `/`
- marketing/demo landing for Unit 1

2. `/unit1`
- a more detailed Unit 1 overview page
- may include:
  - concept scope
  - tutoring flow summary
  - demo entry buttons

3. `/unit1/proof`
- explicit proof page with:
  - validation facts
  - transcript evidence summary
  - known limits

Optional later:

4. `/unit1/demo`
- if a browser-safe demo wrapper is built later

## Architecture Recommendation

### Recommended split

- Vercel app:
  - presentation layer only
  - static or Next.js
  - explains and routes to demo/proof
- Current `sujimathAI` repo runtime:
  - remains the source of truth for tutoring behavior
  - remains the place for transcript replay, harness, and content validation

### Why this split is better

- faster visible result
- lower deployment complexity
- easier to message honestly
- avoids forcing the Python operator QA surface directly into a public web app

## MVP Scope

- For the first Vercel release, do only this:
  - build the landing page
  - build the Unit 1 proof page
  - link to screenshots or selected proof snippets from the current repo
- Do not try to expose live tutoring on Vercel in the first pass.

## Source Material To Reuse

- `docs/unit1-deliverable-definition-2026-04-04.md`
- `docs/unit1-validation-closeout-2026-03-29.md`
- `docs/unit1-expert-brief.md`
- `output/playwright/unit1-first-screen-v2.png`

## Copy Constraints

- Speak in product language, not repo-maintainer language.
- Avoid:
  - `harness`
  - `fixture`
  - `provisional house format`
  in the first screen unless they are translated into user-facing meaning.
- Keep technical terms for the proof page, not the hero.

## Success Criteria

- A non-technical stakeholder can answer these within 10 seconds:
  - what this project does
  - what is real today
  - why only Unit 1 is shown first
  - what will come next
- The landing page feels like a product result, not a development console.
- The page does not overclaim beyond current repo evidence.

## Known Risks

- If the page tries to present all units now, the message becomes weak.
- If the page tries to expose the full Python operator tooling directly, the
  product story becomes cluttered.
- If the page hides all proof, it risks looking like another fast mock product.

## Delivery Sequence

1. Lock this landing plan.
2. Build the Vercel landing surface as a separate frontend.
3. Use Unit 1 screenshots and proof text from the current repo.
4. Keep Unit 2 and Unit 3 off the main claim until their gate is met.

## Immediate Next Work

1. Create a simple page outline and component list for the Vercel landing.
2. Decide whether the Vercel surface lives:
  - in a separate repo
  - or in a new frontend folder added to this repo
3. Build the landing before attempting any live remote tutoring demo.
