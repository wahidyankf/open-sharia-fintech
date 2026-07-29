"use client";

import { useRouter, useSearchParams, usePathname } from "next/navigation";
import { useLocale } from "@/features/i18n/shell/use-locale";
import { t } from "@/features/i18n/core/translations";
import { dataset, type Dataset } from "@/features/ai-benchmark/core/data/models";
import { decodeState, encodeState } from "@/features/ai-benchmark/core/url-state";
import { filterModels, type FilterState } from "@/features/ai-benchmark/core/filter";
import { HowToRead } from "@/features/ai-benchmark/shell/how-to-read";
import { ModelTable } from "@/features/ai-benchmark/shell/model-table";
import { CapabilityChart } from "@/features/ai-benchmark/shell/capability-chart";
import { PriceChart } from "@/features/ai-benchmark/shell/price-chart";
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
  const filterState: FilterState = decodeState(searchParams);
  const filteredModels = filterModels(dataset, filterState);
  const filteredDataset: Dataset = { ...dataset, models: filteredModels };
  const isEmpty = filteredModels.length === 0;

  function handleFilterChange(next: FilterState) {
    const qs = encodeState(next).toString();
    // `scroll: false` is mandatory: this is in-page filter/view state, not a page change, so the
    // default Next.js navigation behaviour (scroll to top of document) would yank the reader back
    // to the page header on every filter change — mirrors
    // `cost-of-living-calculator/calculator-content.tsx`'s in-page filter navigations.
    router.push(qs ? `${pathname}?${qs}` : pathname, { scroll: false });
  }

  return (
    <main data-testid="ai-bench-page" className="mx-auto max-w-6xl space-y-6 px-4 py-6">
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
        // AC-28: an explicit empty-state message replaces both charts (never an empty plot area) —
        // the data table still renders below (a header with zero body rows is not "empty" in the
        // AC's sense; every model's figures already read as "not reported" the same way elsewhere).
        <p
          data-testid="ai-bench-empty-state"
          className="rounded-md border border-dashed p-6 text-center text-sm text-muted-foreground"
        >
          <span className="mb-1 block font-medium text-foreground">{t(locale, "aiBenchEmptyStateTitle")}</span>
          {t(locale, "aiBenchEmptyStateMessage")}
        </p>
      ) : (
        <>
          <CapabilityChart dataset={filteredDataset} fullDataset={dataset} locale={locale} />
          <PriceChart dataset={filteredDataset} fullDataset={dataset} locale={locale} harness={filterState.harness} />
        </>
      )}

      <ModelTable dataset={filteredDataset} fullDataset={dataset} locale={locale} />
    </main>
  );
}
