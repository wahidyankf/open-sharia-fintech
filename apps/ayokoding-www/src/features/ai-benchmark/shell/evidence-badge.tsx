// AI BENCHMARK — evidence-grade badge (Phase 5, W-11/W-13).
//
// Renders a single figure's evidence grade as localized TEXT (never colour alone — WCAG 1.4.1) and
// resolves to the figure's source URL as an anchor (AC-30: every figure links to its source).
// `<FigureCell>` composes one of these per numeric column.

import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { GRADE_LABEL_KEYS } from "../core/data/benchmarks";
import type { EvidenceGrade } from "../core/data/models";

const SLOT = "evidence-badge";

/**
 * A grade marker that doubles as the source link. The grade word is the link's accessible name
 * (prefixed with a localized "Evidence" label for context), so the badge is meaningful both
 * visually and to assistive tech.
 */
export function EvidenceBadge({ grade, source, locale }: { grade: EvidenceGrade; source: string; locale: Locale }) {
  const labelKey = GRADE_LABEL_KEYS[grade];
  const gradeWord = labelKey ? t(locale, labelKey) : grade;
  const evidenceLabel = t(locale, "aiBenchEvidenceLabel");
  const sourceLabel = t(locale, "aiBenchSourceLabel");
  // A small colour dot reinforces the grade for sighted users but is decorative — the grade WORD
  // is the real encoding, so colour is never the sole means (WCAG 1.4.1).
  return (
    <a
      data-slot={SLOT}
      data-grade={grade}
      href={source}
      target="_blank"
      rel="noopener noreferrer nofollow"
      className="inline-flex items-center gap-1 text-xs font-medium text-muted-foreground underline decoration-dotted underline-offset-2 hover:text-foreground"
      aria-label={`${evidenceLabel}: ${gradeWord} — ${sourceLabel}`}
    >
      <span aria-hidden="true" className={dotClass(grade)} data-slot={`${SLOT}-dot`} />
      <span data-slot={`${SLOT}-grade`}>{gradeWord}</span>
      <span className="sr-only">{sourceLabel}</span>
    </a>
  );
}

/** Decorative dot class per grade. Colour is reinforcement only — the grade word is always shown. */
function dotClass(grade: EvidenceGrade): string {
  switch (grade) {
    case "verified":
      return "size-1.5 rounded-full bg-emerald-500";
    case "self-reported":
      return "size-1.5 rounded-full bg-amber-500";
    case "secondary":
      return "size-1.5 rounded-full bg-sky-500";
    case "conflicted":
      return "size-1.5 rounded-full bg-rose-500";
    case "unavailable":
    default:
      return "size-1.5 rounded-full bg-muted-foreground";
  }
}
