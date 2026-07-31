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

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The English page renders its localized heading
Then("the page shows a level-one heading in English", async ({ page }) => {
  const h1 = page.locator("h1").first();
  await expect(h1).toBeVisible();
  const text = (await h1.textContent()) ?? "";
  expect(text.trim().length).toBeGreaterThan(0);
  // The served English H1 must carry the English copy, not the Indonesian one.
  expect(text.trim()).not.toBe("Tolok Ukur Model AI");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The Indonesian page renders its localized heading
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

// UWT-002 fix (Rule-15, 2026-07-30): the chart is now one svg PER rated band
// (`benchmark-chart-svg-{opus,sonnet,light}`), not one shared `benchmark-chart-svg` — the first
// band's own svg is enough to prove the family carries a real accessible name.
// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The merged chart exposes an accessible name
Then("the merged chart exposes an accessible name", async ({ page }) => {
  await expect(page.locator('[data-testid^="benchmark-chart-svg-"]').first()).toHaveAccessibleName(/.+/);
});

// ── Phase 8 — harness and class filters (AC-18, AC-22, AC-27) ─────────────────
// These three scenarios are also bound at the unit layer (test/unit/fe-steps/ai-benchmark.steps.tsx)
// — real browser navigation here proves the SAME behaviour survives an actual production request,
// not just a mocked render. "When the page renders" is already registered globally
// (cost-of-living-calculator.steps.ts) as a bare `waitForLoadState`, so navigation happens in each
// scenario's own Given/When step here, not there.

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The page with no query parameters shows the whole roster
Given("the URL carries no query parameters", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The page with no query parameters shows the whole roster
Then("every roster model is shown in the data table", async ({ page }) => {
  await page.waitForLoadState("networkidle");
  // Appendix A.2 roster — see apps/ayokoding-www's core/data/models.ts's own "38 rows" comment.
  await expect(page.locator('[data-testid="model-table-desktop"] tbody tr[data-model-id]')).toHaveCount(38);
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A harness filter switches the merged chart to that harness's rate
Given("a fixture model priced differently by two harnesses", async ({}) => {
  // The e2e layer exercises the REAL roster (no fixture injection over HTTP) — Grok 4.5
  // (core/data/models.ts) is genuinely priced differently by two harnesses: cursor/opencode-zen at
  // a metered $2/$6 rate, opencode-go at a flat-rate subscription instead.
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A harness filter switches the merged chart to that harness's rate
When("the merged chart renders with that harness selected", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark?harness=opencode-go");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A harness filter switches the merged chart to that harness's rate
Then("that model's price bars use that harness's own rate, not its lowest available rate", async ({ page }) => {
  // opencode-go carries Grok 4.5 as a flat-rate subscription, not a per-token rate — selecting it
  // must remove Grok 4.5's metered bar and show its inline subscription text instead (DD-1).
  await expect(page.getByTestId("benchmark-chart-bar-price-in-grok-4.5")).toHaveCount(0);
  await expect(page.getByTestId("benchmark-chart-subscription-grok-4.5")).toBeVisible();
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
Given("the reader has applied a harness filter and a class filter", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark?harness=cursor&class=opus");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
When("the reader reloads the resulting URL", async ({ page }) => {
  await page.reload();
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:A reloaded filtered URL reproduces the same view
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

const BAND_IDS = ["opus", "sonnet", "light", "unrated"] as const;

// The three bands that actually render as a bar (`benchmark-chart.tsx` never plots `unrated` as
// a bar — it is a plain text list) — the base/bar-fill token `--chart-band-<band>` against
// `--color-background` (the page background a bar renders directly onto) is the pair the M-14 fix
// (delivery.md, Phase 9 Round 1a) actually changed and the one WCAG 1.4.11's 3:1 non-text minimum
// applies to; `unrated`'s base token was never implicated (it aliases the neutral `--warm-400`).
const RATED_BAND_IDS = ["opus", "sonnet", "light"] as const;

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
  light: 0,
  unrated: 0,
};

// Populated alongside `bandContrastRatios` — the base/bar-fill token vs `--color-background` pair
// the M-14 fix actually protects (pr-review-synthesis-maker HIGH finding, PR #122 cycle 1: the
// `-ink`/`-wash` assertion above never reads this pair, so it could not have caught the real
// regression this session found and fixed).
let bandBaseContrastRatios: Record<(typeof RATED_BAND_IDS)[number], number> = {
  opus: 0,
  sonnet: 0,
  light: 0,
};

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Band colours meet contrast in both themes
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

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Band colours meet contrast in both themes
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

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Band colours meet contrast in both themes
Then("every band token meets the WCAG AA contrast ratio against its background", async ({}) => {
  for (const band of BAND_IDS) {
    expect(
      bandContrastRatios[band],
      `--chart-band-${band}-ink vs --chart-band-${band}-wash contrast ratio`,
    ).toBeGreaterThanOrEqual(WCAG_AA_MIN_CONTRAST);
  }
});

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:Band colours meet contrast in both themes
//
// The assertion the M-14 fix (Phase 9 Round 1a) actually needs: the base/bar-fill token
// (`--chart-band-<band>`) is what a bar's `fill` colour resolves to (`chart-primitives.tsx`'s
// `barFillClass`), rendered directly against the page background — a meaningful, non-text
// graphical object under WCAG 1.4.11, whose minimum is 3:1, not the 4.5:1 text minimum the
// `-ink`/`-wash` assertion above checks. `sonnet`/`light` measured ~2.90:1/~2.13:1 before the fix
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
async function navigateAtViewport(page: Page, width: number, locale: string): Promise<void> {
  await page.setViewportSize({ width, height: 800 });
  await page.goto(`/${locale}/tools/ai-benchmark`);
  await page.waitForLoadState("networkidle");
}

let overflowScrollWidth = 0;
let overflowClientWidth = 0;

// @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/ai-benchmark.feature:The document never scrolls horizontally
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
