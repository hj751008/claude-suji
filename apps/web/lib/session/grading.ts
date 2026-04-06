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
