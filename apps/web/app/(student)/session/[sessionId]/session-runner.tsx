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
