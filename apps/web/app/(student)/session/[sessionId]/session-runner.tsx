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
  const progress = ((index + (feedback ? 1 : 0)) / problems.length) * 100;

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
      <div className="space-y-5">
        <ProgressBar value={progress} />
        <FeedbackPanel
          isCorrect={feedback.isCorrect}
          selectedNames={selectedNames}
          correctNames={correctNames}
          webtoonScript={feedback.webtoonScript as never}
        />
        <Button onClick={handleNext} className="w-full" size="lg">
          {index + 1 >= problems.length ? "미션 완료! 🎉" : "다음 문제 ➡️"}
        </Button>
      </div>
    );
  }

  return (
    <div className="space-y-5">
      <ProgressBar value={progress} />
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
        {submitting ? "제출 중... ⏳" : "제출하기 ✨"}
      </Button>
    </div>
  );
}

function ProgressBar({ value }: { value: number }) {
  return (
    <div className="w-full h-2.5 bg-muted rounded-full overflow-hidden">
      <div
        className="h-full bg-gradient-to-r from-primary to-accent rounded-full transition-all duration-500 ease-out"
        style={{ width: `${Math.min(100, Math.max(0, value))}%` }}
      />
    </div>
  );
}
