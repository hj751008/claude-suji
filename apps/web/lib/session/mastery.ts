/**
 * 개념 숙달도(mastery) 판정 — 순수 함수
 *
 * 업그레이드: 정답률 80% AND 최근10문제 중 8정답 AND 최소 15문제 시도 → level+1
 * 다운그레이드: 현재 레벨 최근 5문제 중 3문제 이상 틀림 → level-1
 * MVP: 레벨 1~2만 (Lv2가 상한)
 */

export type MasteryState = {
  level: number;
  accuracyRecent10: number; // 최근 10문제 중 정답 수
  attemptsTotal: number;
  downgradeWarnings: number;
};

export type MasteryEvalInput = {
  current: MasteryState;
  /** 최근 시도들 (최신순, 최대 10개) — true=정답 */
  recentAttempts: boolean[];
  /** 현재 레벨 최근 5문제 (최신순) — true=정답 */
  recentAtCurrentLevel: boolean[];
};

export type MasteryEvalResult = {
  newState: MasteryState;
  levelChanged: "up" | "down" | null;
};

const MAX_LEVEL = 2; // MVP: Lv2까지만
const MIN_LEVEL = 1;

const UPGRADE_MIN_ATTEMPTS = 15;
const UPGRADE_RECENT_WINDOW = 10;
const UPGRADE_RECENT_THRESHOLD = 8; // 10문제 중 8정답
const UPGRADE_ACCURACY_THRESHOLD = 0.8;

const DOWNGRADE_RECENT_WINDOW = 5;
const DOWNGRADE_WRONG_THRESHOLD = 3; // 5문제 중 3틀림

export function evaluateMastery(input: MasteryEvalInput): MasteryEvalResult {
  const { current, recentAttempts, recentAtCurrentLevel } = input;

  const newAttemptsTotal = current.attemptsTotal + 1;

  // 최근 10문제 정답 수 계산
  const recent10 = recentAttempts.slice(0, UPGRADE_RECENT_WINDOW);
  const accuracyRecent10 = recent10.filter(Boolean).length;

  // 전체 정답률 (최근 10문제 기준)
  const accuracyRate = recent10.length > 0 ? accuracyRecent10 / recent10.length : 0;

  // 다운그레이드 체크 (업그레이드보다 먼저)
  const recent5AtLevel = recentAtCurrentLevel.slice(0, DOWNGRADE_RECENT_WINDOW);
  const wrongCount = recent5AtLevel.filter((v) => !v).length;

  if (
    current.level > MIN_LEVEL &&
    recent5AtLevel.length >= DOWNGRADE_RECENT_WINDOW &&
    wrongCount >= DOWNGRADE_WRONG_THRESHOLD
  ) {
    return {
      newState: {
        level: current.level - 1,
        accuracyRecent10,
        attemptsTotal: newAttemptsTotal,
        downgradeWarnings: current.downgradeWarnings + 1,
      },
      levelChanged: "down",
    };
  }

  // 업그레이드 체크
  if (
    current.level < MAX_LEVEL &&
    newAttemptsTotal >= UPGRADE_MIN_ATTEMPTS &&
    recent10.length >= UPGRADE_RECENT_WINDOW &&
    accuracyRecent10 >= UPGRADE_RECENT_THRESHOLD &&
    accuracyRate >= UPGRADE_ACCURACY_THRESHOLD
  ) {
    return {
      newState: {
        level: current.level + 1,
        accuracyRecent10,
        attemptsTotal: newAttemptsTotal,
        downgradeWarnings: 0,
      },
      levelChanged: "up",
    };
  }

  // 변화 없음
  return {
    newState: {
      level: current.level,
      accuracyRecent10,
      attemptsTotal: newAttemptsTotal,
      downgradeWarnings: current.downgradeWarnings,
    },
    levelChanged: null,
  };
}
