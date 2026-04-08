import { Card, CardContent } from "@/components/ui/card";

export function ProblemCard({
  body,
  index,
  total,
}: { body: string; index: number; total: number }) {
  return (
    <Card className="bg-gradient-to-br from-white to-pastel-lavender/20">
      <CardContent className="p-5 space-y-4">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center justify-center h-7 w-7 rounded-full bg-primary/15 text-primary text-xs font-bold">
            {index + 1}
          </span>
          <span className="text-xs text-muted-foreground">/ {total}문제</span>
        </div>
        <p className="text-lg leading-relaxed font-medium">{body}</p>
      </CardContent>
    </Card>
  );
}
