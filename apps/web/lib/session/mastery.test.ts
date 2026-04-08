import { describe, it, expect } from "vitest";
import { evaluateMastery, MasteryEvalInput } from "./mastery";

function makeInput(overrides: Partial<MasteryEvalInput> = {}): MasteryEvalInput {
  return {
    current: { level: 1, accuracyRecent10: 0, attemptsTotal: 0, downgradeWarnings: 0 },
    recentAttempts: [],
    recentAtCurrentLevel: [],
    ...overrides,
  };
}

describe("evaluateMastery", () => {
  it("레벨 유지: 시도 부족 시", () => {
    const result = evaluateMastery(makeInput({
      current: { level: 1, accuracyRecent10: 0, attemptsTotal: 5, downgradeWarnings: 0 },
      recentAttempts: [true, true, true, true, true],
      recentAtCurrentLevel: [true, true, true, true, true],
    }));
    expect(result.levelChanged).toBeNull();
    expect(result.newState.level).toBe(1);
    expect(result.newState.attemptsTotal).toBe(6);
  });

  it("업그레이드: 15+시도, 최근10중 8정답, 정답률80%+", () => {
    const result = evaluateMastery(makeInput({
      current: { level: 1, accuracyRecent10: 8, attemptsTotal: 14, downgradeWarnings: 0 },
      recentAttempts: [true, true, true, true, true, true, true, true, false, false],
      recentAtCurrentLevel: [true, true, true, true, true],
    }));
    expect(result.levelChanged).toBe("up");
    expect(result.newState.level).toBe(2);
    expect(result.newState.attemptsTotal).toBe(15);
    expect(result.newState.downgradeWarnings).toBe(0);
  });

  it("업그레이드 안 됨: 최근10중 7정답 (threshold 미달)", () => {
    const result = evaluateMastery(makeInput({
      current: { level: 1, accuracyRecent10: 7, attemptsTotal: 14, downgradeWarnings: 0 },
      recentAttempts: [true, true, true, true, true, true, true, false, false, false],
      recentAtCurrentLevel: [true, true, true, true, true],
    }));
    expect(result.levelChanged).toBeNull();
    expect(result.newState.level).toBe(1);
  });

  it("레벨2에서 업그레이드 안 됨 (MVP 상한)", () => {
    const result = evaluateMastery(makeInput({
      current: { level: 2, accuracyRecent10: 10, attemptsTotal: 20, downgradeWarnings: 0 },
      recentAttempts: [true, true, true, true, true, true, true, true, true, true],
      recentAtCurrentLevel: [true, true, true, true, true],
    }));
    expect(result.levelChanged).toBeNull();
    expect(result.newState.level).toBe(2);
  });

  it("다운그레이드: 최근5문제 중 3틀림", () => {
    const result = evaluateMastery(makeInput({
      current: { level: 2, accuracyRecent10: 3, attemptsTotal: 20, downgradeWarnings: 0 },
      recentAttempts: [false, false, false, true, true, false, false, true, true, true],
      recentAtCurrentLevel: [false, false, false, true, true],
    }));
    expect(result.levelChanged).toBe("down");
    expect(result.newState.level).toBe(1);
    expect(result.newState.downgradeWarnings).toBe(1);
  });

  it("레벨1에서 다운그레이드 안 됨", () => {
    const result = evaluateMastery(makeInput({
      current: { level: 1, accuracyRecent10: 2, attemptsTotal: 10, downgradeWarnings: 0 },
      recentAttempts: [false, false, false, false, false, true, true, false, false, false],
      recentAtCurrentLevel: [false, false, false, false, true],
    }));
    expect(result.levelChanged).toBeNull();
    expect(result.newState.level).toBe(1);
  });

  it("다운그레이드가 업그레이드보다 우선", () => {
    // 업그레이드 조건도 만족하지만 다운그레이드 조건도 만족하는 경우
    const result = evaluateMastery(makeInput({
      current: { level: 2, accuracyRecent10: 8, attemptsTotal: 20, downgradeWarnings: 0 },
      recentAttempts: [true, true, true, true, true, true, true, true, false, false],
      recentAtCurrentLevel: [false, false, false, true, true],
    }));
    expect(result.levelChanged).toBe("down");
    expect(result.newState.level).toBe(1);
  });

  it("최근 데이터 부족 시 다운그레이드 안 됨", () => {
    const result = evaluateMastery(makeInput({
      current: { level: 2, accuracyRecent10: 0, attemptsTotal: 3, downgradeWarnings: 0 },
      recentAttempts: [false, false, false],
      recentAtCurrentLevel: [false, false, false],
    }));
    expect(result.levelChanged).toBeNull();
    expect(result.newState.level).toBe(2);
  });

  it("accuracyRecent10 올바르게 계산", () => {
    const result = evaluateMastery(makeInput({
      current: { level: 1, accuracyRecent10: 0, attemptsTotal: 4, downgradeWarnings: 0 },
      recentAttempts: [true, false, true, true, false],
      recentAtCurrentLevel: [true, false, true, true, false],
    }));
    expect(result.newState.accuracyRecent10).toBe(3);
  });
});
