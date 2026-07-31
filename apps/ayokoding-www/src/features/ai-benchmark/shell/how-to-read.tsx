// AI BENCHMARK — honesty surface (Phase 5, W-19..W-22; reworked Phase 7, D3).
//
// Three exports, one concern each:
//   - `HowToRead` — AC-29's dataset snapshot date in text, plus AC-32's ONE always-visible honesty
//     line (most frontier scores are vendor self-reported) with the remaining five how-to-read
//     points (index is roster-relative with our weights, coverage varies, figures reflect each
//     vendor's best configuration, a measurement conflict example — Rule-15 UWT-005 fix,
//     2026-07-30: SWE-bench Pro / GPQA Diamond, not ARC-AGI-2 — and the DeepSeek-versus-gateway
//     price gap) behind their own `<details>` (D3 narrowed the Phase-5 "whole block open by
//     default" guarantee to just the honesty line);
//   - `AiBenchLegend` — USS-002's class/grade/coverage-formula legend, now its own `<details>`
//     (AC-57, Phase 7 cycle 7.3) rendered after the roster (Phase 7 cycle 7.2's document reorder);
//   - `AiBenchSources` — AC-34's Sources and Licences section from the dataset-level OPERATORS
//     list, also its own `<details>` (AC-57) rendered after the roster, so a new operator appears
//     with no component edit.
//
// No literal figure lives here — the snapshot date comes from the dataset, the operators from
// `core/data/operators.ts`, and all copy from i18n.

import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { OPERATORS } from "../core/data/operators";

export type HowToReadProps = {
  snapshotDate: string;
  locale: Locale;
};

export function HowToRead({ snapshotDate, locale }: HowToReadProps) {
  // `snapshotDate` (e.g. "2026-07-28") parses per ECMA-262 as UTC midnight. `timeZone: "UTC"` is
  // pinned so the rendered date is always the dataset's UTC date — never reformatted into a
  // visitor's local zone (which renders one day early for every UTC-negative zone) — and so the
  // server render (UTC on the deploy target) and the client render agree, avoiding a hydration
  // mismatch (F2).
  const dateText = new Intl.DateTimeFormat(locale === "id" ? "id-ID" : "en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  }).format(new Date(snapshotDate));

  return (
    <section
      data-slot="how-to-read"
      data-testid="how-to-read"
      className="space-y-4"
      aria-labelledby="how-to-read-heading"
    >
      <h2 id="how-to-read-heading" className="sr-only">
        {t(locale, "aiBenchHowToSummary")}
      </h2>

      {/* AC-29 — snapshot date in text. */}
      <p data-testid="ai-bench-snapshot" className="text-sm text-muted-foreground">
        <span className="font-medium text-foreground">{t(locale, "aiBenchSnapshotLabel")}:</span> {dateText}
      </p>

      {/* AC-32 (reworded, D3) — the ONE always-visible guarantee is this single honesty line;
          it carries no `<details>` ancestor, so it renders before any interaction regardless of
          the remainder disclosure's open/closed state. */}
      <p data-testid="ai-bench-how-to-honesty" className="text-sm">
        {t(locale, "aiBenchHowToVendorReported")}
      </p>

      {/* The remaining five how-to-read points sit behind their own disclosure — D3 narrowed the
          Phase-5 guarantee (the WHOLE six-bullet block open by default) down to just the honesty
          line above, once Phase 6/7's denser layout made a permanently-open six-bullet block feel
          heavy. `group` + `group-open:` (Tailwind's built-in `<details>`-open variant) plus a
          `lg:block` override render the list open at `lg`+ via CSS alone — no JS width check, no
          `matchMedia`, so server and client always agree on markup and there is no hydration
          mismatch (DD-29). Below `lg`, the list starts closed and opens only via the native
          `<summary>` toggle. */}
      <details data-testid="ai-bench-how-to-details" className="group rounded-md border p-3 text-sm">
        <summary className="cursor-pointer font-medium">{t(locale, "aiBenchHowToSummary")}</summary>
        <ul
          data-testid="ai-bench-how-to-list"
          className="mt-2 hidden list-disc space-y-2 pl-5 text-muted-foreground group-open:block lg:block"
        >
          <li>{t(locale, "aiBenchHowToIndexRelative")}</li>
          <li>{t(locale, "aiBenchHowToCoverage")}</li>
          <li>{t(locale, "aiBenchHowToBestConfig")}</li>
          <li>{t(locale, "aiBenchHowToArcConflict")}</li>
          <li>{t(locale, "aiBenchHowToPriceGap")}</li>
        </ul>
      </details>
    </section>
  );
}

// Rule-15 UWT-002/UWT-003/UWT-005/USS-002 fix — a legend defining the four capability classes,
// the five evidence grades, and the coverage formula. Reuses the SAME label words the page already
// shows (`aiBenchBand*`, `aiBenchGrade*`) so the legend and the live page never drift into two
// vocabularies. AC-57 (Phase 7, cycle 7.3): wrapped in its own `<details>` with a localized
// `<summary>` so it stays reachable after the page's document-order reshuffle (cycle 7.2) moved it
// below the roster, rather than staying unconditionally visible at that position.
export function AiBenchLegend({ locale }: { locale: Locale }) {
  return (
    <details
      data-slot="ai-bench-legend"
      data-testid="ai-bench-legend"
      className="space-y-3 rounded-md border p-3 text-sm"
    >
      <summary className="cursor-pointer font-semibold">{t(locale, "aiBenchLegendHeading")}</summary>

      <div className="mt-3 space-y-3">
        <div>
          <p className="text-muted-foreground">{t(locale, "aiBenchLegendClassIntro")}</p>
          <dl data-testid="ai-bench-legend-classes" className="mt-1 space-y-1">
            {(
              [
                ["opus", "aiBenchBandOpus", "aiBenchLegendClassOpus"],
                ["sonnet", "aiBenchBandSonnet", "aiBenchLegendClassSonnet"],
                ["haiku", "aiBenchBandHaiku", "aiBenchLegendClassHaiku"],
                ["unrated", "aiBenchBandUnrated", "aiBenchLegendClassUnrated"],
              ] as const
            ).map(([band, labelKey, defKey]) => (
              <div key={band} data-testid={`ai-bench-legend-class-${band}`}>
                <dt className="inline font-medium">{t(locale, labelKey)}: </dt>
                <dd className="inline text-muted-foreground">{t(locale, defKey)}</dd>
              </div>
            ))}
          </dl>
        </div>

        <div>
          <p className="text-muted-foreground">{t(locale, "aiBenchLegendGradeIntro")}</p>
          <dl data-testid="ai-bench-legend-grades" className="mt-1 space-y-1">
            {(
              [
                ["verified", "aiBenchGradeVerified", "aiBenchLegendGradeVerified"],
                ["self-reported", "aiBenchGradeSelfReported", "aiBenchLegendGradeSelfReported"],
                ["secondary", "aiBenchGradeSecondary", "aiBenchLegendGradeSecondary"],
                ["conflicted", "aiBenchGradeConflicted", "aiBenchLegendGradeConflicted"],
                ["unavailable", "aiBenchGradeUnavailable", "aiBenchLegendGradeUnavailable"],
              ] as const
            ).map(([grade, labelKey, defKey]) => (
              <div key={grade} data-testid={`ai-bench-legend-grade-${grade}`}>
                <dt className="inline font-medium">{t(locale, labelKey)}: </dt>
                <dd className="inline text-muted-foreground">{t(locale, defKey)}</dd>
              </div>
            ))}
          </dl>
        </div>

        {/* UWT-005 — the bare "Coverage" percentage carries no visible unit/derivation; this states
            the exact weighted formula (mirrors `core/score.ts`'s `coverage()` / `BENCHMARK_WEIGHTS`). */}
        <p data-testid="ai-bench-legend-coverage" className="text-muted-foreground">
          {t(locale, "aiBenchLegendCoverageFormula")}
        </p>
      </div>
    </details>
  );
}

// AC-34 — Sources and Licences, rendered from the OPERATORS dataset list. AC-57 (Phase 7, cycle
// 7.3): wrapped in its own `<details>` with a localized `<summary>`, same rationale as
// `AiBenchLegend` above.
export function AiBenchSources({ locale }: { locale: Locale }) {
  return (
    <details data-testid="ai-bench-sources" className="space-y-2 rounded-md border p-3 text-sm">
      <summary className="cursor-pointer font-semibold">{t(locale, "aiBenchSourcesHeading")}</summary>
      <div className="mt-2 space-y-2">
        <p className="text-muted-foreground">{t(locale, "aiBenchSourcesIntro")}</p>
        <dl className="space-y-2">
          {OPERATORS.map((op) => (
            <div
              key={op.name}
              data-slot="source-operator"
              data-testid="source-operator"
              className="grid grid-cols-1 gap-1 sm:grid-cols-[minmax(0,10rem)_1fr]"
            >
              <dt className="font-medium">
                {op.url ? (
                  <a
                    href={op.url}
                    target="_blank"
                    rel="noopener noreferrer nofollow"
                    className="underline decoration-dotted underline-offset-2"
                  >
                    {op.name}
                  </a>
                ) : (
                  op.name
                )}
              </dt>
              <dd className="text-muted-foreground" data-testid="operator-terms">
                {t(locale, op.termsKey)}
              </dd>
            </div>
          ))}
        </dl>
      </div>
    </details>
  );
}
