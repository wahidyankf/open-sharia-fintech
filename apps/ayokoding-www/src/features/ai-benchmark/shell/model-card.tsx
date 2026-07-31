// AI BENCHMARK — collapsed roster summary card with a per-card disclosure (Phase 6, DD-28).
//
// Below `md`, each model renders as this card: an always-visible summary (name, class, composite
// index, price) plus the remaining figures inside a native `<details>`, closed by default. Native
// `<details>`/`<summary>` (not a JS accordion) gives correct `aria-expanded` semantics, keyboard
// operation, and find-in-page expansion for free, and works without client JS.
//
// W-26/W-30 parity: the summary and the expanded content are two slices of the SAME shared figure
// list `./model-figures` builds — the same `renderBenchmarkFigures`/`renderStaticFigures` the
// desktop table calls — so the card and the table can never drift to show different figure sets
// for the same model (AC-54).
//
// FCIS boundary: no literal figure, price, model name, or threshold lives here — every number
// comes from the passed `model`/`view` via the pure `core/` selectors, formatted by `shell/format.ts`.

import { t } from "@/features/i18n/core/translations";
import type { Locale } from "@/features/i18n/core/config";
import type { Model } from "../core/data/models";
import { HARNESS_DISPLAY_NAMES } from "../core/data/benchmarks";
import {
  classLabel,
  integrityNotes,
  renderBenchmarkFigures,
  renderStaticFigures,
  type ModelFigure,
  type ScoreView,
} from "./model-figures";

const SLOT = "model-card";

export type ModelCardProps = {
  model: Model;
  view: ScoreView;
  locale: Locale;
};

export function ModelCard({ model, view, locale }: ModelCardProps) {
  const staticFigures = renderStaticFigures(model, view, locale);
  const benchmarkFigures = renderBenchmarkFigures(model, locale);

  // The summary carries index and price (DD-28); the remaining static figure (coverage) joins the
  // benchmark figures inside the disclosure. Partitioning by LABEL match — rather than duplicating
  // the underlying index/price selection logic — keeps this the ONLY place that decides which
  // slice of the shared list is always-visible (W-30: parity holds by construction).
  const indexLabel = t(locale, "aiBenchColIndex");
  const inputLabel = t(locale, "aiBenchColInputPrice");
  const outputLabel = t(locale, "aiBenchColOutputPrice");
  const indexFigure = staticFigures.find((f) => f.label === indexLabel);
  const inputFigure = staticFigures.find((f) => f.label === inputLabel);
  const outputFigure = staticFigures.find((f) => f.label === outputLabel);
  const detailStaticFigures = staticFigures.filter(
    (f) => f.label !== indexLabel && f.label !== inputLabel && f.label !== outputLabel,
  );
  // A subscription rate (or a genuinely absent price) reuses the SAME rendered node for input and
  // output (`model-figures.tsx`'s `priceCells`) — referential equality collapses that duplicate
  // node to a single visible price in the summary rather than showing the identical text twice.
  const samePrice = inputFigure !== undefined && inputFigure.node === outputFigure?.node;

  const harnessNames = model.harnesses.map((h) => HARNESS_DISPLAY_NAMES[h] ?? h).join(", ");
  const detailFigures: ModelFigure[] = [
    { label: t(locale, "aiBenchColVendor"), node: <span>{model.vendor}</span> },
    { label: t(locale, "aiBenchColHarnesses"), node: <span>{harnessNames}</span> },
    ...benchmarkFigures,
    ...detailStaticFigures,
  ];

  return (
    <li data-slot={SLOT} data-testid={`${SLOT}-${model.id}`} data-model-id={model.id} className="rounded-md border p-3">
      <div data-slot={`${SLOT}-summary`} data-testid={`${SLOT}-summary-${model.id}`}>
        <div className="flex flex-wrap items-baseline justify-between gap-x-2">
          <h3 className="text-base font-semibold" data-slot="model-name" data-testid={`${SLOT}-name-${model.id}`}>
            {model.name}
          </h3>
          <span data-testid={`${SLOT}-class-${model.id}`} className="text-sm text-muted-foreground">
            {classLabel(view.band, locale)}
          </span>
        </div>
        {integrityNotes(model, locale)}
        <div
          className="mt-1 flex flex-wrap items-baseline gap-x-3 text-sm"
          data-testid={`${SLOT}-index-price-${model.id}`}
        >
          {indexFigure ? <span data-testid={`${SLOT}-index-${model.id}`}>{indexFigure.node}</span> : null}
          <span data-testid={`${SLOT}-price-${model.id}`} className="inline-flex flex-wrap items-baseline gap-x-2">
            {samePrice ? (
              <span data-testid={`${SLOT}-price-single-${model.id}`}>{inputFigure?.node}</span>
            ) : (
              <>
                {inputFigure ? <span data-testid={`${SLOT}-price-in-${model.id}`}>{inputFigure.node}</span> : null}
                {outputFigure ? <span data-testid={`${SLOT}-price-out-${model.id}`}>{outputFigure.node}</span> : null}
              </>
            )}
          </span>
        </div>
      </div>
      <details data-testid={`${SLOT}-details-${model.id}`}>
        <summary data-testid={`${SLOT}-disclosure-${model.id}`}>{t(locale, "aiBenchCardAllFigures")}</summary>
        <dl className="mt-2 space-y-2 text-sm">
          {detailFigures.map((fig) => (
            <div key={fig.label} className="flex flex-col gap-0.5">
              <dt className="text-xs font-medium text-muted-foreground">{fig.label}</dt>
              <dd>{fig.node}</dd>
            </div>
          ))}
        </dl>
      </details>
    </li>
  );
}
