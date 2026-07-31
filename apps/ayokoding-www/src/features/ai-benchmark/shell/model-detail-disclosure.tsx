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
import { DETAIL_FIELD_LABEL_CLASS, DETAIL_FIELD_VALUE_CLASS, type FigureGroup } from "./model-figures";

export type ModelDetailDisclosureProps = {
  slot: string;
  modelId: string;
  /** Built by `model-figures.tsx`'s `buildDetailGroups` (DD-34 Treatment 3) — always exactly two groups. */
  groups: FigureGroup[];
  locale: Locale;
};

export function ModelDetailDisclosure({ slot, modelId, groups, locale }: ModelDetailDisclosureProps) {
  return (
    <details data-testid={`${slot}-details-${modelId}`}>
      <summary data-testid={`${slot}-disclosure-${modelId}`}>{t(locale, "aiBenchCardAllFigures")}</summary>
      {groups.map((group) => (
        // DD-34 Treatment 3 (DN-3 fix): each group is its own <section>, headed by an <h4> one
        // level below the card's own <h3> model name — a heading is not valid <dl> content, so the
        // heading and its <dl> both live inside the section rather than the heading floating above
        // a single flat list.
        <section key={group.heading} className="mt-3 first:mt-2">
          <h4 className="text-xs font-semibold tracking-wide text-muted-foreground uppercase">{group.heading}</h4>
          <dl className="mt-1 space-y-2 text-sm">
            {group.figures.map((fig) => (
              // DD-34 Treatment 2 (DN-2 fix): a `<dt>`/`<dd>` rail row rather than the old stacked
              // pair — the label sits in a fixed-width first column so the (now `inline`-layout)
              // value + evidence badge can flow on the SAME row instead of costing a third line box.
              <div
                key={fig.label}
                className="grid grid-cols-[6.5rem_1fr] items-baseline gap-x-2 gap-y-0.5 md:grid-cols-[9rem_1fr]"
              >
                <dt className={`${DETAIL_FIELD_LABEL_CLASS} m-0 text-left`}>{fig.label}</dt>
                <dd className={`${DETAIL_FIELD_VALUE_CLASS} m-0 text-left`}>{fig.node}</dd>
              </div>
            ))}
          </dl>
        </section>
      ))}
    </details>
  );
}
