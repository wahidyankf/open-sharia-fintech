"use client";

// AI BENCHMARK — harness/class filter bar (Phase 8, N-3..N-19).
//
// Two selectors — harness and class — read from and write to the URL (the route owns
// `decodeState`/`encodeState`/`filterModels`; this component is a controlled view over the
// resulting `FilterState`, changing it via `onChange`). Responsive strategy (N-17/N-18): below
// `md` a collapsed `<details>` disclosure names the active-filter count in its summary; at `md`
// and `lg` an inline, wrapping bar names the result count instead — both variants render the SAME
// two `<select>` controls (same accessible names via matching `aria-label`s), simultaneously in the
// DOM, with CSS toggling which is visible (the same dual-render pattern `model-table.tsx` already
// uses for its own mobile/desktop split).
//
// N-19 refactor: both selectors are one generic `<FilterSelect>` (label, option list, onChange)
// rather than two hand-written `<select>` blocks, so a third filter axis would cost one call, not
// one new block.
//
// FCIS boundary: no literal harness id, band name, or threshold lives here — every option comes
// from `core/filter.ts`'s `HARNESS_IDS`/`BANDS` (the single source of truth, F-9), every harness
// display name from `core/data/benchmarks.ts`, and every band label from `chart-primitives.tsx`'s
// `bandLabel`.

import { ChevronDown } from "lucide-react";
import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import { cn } from "@/lib/utils";
import type { HarnessId } from "../core/data/models";
import { HARNESS_IDS, BANDS, type FilterState } from "../core/filter";
import type { Band } from "../core/bands";
import { HARNESS_DISPLAY_NAMES } from "../core/data/benchmarks";
import { bandLabel } from "./chart-primitives";

const SLOT = "benchmark-filters";

const SELECT_CLASS =
  "h-11 min-h-[44px] w-full max-w-full min-w-0 appearance-none rounded-md border border-input bg-transparent py-1 pr-8 pl-3 text-sm shadow-xs transition-[color,box-shadow] outline-none focus-visible:border-ring focus-visible:ring-[3px] focus-visible:ring-ring/50";

export type FilterOption = { value: string; label: string };

export type FilterSelectProps = {
  id: string;
  label: string;
  value: string;
  options: readonly FilterOption[];
  /**
   * The "no filter on this axis" empty option's label. OPTIONAL: omit it entirely for a control
   * that has no such state (e.g. the sort dropdowns in `benchmark-chart.tsx`, which always have
   * an active `SortMode` — there is no "no sort"). Passing it renders `<option value="">` as the
   * first option; omitting it renders no empty option at all, so `onChange` only ever receives one
   * of `options`' own values.
   */
  allLabel?: string;
  onChange: (value: string) => void;
};

/**
 * One generic labelled `<select>` — the harness selector and the class selector are both a single
 * call to this component (N-19), differing only in id/label/options/onChange. The empty option
 * (`value=""`) is always "no filter on this axis" (rendered with the caller's localized `allLabel`)
 * — and is omitted entirely when the caller passes no `allLabel` (see its doc above).
 */
export function FilterSelect({ id, label, value, options, allLabel, onChange }: FilterSelectProps) {
  return (
    <div data-slot="filter-select" className="flex min-w-0 basis-full items-center gap-2 sm:basis-auto">
      <label htmlFor={id} className="text-sm font-medium">
        {label}
      </label>
      <div className="relative w-full max-w-full min-w-0 sm:w-48">
        <select
          id={id}
          aria-label={label}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          className={SELECT_CLASS}
        >
          {allLabel !== undefined ? <option value="">{allLabel}</option> : null}
          {options.map((opt) => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>
        <ChevronDown
          aria-hidden="true"
          className="pointer-events-none absolute top-1/2 right-2 size-4 -translate-y-1/2 text-muted-foreground"
        />
      </div>
    </div>
  );
}

export type BenchmarkFiltersProps = {
  state: FilterState;
  resultCount: number;
  locale: Locale;
  /**
   * Reports a PATCH (only the axis that changed), not a pre-merged full `FilterState` — the caller
   * (`benchmark-content.tsx`) owns merging it onto its own always-current ref-tracked state. This
   * component previously spread its own `state` PROP into the merge (`{...state, harness}`), which
   * is correct in isolation but becomes a stale-closure race once the caller's `state` prop lags
   * behind an in-flight `router.push` (Rule-15 EWT-003 fix): change the harness select then the
   * class select in rapid succession, and the second call's `state` prop still reflected the
   * pre-harness-change URL, so its merge silently dropped the harness change.
   */
  onChange: (patch: Partial<FilterState>) => void;
};

export function BenchmarkFilters({ state, resultCount, locale, onChange }: BenchmarkFiltersProps) {
  const harnessOptions: FilterOption[] = HARNESS_IDS.map((h) => ({
    value: h,
    label: HARNESS_DISPLAY_NAMES[h] ?? h,
  }));
  const classOptions: FilterOption[] = BANDS.map((b) => ({ value: b, label: bandLabel(b, locale) }));

  const harnessLabel = t(locale, "aiBenchFilterHarnessLabel");
  const classLabel = t(locale, "aiBenchFilterClassLabel");
  const allHarnessesLabel = t(locale, "aiBenchFilterAllHarnesses");
  const allClassesLabel = t(locale, "aiBenchFilterAllClasses");

  const activeCount = (state.harness !== undefined ? 1 : 0) + (state.class !== undefined ? 1 : 0);

  function handleHarnessChange(raw: string) {
    const harness = raw === "" ? undefined : (raw as HarnessId);
    onChange({ harness });
  }

  function handleClassChange(raw: string) {
    const bandClass = raw === "" ? undefined : (raw as Band);
    onChange({ class: bandClass });
  }

  return (
    <div data-slot={SLOT} data-testid={SLOT}>
      {/* Below `md`: a collapsed disclosure naming the active-filter count. */}
      <details data-testid={`${SLOT}-mobile`} className={cn("rounded-md border p-3 md:hidden")}>
        <summary data-testid={`${SLOT}-mobile-summary`} className="cursor-pointer text-sm font-medium">
          {t(locale, "aiBenchFilterSummary")} ({activeCount} {t(locale, "aiBenchFilterActiveCountLabel")})
        </summary>
        <div className="mt-3 flex flex-col gap-3">
          <FilterSelect
            id="benchmark-filter-harness-mobile"
            label={harnessLabel}
            value={state.harness ?? ""}
            options={harnessOptions}
            allLabel={allHarnessesLabel}
            onChange={handleHarnessChange}
          />
          <FilterSelect
            id="benchmark-filter-class-mobile"
            label={classLabel}
            value={state.class ?? ""}
            options={classOptions}
            allLabel={allClassesLabel}
            onChange={handleClassChange}
          />
        </div>
      </details>

      {/* `md`/`lg`: an inline, wrapping bar naming the result count (single row once `lg` gives it
          enough width). */}
      <div data-testid={`${SLOT}-desktop`} className="hidden md:flex md:flex-wrap md:items-center md:gap-3">
        <FilterSelect
          id="benchmark-filter-harness-desktop"
          label={harnessLabel}
          value={state.harness ?? ""}
          options={harnessOptions}
          allLabel={allHarnessesLabel}
          onChange={handleHarnessChange}
        />
        <FilterSelect
          id="benchmark-filter-class-desktop"
          label={classLabel}
          value={state.class ?? ""}
          options={classOptions}
          allLabel={allClassesLabel}
          onChange={handleClassChange}
        />
        {/* `role="status"` (implicit `aria-live="polite"`) — WCAG 4.1.3 Status Messages: a filter
            change never moves focus or scrolls (`scroll: false` above is intentional), so the
            narrowed/widened result count must announce itself to assistive tech instead
            (Rule-15 EWT-004 fix). */}
        <span data-testid={`${SLOT}-result-count`} role="status" className="text-sm text-muted-foreground">
          {t(locale, "aiBenchFilterResultCountLabel")}: {resultCount}
        </span>
      </div>
    </div>
  );
}
