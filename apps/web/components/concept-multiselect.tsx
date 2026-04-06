"use client";

import { Checkbox } from "@/components/ui/checkbox";
import { Label } from "@/components/ui/label";

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
    if (selectedIds.includes(id)) {
      onChange(selectedIds.filter((x) => x !== id));
    } else {
      onChange([...selectedIds, id]);
    }
  }

  return (
    <div className="space-y-3">
      <p className="text-sm font-medium">💡 이 문제는 어떤 개념?</p>
      <div className="space-y-2">
        {concepts.map((c) => (
          <div key={c.id} className="flex items-center space-x-3 py-1">
            <Checkbox
              id={`concept-${c.id}`}
              checked={selectedIds.includes(c.id)}
              onCheckedChange={() => toggle(c.id)}
              disabled={disabled}
            />
            <Label htmlFor={`concept-${c.id}`} className="cursor-pointer text-base">
              {c.name}
            </Label>
          </div>
        ))}
      </div>
    </div>
  );
}
