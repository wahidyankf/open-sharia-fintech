"use client";

import { useLocale } from "@/features/i18n/shell/use-locale";
import { t } from "@/features/i18n/core/translations";
import { dataset } from "@/features/ai-benchmark/core/data/models";
import { HowToRead } from "@/features/ai-benchmark/shell/how-to-read";
import { ModelTable } from "@/features/ai-benchmark/shell/model-table";
import { CapabilityChart } from "@/features/ai-benchmark/shell/capability-chart";

export function BenchmarkContent() {
  const locale = useLocale();
  return (
    <main data-testid="ai-bench-page" className="mx-auto max-w-6xl space-y-6 px-4 py-6">
      <header className="space-y-1">
        <h1 className="text-2xl font-bold tracking-tight">{t(locale, "aiBenchTitle")}</h1>
        <p data-testid="ai-bench-subtitle" className="text-sm text-muted-foreground">
          {t(locale, "aiBenchSubtitle")}
        </p>
      </header>

      <HowToRead snapshotDate={dataset.snapshotDate} locale={locale} />

      <CapabilityChart dataset={dataset} locale={locale} />

      <ModelTable dataset={dataset} locale={locale} />
    </main>
  );
}
