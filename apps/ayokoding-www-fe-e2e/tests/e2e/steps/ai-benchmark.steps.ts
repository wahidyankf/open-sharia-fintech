import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";
import type { Page } from "@playwright/test";
import {
  computeGroups,
  type Band,
  type ModelScore,
} from "../../../../ayokoding-www/src/features/ai-benchmark/core/bands";
import {
  dataset,
  isConflictedFigure,
  type EvidenceGrade,
  type Model,
} from "../../../../ayokoding-www/src/features/ai-benchmark/core/data/models";
import {
  BAND_LABEL_KEYS,
  BENCHMARK_COLUMNS,
  GRADE_LABEL_KEYS,
  HARNESS_DISPLAY_NAMES,
} from "../../../../ayokoding-www/src/features/ai-benchmark/core/data/benchmarks";
import { OPERATORS } from "../../../../ayokoding-www/src/features/ai-benchmark/core/data/operators";
import { lowestRate } from "../../../../ayokoding-www/src/features/ai-benchmark/core/price";
import { coverage } from "../../../../ayokoding-www/src/features/ai-benchmark/core/score";
import { t } from "../../../../ayokoding-www/src/features/i18n/core/translations";

const { Given, When, Then } = createBdd();

// AI Benchmark public-boundary step bindings.

// The active locale for the scenario — set by "Given the locale is …" and read by the navigation
// step. Module-scoped because playwright-bdd step functions are stateless over the fixture context.
let scenarioLocale = "en";
let targetModelId = "";
let modelIdsBefore: string[] = [];
let unrelatedBandOrdersBefore: Record<string, string[]> = {};
let copiedUrl = "";
let inspectedElements: ReturnType<Page["locator"]>[] = [];
let sampledValues: number[] = [];
let sampledStrings: string[] = [];

const productionGroups = computeGroups(dataset);
const productionScores = new Map<string, ModelScore>();
for (const scores of Object.values(productionGroups)) {
  for (const score of scores) productionScores.set(score.model.id, score);
}

function sorted(values: readonly string[]): string[] {
  return [...values].sort((left, right) => left.localeCompare(right));
}

function rosterModelIds(): string[] {
  return dataset.models.map((model) => model.id);
}

function modelsForHarness(harness: Model["harnesses"][number]): string[] {
  return dataset.models.filter((model) => model.harnesses.includes(harness)).map((model) => model.id);
}

function formatIndex(value: number): string {
  return new Intl.NumberFormat("en-US", { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(value);
}

function formatPercent(value: number): string {
  return `${new Intl.NumberFormat("en-US", { minimumFractionDigits: 1, maximumFractionDigits: 1 }).format(value)}%`;
}

function formatCoverage(ratio: number): string {
  return `${new Intl.NumberFormat("en-US", { maximumFractionDigits: 0 }).format(ratio * 100)}%`;
}

function formatPriceUsd(value: number): string {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  }).format(value);
}

function bandLabel(band: Band): string {
  const key = BAND_LABEL_KEYS[band];
  if (!key) throw new Error(`Missing production label key for band ${band}`);
  return t("en", key);
}

function expectedSnapshotText(): string {
  const date = new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
    timeZone: "UTC",
  }).format(new Date(dataset.snapshotDate));
  return `${t("en", "aiBenchSnapshotLabel")}: ${date}`;
}

function expectedPrimaryPrice(model: Model): { input: string; output: string } {
  const rate = lowestRate(model);
  if (!rate) {
    const unavailable = t("en", "aiBenchNoFigure");
    return { input: unavailable, output: unavailable };
  }
  if (rate.kind === "subscription") {
    const value = `${t("en", "aiBenchSubscription")} (${formatPriceUsd(rate.planCostUsd)})`;
    return { input: value, output: value };
  }
  return { input: formatPriceUsd(rate.input), output: formatPriceUsd(rate.output) };
}

async function loadBenchmark(page: Page, query = "", locale = scenarioLocale): Promise<void> {
  await page.goto(`/${locale}/tools/ai-benchmark${query}`);
  await page.waitForLoadState("networkidle");
  await expect(page.getByTestId("ai-bench-page")).toBeVisible();
}

async function bandRowIds(page: Page, band: string): Promise<string[]> {
  return page
    .getByTestId(`benchmark-chart-band-${band}`)
    .locator('[data-testid^="benchmark-chart-row-"]')
    .evaluateAll((rows) => rows.map((row) => row.getAttribute("data-testid")!.replace("benchmark-chart-row-", "")));
}

async function tableRowIds(page: Page): Promise<string[]> {
  return page
    .locator('[data-testid="model-table-desktop"] tbody tr[data-model-id]')
    .evaluateAll((rows) => rows.map((row) => row.getAttribute("data-model-id")!));
}

async function allChartModelIds(page: Page): Promise<string[]> {
  return page
    .getByTestId("benchmark-chart")
    .locator('[data-testid^="benchmark-chart-row-"], [data-testid^="benchmark-chart-unrated-model-"]')
    .evaluateAll((nodes) =>
      nodes.map((node) =>
        (node.getAttribute("data-testid") ?? "")
          .replace("benchmark-chart-row-", "")
          .replace("benchmark-chart-unrated-model-", ""),
      ),
    );
}

// ── Preconditions ─────────────────────────────────────────────────────────────

// A real route render is the public proof that the server loaded the benchmark dataset. Every
// scenario starts from this usable page; scenario-specific URL steps may deliberately navigate
// again with their own locale or query string.
Given("the AI benchmark dataset is loaded", async ({ page }) => {
  scenarioLocale = "en";
  targetModelId = "";
  modelIdsBefore = [];
  unrelatedBandOrdersBefore = {};
  copiedUrl = "";
  inspectedElements = [];
  sampledValues = [];
  sampledStrings = [];
  await loadBenchmark(page, "", "en");
});

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

Then("the page shows a level-one heading in English", async ({ page }) => {
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(t("en", "aiBenchTitle"));
});

Then("the page shows a level-one heading in Indonesian", async ({ page }) => {
  await expect(page.getByRole("heading", { level: 1 })).toHaveText(t("id", "aiBenchTitle"));
  expect(t("id", "aiBenchTitle")).not.toBe(t("en", "aiBenchTitle"));
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
Then("each rated band's chart region exposes a localized accessible name", async ({ page }) => {
  for (const band of ["opus", "sonnet", "haiku"] as const) {
    await expect(page.getByTestId(`benchmark-chart-band-${band}`)).toHaveAccessibleName(bandLabel(band));
  }
});

// ── Phase 8 — harness and class filters (AC-18, AC-22, AC-27) ─────────────────
// These three scenarios are also bound at the unit layer (test/unit/fe-steps/ai-benchmark.steps.tsx)
// — real browser navigation here proves the SAME behaviour survives an actual production request,
// not just a mocked render. "When the page renders" is already registered globally
// (cost-of-living-calculator.steps.ts) as a bare `waitForLoadState`, so navigation happens in each
// scenario's own Given/When step here, not there.

Given("the URL carries no query parameters", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark");
});

Then("every roster model is shown in the data table", async ({ page }) => {
  await page.waitForLoadState("networkidle");
  expect(sorted(await tableRowIds(page))).toEqual(sorted(rosterModelIds()));
});

Given("a fixture model priced differently by two harnesses", async ({}) => {
  // The e2e layer exercises the REAL roster (no fixture injection over HTTP) — Grok 4.5
  // (core/data/models.ts) is genuinely priced differently by two harnesses: cursor/opencode-zen at
  // a metered $2/$6 rate, opencode-go at a flat-rate subscription instead.
  targetModelId = "grok-4.5";
});

When("the merged chart renders with that harness selected", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark?harness=opencode-go");
  await page.waitForLoadState("networkidle");
});

Then("that model's price bars use that harness's own rate, not its lowest available rate", async ({ page }) => {
  // opencode-go carries Grok 4.5 as a flat-rate subscription, not a per-token rate — selecting it
  // must remove Grok 4.5's metered bar and show its inline subscription text instead (DD-1).
  await expect(page.getByTestId("benchmark-chart-bar-price-in-grok-4.5")).toHaveCount(0);
  await expect(page.getByTestId("benchmark-chart-subscription-grok-4.5")).toBeVisible();
});

Given("the reader has applied a harness filter and a class filter", async ({ page }) => {
  await page.goto("/en/tools/ai-benchmark?harness=cursor&class=opus");
  await page.waitForLoadState("networkidle");
});

When("the reader reloads the resulting URL", async ({ page }) => {
  await page.reload();
  await page.waitForLoadState("networkidle");
});

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
  expect(idsAfterReload.length).toBeLessThan(dataset.models.length);
});

// ── Public roster, metadata, and explanatory content ─────────────────────────

When("the page first renders", async ({ page }) => {
  await expect(page.getByTestId("ai-bench-page")).toBeVisible();
});

When("the data table is rendered", async ({ page }) => {
  await expect(page.getByTestId("model-table")).toBeAttached();
});

Then("a data table is present in the document", async ({ page }) => {
  await expect(page.getByTestId("model-table-desktop").locator("table")).toHaveCount(1);
});

Then("the table has a caption", async ({ page }) => {
  const caption = page.getByTestId("model-table-desktop").locator("caption");
  await expect(caption).toHaveCount(1);
  expect((await caption.textContent())?.trim().length).toBeGreaterThan(0);
});

Then("every table header cell declares a scope", async ({ page }) => {
  const headers = page.getByTestId("model-table-desktop").locator("th");
  expect(await headers.count()).toBeGreaterThan(0);
  const scopes = await headers.evaluateAll((cells) => cells.map((cell) => cell.getAttribute("scope")));
  expect(scopes.every((scope) => scope === "col" || scope === "row")).toBe(true);
});

Then(
  "each model row lists its harnesses, class, every benchmark score, composite index, coverage ratio, input price, and output price",
  async ({ page }) => {
    const primaryRows = page.locator('[data-testid="model-table-desktop"] tbody tr[data-model-id]');
    const detailRows = page.locator('[data-testid="model-table-desktop"] tbody tr[data-model-detail-id]');
    await expect(primaryRows).toHaveCount(dataset.models.length);
    await expect(detailRows).toHaveCount(dataset.models.length);

    for (const model of dataset.models) {
      const score = productionScores.get(model.id);
      if (!score) throw new Error(`Production score is missing for ${model.id}`);

      const primary = page.locator(`[data-testid="model-table-desktop"] tbody tr[data-model-id="${model.id}"]`);
      const detail = page.locator(`[data-testid="model-table-desktop"] tbody tr[data-model-detail-id="${model.id}"]`);
      const primaryCells = primary.locator(":scope > th, :scope > td");
      await expect(primaryCells).toHaveCount(6);
      await expect(primaryCells.nth(0)).toContainText(model.name);
      await expect(primaryCells.nth(1)).toHaveText(model.vendor);
      await expect(primaryCells.nth(2)).toHaveText(bandLabel(score.band));
      await expect(primaryCells.nth(3)).toContainText(
        score.index === undefined ? t("en", "aiBenchNoFigure") : formatIndex(score.index),
      );

      const expectedPrice = expectedPrimaryPrice(model);
      await expect(primaryCells.nth(4)).toContainText(expectedPrice.input);
      await expect(primaryCells.nth(5)).toContainText(expectedPrice.output);

      const detailText = (await detail.textContent()) ?? "";
      for (const harness of model.harnesses) {
        expect(detailText).toContain(HARNESS_DISPLAY_NAMES[harness] ?? harness);
      }
      expect(detailText).toContain(formatCoverage(score.coverage));

      for (const column of BENCHMARK_COLUMNS) {
        expect(detailText).toContain(t("en", column.labelKey));
        const figure = model.figures.find((candidate) => candidate.benchmark === column.id);
        if (!figure) continue;
        const expectedValue = isConflictedFigure(figure)
          ? `${formatPercent(figure.low)} ${t("en", "aiBenchRangeSeparator")} ${formatPercent(figure.high)}`
          : formatPercent(figure.value);
        expect(detailText).toContain(expectedValue);
      }
    }
  },
);

Then("every benchmark score cell carries an evidence grade marker", async ({ page }) => {
  const details = page.locator('[data-testid="model-table-desktop"] tr[data-model-detail-id]');
  const reportedFigures = details.locator('[data-slot="figure-cell"]');
  expect(await reportedFigures.count()).toBeGreaterThan(0);
  expect(await reportedFigures.locator('[data-slot="evidence-badge"]').count()).toBe(await reportedFigures.count());
});

Then("every price cell carries an evidence grade marker", async ({ page }) => {
  const pricedCells = page.locator(
    '[data-testid="model-table-desktop"] tr[data-model-id] td:nth-last-child(-n+2) [data-slot="figure-cell"]',
  );
  expect(await pricedCells.count()).toBeGreaterThan(0);
  expect(await pricedCells.locator('[data-slot="evidence-badge"]').count()).toBe(await pricedCells.count());
});

Then("every benchmark score cell resolves to a source link", async ({ page }) => {
  const figures = page.locator(
    '[data-testid="model-table-desktop"] tr[data-model-detail-id] [data-slot="figure-cell"]',
  );
  const links = figures.locator('a[href^="http"]');
  expect(await links.count()).toBe(await figures.count());
});

Then("every price cell resolves to a source link", async ({ page }) => {
  const figures = page.locator(
    '[data-testid="model-table-desktop"] tr[data-model-id] td:nth-last-child(-n+2) [data-slot="figure-cell"]',
  );
  expect(await figures.locator('a[href^="http"]').count()).toBe(await figures.count());
});

Given("the dataset carries a snapshot date", async ({ page }) => {
  await expect(page.getByTestId("ai-bench-snapshot")).toBeAttached();
});

Then("the snapshot date is shown in text", async ({ page }) => {
  await expect(page.getByTestId("ai-bench-snapshot")).toHaveText(expectedSnapshotText());
});

Given("the page carries a how-to-read disclosure", async ({ page }) => {
  await expect(page.getByTestId("how-to-read")).toBeAttached();
});

Then(
  "a single honesty line stating that most frontier benchmark scores are vendor self-reported is visible without interaction",
  async ({ page }) => {
    const honesty = page.getByTestId("ai-bench-how-to-honesty");
    await expect(honesty).toBeVisible();
    await expect(honesty).toContainText(/vendor|penyedia/i);
  },
);

Then("the remaining how-to-read points are reachable from that line's disclosure control", async ({ page }) => {
  const details = page.getByTestId("ai-bench-how-to-details");
  await details.locator("summary").click();
  await expect(page.getByTestId("ai-bench-how-to-list")).toBeVisible();
});

Given('the reader opens "How to read this benchmark"', async ({ page }) => {
  const details = page.getByTestId("ai-bench-how-to-details");
  if (!(await details.getAttribute("open"))) await details.locator("summary").click();
});

When("the reader reads the price-related guidance", async ({ page }) => {
  await expect(page.getByTestId("ai-bench-how-to-price-unit")).toBeVisible();
});

Then("the text states the unit each dollar figure is priced per", async ({ page }) => {
  const locale = scenarioLocale === "id" ? "id" : "en";
  await expect(page.getByTestId("ai-bench-how-to-price-unit")).toHaveText(t(locale, "aiBenchHowToPriceUnit"));
});

Then("a Subscription-priced model's figure is visibly distinguished from a per-unit price", async ({ page }) => {
  const subscriptionModel = dataset.models.find((model) => lowestRate(model)?.kind === "subscription");
  expect(subscriptionModel, "the public roster has a subscription-priced model").toBeDefined();
  const rate = lowestRate(subscriptionModel!);
  expect(rate?.kind).toBe("subscription");
  if (rate?.kind !== "subscription") throw new Error("Expected a subscription rate");

  const figure = page.locator(
    `[data-testid="benchmark-chart-subscription-${subscriptionModel!.id}"], ` +
      `[data-testid="benchmark-chart-unrated-model-${subscriptionModel!.id}"]`,
  );
  await expect(figure).toBeVisible();
  await expect(figure).toContainText(t("en", "aiBenchSubscription"));
  await expect(figure).toContainText(formatPriceUsd(rate.planCostUsd));
});

Given("I am on the AI Model Benchmark page", async ({ page }) => {
  await expect(page.getByTestId("ai-bench-page")).toBeVisible();
});

When('I look for an explanation of the "Class" and evidence-grade labels', async ({ page }) => {
  await page.getByTestId("ai-bench-legend").locator("summary").click();
});

Then("an expandable legend defines each of the four classes and each of the five evidence grades", async ({ page }) => {
  const classes = [
    ["opus", "aiBenchBandOpus", "aiBenchLegendClassOpus"],
    ["sonnet", "aiBenchBandSonnet", "aiBenchLegendClassSonnet"],
    ["haiku", "aiBenchBandHaiku", "aiBenchLegendClassHaiku"],
    ["unrated", "aiBenchBandUnrated", "aiBenchLegendClassUnrated"],
  ] as const;
  const grades = [
    ["verified", "aiBenchGradeVerified", "aiBenchLegendGradeVerified"],
    ["self-reported", "aiBenchGradeSelfReported", "aiBenchLegendGradeSelfReported"],
    ["secondary", "aiBenchGradeSecondary", "aiBenchLegendGradeSecondary"],
    ["conflicted", "aiBenchGradeConflicted", "aiBenchLegendGradeConflicted"],
    ["unavailable", "aiBenchGradeUnavailable", "aiBenchLegendGradeUnavailable"],
  ] as const;

  for (const [id, labelKey, definitionKey] of classes) {
    const entry = page.getByTestId(`ai-bench-legend-class-${id}`);
    await expect(entry.locator("dt")).toHaveText(`${t("en", labelKey)}:`);
    await expect(entry.locator("dd")).toHaveText(t("en", definitionKey));
  }
  for (const [id, labelKey, definitionKey] of grades) {
    const entry = page.getByTestId(`ai-bench-legend-grade-${id}`);
    await expect(entry.locator("dt")).toHaveText(`${t("en", labelKey)}:`);
    await expect(entry.locator("dd")).toHaveText(t("en", definitionKey));
  }
});

Given("the dataset names its benchmark operators", async ({ page }) => {
  await expect(page.getByTestId("ai-bench-sources")).toBeAttached();
});

Then("a sources and licences section lists every named operator", async ({ page }) => {
  await page.getByTestId("ai-bench-sources").locator("summary").click();
  const entries = page.getByTestId("ai-bench-sources").getByTestId("source-operator");
  await expect(entries).toHaveCount(OPERATORS.length);
  for (const [index, operator] of OPERATORS.entries()) {
    const entry = entries.nth(index);
    await expect(entry.locator("dt")).toHaveText(operator.name);
    await expect(entry.getByTestId("operator-terms")).toHaveText(t("en", operator.termsKey));
    if (operator.url) await expect(entry.locator("dt a")).toHaveAttribute("href", operator.url);
  }
});

Then("each operator entry states its republication terms or records that none are stated", async ({ page }) => {
  const terms = page.getByTestId("ai-bench-sources").getByTestId("operator-terms");
  await expect(terms).toHaveCount(OPERATORS.length);
  for (const [index, operator] of OPERATORS.entries()) {
    await expect(terms.nth(index)).toHaveText(t("en", operator.termsKey));
  }
});

Then("no rendered text matches a raw translation key", async ({ page }) => {
  await expect(page.locator("body")).not.toContainText(/aiBench/);
});

Given('the class legend is rendered in the "en" locale', async ({ page }) => {
  scenarioLocale = "en";
  await loadBenchmark(page, "", "en");
  await page.getByTestId("ai-bench-legend").locator("summary").click();
});

Given('the class legend is rendered in the "id" locale', async ({ page }) => {
  scenarioLocale = "id";
  await loadBenchmark(page, "", "id");
  await page.getByTestId("ai-bench-legend").locator("summary").click();
});

When("the haiku class label is read", async ({ page }) => {
  copiedUrl = (await page.getByTestId("ai-bench-legend-class-haiku").locator("dt").textContent())?.trim() ?? "";
});

Then('that label is "Haiku"', async ({}) => {
  expect(copiedUrl.replace(/:$/, "")).toBe("Haiku");
});

Then("that label is identical to the label the other locale renders", async ({ page }) => {
  const otherLocale = scenarioLocale === "en" ? "id" : "en";
  await loadBenchmark(page, "", otherLocale);
  await page.getByTestId("ai-bench-legend").locator("summary").click();
  const other = (await page.getByTestId("ai-bench-legend-class-haiku").locator("dt").textContent())?.trim() ?? "";
  expect(other).toBe(copiedUrl);
});

When("the set of known capability class identifiers is inspected", async ({ page }) => {
  await page.getByTestId("ai-bench-legend").locator("summary").click();
  sampledValues = [];
  inspectedElements = [page.getByTestId("ai-bench-legend-classes")];
});

Then('the identifiers are exactly "opus", "sonnet", "haiku", and "unrated"', async ({ page }) => {
  for (const band of BAND_IDS) await expect(page.getByTestId(`ai-bench-legend-class-${band}`)).toHaveCount(1);
  await expect(inspectedElements[0]!.locator(":scope > div")).toHaveCount(4);
});

Then('no identifier is "light"', async ({ page }) => {
  await expect(page.locator('[data-testid*="light"]')).toHaveCount(0);
  await expect(inspectedElements[0]!).not.toContainText(/\blight\b/i);
});

Given("the dataset records a benchmark-integrity note for a model", async ({ page }) => {
  targetModelId = "gpt-5.6-sol";
  await expect(page.locator(`[data-model-id="${targetModelId}"]`)).toHaveCount(2);
});

Given('the dataset records a benchmark-integrity note for the model "gpt-5.6-sol"', async ({ page }) => {
  targetModelId = "gpt-5.6-sol";
  await expect(page.locator(`[data-model-id="${targetModelId}"]`)).toHaveCount(2);
});

When("that model is rendered in the data table", async ({ page }) => {
  const row = page.locator(`[data-testid="model-table-desktop"] tr[data-model-id="${targetModelId}"]`);
  await expect(row).toBeAttached();
  inspectedElements = [row];
});

Then("the integrity note is reachable from that model's row", async ({}) => {
  const noteLink = inspectedElements[0]!.locator('[data-slot="integrity-note"]');
  await expect(noteLink).toHaveCount(1);
  await expect(noteLink).toHaveAttribute("href", /^https:/);
});

When('that model is rendered in the data table on the "id" locale', async ({ page }) => {
  scenarioLocale = "id";
  await loadBenchmark(page, "", "id");
  const row = page.locator(`[data-testid="model-table-desktop"] tr[data-model-id="${targetModelId}"]`);
  await expect(row).toBeAttached();
  inspectedElements = [row];
});

Then("the claim text is visible as real on-page text behind a click-to-reveal disclosure", async ({}) => {
  const details = inspectedElements[0]!.locator('[data-slot="integrity-note-detail"]');
  await details.locator("summary").click();
  await expect(details.locator("p")).toBeVisible();
  expect((await details.locator("p").textContent())?.trim().length).toBeGreaterThan(40);
});

Then("the visible claim text is the Indonesian translation, not the English source text", async ({}) => {
  const claim = inspectedElements[0]!.locator('[data-slot="integrity-note-detail"] p');
  await expect(claim).toContainText(/melaporkan|mencurangi/i);
  await expect(claim).not.toContainText(/reported|gamed/i);
});

Given("the legend and sources are rendered as disclosures below the roster", async ({ page }) => {
  const roster = page.getByTestId("model-table");
  const legend = page.getByTestId("ai-bench-legend");
  const sources = page.getByTestId("ai-bench-sources");
  inspectedElements = [roster, legend, sources];
  await expect(legend).not.toHaveAttribute("open", "");
  await expect(sources).not.toHaveAttribute("open", "");
});

When("each disclosure is expanded", async ({}) => {
  await inspectedElements[1]!.locator("summary").click();
  await inspectedElements[2]!.locator("summary").click();
});

Then("the legend defines each of the four classes and each of the five evidence grades", async ({ page }) => {
  const classDefinitions: Readonly<Record<string, string>> = {
    opus: "aiBenchLegendClassOpus",
    sonnet: "aiBenchLegendClassSonnet",
    haiku: "aiBenchLegendClassHaiku",
    unrated: "aiBenchLegendClassUnrated",
  };
  const gradeDefinitions: Readonly<Record<EvidenceGrade, string>> = {
    verified: "aiBenchLegendGradeVerified",
    "self-reported": "aiBenchLegendGradeSelfReported",
    secondary: "aiBenchLegendGradeSecondary",
    conflicted: "aiBenchLegendGradeConflicted",
    unavailable: "aiBenchLegendGradeUnavailable",
  };
  for (const [band, labelKey] of Object.entries(BAND_LABEL_KEYS)) {
    const entry = page.getByTestId(`ai-bench-legend-class-${band}`);
    await expect(entry.locator("dt")).toHaveText(`${t("en", labelKey)}:`);
    const definitionKey = classDefinitions[band];
    if (!definitionKey) throw new Error(`Missing legend definition key for ${band}`);
    await expect(entry.locator("dd")).toHaveText(t("en", definitionKey));
  }
  for (const [grade, labelKey] of Object.entries(GRADE_LABEL_KEYS)) {
    const entry = page.getByTestId(`ai-bench-legend-grade-${grade}`);
    await expect(entry.locator("dt")).toHaveText(`${t("en", labelKey)}:`);
    const definitionKey = gradeDefinitions[grade as EvidenceGrade];
    await expect(entry.locator("dd")).toHaveText(t("en", definitionKey));
  }
});

Then("the sources section lists every named operator", async ({ page }) => {
  const entries = page.getByTestId("ai-bench-sources").getByTestId("source-operator");
  await expect(entries).toHaveCount(OPERATORS.length);
  for (const [index, operator] of OPERATORS.entries()) {
    const entry = entries.nth(index);
    await expect(entry.locator("dt")).toHaveText(operator.name);
    await expect(entry.getByTestId("operator-terms")).toHaveText(t("en", operator.termsKey));
  }
});

Given("the page renders with no filters applied", async ({ page }) => {
  await loadBenchmark(page);
});

When("the document order of the page's regions is inspected", async ({ page }) => {
  inspectedElements = [
    page.getByTestId("benchmark-chart"),
    page.getByTestId("model-table"),
    page.getByTestId("ai-bench-legend"),
    page.getByTestId("ai-bench-sources"),
  ];
});

Then("the chart region precedes the roster region", async ({ page }) => {
  expect(
    await page.evaluate(() => {
      const chart = document.querySelector('[data-testid="benchmark-chart"]')!;
      const roster = document.querySelector('[data-testid="model-table"]')!;
      return Boolean(chart.compareDocumentPosition(roster) & Node.DOCUMENT_POSITION_FOLLOWING);
    }),
  ).toBe(true);
});

Then("the legend and sources disclosures both follow the roster region", async ({ page }) => {
  expect(
    await page.evaluate(() => {
      const roster = document.querySelector('[data-testid="model-table"]')!;
      const legend = document.querySelector('[data-testid="ai-bench-legend"]')!;
      const sources = document.querySelector('[data-testid="ai-bench-sources"]')!;
      return [legend, sources].every((node) =>
        Boolean(roster.compareDocumentPosition(node) & Node.DOCUMENT_POSITION_FOLLOWING),
      );
    }),
  ).toBe(true);
});

// ── Live chart and roster semantics ──────────────────────────────────────────

When("the capability groups are computed", async ({ page }) => {
  inspectedElements = BAND_IDS.map((band) =>
    page.getByTestId(band === "unrated" ? "benchmark-chart-unrated" : `benchmark-chart-band-${band}`),
  );
});

Then('each model appears in exactly one of "opus", "sonnet", "haiku", or "unrated"', async ({ page }) => {
  const chartIds = await allChartModelIds(page);
  const tableIds = await tableRowIds(page);
  expect(new Set(chartIds).size).toBe(chartIds.length);
  expect([...chartIds].sort()).toEqual([...tableIds].sort());
});

Given("a fixture model whose coverage ratio is below the low-coverage threshold", async ({ page }) => {
  targetModelId = "gpt-5.6-terra";
  await expect(page.getByTestId(`benchmark-chart-row-${targetModelId}`)).toBeVisible();
});

When("the merged chart is rendered", async ({ page }) => {
  await expect(page.getByTestId("benchmark-chart")).toBeVisible();
});

Then("that model's row carries a low-coverage marker", async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-low-coverage-${targetModelId}`)).toBeVisible();
});

Then("the marker states the model's coverage ratio in text", async ({ page }) => {
  const model = dataset.models.find((candidate) => candidate.id === targetModelId);
  if (!model) throw new Error(`Production model is missing for ${targetModelId}`);
  await expect(page.getByTestId(`benchmark-chart-low-coverage-${targetModelId}`)).toHaveText(
    `${t("en", "aiBenchCoverageLow")} (${formatCoverage(coverage(model))})`,
  );
});

Given("two fixture models whose composite indices differ", async ({ page }) => {
  inspectedElements = [
    page.getByTestId("benchmark-chart-row-claude-opus-5"),
    page.getByTestId("benchmark-chart-row-claude-sonnet-5"),
  ];
  await expect(inspectedElements[0]!).toBeVisible();
  await expect(inspectedElements[1]!).toBeVisible();
});

Then("the ratio of their bar lengths equals the ratio of their composite indices", async ({}) => {
  const values = await Promise.all(
    inspectedElements.map(async (row) => {
      const label = (await row.locator('[data-slot="chart-bar-label"]').textContent()) ?? "";
      const numeric = Number(label.match(/([\d.]+)\s*$/)?.[1]);
      const width = await row
        .locator('[data-slot="chart-bar-row-fill"]')
        .first()
        .evaluate((element: HTMLElement) => Number.parseFloat(element.style.width));
      return { numeric, width };
    }),
  );
  expect(values.every(({ numeric, width }) => Number.isFinite(numeric) && Number.isFinite(width))).toBe(true);
  // The public index label is intentionally rounded to one decimal, while the CSS width retains
  // the unrounded index. Therefore each true index lies within +/- 0.05 of its published label;
  // assert the rendered ratio is inside the exact interval those two published values imply.
  const [first, second] = values as [{ numeric: number; width: number }, { numeric: number; width: number }];
  const renderedRatio = first.width / second.width;
  const minimumPublishedRatio = (first.numeric - 0.05) / (second.numeric + 0.05);
  const maximumPublishedRatio = (first.numeric + 0.05) / (second.numeric - 0.05);
  expect(renderedRatio).toBeGreaterThanOrEqual(minimumPublishedRatio);
  expect(renderedRatio).toBeLessThanOrEqual(maximumPublishedRatio);
});

Then("the chart states its axis maximum", async ({ page }) => {
  await expect(page.getByTestId("chart-axis-max").first()).toContainText(/100(?:\.0)?/);
});

Then("every bar has a text label carrying the model name", async ({ page }) => {
  for (const band of ["opus", "sonnet", "haiku"] as const) {
    for (const score of productionGroups[band]) {
      await expect(page.getByTestId(`benchmark-chart-label-${score.model.id}`)).toHaveText(
        `${score.model.name} — ${formatIndex(score.index ?? 0)}`,
      );
    }
  }
});

Then("every bar has a text label carrying its numeric composite index", async ({ page }) => {
  for (const band of ["opus", "sonnet", "haiku"] as const) {
    for (const score of productionGroups[band]) {
      if (score.index === undefined) throw new Error(`Rated model ${score.model.id} has no production index`);
      await expect(page.getByTestId(`benchmark-chart-label-${score.model.id}`)).toHaveText(
        `${score.model.name} — ${formatIndex(score.index)}`,
      );
    }
  }
});

Given("a fixture model with a per-token input rate and output rate", async ({ page }) => {
  targetModelId = "claude-opus-5";
  await expect(page.getByTestId(`benchmark-chart-row-${targetModelId}`)).toBeVisible();
});

Then("that model has one bar labelled as the input rate", async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-bar-price-in-${targetModelId}`)).toContainText(/input/i);
});

Then("that model has one bar labelled as the output rate", async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-bar-price-out-${targetModelId}`)).toContainText(/output/i);
});

Given(
  "a fixture model with no published composite score, available only under a flat-rate subscription",
  async ({ page }) => {
    targetModelId = "mimo-v2.5";
    await expect(page.getByTestId(`benchmark-chart-unrated-model-${targetModelId}`)).toBeVisible();
  },
);

When("the merged chart renders the roster", async ({ page }) => {
  await expect(page.getByTestId("benchmark-chart")).toBeVisible();
});

Then("that model appears in the unrated group's plain text list", async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-unrated-model-${targetModelId}`)).toBeVisible();
});

Then("that list entry states the model's subscription plan cost", async ({ page }) => {
  const model = dataset.models.find((candidate) => candidate.id === targetModelId);
  if (!model) throw new Error(`Production model is missing for ${targetModelId}`);
  const rate = lowestRate(model);
  if (!rate || rate.kind !== "subscription") {
    throw new Error(`Production model ${targetModelId} has no subscription price`);
  }
  const expected = `${model.name} — ${t("en", "aiBenchSubscription")}: ${formatPriceUsd(rate.planCostUsd)}${
    rate.caps ? ` (${rate.caps})` : ""
  }`;
  await expect(page.getByTestId(`benchmark-chart-unrated-model-${targetModelId}`)).toHaveText(expected);
});

Then("that model renders no per-token bar and no zero value", async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-bar-price-in-${targetModelId}`)).toHaveCount(0);
  await expect(page.getByTestId(`benchmark-chart-bar-price-out-${targetModelId}`)).toHaveCount(0);
  await expect(page.getByTestId(`benchmark-chart-unrated-model-${targetModelId}`)).not.toContainText(
    /—\s*0(?:\.0)?(?:\D|$)/,
  );
});

When("the merged chart is rendered without a harness filter", async ({ page }) => {
  await loadBenchmark(page);
});

Then("that model's bars use the lower of the two harness rates", async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-bar-price-in-${targetModelId}`)).toContainText("$2.00");
  await expect(page.getByTestId(`benchmark-chart-bar-price-out-${targetModelId}`)).toContainText("$6.00");
});

Then("the chart states that it shows the lowest available harness rate", async ({ page }) => {
  await expect(page.getByTestId("benchmark-chart-subtitle")).toContainText(/lowest|terendah/i);
});

Then("every band group carries its class name as text", async ({ page }) => {
  for (const band of ["opus", "sonnet", "haiku"]) {
    await expect(page.getByTestId(`benchmark-chart-band-${band}-label`)).toContainText(new RegExp(band, "i"));
  }
  await expect(page.getByTestId("benchmark-chart-unrated-heading")).toContainText(/unrated|belum dinilai/i);
});

Then("every model row carries its class as text in the data table", async ({ page }) => {
  for (const model of dataset.models) {
    const score = productionScores.get(model.id);
    if (!score) throw new Error(`Production score is missing for ${model.id}`);
    const row = page.locator(`[data-testid="model-table-desktop"] tbody tr[data-model-id="${model.id}"]`);
    await expect(row.locator(":scope > td:nth-of-type(2)")).toHaveText(bandLabel(score.band));
  }
});

Given("the merged chart has replaced the two former charts", async ({ page }) => {
  await expect(page.getByTestId("benchmark-chart")).toHaveCount(1);
  await expect(page.locator('[data-testid="capability-chart"], [data-testid="price-chart"]')).toHaveCount(0);
});

When("a screen reader encounters the chart", async ({ page }) => {
  inspectedElements = [page.getByTestId("benchmark-chart")];
});

Then(
  "each rated band renders its own labelled region carrying its localized band name as its accessible name",
  async ({ page }) => {
    for (const band of ["opus", "sonnet", "haiku"]) {
      await expect(page.getByTestId(`benchmark-chart-band-${band}`)).toHaveAccessibleName(new RegExp(band, "i"));
    }
  },
);

Then("every figure the chart encodes is still reachable via the roster below", async ({ page }) => {
  expect((await allChartModelIds(page)).sort()).toEqual((await tableRowIds(page)).sort());
});

Given("a fixture model whose benchmark figure has conflicting published values", async ({ page }) => {
  targetModelId = "claude-opus-5";
  const detail = page.locator(`[data-testid="model-table-desktop"] tr[data-model-detail-id="${targetModelId}"]`);
  await expect(detail).toBeAttached();
  inspectedElements = [detail];
});

Then("that cell shows the lowest and highest published values", async ({}) => {
  const model = dataset.models.find((candidate) => candidate.id === targetModelId);
  const figure = model?.figures.find(isConflictedFigure);
  if (!figure) throw new Error(`Production model ${targetModelId} has no conflicted figure`);
  const expectedRange = `${formatPercent(figure.low)} ${t("en", "aiBenchRangeSeparator")} ${formatPercent(figure.high)}`;
  const ranged = inspectedElements[0]!.locator('[data-slot="figure-cell-value"]', { hasText: expectedRange });
  await expect(ranged).toHaveText(expectedRange);
  sampledValues = [figure.low, figure.high];
  inspectedElements.push(ranged);
});

Then("that cell shows no averaged value", async ({}) => {
  expect(sampledValues).toHaveLength(2);
  const average = formatPercent((sampledValues[0]! + sampledValues[1]!) / 2);
  await expect(inspectedElements[1]!).not.toContainText(average);
});

Given("a model in the sonnet band with a metered input and output rate", async ({ page }) => {
  targetModelId = "claude-sonnet-5";
  await expect(
    page.getByTestId(`benchmark-chart-band-sonnet`).getByTestId(`benchmark-chart-row-${targetModelId}`),
  ).toBeVisible();
});

When("the merged chart renders that model's row", async ({ page }) => {
  inspectedElements = [page.getByTestId(`benchmark-chart-row-${targetModelId}`)];
  await expect(inspectedElements[0]!).toBeVisible();
});

Then("the row shows one capability bar, one price-in bar, and one price-out bar", async ({ page }) => {
  for (const kind of ["capability", "price-in", "price-out"]) {
    await expect(page.getByTestId(`benchmark-chart-bar-${kind}-${targetModelId}`)).toHaveCount(1);
  }
});

Then("all three bars appear stacked within that single row, not in separate chart sections", async ({}) => {
  await expect(inspectedElements[0]!.locator('[data-slot="chart-bar-row"]')).toHaveCount(3);
  await expect(inspectedElements[0]!.locator("xpath=ancestor::*[@data-testid='benchmark-chart'][1]")).toHaveCount(1);
});

Given("a model in the haiku band with no metered rate and one subscription rate", async ({ page }) => {
  targetModelId = "deepseek-v4-flash";
  await loadBenchmark(page, "?harness=opencode-go");
  await expect(
    page.getByTestId("benchmark-chart-band-haiku").getByTestId(`benchmark-chart-row-${targetModelId}`),
  ).toBeVisible();
});

Then("the row shows its capability bar as normal", async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-bar-capability-${targetModelId}`)).toBeVisible();
});

Then('the price-bar area of that row shows "Subscription \\($cost\\)" text instead of two bars', async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-subscription-${targetModelId}`)).toContainText(
    /subscription|langganan/i,
  );
  await expect(page.getByTestId(`benchmark-chart-bar-price-in-${targetModelId}`)).toHaveCount(0);
  await expect(page.getByTestId(`benchmark-chart-bar-price-out-${targetModelId}`)).toHaveCount(0);
});

Given("a model with no published composite score on any benchmark", async ({ page }) => {
  targetModelId = "gpt-5.5";
  await expect(page.getByTestId(`benchmark-chart-unrated-model-${targetModelId}`)).toBeVisible();
});

Then("no capability bar or price bar is rendered for that model", async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-row-${targetModelId}`)).toHaveCount(0);
  await expect(page.locator(`[data-testid*="bar-"][data-testid$="-${targetModelId}"]`)).toHaveCount(0);
});

Given("a model in the haiku band with no metered rate and no subscription rate", async ({ page }) => {
  targetModelId = "gemini-3.1-pro";
  await expect(page.getByTestId(`benchmark-chart-row-${targetModelId}`)).toBeVisible();
});

Then('the price-bar area of that row shows a "not reported" placeholder instead of two bars', async ({ page }) => {
  await expect(page.getByTestId(`benchmark-chart-not-reported-${targetModelId}`)).toBeVisible();
  await expect(page.getByTestId(`benchmark-chart-bar-price-in-${targetModelId}`)).toHaveCount(0);
  await expect(page.getByTestId(`benchmark-chart-bar-price-out-${targetModelId}`)).toHaveCount(0);
});

Given("the full roster is rendered below the md breakpoint", async ({ page }) => {
  await navigateAtViewport(page, 390, "en");
  await expect(page.getByTestId("model-table-mobile")).toBeVisible();
});

When("a model's card is inspected before any interaction", async ({ page }) => {
  inspectedElements = [page.locator('[data-testid^="model-card-"][data-model-id]').first()];
  targetModelId = (await inspectedElements[0]!.getAttribute("data-model-id")) ?? "";
});

Then("the card shows the model name, its class, its composite index, and its price", async ({ page }) => {
  for (const field of ["name", "class", "index", "price"]) {
    const value = page.getByTestId(`model-card-${field}-${targetModelId}`);
    await expect(value).toBeVisible();
    expect((await value.textContent())?.trim().length).toBeGreaterThan(0);
  }
});

Then("the card's remaining figures are inside a closed disclosure", async ({ page }) => {
  const details = page.getByTestId(`model-card-details-${targetModelId}`);
  await expect(details).not.toHaveAttribute("open", "");
  expect(await details.locator("dt").count()).toBeGreaterThan(0);
});

Given("a model is rendered in both the roster card and the desktop table", async ({ page }) => {
  await navigateAtViewport(page, 390, "en");
  const card = page.locator('[data-testid^="model-card-"][data-model-id]').first();
  targetModelId = (await card.getAttribute("data-model-id")) ?? "";
  inspectedElements = [
    card,
    page.locator(`[data-testid="model-table-desktop"] tr[data-model-id="${targetModelId}"]`),
    page.locator(`[data-testid="model-table-desktop"] tr[data-model-detail-id="${targetModelId}"]`),
  ];
  expect(await inspectedElements[1]!.count()).toBe(1);
  expect(await inspectedElements[2]!.count()).toBe(1);
});

When("that model's card disclosure is expanded", async ({ page }) => {
  await page.getByTestId(`model-card-disclosure-${targetModelId}`).click();
  await expect(page.getByTestId(`model-card-details-${targetModelId}`)).toHaveAttribute("open", "");
});

Then(
  "the card's summary and expanded content together carry every figure that model's table row carries",
  async ({}) => {
    const cardValues = await inspectedElements[0]!.locator('[data-slot="figure-cell-value"]').allTextContents();
    const tableValues = await inspectedElements[1]!.locator('[data-slot="figure-cell-value"]').allTextContents();
    tableValues.push(...(await inspectedElements[2]!.locator('[data-slot="figure-cell-value"]').allTextContents()));
    expect(new Set(cardValues)).toEqual(new Set(tableValues));
    expect(cardValues.length).toBeGreaterThan(0);
  },
);

// ── URL-backed filters and independent per-band sorting ───────────────────────

Given("the URL carries a harness parameter naming a known harness", async ({ page }) => {
  await loadBenchmark(page, "?harness=cursor");
});

Then("only models that harness exposes are shown in the merged chart", async ({ page }) => {
  const ids = await allChartModelIds(page);
  expect(sorted(ids)).toEqual(sorted(modelsForHarness("cursor")));
});

Then("only models that harness exposes are shown in the data table", async ({ page }) => {
  expect((await tableRowIds(page)).sort()).toEqual((await allChartModelIds(page)).sort());
});

Given("the URL carries a class parameter naming a known band", async ({ page }) => {
  await loadBenchmark(page, "?class=haiku");
});

Then("only models in that band are shown in the merged chart", async ({ page }) => {
  const ids = await allChartModelIds(page);
  const expected = productionGroups.haiku.map((score) => score.model.id);
  expect(sorted(ids)).toEqual(sorted(expected));
  expect(sorted(ids)).toEqual(sorted(await bandRowIds(page, "haiku")));
});

Then("only models in that band are shown in the data table", async ({ page }) => {
  const expected = productionGroups.haiku.map((score) => score.model.id);
  expect(sorted(await tableRowIds(page))).toEqual(sorted(expected));
});

Given("the URL carries both a harness parameter and a class parameter", async ({ page }) => {
  await loadBenchmark(page, "?harness=cursor&class=opus");
});

Then("only models satisfying both filters are shown", async ({ page }) => {
  const ids = await tableRowIds(page);
  const expected = productionGroups.opus
    .filter((score) => score.model.harnesses.includes("cursor"))
    .map((score) => score.model.id);
  expect(sorted(ids)).toEqual(sorted(expected));
  expect(sorted(ids)).toEqual(sorted(await allChartModelIds(page)));
});

Given("the URL carries a harness parameter with an unknown value", async ({ page }) => {
  modelIdsBefore = await tableRowIds(page);
  await loadBenchmark(page, "?harness=not-a-real-harness");
});

Then("every roster model is shown", async ({ page }) => {
  const actual = await tableRowIds(page);
  expect(sorted(actual)).toEqual(sorted(rosterModelIds()));
  expect(sorted(actual)).toEqual(sorted(modelIdsBefore));
});

Then("no error is surfaced to the reader", async ({ page }) => {
  await expect(page.locator("h1")).toBeVisible();
  await expect(page.getByTestId("ai-bench-empty-state")).toHaveCount(0);
});

Given("the URL carries the harness parameter twice with two different known harness values", async ({ page }) => {
  await loadBenchmark(page, "?harness=claude-code&harness=codex-cli");
});

Then("the filter uses the first of the two values", async ({ page }) => {
  await expect(page.locator("#benchmark-filter-harness-desktop")).toHaveValue("claude-code");
});

Then("every roster model matching that harness is shown", async ({ page }) => {
  const ids = await tableRowIds(page);
  expect(sorted(ids)).toEqual(sorted(modelsForHarness("claude-code")));
  expect(sorted(ids)).toEqual(sorted(await allChartModelIds(page)));
});

Given(
  "the URL carries the harness parameter twice, an unknown value first and a known harness second",
  async ({ page }) => {
    modelIdsBefore = await tableRowIds(page);
    await loadBenchmark(page, "?harness=not-a-real-harness&harness=claude-code");
  },
);

Then("the filter falls back to unfiltered", async ({ page }) => {
  await expect(page.locator("#benchmark-filter-harness-desktop")).toHaveValue("");
});

Given("the URL carries a filter combination that matches no model", async ({ page }) => {
  await loadBenchmark(page, "?harness=opencode-go&class=opus");
});

Then("an explicit empty-state message is shown", async ({ page }) => {
  const empty = page.getByTestId("ai-bench-empty-state");
  await expect(empty).toBeVisible();
  expect((await empty.textContent())?.trim().length).toBeGreaterThan(0);
});

Then("the chart and the data table do not render in the empty state", async ({ page }) => {
  await expect(page.getByTestId("benchmark-chart")).toHaveCount(0);
  await expect(page.getByTestId("model-table")).toHaveCount(0);
});

Given("a Class filter is active that excludes every model in the Sonnet band", async ({ page }) => {
  await loadBenchmark(page, "?class=opus");
});

When("the page renders the Sonnet band", async ({ page }) => {
  await expect(page.getByTestId("benchmark-chart-band-sonnet")).toBeVisible();
});

Then("the band shows an explicit message that no models in this class match the current filter", async ({ page }) => {
  const message = page.getByTestId("benchmark-chart-band-sonnet-empty");
  await expect(message).toBeVisible();
  expect((await message.textContent())?.trim().length).toBeGreaterThan(0);
});

Then("the band's own sort control is hidden rather than left interactive", async ({ page }) => {
  await expect(page.locator("#benchmark-chart-sort-sonnet")).toHaveCount(0);
});

When('the reader resets the class filter to "All classes"', async ({ page }) => {
  await page.locator("#benchmark-filter-class-desktop").selectOption("");
  await page.waitForURL((url) => !url.searchParams.has("class"));
});

Then("the URL retains the harness parameter but no longer carries the class parameter", async ({ page }) => {
  const url = new URL(page.url());
  expect(url.searchParams.get("harness")).toBe("cursor");
  expect(url.searchParams.has("class")).toBe(false);
});

Then("the roster reflects only the harness filter", async ({ page }) => {
  const ids = await tableRowIds(page);
  expect(sorted(ids)).toEqual(sorted(modelsForHarness("cursor")));
});

Given("the sonnet band is displaying models in capability-descending order", async ({ page }) => {
  await loadBenchmark(page);
  modelIdsBefore = await bandRowIds(page, "sonnet");
  unrelatedBandOrdersBefore = {
    opus: await bandRowIds(page, "opus"),
    haiku: await bandRowIds(page, "haiku"),
  };
  await expect(page.locator("#benchmark-chart-sort-sonnet")).toHaveValue("capability");
});

When('the reader selects "Price: Low to High" from the sonnet band\'s sort control', async ({ page }) => {
  await page.locator("#benchmark-chart-sort-sonnet").selectOption("price-asc");
  await page.waitForURL(/sort-sonnet=price-asc/);
});

Then("the sonnet band's rows re-render sorted by ascending output rate", async ({ page }) => {
  const labels = await page
    .getByTestId("benchmark-chart-band-sonnet")
    .locator('[data-testid^="benchmark-chart-bar-price-out-"] [data-slot="chart-bar-row-label"]')
    .allTextContents();
  const rates = labels.map((label) => Number(label.match(/\$([\d.]+)/)?.[1])).filter(Number.isFinite);
  expect(rates.length).toBeGreaterThan(1);
  expect(rates).toEqual([...rates].sort((a, b) => a - b));
});

Then("the opus and haiku bands keep their own independently-selected sort order", async ({ page }) => {
  expect(await bandRowIds(page, "opus")).toEqual(unrelatedBandOrdersBefore.opus);
  expect(await bandRowIds(page, "haiku")).toEqual(unrelatedBandOrdersBefore.haiku);
});

Given("the opus band is sorted by capability", async ({ page }) => {
  await loadBenchmark(page);
  modelIdsBefore = await bandRowIds(page, "opus");
  await expect(page.locator("#benchmark-chart-sort-opus")).toHaveValue("capability");
});

When("the reader switches the opus band's sort to price low to high", async ({ page }) => {
  await page.locator("#benchmark-chart-sort-opus").selectOption("price-asc");
  await page.waitForURL(/sort-opus=price-asc/);
});

Then("every model previously in the opus band still appears in the opus band", async ({ page }) => {
  expect((await bandRowIds(page, "opus")).sort()).toEqual([...modelIdsBefore].sort());
});

Then("the set of models in the band is unchanged, only their order changes", async ({ page }) => {
  const after = await bandRowIds(page, "opus");
  expect([...after].sort()).toEqual([...modelIdsBefore].sort());
  expect(after).not.toEqual(modelIdsBefore);
});

Given('the reader has selected "Price: High to Low" for the opus band', async ({ page }) => {
  await loadBenchmark(page);
  await page.locator("#benchmark-chart-sort-opus").selectOption("price-desc");
  await page.waitForURL(/sort-opus=price-desc/);
  modelIdsBefore = await bandRowIds(page, "opus");
});

When("the reader copies the current page URL", async ({ page }) => {
  copiedUrl = page.url();
});

Then('the URL contains a "sort-opus" query parameter set to the descending-price value', async ({}) => {
  expect(new URL(copiedUrl).searchParams.get("sort-opus")).toBe("price-desc");
});

Then("loading that URL directly reproduces the opus band sorted the same way", async ({ page }) => {
  await page.goto(copiedUrl);
  await page.waitForLoadState("networkidle");
  expect(await bandRowIds(page, "opus")).toEqual(modelIdsBefore);
  await expect(page.locator("#benchmark-chart-sort-opus")).toHaveValue("price-desc");
});

Given('a URL containing "sort-sonnet=not-a-real-value"', async ({ page }) => {
  await loadBenchmark(page, "?sort-sonnet=not-a-real-value");
});

When("the page loads with that URL", async ({ page }) => {
  await expect(page.getByTestId("benchmark-chart")).toBeVisible();
});

Then("the sonnet band renders sorted by capability \\(the default\\)", async ({ page }) => {
  await expect(page.locator("#benchmark-chart-sort-sonnet")).toHaveValue("capability");
  const labels = await page
    .getByTestId("benchmark-chart-band-sonnet")
    .locator('[data-slot="chart-bar-label"]')
    .allTextContents();
  const indices = labels.map((label) => Number(label.match(/([\d.]+)\s*$/)?.[1]));
  expect(indices).toEqual([...indices].sort((a, b) => b - a));
});

Then("no error is thrown", async ({ page }) => {
  await expect(page.getByTestId("benchmark-chart")).toBeVisible();
  await expect(page.getByTestId("ai-bench-empty-state")).toHaveCount(0);
});

Given('a query string of "class=haiku&sort-haiku=price-asc"', async ({ page }) => {
  await loadBenchmark(page, "?class=haiku&sort-haiku=price-asc");
  copiedUrl = page.url();
});

When("that query string is decoded and then re-encoded", async ({ page }) => {
  await expect(page.locator("#benchmark-filter-class-desktop")).toHaveValue("haiku");
  await expect(page.locator("#benchmark-chart-sort-haiku")).toHaveValue("price-asc");
});

Then("the re-encoded query string is identical to the original", async ({ page }) => {
  const params = new URL(page.url()).searchParams;
  expect(params.toString()).toBe("class=haiku&sort-haiku=price-asc");
});

Then(
  'a query string carrying the retired "class=light" or "sortLight" decodes to the default unfiltered, capability-sorted state',
  async ({ page }) => {
    await loadBenchmark(page, "?class=light&sortLight=price-asc");
    await expect(page.locator("#benchmark-filter-class-desktop")).toHaveValue("");
    for (const band of ["opus", "sonnet", "haiku"]) {
      await expect(page.locator(`#benchmark-chart-sort-${band}`)).toHaveValue("capability");
    }
    expect(sorted(await tableRowIds(page))).toEqual(sorted(rosterModelIds()));
  },
);

// ── Responsive and disclosure structure ──────────────────────────────────────

Given("a model's roster card is rendered with its disclosure expanded", async ({ page }) => {
  await navigateAtViewport(page, 390, "en");
  const card = page.locator('[data-testid^="model-card-"][data-model-id]').first();
  targetModelId = (await card.getAttribute("data-model-id")) ?? "";
  await page.getByTestId(`model-card-disclosure-${targetModelId}`).click();
  inspectedElements = [page.getByTestId(`model-card-details-${targetModelId}`)];
});

When("the structure of the disclosure's content is inspected", async ({}) => {
  await expect(inspectedElements[0]!.locator(":scope > section")).toHaveCount(2);
});

Then("every field belongs to exactly one labelled group", async ({}) => {
  const sections = inspectedElements[0]!.locator(":scope > section");
  const totalTerms = await inspectedElements[0]!.locator("dt").count();
  let groupedTerms = 0;
  for (let index = 0; index < (await sections.count()); index += 1) {
    await expect(sections.nth(index).locator(":scope > h4")).toHaveCount(1);
    groupedTerms += await sections.nth(index).locator("dt").count();
  }
  expect(groupedTerms).toBe(totalTerms);
  expect(totalTerms).toBeGreaterThan(0);
});

Then("each group's heading is one level below the card's own model-name heading", async ({ page }) => {
  await expect(page.getByTestId(`model-card-name-${targetModelId}`)).toHaveJSProperty("tagName", "H3");
  await expect(inspectedElements[0]!.locator(":scope > section > h4")).toHaveCount(2);
});

Given(
  "a model with more than one unpublished benchmark figure is rendered with its disclosure expanded",
  async ({ page }) => {
    await navigateAtViewport(page, 390, "en");
    targetModelId = "gpt-5.6-terra";
    await page.getByTestId(`model-card-disclosure-${targetModelId}`).click();
    inspectedElements = [page.getByTestId(`model-card-details-${targetModelId}`)];
  },
);

When("the disclosure's name-value groups are inspected", async ({}) => {
  const groups = inspectedElements[0]!.locator("dl > div");
  expect(await groups.count()).toBeGreaterThan(0);
  inspectedElements.push(groups);
});

Then(
  'every unpublished figure\'s label is a term in one single group sharing one "not reported" description',
  async ({}) => {
    const groups = inspectedElements[1]!;
    let shared: ReturnType<Page["locator"]> | undefined;
    for (let index = 0; index < (await groups.count()); index += 1) {
      const candidate = groups.nth(index);
      if (
        (await candidate.locator("dt").count()) >= 2 &&
        /not reported|tidak dilaporkan/i.test((await candidate.locator("dd").textContent()) ?? "")
      ) {
        shared = candidate;
        break;
      }
    }
    expect(shared).toBeDefined();
    expect(await shared!.locator("dt").count()).toBeGreaterThanOrEqual(2);
    await expect(shared!.locator("dd")).toHaveCount(1);
    inspectedElements.push(shared!);
  },
);

Then("no unpublished figure occupies a name-value group of its own", async ({}) => {
  expect(await inspectedElements[2]!.locator("dt").count()).toBeGreaterThanOrEqual(2);
  await expect(inspectedElements[2]!.locator("dd")).toHaveCount(1);
});

Given("the merged chart is rendered at a mobile, a tablet, and a desktop viewport width", async ({ page }) => {
  sampledValues = [390, 768, 1280];
  await navigateAtViewport(page, sampledValues[0]!, "en");
});

When("the DOM structure and the declared text sizes at each width are inspected", async ({ page }) => {
  const widths = [...sampledValues];
  sampledValues = [];
  sampledStrings = [];
  for (const width of widths) {
    await navigateAtViewport(page, width, "en");
    const label = page.locator('[data-slot="chart-bar-label"]').first();
    const row = page.locator('[data-testid^="benchmark-chart-row-"]').first();
    sampledValues.push(await label.evaluate((element) => Number.parseFloat(getComputedStyle(element).fontSize)));
    sampledStrings.push(await row.evaluate((element) => getComputedStyle(element).display));
  }
});

Then("the declared text size of every chart label is identical at all three widths", async ({}) => {
  expect(sampledValues).toHaveLength(3);
  expect(new Set(sampledValues).size).toBe(1);
  expect(sampledValues[0]).toBeGreaterThanOrEqual(12);
});

Then("the row layout changes from stacked to a label column only at the desktop width", async ({}) => {
  expect(sampledStrings).toEqual(["block", "block", "grid"]);
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

Then("every band token meets the WCAG AA contrast ratio against its background", async ({}) => {
  for (const band of BAND_IDS) {
    expect(
      bandContrastRatios[band],
      `--chart-band-${band}-ink vs --chart-band-${band}-wash contrast ratio`,
    ).toBeGreaterThanOrEqual(WCAG_AA_MIN_CONTRAST);
  }
});

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
