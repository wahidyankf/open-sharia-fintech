// AI BENCHMARK — evidence-grade badge (Phase 5, W-11/W-13).
//
// Renders a single figure's evidence grade as localized TEXT (never colour alone — WCAG 1.4.1) and
// resolves to the figure's source URL as an anchor (AC-30: every figure links to its source).
// `<FigureCell>` composes one of these per numeric column.

import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { GRADE_LABEL_KEYS } from "../core/data/benchmarks";
import type { EvidenceGrade } from "../core/data/models";
import { TAP_TARGET_MIN_CLASS } from "./tap-target";

const SLOT = "evidence-badge";

/**
 * A grade marker that doubles as the source link. The grade word is the link's accessible name
 * (prefixed with a localized "Evidence" label for context), so the badge is meaningful both
 * visually and to assistive tech. "Source" is rendered visibly too, in parentheses after the grade
 * word (Rule-15 UWT-004 fix) — previously it existed only as `sr-only` text, so a sighted user saw
 * only a bare grade adjective with nothing signalling the underline is a link to an external page.
 */
export function EvidenceBadge({ grade, source, locale }: { grade: EvidenceGrade; source: string; locale: Locale }) {
  const labelKey = GRADE_LABEL_KEYS[grade];
  const gradeWord = labelKey ? t(locale, labelKey) : grade;
  const evidenceLabel = t(locale, "aiBenchEvidenceLabel");
  const sourceLabel = t(locale, "aiBenchSourceLabel");
  // A small colour dot reinforces the grade for sighted users but is decorative — the grade WORD
  // is the real encoding, so colour is never the sole means (WCAG 1.4.1). `title` gives a sighted
  // mouse user an immediate hover tooltip naming the grade (Rule-15 UWT-003 fix, alongside the
  // always-visible legend in `how-to-read.tsx`).
  return (
    <a
      data-slot={SLOT}
      data-grade={grade}
      href={source}
      target="_blank"
      rel="noopener noreferrer nofollow"
      title={`${evidenceLabel}: ${gradeWord}`}
      // DD-30/AC-58: a 24x24 CSS px minimum tap target (WCAG 2.5.8) — see `tap-target.ts`.
      className={`inline-flex items-center gap-1 text-xs font-medium text-muted-foreground underline decoration-dotted underline-offset-2 hover:text-foreground ${TAP_TARGET_MIN_CLASS}`}
      aria-label={`${evidenceLabel}: ${gradeWord} — ${sourceLabel}`}
    >
      <span aria-hidden="true" className={dotClass(grade)} data-slot={`${SLOT}-dot`} />
      <span data-slot={`${SLOT}-grade`}>{gradeWord}</span>
      <span aria-hidden="true" data-slot={`${SLOT}-source`} className="text-[0.7rem]">
        ({sourceLabel})
      </span>
    </a>
  );
}

/**
 * Decorative dot class per grade. Colour is reinforcement only — the grade word is always shown
 * (never colour alone). Routes through the AyoKoding semantic `--evidence-*` tokens
 * (`libs/web-ui-token/src/ayokoding.css`) rather than raw Tailwind default-palette classes (Rule-15
 * DWT-002 fix) — each token is a `var()` alias onto an existing `--hue-*-ink` tone, so light/dark
 * both resolve automatically from the one class, no `dark:` variant needed.
 */
function dotClass(grade: EvidenceGrade): string {
  switch (grade) {
    case "verified":
      return "size-1.5 rounded-full bg-[var(--evidence-verified)]";
    case "self-reported":
      return "size-1.5 rounded-full bg-[var(--evidence-self-reported)]";
    case "secondary":
      return "size-1.5 rounded-full bg-[var(--evidence-secondary)]";
    case "conflicted":
      return "size-1.5 rounded-full bg-[var(--evidence-conflicted)]";
    case "unavailable":
    default:
      return "size-1.5 rounded-full bg-muted-foreground";
  }
}
