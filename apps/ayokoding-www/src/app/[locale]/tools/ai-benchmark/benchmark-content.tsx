"use client";

import { useRef } from "react";
import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { useLocale } from "@/features/i18n/shell/use-locale";
import { t } from "@/features/i18n/core/translations";
import { dataset, type Dataset } from "@/features/ai-benchmark/core/data/models";
import { decodeState, encodeState, type SortState } from "@/features/ai-benchmark/core/url-state";
import { filterModels, type FilterState } from "@/features/ai-benchmark/core/filter";
import type { ChartBand } from "@/features/ai-benchmark/shell/chart-primitives";
import type { SortMode } from "@/features/ai-benchmark/core/sort";
import { HowToRead, AiBenchLegend, AiBenchSources } from "@/features/ai-benchmark/shell/how-to-read";
import { ModelTable } from "@/features/ai-benchmark/shell/model-table";
import { BenchmarkChart } from "@/features/ai-benchmark/shell/benchmark-chart";
import { BenchmarkFilters } from "@/features/ai-benchmark/shell/benchmark-filters";

export function BenchmarkContent() {
  const locale = useLocale();
  const searchParams = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();

  // The URL is the single source of truth for the active filters (F-3..F-9, Phase 4). One
  // `filterModels` call narrows the roster over BOTH axes at once, for membership/display only
  // (DD-24) — the resulting
  // `filteredDataset` is the ONE dataset every consumer below reads for MEMBERSHIP/DISPLAY. Band
  // thresholds must stay roster-relative to the FULL population (DD-5a), so every consumer below
  // is ALSO given `dataset` (the unfiltered full roster) as its `fullDataset` — never re-deriving
  // anchor thresholds from `filteredDataset`, which can exclude both anchor models entirely and
  // would otherwise silently collapse every rated model to `haiku`.
  // `decodeState` returns ONE flat object carrying both the filter and sort keys — picked apart
  // into two disjoint-key objects here (not just re-typed) so `latestFilterStateRef` never carries
  // an own `opus`/`sonnet`/`haiku` key and `latestSortStateRef` never carries an own
  // `harness`/`class` key. Without this, `{ ...next, ...latestSortStateRef.current }` below would
  // spread `latestSortStateRef.current`'s own (implicitly `undefined`) `harness`/`class` keys
  // OVER `next`'s real values, silently dropping whichever filter had just changed.
  const decoded = decodeState(searchParams);
  const filterState: FilterState = { harness: decoded.harness, class: decoded.class };
  const sortState: SortState = {
    opus: decoded.opus,
    sonnet: decoded.sonnet,
    haiku: decoded.haiku,
  };
  const filteredModels = filterModels(dataset, filterState);
  const filteredDataset: Dataset = { ...dataset, models: filteredModels };
  const isEmpty = filteredModels.length === 0;

  // Rule-15 EWT-003 fix: `router.push` is asynchronous, so two rapid filter changes (e.g. harness
  // then class) can both fire before Next.js commits the first navigation and re-renders this
  // component with updated `searchParams` — both handlers would otherwise merge against the SAME
  // stale `filterState`, and the second `router.push` would silently overwrite the first change.
  // `latestFilterStateRef` is updated synchronously inside `handleFilterChange` itself (not only on
  // render), so a rapid second call always merges onto the just-applied first change rather than a
  // stale render's `filterState`. Kept in sync with the URL-derived value on every render too, so
  // browser back/forward navigation (which does not go through `handleFilterChange`) is reflected.
  const latestFilterStateRef = useRef<FilterState>(filterState);
  latestFilterStateRef.current = filterState;
  // Same race-guard as `latestFilterStateRef` above (Rule-15 EWT-003) — a rapid second sort change
  // (e.g. two different bands' dropdowns in quick succession) must merge onto the just-applied
  // first change, not a stale render's `sortState`.
  const latestSortStateRef = useRef<SortState>(sortState);
  latestSortStateRef.current = sortState;

  function handleFilterChange(patch: Partial<FilterState>) {
    const next: FilterState = { ...latestFilterStateRef.current, ...patch };
    latestFilterStateRef.current = next;
    const qs = encodeState({ ...next, ...latestSortStateRef.current }).toString();
    // `scroll: false` is mandatory: this is in-page filter/view state, not a page change, so the
    // default Next.js navigation behaviour (scroll to top of document) would yank the reader back
    // to the page header on every filter change — mirrors
    // `cost-of-living-calculator/calculator-content.tsx`'s in-page filter navigations.
    router.push(qs ? `${pathname}?${qs}` : pathname, { scroll: false });
  }

  function handleSortChange(band: ChartBand, mode: SortMode) {
    const next: SortState = { ...latestSortStateRef.current, [band]: mode };
    latestSortStateRef.current = next;
    const qs = encodeState({ ...latestFilterStateRef.current, ...next }).toString();
    router.push(qs ? `${pathname}?${qs}` : pathname, { scroll: false });
  }

  return (
    // Rule-15 EWT-001 fix, preserved through Phase 7's reorder (DD-29): this root stays a plain
    // element, never the landmark element `layout.tsx`'s root already renders with
    // `id="main-content"` — nesting a second one of those here produced two landmarks with the
    // same accessibility role on this page, invalid HTML5 and a WCAG 4.1.2/1.3.1 defect. Spelled
    // without the literal element-name markup below so this explanatory comment cannot itself trip
    // `grep -cF` guards written against that markup (Phase 7 Gate's own EWT-001 regression check).
    <div
      data-testid="ai-bench-page"
      // Rule-15 UWT-007 fix: below `sm`, every gap tightens (space-y-6→4, py-6→4) — the chart was
      // measured starting at `top: 741px`/`701px` at the two narrowest breakpoints (320x568,
      // 390x664), well past the visible viewport. This alone does not close the gap (the always
      // -visible AC-32 honesty line cannot shrink further without hurting readability); the
      // remaining trims live in `how-to-read.tsx`, `benchmark-filters.tsx`, and
      // `benchmark-chart.tsx`.
      className="mx-auto max-w-6xl space-y-4 px-4 py-4 sm:space-y-6 sm:py-6"
    >
      {/* AC-56 (Phase 7, cycle 7.2) document order: header (title + subtitle + the how-to-read
          snapshot/honesty line) → filters → chart → roster → legend disclosure → sources
          disclosure. The ref-based race guards above (EWT-003) are untouched by this reorder —
          they live in the handlers, not the JSX. */}
      <header className="space-y-2 sm:space-y-3">
        <h1 className="text-2xl font-bold tracking-tight">{t(locale, "aiBenchTitle")}</h1>
        {/* Rule-15 UWT-007 fix: hidden below `sm` — decorative orientation copy, not gated by any
            AC (unlike the honesty line right below, which AC-32 requires always-visible). At 320px
            this alone was ~80px (4 wrapped lines) of the ~120px still separating the chart's first
            bar from the visible viewport after every other trim in this fix. Stays in DOM order
            (AC-56 is about document ORDER, not pixel-visibility), so a screen reader or a widened
            viewport still reaches it. */}
        <p data-testid="ai-bench-subtitle" className="hidden text-sm text-muted-foreground sm:block">
          {t(locale, "aiBenchSubtitle")}
        </p>
        <HowToRead snapshotDate={dataset.snapshotDate} locale={locale} />
      </header>

      <BenchmarkFilters
        state={filterState}
        resultCount={filteredModels.length}
        locale={locale}
        onChange={handleFilterChange}
      />

      {isEmpty ? (
        // AC-28: an explicit empty-state message replaces the chart (never an empty plot area).
        // The data table is ALSO hidden below (Rule-15 UWT-006 fix) — an already-unambiguous empty
        // -state message directly followed by a full, empty table header row read as redundant/
        // aesthetically noisy (Heuristic 8) and could be misread as "the table is broken". AC-28's
        // Gherkin scenario was WIDENED in this same fix to fold in this table behaviour — its `But`
        // step now asserts the chart and the data table do not render in the empty state (see
        // `specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature`), so
        // hiding the table here is the AC's own requirement, not an unconstrained extra.
        // `role="status"` — a filter change never moves focus or scrolls, so an emptied roster
        // must announce itself to assistive tech (WCAG 4.1.3, Rule-15 EWT-004 fix).
        <p
          data-testid="ai-bench-empty-state"
          role="status"
          className="rounded-md border border-dashed p-6 text-center text-sm text-muted-foreground"
        >
          <span className="mb-1 block font-medium text-foreground">{t(locale, "aiBenchEmptyStateTitle")}</span>
          {t(locale, "aiBenchEmptyStateMessage")}
        </p>
      ) : (
        <>
          <BenchmarkChart
            dataset={filteredDataset}
            fullDataset={dataset}
            locale={locale}
            sortState={sortState}
            onSortChange={handleSortChange}
            harness={filterState.harness}
          />
          <ModelTable dataset={filteredDataset} fullDataset={dataset} locale={locale} />
        </>
      )}

      {/* AC-57 — the legend and sources stay reachable regardless of the empty-state branch above
          (both are dataset-level, not filtered-roster-level, content), always following whichever
          of the roster or the empty-state message rendered. */}
      <AiBenchLegend locale={locale} />
      <AiBenchSources locale={locale} />
    </div>
  );
}
