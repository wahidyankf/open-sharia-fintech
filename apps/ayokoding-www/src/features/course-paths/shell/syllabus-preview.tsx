/** How many leading courses count as the "first phase" preview (Cycle 3.1c-ii, R7). */
const FIRST_PHASE_PREVIEW_COUNT = 3;

export interface SyllabusPreviewProps {
  /** Already-resolved course titles, in manifest `courseOrder`. Only the first 3 are shown. */
  courseTitles: readonly string[];
}

/**
 * The single-role arc landing's inline first-phase syllabus preview (Cycle 3.1c-ii, R7) — a small
 * `<ol>` of the manifest's first courses, sharing the same "number is order" list semantics
 * `path-landing.tsx`'s own syllabus uses (Cycle 3.1's REFACTOR note), so a lone role card never
 * reads as a stub next to a fabricated empty second card.
 *
 * `PathManifest` has no explicit phase-boundary field, so "first phase" is approximated as the
 * first {@link FIRST_PHASE_PREVIEW_COUNT} courses in `courseOrder` — a documented simplification,
 * not a hidden one.
 */
export function SyllabusPreview({ courseTitles }: SyllabusPreviewProps) {
  const preview = courseTitles.slice(0, FIRST_PHASE_PREVIEW_COUNT);

  return (
    <p className="mt-2 text-xs text-muted-foreground">
      <span className="font-medium text-foreground">Starts with:</span>{" "}
      <ol className="inline">
        {preview.map((title, index) => (
          <li key={title} className="inline">
            {index > 0 && " · "}
            {index + 1}. {title}
          </li>
        ))}
      </ol>
      {" →"}
    </p>
  );
}
