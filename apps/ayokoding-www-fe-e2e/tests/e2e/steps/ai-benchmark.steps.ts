import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";
import type { Page } from "@playwright/test";

const { Given, When, Then } = createBdd();

// AI Benchmark e2e step bindings. AC-1, AC-2, and AC-36 are the scenarios bound at the e2e layer
// in this plan; every other scenario is permanently unit-only (see DD-22 in tech-docs.md) and
// renders as `test.fixme` under this project's `missingSteps: "skip-scenario"` config — they are
// not deferred pending a later e2e binding.

// The active locale for the scenario — set by "Given the locale is …" and read by the navigation
// step. Module-scoped because playwright-bdd step functions are stateless over the fixture context.
let scenarioLocale = "en";

// ── Preconditions ─────────────────────────────────────────────────────────────

// Background step — the dataset is always loaded on the served page; nothing to set up. The empty
// fixture destructuring is the playwright-bdd idiom for a fixture-less step (an `no-empty-pattern`
// lint warning, non-failing, matching the project's generated step files).
Given("the AI benchmark dataset is loaded", async ({}) => {});

Given("the locale is {string}", async ({}, locale: string) => {
  scenarioLocale = locale;
});

// AC-36's precondition. The generic "the page renders" step (bound elsewhere, shared across
// features) only waits for load state, so navigation happens here.
Given("the full roster is loaded", async ({ page }) => {
  await page.goto(`/${scenarioLocale}/tools/ai-benchmark`);
});

// ── Navigation ────────────────────────────────────────────────────────────────

When("the AI benchmark page renders", async ({ page }) => {
  await page.goto(`/${scenarioLocale}/tools/ai-benchmark`);
  await page.waitForLoadState("networkidle");
});

// ── Page shell assertions (AC-1 / AC-2) ───────────────────────────────────────

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The English page renders its localized heading
Then("the page shows a level-one heading in English", async ({ page }) => {
  const h1 = page.locator("h1").first();
  await expect(h1).toBeVisible();
  const text = (await h1.textContent()) ?? "";
  expect(text.trim().length).toBeGreaterThan(0);
  // The served English H1 must carry the English copy, not the Indonesian one.
  expect(text.trim()).not.toBe("Tolok Ukur Model AI");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The Indonesian page renders its localized heading
Then("the page shows a level-one heading in Indonesian", async ({ page }) => {
  const h1 = page.locator("h1").first();
  await expect(h1).toBeVisible();
  const text = (await h1.textContent()) ?? "";
  expect(text.trim().length).toBeGreaterThan(0);
  // The served Indonesian H1 must carry the localized copy, distinct from English.
  expect(text.trim()).not.toBe("AI Model Benchmark");
});

Then("the document language attribute is {string}", async ({ page }, expectedLang: string) => {
  // The root layout sets <html lang> from the locale URL segment.
  await expect(page.locator("html")).toHaveAttribute("lang", expectedLang);
});

// ── Chart accessible-name assertion (AC-36) ───────────────────────────────────

// DD-25 reword (Phase 5, 2026-07-31): the chart no longer renders any svg — each rated band's own
// DOM region instead carries `role="group"` with `aria-labelledby` (`benchmark-chart-band-{opus,
// sonnet,haiku}`), not one shared svg — the first band's own region is enough to prove the family
// carries a real accessible name.
// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The merged chart exposes an accessible name
Then("each rated band's chart region exposes a localized accessible name", async ({ page }) => {
  await expect(page.locator('[data-testid^="benchmark-chart-band-"][role="group"]').first()).toHaveAccessibleName(/.+/);
});

// ── Phase 8 — harness and class filters (AC-18, AC-22, AC-27) ─────────────────
// These three scenarios are also bound at the unit layer (test/unit/fe-steps/ai-benchmark.steps.tsx)
// — real browser navigation here proves the SAME behaviour survives an actual production request,
// not just a mocked render. "When the page renders" is already registered globally
// (cost-of-living-calculator.steps.ts) as a bare `waitForLoadState`, so navigation happens in each
// scenario's own Given/When step here, not there.

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The page with no query parameters shows the whole roster
Given("the URL carries no query parameters", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The page with no query parameters shows the whole roster
Then("every roster model is shown in the data table", async ({ page }) => {
  await page.waitForLoadState("networkidle");
  // Appendix A.2 roster — see apps/ayokoding-www's core/data/models.ts's own "38 rows" comment.
  await expect(page.locator('[data-testid="model-table-desktop"] tbody tr[data-model-id]')).toHaveCount(38);
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A harness filter switches the merged chart to that harness's rate
Given("a fixture model priced differently by two harnesses", async ({}) => {
  // The e2e layer exercises the REAL roster (no fixture injection over HTTP) — Grok 4.5
  // (core/data/models.ts) is genuinely priced differently by two harnesses: cursor/opencode-zen at
  // a metered $2/$6 rate, opencode-go at a flat-rate subscription instead.
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A harness filter switches the merged chart to that harness's rate
When("the merged chart renders with that harness selected", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark?harness=opencode-go");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A harness filter switches the merged chart to that harness's rate
Then("that model's price bars use that harness's own rate, not its lowest available rate", async ({ page }) => {
  // opencode-go carries Grok 4.5 as a flat-rate subscription, not a per-token rate — selecting it
  // must remove Grok 4.5's metered bar and show its inline subscription text instead (DD-1).
  await expect(page.getByTestId("benchmark-chart-bar-price-in-grok-4.5")).toHaveCount(0);
  await expect(page.getByTestId("benchmark-chart-subscription-grok-4.5")).toBeVisible();
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
Given("the reader has applied a harness filter and a class filter", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark?harness=cursor&class=opus");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
When("the reader reloads the resulting URL", async ({ page }) => {
  await page.reload();
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
Then("the same filtered set of models is shown", async ({ page }) => {
  const rowIds = () =>
    page
      .locator('[data-testid="model-table-desktop"] tbody tr[data-model-id]')
      .evaluateAll((els) => els.map((el) => el.getAttribute("data-model-id")));

  const idsAfterReload = (await rowIds()).sort();

  // Idempotence check: a FRESH, independent navigation to the exact same URL must decode to the
  // identical filtered set the reload just showed — proving the URL alone (not any client-side
  // navigation history) determines the view.
  await page.goto("/en/tools/ai-benchmark?harness=cursor&class=opus");
  await page.waitForLoadState("networkidle");
  const idsFreshLoad = (await rowIds()).sort();

  expect(idsAfterReload).toEqual(idsFreshLoad);
  // A genuine narrowing — neither empty (that combination has matches on the live roster) nor the
  // full 38-row roster (the filters really did narrow it).
  expect(idsAfterReload.length).toBeGreaterThan(0);
  expect(idsAfterReload.length).toBeLessThan(38);
});

// ── AC-38 — live-page band-token contrast (Phase 9, M-11/M-12) ────────────────
//
// jsdom cannot resolve `oklch()` custom properties through a cascade (see
// `shell/band-tokens.unit.test.ts`'s own docstring and tech-docs.md §Band design tokens), so this
// assertion reads the tokens' ACTUAL resolved colours from a real browser and computes the WCAG
// contrast ratio itself — there is no third-party a11y-audit dependency in this repo to lean on.
//
// The four band tokens all share ONE `-ink` value and ONE `-wash` value per theme (see
// `libs/web-ui-token/src/ayokoding.css`) — only the BASE (`--chart-band-<band>`) hue differs
// per band, and the chart currently renders no `-wash` as an actual background (see
// `tech-docs.md`'s "Feature gating" is unrelated; the relevant note is in the Band design tokens
// section: "-ink/-wash pair provides the text-on-background contrast" — a token-level contract,
// not tied to any one component's current usage). Reading the CSS custom properties directly,
// exactly as declared, is therefore the correct level to assert this at — not by locating one
// particular rendered DOM element.

const BAND_IDS = ["opus", "sonnet", "haiku", "unrated"] as const;

// The three bands that actually render as a bar (`benchmark-chart.tsx` never plots `unrated` as
// a bar — it is a plain text list) — the base/bar-fill token `--chart-band-<band>` against
// `--color-background` (the page background a bar renders directly onto) is the pair the M-14 fix
// (delivery.md, Phase 9 Round 1a) actually changed and the one WCAG 1.4.11's 3:1 non-text minimum
// applies to; `unrated`'s base token was never implicated (it aliases the neutral `--warm-400`).
const RATED_BAND_IDS = ["opus", "sonnet", "haiku"] as const;

const WCAG_NON_TEXT_MIN_CONTRAST = 3.0;

type Rgb = readonly [number, number, number];

/** WCAG relative luminance (https://www.w3.org/TR/WCAG21/#dfn-relative-luminance). */
function relativeLuminance([r, g, b]: Rgb): number {
  const toLinear = (c: number): number => {
    const s = c / 255;
    return s <= 0.04045 ? s / 12.92 : Math.pow((s + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * toLinear(r) + 0.7152 * toLinear(g) + 0.0722 * toLinear(b);
}

/** WCAG contrast ratio (https://www.w3.org/TR/WCAG21/#dfn-contrast-ratio) — always ≥ 1. */
function contrastRatio(a: Rgb, b: Rgb): number {
  const l1 = relativeLuminance(a);
  const l2 = relativeLuminance(b);
  const [lighter, darker] = l1 > l2 ? [l1, l2] : [l2, l1];
  return (lighter + 0.05) / (darker + 0.05);
}

const WCAG_AA_MIN_CONTRAST = 4.5;

// Populated by the "the computed styles of the band tokens are read" step, read by the assertion
// step — module-scoped for the same reason `scenarioLocale` is above (stateless step functions).
let bandContrastRatios: Record<(typeof BAND_IDS)[number], number> = {
  opus: 0,
  sonnet: 0,
  haiku: 0,
  unrated: 0,
};

// Populated alongside `bandContrastRatios` — the base/bar-fill token vs `--color-background` pair
// the M-14 fix actually protects (pr-review-synthesis-maker HIGH finding, PR #122 cycle 1: the
// `-ink`/`-wash` assertion above never reads this pair, so it could not have caught the real
// regression this session found and fixed).
let bandBaseContrastRatios: Record<(typeof RATED_BAND_IDS)[number], number> = {
  opus: 0,
  sonnet: 0,
  haiku: 0,
};

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Band colours meet contrast in both themes
Given("the page is rendered in the {string} theme", async ({ page }, theme: string) => {
  await page.goto(`/${scenarioLocale}/tools/ai-benchmark`);
  await page.waitForLoadState("networkidle");
  // next-themes applies dark mode as a `class="dark"` on `<html>` (see
  // `apps/ayokoding-www/src/app/[locale]/layout.tsx`'s `<ThemeProvider attribute="class" ...>`),
  // which is exactly the selector `libs/web-ui-token/src/ayokoding.css`'s dark override block
  // matches (`[data-theme="dark"], .dark`). Setting the class directly is deterministic and avoids
  // coupling this token-contrast assertion to the theme-toggle dropdown's own interaction path.
  if (theme === "dark") {
    await page.evaluate(() => document.documentElement.classList.add("dark"));
  } else {
    await page.evaluate(() => document.documentElement.classList.remove("dark"));
  }
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Band colours meet contrast in both themes
When("the computed styles of the band tokens are read from the live page", async ({ page }) => {
  // The colour-SYNTAX resolution (`oklch()`/`lab()`/nested `var()` → concrete sRGB bytes) can only
  // happen inside the browser — a `<canvas>` 2D context is the one API guaranteed to fully
  // rasterize any CSS colour a browser accepts, regardless of which serialization
  // `getComputedStyle` itself reports. The WCAG relative-luminance/contrast MATH that follows is
  // plain arithmetic over those bytes, so it runs here in Node instead of being re-serialized into
  // the page — one browser round-trip per theme, not four.
  const rgbByBand = await page.evaluate(
    (args: { bands: readonly string[]; ratedBands: readonly string[] }) => {
      function resolvedRgb(colorValue: string): [number, number, number] {
        const canvas = document.createElement("canvas");
        canvas.width = 1;
        canvas.height = 1;
        const ctx = canvas.getContext("2d");
        if (!ctx) throw new Error("2D canvas context unavailable");
        ctx.fillStyle = colorValue;
        ctx.fillRect(0, 0, 1, 1);
        const data = ctx.getImageData(0, 0, 1, 1).data;
        return [data[0] ?? 0, data[1] ?? 0, data[2] ?? 0];
      }
      function resolvedVarRgb(varExpr: string): [number, number, number] {
        const probe = document.createElement("div");
        probe.style.color = varExpr;
        document.body.appendChild(probe);
        const resolved = getComputedStyle(probe).color;
        document.body.removeChild(probe);
        return resolvedRgb(resolved);
      }
      const out: Record<string, { ink: [number, number, number]; wash: [number, number, number] }> = {};
      for (const band of args.bands) {
        out[band] = {
          ink: resolvedVarRgb(`var(--chart-band-${band}-ink)`),
          wash: resolvedVarRgb(`var(--chart-band-${band}-wash)`),
        };
      }
      const background = resolvedVarRgb("var(--color-background)");
      const baseByBand: Record<string, [number, number, number]> = {};
      for (const band of args.ratedBands) {
        baseByBand[band] = resolvedVarRgb(`var(--chart-band-${band})`);
      }
      return { pairs: out, background, baseByBand };
    },
    { bands: BAND_IDS, ratedBands: RATED_BAND_IDS },
  );

  const next = { ...bandContrastRatios };
  for (const band of BAND_IDS) {
    const entry = rgbByBand.pairs[band];
    if (!entry) throw new Error(`No resolved RGB pair for band "${band}"`);
    next[band] = contrastRatio(entry.ink, entry.wash);
  }
  bandContrastRatios = next;

  const nextBase = { ...bandBaseContrastRatios };
  for (const band of RATED_BAND_IDS) {
    const baseRgb = rgbByBand.baseByBand[band];
    if (!baseRgb) throw new Error(`No resolved base RGB for band "${band}"`);
    nextBase[band] = contrastRatio(baseRgb, rgbByBand.background);
  }
  bandBaseContrastRatios = nextBase;
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Band colours meet contrast in both themes
Then("every band token meets the WCAG AA contrast ratio against its background", async ({}) => {
  for (const band of BAND_IDS) {
    expect(
      bandContrastRatios[band],
      `--chart-band-${band}-ink vs --chart-band-${band}-wash contrast ratio`,
    ).toBeGreaterThanOrEqual(WCAG_AA_MIN_CONTRAST);
  }
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Band colours meet contrast in both themes
//
// The assertion the M-14 fix (Phase 9 Round 1a) actually needs: the base/bar-fill token
// (`--chart-band-<band>`) is what a DOM bar's `bg-*` background colour resolves to
// (`chart-primitives.tsx`'s `bandBarBgClass` — the SVG-era `barFillClass` this comment used to name
// was deleted in DD-32 once the DOM rewrite left it with zero consumers), rendered directly against
// the page background — a meaningful, non-text
// graphical object under WCAG 1.4.11, whose minimum is 3:1, not the 4.5:1 text minimum the
// `-ink`/`-wash` assertion above checks. `sonnet`/`haiku` measured ~2.90:1/~2.13:1 before the fix
// pinned literal OKLCH values (`ayokoding.css:107-108`); this would have failed against those
// pre-fix alias values and passes against the pinned literals.
Then("every rated band's bar fill meets the WCAG non-text contrast ratio against the page background", async ({}) => {
  for (const band of RATED_BAND_IDS) {
    expect(
      bandBaseContrastRatios[band],
      `--chart-band-${band} vs --color-background contrast ratio`,
    ).toBeGreaterThanOrEqual(WCAG_NON_TEXT_MIN_CONTRAST);
  }
});

// ── Horizontal overflow regression (AC-52 / R5) ───────────────────────────────

// Shared by every viewport-and-locale-parametrized scenario outline against this page (AC-52 here;
// the later AC-49/AC-50/AC-58 outlines reuse it instead of re-implementing navigation).
async function navigateAtViewport(page: Page, width: number, locale: string, height = 800): Promise<void> {
  await page.setViewportSize({ width, height });
  await page.goto(`/${locale}/tools/ai-benchmark`);
  await page.waitForLoadState("networkidle");
}

let overflowScrollWidth = 0;
let overflowClientWidth = 0;

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The document never scrolls horizontally
Given(
  "the AI benchmark page is loaded at a {string} px viewport in the {string} locale",
  async ({ page }, width: string, locale: string) => {
    await navigateAtViewport(page, Number(width), locale);
  },
);

When("the document's scroll width is compared with its client width", async ({ page }) => {
  overflowScrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
  overflowClientWidth = await page.evaluate(() => document.documentElement.clientWidth);
});

Then("the document scroll width does not exceed the document client width", async ({}) => {
  expect(overflowScrollWidth).toBeLessThanOrEqual(overflowClientWidth);
});

// ── Sticky desktop header (AC-59, DD-27 Unit 2) ───────────────────────────────

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The roster table header stays visible while the page scrolls at desktop width
Given("the AI benchmark page is loaded at a 1440 px viewport", async ({ page }) => {
  await navigateAtViewport(page, 1440, "en");
});

When("the page is scrolled until the roster table's last row is in view", async ({ page }) => {
  const lastRow = page.locator('[data-testid="model-table-desktop"] tbody tr[data-model-id]').last();
  await lastRow.scrollIntoViewIfNeeded();
});

Then("the table's header row is still visible", async ({ page }) => {
  const headerRow = page.locator('[data-testid="model-table-desktop"] thead tr').first();
  await expect(headerRow).toBeInViewport();
});

// ── Expanded card field density (DD-34, cycles 6.4/6.5) ───────────────────────

async function navigateWithFirstCardExpanded(page: Page): Promise<void> {
  await navigateAtViewport(page, 390, "en");
  const summary = page.locator('[data-testid^="model-card-disclosure-"]').first();
  await summary.click();
}

type ComputedTextStyle = { fontSize: number; fontWeight: number };

async function readComputedTextStyle(locator: ReturnType<Page["locator"]>): Promise<ComputedTextStyle> {
  return locator.evaluate((el) => {
    const cs = getComputedStyle(el);
    return { fontSize: parseFloat(cs.fontSize), fontWeight: parseFloat(cs.fontWeight) };
  });
}

let cardLabelStyle: ComputedTextStyle | null = null;
let cardValueStyle: ComputedTextStyle | null = null;

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded card's figure value out-ranks its own field label
Given("the AI benchmark page is loaded at a 390 px viewport with one roster card expanded", async ({ page }) => {
  await navigateWithFirstCardExpanded(page);
});

When(
  "the computed font size and font weight of a field label and of its own value are read from the live page",
  async ({ page }) => {
    const details = page.locator('[data-testid^="model-card-details-"]').first();
    cardLabelStyle = await readComputedTextStyle(details.locator("dt").first());
    cardValueStyle = await readComputedTextStyle(details.locator("dd").first());
  },
);

Then("the value's computed font size is larger than the label's computed font size", async ({}) => {
  expect(cardValueStyle!.fontSize).toBeGreaterThan(cardLabelStyle!.fontSize);
});

Then("the value's computed font weight is greater than the label's computed font weight", async ({}) => {
  expect(cardValueStyle!.fontWeight).toBeGreaterThan(cardLabelStyle!.fontWeight);
});

let gradedCellFlexDirection = "";
let labelBox: { top: number; bottom: number } | null = null;
let valueBox: { top: number; bottom: number } | null = null;

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:An expanded card's figure value and its evidence badge flow on one row
When("the computed flex direction of a graded figure cell is read from the live page", async ({ page }) => {
  const details = page.locator('[data-testid^="model-card-details-"]').first();
  const gradedCell = details.locator('[data-slot="figure-cell"]').first();
  gradedCellFlexDirection = await gradedCell.evaluate((el) => getComputedStyle(el).flexDirection);
  // The field's own <dd> is the nearest <dd> ancestor of the graded cell; its parent is the
  // shared name-value wrapper `model-detail-disclosure.tsx` renders one per field, so this
  // navigation is stable whether that wrapper is today's stacked layout or 6.5's rail layout.
  const dd = gradedCell.locator("xpath=ancestor::dd[1]");
  const fieldRow = dd.locator("xpath=parent::div[1]");
  const dt = fieldRow.locator("dt").first();
  labelBox = await dt.evaluate((el) => {
    const r = el.getBoundingClientRect();
    return { top: r.top, bottom: r.bottom };
  });
  valueBox = await dd.evaluate((el) => {
    const r = el.getBoundingClientRect();
    return { top: r.top, bottom: r.bottom };
  });
});

Then("that computed flex direction is row rather than column", async ({}) => {
  expect(gradedCellFlexDirection).toBe("row");
});

Then("the field label's vertical band overlaps the vertical band of its own value", async ({}) => {
  const overlaps = labelBox!.top < valueBox!.bottom && valueBox!.top < labelBox!.bottom;
  expect(overlaps).toBe(true);
});

// ── Phase 8 — accessibility: tap targets and the live layout criteria ────────
//
// AC-49, AC-50, AC-51, AC-55, AC-58, AC-60 all read a computed style, a bounding box, or a real
// viewport dimension jsdom cannot produce (DD-26's "verification gap" — see tech-docs.md). Every
// scenario below shares `navigateAtViewport` above rather than re-implementing navigation
// (delivery.md's cycle 8.4/8.6 REFACTOR instruction).

// Quoted-width Given, shared by AC-58 (8.1) and AC-49 (8.2) — the Scenario Outline's own Gherkin
// text quotes `"<width>"`, which is what makes this Cucumber Expression `{string}` step distinct
// from the UNQUOTED literal `Given`s below (AC-50's "1440 px viewport", AC-51's "320 px viewport"):
// a bare Cucumber Expression `{string}` only matches a quoted substring, so there is no ambiguity
// between this generic step and any of the pre-existing literal ones (AC-59's, for instance).
Given("the AI benchmark page is loaded at a {string} px viewport", async ({ page }, width: string) => {
  await navigateAtViewport(page, Number(width), "en");
});

// ── AC-58 — every interactive target reaches WCAG 2.5.8's 24x24 CSS px minimum (DD-30) ───────

type TapTargetFailure = { description: string; width: number; height: number };
let tapTargetFailures: TapTargetFailure[] = [];

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Every interactive target meets the minimum target size
When("the bounding box of every link and every disclosure control is measured", async ({ page }) => {
  const targets = page.locator('[data-testid="ai-bench-page"] a, [data-testid="ai-bench-page"] summary');
  const count = await targets.count();
  const failures: TapTargetFailure[] = [];
  for (let i = 0; i < count; i++) {
    const el = targets.nth(i);
    // A target inside a still-closed `<details>`, or inside whichever of the mobile card / desktop
    // table CSS hides at the current width, is NOT an operable target right now — it carries no
    // WCAG 2.5.8 obligation until it becomes visible. `boundingBox()` alone does not detect this:
    // a `display: none` ancestor still yields a real (zero-sized) box rather than `null`, so
    // `isVisible()` (which correctly accounts for `display`/`visibility` and a closed `<details>`)
    // is the actual visibility gate; `boundingBox()` only handles the "detached from the DOM" case.
    if (!(await el.isVisible())) continue;
    const box = await el.boundingBox();
    if (!box) continue;
    if (box.width < 24 || box.height < 24) {
      const raw = (await el.getAttribute("aria-label")) ?? (await el.textContent()) ?? "(unnamed target)";
      failures.push({ description: raw.trim().slice(0, 80), width: box.width, height: box.height });
    }
  }
  tapTargetFailures = failures;
});

Then("every measured target is at least 24 CSS pixels wide and at least 24 CSS pixels tall", async ({}) => {
  expect(tapTargetFailures, `undersized target(s): ${JSON.stringify(tapTargetFailures)}`).toEqual([]);
});

// ── AC-49 — chart label typography is viewport-independent (DD-25/DD-26) ─────────────────────

let chartLabelFontSizePx = 0;

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Chart label text renders at a fixed size across viewports
When("the computed font size of a chart model label is read from the live page", async ({ page }) => {
  const label = page.locator('[data-testid^="benchmark-chart-label-"]').first();
  chartLabelFontSizePx = await label.evaluate((el) => parseFloat(getComputedStyle(el).fontSize));
});

// The declared size (`text-xs`, 12px — `benchmark-chart.tsx`'s `chart-bar-label`) carries no
// responsive (`sm:`/`lg:`) modifier (DD-25/DD-26), so every one of the five Outline rows
// independently equalling this ONE fixed constant is what proves the property this scenario names
// ("equals ... at every other tested width") — comparing five live values pairwise across rows
// would need module-scoped state to survive Playwright's `fullyParallel` worker split, which is not
// guaranteed, whereas each row asserting the same known constant is both simpler and a strictly
// equivalent proof of the same invariant.
const CHART_LABEL_DECLARED_FONT_SIZE_PX = 12;

Then(
  "that computed font size equals the computed font size of the same label at every other tested width",
  async ({}) => {
    expect(chartLabelFontSizePx).toBe(CHART_LABEL_DECLARED_FONT_SIZE_PX);
  },
);

Then("that computed font size is at least 12 CSS pixels", async ({}) => {
  expect(chartLabelFontSizePx).toBeGreaterThanOrEqual(12);
});

// ── AC-50 — chart label typography never outranks the page's own body text ───────────────────
// Reuses the pre-existing literal `Given("the AI benchmark page is loaded at a 1440 px viewport", …)`
// bound above for AC-59 — this scenario's own Gherkin line is the identical, UNQUOTED literal text.

let chartLabelFontSizeAt1440 = 0;
let bodyFontSizeAt1440 = 0;

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:Chart label text never exceeds the page's own body text size
When(
  "the computed font sizes of a chart model label and the page body text are read from the live page",
  async ({ page }) => {
    const label = page.locator('[data-testid^="benchmark-chart-label-"]').first();
    chartLabelFontSizeAt1440 = await label.evaluate((el) => parseFloat(getComputedStyle(el).fontSize));
    bodyFontSizeAt1440 = await page.evaluate(() => parseFloat(getComputedStyle(document.body).fontSize));
  },
);

Then("the chart label's computed font size is no larger than the page body text's computed font size", async ({}) => {
  expect(chartLabelFontSizeAt1440).toBeLessThanOrEqual(bodyFontSizeAt1440);
});

// ── AC-51 — the chart plot spans the full container width on a phone (DD-25/DWT-001) ─────────

Given("the AI benchmark page is loaded at a 320 px viewport", async ({ page }) => {
  await navigateAtViewport(page, 320, "en");
});

let barTrackWidthAt320 = 0;
let chartRowWidthAt320 = 0;
let chartRowDisplayAt320 = "";

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart plot occupies the full container width on a phone
When(
  "the width of a capability bar's track is compared with the width of its containing chart region",
  async ({ page }) => {
    const row = page.locator('[data-testid^="benchmark-chart-row-"]').first();
    const track = row.locator('[data-slot="chart-bar-row-track"]').first();
    const rowBox = await row.boundingBox();
    const trackBox = await track.boundingBox();
    if (!rowBox || !trackBox) throw new Error("chart row or bar track is not visible at 320px");
    chartRowWidthAt320 = rowBox.width;
    barTrackWidthAt320 = trackBox.width;
    // `lg:grid-cols-[10rem_1fr]` is the ONLY mechanism that reserves a label column — it applies
    // from `lg` up only, so at 320px the row's own computed `display` must not be `grid`.
    chartRowDisplayAt320 = await row.evaluate((el) => getComputedStyle(el).display);
  },
);

Then("the bar track spans the full width of that region", async ({}) => {
  expect(Math.abs(barTrackWidthAt320 - chartRowWidthAt320)).toBeLessThan(2);
});

Then("no reserved label column is present at that width", async ({}) => {
  expect(chartRowDisplayAt320).not.toBe("grid");
});

// ── AC-55 — the chart is visible above the fold on a phone (DD-29) ───────────────────────────
//
// Rule-15 UWT-007 regression fix (Phase 12 PR review, finding F2): the Given below used to load a
// fixed 390x844 viewport — a height tall enough that the pre-fix chart position (701px measured at
// 390px width) already satisfied the fold check, so this scenario stayed green throughout the
// defect. `delivery.md`'s own UWT-007 entry retested at 320x568 and 390x664 (the realistic visible
// height once mobile browser chrome is accounted for) and is the source of both the pre-fix
// (741px/701px) and post-fix (536.5px/517.25px) measurements this Outline now guards against —
// `loadedViewportHeight` below is set from whichever breakpoint the Given loads, so the assertion
// checks the SAME height the page was actually measured at, not a hardcoded constant.

let loadedViewportHeight = 0;

Given(
  "the AI benchmark page is loaded at a {string} px wide, {string} px tall viewport",
  async ({ page }, width: string, height: string) => {
    loadedViewportHeight = Number(height);
    await page.setViewportSize({ width: Number(width), height: loadedViewportHeight });
    await page.goto("/en/tools/ai-benchmark");
    await page.waitForLoadState("networkidle");
  },
);

let firstChartElementOffsetTop = 0;

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The chart is visible above the fold on a phone
When("the vertical offset of the first chart element is read from the live page", async ({ page }) => {
  const chart = page.locator('[data-testid="benchmark-chart"]').first();
  const box = await chart.boundingBox();
  if (!box) throw new Error(`chart is not visible at the loaded viewport (height ${loadedViewportHeight})`);
  firstChartElementOffsetTop = box.y;
});

Then("that offset is less than the viewport height", async ({}) => {
  expect(firstChartElementOffsetTop).toBeLessThan(loadedViewportHeight);
});

// ── AC-60 — the whole overhaul holds identically in both locales ─────────────────────────────
// `navigateAtViewport`'s own default height (800) is used by every OTHER viewport-parametrized
// scenario in this file that reuses it (delivery.md's cycle 8.6 REFACTOR instruction) — but this
// scenario's own fold check is overridden to 664 (Rule-15 UWT-007 regression fix, Phase 12 PR
// review finding F2): 800 already satisfied the fold check throughout the UWT-007 defect (the
// pre-fix chart position measured 701px at 390px width), so it was non-protective; 664 is the
// realistic breakpoint `delivery.md`'s UWT-007 retest actually measured the defect and its fix at.

// @covers specs/apps/ayokoding/www/behaviors/frontend/tools/ai-benchmark.feature:The overhauled page behaves identically in both locales
Given(
  "the AI benchmark page is loaded in the {string} locale at a 390 px viewport",
  async ({ page }, locale: string) => {
    await navigateAtViewport(page, 390, locale, 664);
  },
);

Then("the chart is present above the fold", async ({ page }) => {
  const chart = page.locator('[data-testid="benchmark-chart"]').first();
  const box = await chart.boundingBox();
  expect(box).not.toBeNull();
  expect(box!.y).toBeLessThan(664);
});

Then("every roster card is collapsed", async ({ page }) => {
  const details = page.locator('[data-testid^="model-card-details-"]');
  const count = await details.count();
  expect(count).toBeGreaterThan(0);
  const openFlags = await details.evaluateAll((els) => els.map((el) => (el as HTMLDetailsElement).open));
  expect(openFlags.every((open) => open === false)).toBe(true);
});

Then("no raw translation key is rendered", async ({ page }) => {
  const bodyText = await page.locator("body").textContent();
  expect(bodyText).not.toMatch(/aiBench/);
});
