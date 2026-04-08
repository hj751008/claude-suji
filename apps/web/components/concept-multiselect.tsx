"use client";

import { cn } from "@/lib/utils";

export function ConceptMultiselect({
  concepts,
  selectedIds,
  onChange,
  disabled,
}: {
  concepts: { id: string; name: string }[];
  selectedIds: string[];
  onChange: (ids: string[]) => void;
  disabled?: boolean;
}) {
  function toggle(id: string) {
    if (disabled) return;
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((x) => x !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  }

  return (
    <div className="space-y-3">
      <p className="text-sm font-semibold flex items-center gap-1">
        <span className="text-lg">💡</span> 이 문제는 어떤 개념?
      </p>
      <div className="flex flex-wrap gap-2">
        {concepts.map((c) => {
          const selected = selectedIds.includes(c.id);
          return (
            <button
              key={c.id}
              type="button"
              onClick={() => toggle(c.id)}
              disabled={disabled}
              className={cn(
                "px-4 py-2.5 rounded-xl text-sm font-medium transition-all duration-150 border-2 min-h-[44px]",
                selected
                  ? "bg-primary text-primary-foreground border-primary shadow-soft scale-[1.03]"
                  : "bg-white text-foreground border-border hover:border-primary/40 hover:bg-pastel-lavender/20",
                disabled && "opacity-50 cursor-not-allowed",
              )}
            >
              {selected && "✓ "}{c.name}
            </button>
          );
        })}
      </div>
    </div>
  );
}
