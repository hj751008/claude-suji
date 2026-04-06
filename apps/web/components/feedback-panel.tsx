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
    <div className="space-y-4">
      <div
        className={`text-center p-4 rounded-lg ${
          isCorrect ? "bg-green-50 text-green-900" : "bg-amber-50 text-amber-900"
        }`}
      >
        <p className="text-lg font-bold">
          {isCorrect ? "✅ 맞았어!" : "❌ 아쉬워, 다시 볼까?"}
        </p>
        {!isCorrect && (
          <p className="text-sm mt-2">
            네가 고른: {selectedNames.join(", ") || "없음"}<br />
            정답: {correctNames.join(", ")}
          </p>
        )}
        {isCorrect && (
          <p className="text-sm mt-2">개념: {correctNames.join(", ")}</p>
        )}
      </div>

      {webtoonScript && webtoonScript.length > 0 && (
        <Card>
          <CardContent className="p-4 space-y-3">
            <p className="text-sm font-medium">📖 웹툰 설명</p>
            {webtoonScript.map((line, i) => (
              <div key={i} className="text-sm">
                {"type" in line ? (
                  <p className="italic text-muted-foreground">[{line.text}]</p>
                ) : (
                  <p>
                    <span className="font-semibold">{line.speaker}: </span>
                    {line.text}
                  </p>
                )}
              </div>
            ))}
          </CardContent>
        </Card>
      )}
    </div>
  );
}
