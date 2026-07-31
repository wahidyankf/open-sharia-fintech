// AI BENCHMARK — shared per-model "remaining figures" disclosure (Phase 6, DD-28/DD-34).
//
// Both the mobile roster card (`model-card.tsx`) and the desktop table's per-row detail region
// (`model-table.tsx`) reveal the SAME shape of content behind a native `<details>`/`<summary>`
// disclosure: a `<dl>` of the figures that don't fit the always-visible summary. Sharing this one
// component means DD-34's Treatments 1-4 (cycles 6.4-6.7) are applied ONCE here rather than twice,
// so the card and the table's detail region cannot drift apart in typography, layout, or grouping.
//
// `slot` lets each caller keep its own established `data-testid` prefix (`model-card` /
// `model-table`) so this extraction changes no existing test's selectors.

import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import type { ModelFigure } from "./model-figures";

export type ModelDetailDisclosureProps = {
  slot: string;
  modelId: string;
  figures: ModelFigure[];
  locale: Locale;
};

export function ModelDetailDisclosure({ slot, modelId, figures, locale }: ModelDetailDisclosureProps) {
  return (
    <details data-testid={`${slot}-details-${modelId}`}>
      <summary data-testid={`${slot}-disclosure-${modelId}`}>{t(locale, "aiBenchCardAllFigures")}</summary>
      <dl className="mt-2 space-y-2 text-sm">
        {figures.map((fig) => (
          <div key={fig.label} className="flex flex-col gap-0.5">
            <dt className="text-xs font-medium text-muted-foreground">{fig.label}</dt>
            <dd>{fig.node}</dd>
          </div>
        ))}
      </dl>
    </details>
  );
}
