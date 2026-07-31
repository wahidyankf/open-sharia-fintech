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
import {
  DETAIL_FIELD_LABEL_CLASS,
  DETAIL_FIELD_VALUE_CLASS,
  type FigureGroup,
  type ModelFigure,
} from "./model-figures";
import { TAP_TARGET_MIN_CLASS } from "./tap-target";

export type ModelDetailDisclosureProps = {
  slot: string;
  modelId: string;
  /** Built by `model-figures.tsx`'s `buildDetailGroups` (DD-34 Treatment 3) — always exactly two groups. */
  groups: FigureGroup[];
  locale: Locale;
};

/**
 * DD-34 Treatment 4 (DN-4 fix, tech-docs.md §Treatment 4 — absent figures collapse into one
 * shared-value run): renders one group's figures, but collapses every unpublished figure
 * (`reported === false`) into ONE shared trailing name-value pair — many `<dt>` terms, one `<dd>`
 * description — instead of giving each one its own full field slot at the same visual weight as a
 * real, measured figure. W-26/W-30 parity is preserved by construction, not by a second assertion:
 * every absent label is STILL a real `<dt>` in the DOM for every one of them — nothing is removed,
 * only regrouped; only the number of `<dd>`s shrinks from one-per-absent-figure to one shared.
 */
function GroupFigures({ figures, locale }: { figures: ModelFigure[]; locale: Locale }) {
  const reportedFigures = figures.filter((fig) => fig.reported !== false);
  const unreportedFigures = figures.filter((fig) => fig.reported === false);
  return (
    <>
      {reportedFigures.map((fig) => (
        // DD-34 Treatment 2 (DN-2 fix): a `<dt>`/`<dd>` rail row rather than the old stacked pair —
        // the label sits in a fixed-width first column so the (now `inline`-layout) value +
        // evidence badge can flow on the SAME row instead of costing a third line box.
        <div
          key={fig.label}
          className="grid grid-cols-[6.5rem_1fr] items-baseline gap-x-2 gap-y-0.5 md:grid-cols-[9rem_1fr]"
        >
          <dt className={`${DETAIL_FIELD_LABEL_CLASS} m-0 text-left`}>{fig.label}</dt>
          <dd className={`${DETAIL_FIELD_VALUE_CLASS} m-0 text-left`}>{fig.node}</dd>
        </div>
      ))}
      {unreportedFigures.length > 0 ? (
        // Rule-15 DWT-006 fix, corrected by the Phase 12 PR review (finding F3): the collapsed run
        // used to be a single `flex flex-wrap` row, so its `<dd>` sat flush against its own `<dt>`
        // run instead of the fixed-width rail column every REPORTED figure's `<dd>` above already
        // aligns to (Treatment 2) — a visible ~61px left-edge gap. The DWT-006 fix closed that gap
        // by wrapping the `<dt>` run in its own `<div>` inside this grid cell — but a `<div>` wrapping
        // `<dt>`s is not permitted content for a `dl > div` (MDN's `<dl>` content model: a `dl`'s
        // `<div>` child may directly contain only `<dt>`s then `<dd>`s, intermixed with
        // script-supporting elements — never a nested element wrapping the `<dt>`s). Fixed here by
        // making every `<dt>` a DIRECT child of this grid `<div>` (each pinned to the label column
        // via `col-start-1`, so grid auto-placement — which would otherwise route every other item
        // into the value column — cannot misplace them) and giving the shared `<dd>` an explicit
        // `gridRow` span covering exactly as many rows as there are unreported labels, so it stays
        // vertically centred beside the whole stacked label run. `GroupFigures`'s own docstring above
        // still holds: every absent label is STILL a real `<dt>` in the DOM, one per unreported
        // figure — only the wrapping element changed, not the element count.
        <div className="grid grid-cols-[6.5rem_1fr] items-baseline gap-x-2 gap-y-0.5 md:grid-cols-[9rem_1fr]">
          {unreportedFigures.map((fig, i) => (
            <dt key={fig.label} className={`${DETAIL_FIELD_LABEL_CLASS} col-start-1 m-0 text-left`}>
              {fig.label}
              {i < unreportedFigures.length - 1 ? "," : ""}
            </dt>
          ))}
          <dd
            className={`${DETAIL_FIELD_VALUE_CLASS} col-start-2 m-0 self-center text-left`}
            style={{ gridRow: `1 / span ${unreportedFigures.length}` }}
            data-slot="figure-cell-value"
          >
            {t(locale, "aiBenchNoFigure")}
          </dd>
        </div>
      ) : null}
    </>
  );
}

export function ModelDetailDisclosure({ slot, modelId, groups, locale }: ModelDetailDisclosureProps) {
  return (
    <details data-testid={`${slot}-details-${modelId}`}>
      {/* DD-30/AC-58: a 24x24 CSS px minimum tap target (WCAG 2.5.8) — see `tap-target.ts`. */}
      <summary data-testid={`${slot}-disclosure-${modelId}`} className={TAP_TARGET_MIN_CLASS}>
        {t(locale, "aiBenchCardAllFigures")}
      </summary>
      {groups.map((group) => (
        // DD-34 Treatment 3 (DN-3 fix): each group is its own <section>, headed by an <h4> one
        // level below the card's own <h3> model name — a heading is not valid <dl> content, so the
        // heading and its <dl> both live inside the section rather than the heading floating above
        // a single flat list.
        <section key={group.heading} className="mt-3 first:mt-2">
          <h4 className="text-xs font-semibold tracking-wide text-muted-foreground uppercase">{group.heading}</h4>
          <dl className="mt-1 space-y-2 text-sm">
            <GroupFigures figures={group.figures} locale={locale} />
          </dl>
        </section>
      ))}
    </details>
  );
}
