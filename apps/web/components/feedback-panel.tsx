import { Card, CardContent } from "@/components/ui/card";

type WebtoonLine =
  | { type: "scene"; text: string }
  | { speaker: string; text: string };

export function FeedbackPanel({
  isCorrect,
  selectedNames,
  correctNames,
  webtoonScript,
}: {
  isCorrect: boolean;
  selectedNames: string[];
  correctNames: string[];
  webtoonScript: WebtoonLine[] | null;
}) {
  return (
    <div className="space-y-4 animate-pop-in">
      <div
        className={`text-center p-6 rounded-2xl ${
          isCorrect
            ? "bg-gradient-to-br from-pastel-mint/60 to-pastel-yellow/40 text-green-800"
            : "bg-gradient-to-br from-pastel-pink/50 to-pastel-peach/40 text-amber-800"
        }`}
      >
        <p className="text-4xl mb-2">{isCorrect ? "🎉" : "💪"}</p>
        <p className="text-lg font-bold">
          {isCorrect ? "맞았어! 대단해!" : "아쉬워, 다시 볼까?"}
        </p>
        {!isCorrect && (
          <div className="text-sm mt-3 space-y-1">
            <p>네가 고른: {selectedNames.join(", ") || "없음"}</p>
            <p className="font-semibold">정답: {correctNames.join(", ")}</p>
          </div>
        )}
        {isCorrect && (
          <p className="text-sm mt-2 font-medium">개념: {correctNames.join(", ")}</p>
        )}
      </div>

      {webtoonScript && webtoonScript.length > 0 && (
        <Card className="bg-pastel-yellow/20 border-pastel-yellow/40">
          <CardContent className="p-4 space-y-3">
            <p className="text-sm font-bold flex items-center gap-1">
              <span className="text-lg">📖</span> 해설
            </p>
            {webtoonScript.map((line, i) => (
              <div key={i} className="text-sm">
                {"type" in line ? (
                  <p className="italic text-muted-foreground text-xs">[{line.text}]</p>
                ) : (
                  <div className="bg-white/70 rounded-xl px-3 py-2 shadow-sm">
                    <span className="font-bold text-primary">{line.speaker}</span>{" "}
                    {line.text}
                  </div>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
