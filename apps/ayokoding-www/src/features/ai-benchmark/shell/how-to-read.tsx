// AI BENCHMARK — honesty surface (Phase 5, W-19..W-22).
//
// Three behaviours land here:
//   - AC-29: the dataset snapshot date shown in text;
//   - AC-32: a `<details open>` how-to-read disclosure (visible without interaction) whose copy
//     states, in both locales, that most frontier scores are vendor self-reported, the index is
//     roster-relative with our weights, coverage varies, figures reflect each vendor's best
//     configuration, the ARC-AGI-2 measurement conflict, and the DeepSeek-versus-gateway price gap;
//   - AC-34: a Sources and Licences section rendered from the dataset-level OPERATORS list, so a
//     new operator appears with no component edit.
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

      {/* AC-32 — how-to-read disclosure, open by default. */}
      <details open data-testid="ai-bench-how-to" className="rounded-md border p-3 text-sm">
        <summary className="cursor-pointer font-medium">{t(locale, "aiBenchHowToSummary")}</summary>
        <ul data-testid="ai-bench-how-to-list" className="mt-2 list-disc space-y-2 pl-5 text-muted-foreground">
          <li>{t(locale, "aiBenchHowToVendorReported")}</li>
          <li>{t(locale, "aiBenchHowToIndexRelative")}</li>
          <li>{t(locale, "aiBenchHowToCoverage")}</li>
          <li>{t(locale, "aiBenchHowToBestConfig")}</li>
          <li>{t(locale, "aiBenchHowToArcConflict")}</li>
          <li>{t(locale, "aiBenchHowToPriceGap")}</li>
        </ul>
      </details>

      {/* Rule-15 UWT-002/UWT-003/UWT-005/USS-002 fix — a visible, always-available legend (not
          inside the collapsible `<details>` above, so it stays visible even if the reader closes
          that disclosure) defining the four capability classes, the five evidence grades, and the
          coverage formula. Reuses the SAME label words the page already shows (`aiBenchBand*`,
          `aiBenchGrade*`) so the legend and the live page never drift into two vocabularies. */}
      <section
        data-slot="ai-bench-legend"
        data-testid="ai-bench-legend"
        className="space-y-3 rounded-md border p-3 text-sm"
        aria-labelledby="ai-bench-legend-heading"
      >
        <h3 id="ai-bench-legend-heading" className="font-semibold">
          {t(locale, "aiBenchLegendHeading")}
        </h3>

        <div>
          <p className="text-muted-foreground">{t(locale, "aiBenchLegendClassIntro")}</p>
          <dl data-testid="ai-bench-legend-classes" className="mt-1 space-y-1">
            {(
              [
                ["opus", "aiBenchBandOpus", "aiBenchLegendClassOpus"],
                ["sonnet", "aiBenchBandSonnet", "aiBenchLegendClassSonnet"],
                ["light", "aiBenchBandLight", "aiBenchLegendClassLight"],
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
      </section>

      {/* AC-34 — Sources and Licences, rendered from the OPERATORS dataset list. */}
      <section data-testid="ai-bench-sources" className="space-y-2 text-sm" aria-labelledby="ai-bench-sources-heading">
        <h3 id="ai-bench-sources-heading" className="font-semibold">
          {t(locale, "aiBenchSourcesHeading")}
        </h3>
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
      </section>
    </section>
  );
}
