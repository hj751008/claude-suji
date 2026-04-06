import { Card, CardContent } from "@/components/ui/card";

export function ProblemCard({
  body,
  index,
  total,
}: { body: string; index: number; total: number }) {
  return (
    <Card>
      <CardContent className="p-6 space-y-4">
        <p className="text-xs text-muted-foreground">문제 {index + 1}/{total}</p>
        <p className="text-base leading-relaxed">{body}</p>
      </CardContent>
    </Card>
  );
}
