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
import { HowToRead } from "@/features/ai-benchmark/shell/how-to-read";
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
  // would otherwise silently collapse every rated model to `light`.
  // `decodeState` returns ONE flat object carrying both the filter and sort keys — picked apart
  // into two disjoint-key objects here (not just re-typed) so `latestFilterStateRef` never carries
  // an own `opus`/`sonnet`/`light` key and `latestSortStateRef` never carries an own
  // `harness`/`class` key. Without this, `{ ...next, ...latestSortStateRef.current }` below would
  // spread `latestSortStateRef.current`'s own (implicitly `undefined`) `harness`/`class` keys
  // OVER `next`'s real values, silently dropping whichever filter had just changed.
  const decoded = decodeState(searchParams);
  const filterState: FilterState = { harness: decoded.harness, class: decoded.class };
  const sortState: SortState = {
    opus: decoded.opus,
    sonnet: decoded.sonnet,
    light: decoded.light,
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
    // A plain `<div>`, not `<main>` — `layout.tsx`'s `<main id="main-content">` is already the
    // page's one landmark; a second nested `<main>` here produced two `role="main"` landmarks on
    // this page, invalid HTML5 and a WCAG 4.1.2/1.3.1 defect (Rule-15 EWT-001 fix).
    <div data-testid="ai-bench-page" className="mx-auto max-w-6xl space-y-6 px-4 py-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight">{t(locale, "aiBenchTitle")}</h1>
        <p data-testid="ai-bench-subtitle" className="text-sm text-muted-foreground">
          {t(locale, "aiBenchSubtitle")}
        </p>
      </header>

      <HowToRead snapshotDate={dataset.snapshotDate} locale={locale} />

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
        // `specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature`), so
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
    </div>
  );
}
