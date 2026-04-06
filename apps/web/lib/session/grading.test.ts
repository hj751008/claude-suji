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
