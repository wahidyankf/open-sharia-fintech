const MILESTONES = ["Dangerous", "Comfortable", "Confident"] as const;

/**
 * The skills category landing's compact ramp-progress preview (Cycle 3.1b-ii, R7/R8) — the
 * dangerous/comfortable/confident course markers as a small horizontal `<ol>` of three labelled
 * ticks, rendered once per subject `PathCard`. **Compact preview only** — the detailed can/cannot
 * text, runway-justification paragraph, and linked-prerequisite outbound links render on that
 * subject's own `path-landing.tsx` page (Cycle 3.1d), not here.
 */
export function RampMilestoneStrip() {
  return (
    <ol className="mt-2 flex gap-3 text-[10px] text-muted-foreground">
      {MILESTONES.map((label) => (
        <li key={label} className="flex items-center gap-1">
          <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-[var(--hue-sky)]" />
          {label}
        </li>
      ))}
    </ol>
  );
}
