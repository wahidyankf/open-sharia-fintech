import { createBdd } from "playwright-bdd";
import { expect, type Page } from "@playwright/test";

const { Given, When, Then } = createBdd();

/**
 * A real docs page that renders both the desktop resizable rail
 * (`ResizableSidebar`, `apps/ayokoding-www/src/features/navigation/shell/resizable-sidebar.tsx`)
 * and — via `Header` — the mobile drawer trigger. Matches the target already used by
 * `navigation.steps.ts`.
 */
const DOCS_PAGE = "/en/learn/overview";

/** `localStorage` key `ResizableSidebar` persists the desktop rail's chosen width under. */
const SIDEBAR_STORAGE_KEY = "ayokoding-sidebar-width";

/** Selector for the primitive's outer sizing element (see `resizable-panel.tsx`'s `data-slot`). */
const PANEL_SELECTOR = '[data-slot="resizable-panel"]';

/**
 * `clampWidth`'s upper band bound, as a percentage of the viewport width — mirrors
 * `width-model.ts`'s `MAX_PCT`, duplicated locally the same way `resizable-sidebar.tsx` already
 * duplicates `MIN_WIDTH_PCT`/`MAX_WIDTH_PCT` rather than importing library internals into a test.
 */
const MAX_WIDTH_PCT = 35;

/** Sets the desktop rail's persisted width directly, mirroring a prior drag/keyboard commit. */
async function setPersistedSidebarWidth(page: Page, widthPx: number): Promise<void> {
  await page.evaluate(({ key, px }) => localStorage.setItem(key, String(px)), {
    key: SIDEBAR_STORAGE_KEY,
    px: widthPx,
  });
}

Given(
  "a resizable panel rendered at {int} pixels with a {int} to {int} pixel band",
  async ({ page }, startPx: number, _minPx: number, maxPx: number) => {
    // Tune the viewport so MAX_WIDTH_PCT of it equals the scenario's literal band maximum,
    // making the real app's percentage-of-viewport clamp band match the primitive's synthetic
    // pixel band exactly (e.g. a 150-350 band ⇒ a 1000px-wide viewport).
    const viewportWidth = Math.round(maxPx / (MAX_WIDTH_PCT / 100));
    await page.setViewportSize({ width: viewportWidth, height: 800 });
    await page.goto(DOCS_PAGE);
    await setPersistedSidebarWidth(page, startPx);
    await page.reload();

    const panel = page.locator(PANEL_SELECTOR);
    await expect(panel).toHaveCSS("width", `${startPx}px`);
  },
);

When("the user drags the separator handle {int} pixels to the right", async ({ page }, deltaPx: number) => {
  const handle = page.getByRole("separator");
  const box = await handle.boundingBox();
  if (!box) {
    throw new Error("the separator handle has no bounding box (is it rendered and visible?)");
  }

  const startX = box.x + box.width / 2;
  const y = box.y + box.height / 2;
  await page.mouse.move(startX, y);
  await page.mouse.down();
  await page.mouse.move(startX + deltaPx, y, { steps: 10 });
  await page.mouse.up();
});

Then("the panel width becomes {int} pixels", async ({ page }, expectedPx: number) => {
  const panel = page.locator(PANEL_SELECTOR);
  await expect(panel).toHaveCSS("width", `${expectedPx}px`);
});

Then("the panel width stops at {int} pixels", async ({ page }, expectedPx: number) => {
  const panel = page.locator(PANEL_SELECTOR);
  await expect(panel).toHaveCSS("width", `${expectedPx}px`);
});

/**
 * Bridges the keyboard scenario's Given (which records the panel's known starting width) to its
 * Then (which asserts the width grew from that starting point) — the two steps share one `page`
 * fixture instance per scenario, so a `WeakMap` keyed by `page` is scenario-safe without any
 * shared mutable module state leaking across parallel scenario runs.
 */
const keyboardScenarioStartWidth = new WeakMap<Page, number>();

Given("the separator handle is focused on a panel at {int} pixels", async ({ page }, startPx: number) => {
  await page.goto(DOCS_PAGE);
  await setPersistedSidebarWidth(page, startPx);
  await page.reload();

  const panel = page.locator(PANEL_SELECTOR);
  await expect(panel).toHaveCSS("width", `${startPx}px`);
  await page.getByRole("separator").focus();
  keyboardScenarioStartWidth.set(page, startPx);
});

When("the user presses ArrowRight", async ({ page }) => {
  await page.keyboard.press("ArrowRight");
});

Then("the panel width increases by the keyboard step", async ({ page }) => {
  const before = keyboardScenarioStartWidth.get(page);
  if (before === undefined) {
    throw new Error("expected the panel's starting width to have been recorded by the Given step");
  }

  const panel = page.locator(PANEL_SELECTOR);
  await expect.poll(() => panel.evaluate((el) => el.getBoundingClientRect().width)).toBeGreaterThan(before);
});

Then("the handle exposes the new width via aria-valuenow", async ({ page }) => {
  const panel = page.locator(PANEL_SELECTOR);
  const width = await panel.evaluate((el) => el.getBoundingClientRect().width);
  await expect(page.getByRole("separator")).toHaveAttribute("aria-valuenow", String(width));
});

Given("the reader has resized the docs sidebar to {int} pixels on a desktop viewport", async ({ page }, px: number) => {
  await page.goto(DOCS_PAGE);
  await setPersistedSidebarWidth(page, px);
});

When("the reader reloads the page", async ({ page }) => {
  await page.reload();
});

Then("the docs sidebar renders at {int} pixels", async ({ page }, expectedPx: number) => {
  const panel = page.locator(PANEL_SELECTOR);
  await expect(panel).toHaveCSS("width", `${expectedPx}px`);
});

Given("the docs page is open at a {int} pixel viewport", async ({ page }, viewportWidth: number) => {
  await page.setViewportSize({ width: viewportWidth, height: 800 });
  await page.goto(DOCS_PAGE);
});

When("the layout renders", async ({ page }) => {
  await expect(page.getByRole("article")).toBeVisible();
});

Then("the resizable aside is not displayed", async ({ page }) => {
  const aside = page.locator(`aside:has(${PANEL_SELECTOR})`);
  await expect(aside).toBeHidden();
});

Then("navigation is available through the mobile drawer", async ({ page }) => {
  await expect(page.getByRole("button", { name: "Open navigation menu" })).toBeVisible();
});

/** The tree container `sidebar-tree.tsx` wraps its depth-0 `<ul>` in, so long labels scroll. */
const SCROLL_CONTAINER_SELECTOR = `aside:has(${PANEL_SELECTOR}) .overflow-x-auto`;

Given(
  "a docs sidebar narrowed to {int} pixels containing a nav label wider than {int} pixels",
  async ({ page }, widthPx: number) => {
    await page.goto(DOCS_PAGE);
    await setPersistedSidebarWidth(page, widthPx);
    await page.reload();

    const panel = page.locator(PANEL_SELECTOR);
    await expect(panel).toHaveCSS("width", `${widthPx}px`);
  },
);

When("the reader views the sidebar", async ({ page }) => {
  await expect(page.getByRole("article")).toBeVisible();
});

Then("the sidebar content area is horizontally scrollable", async ({ page }) => {
  const scrollContainer = page.locator(SCROLL_CONTAINER_SELECTOR);
  await expect(scrollContainer).toHaveCount(1);
  await expect.poll(async () => scrollContainer.evaluate((el) => el.scrollWidth > el.clientWidth)).toBe(true);
});

Then("the label is not clipped or wrapped", async ({ page }) => {
  const noWrapLinks = page.locator(`aside:has(${PANEL_SELECTOR}) a.whitespace-nowrap:not(.truncate)`);
  await expect(noWrapLinks.first()).toBeAttached();
});

/** Selector for `mobile-nav.tsx`'s `SheetContent` root (see its `data-slot`). */
const MOBILE_DRAWER_SELECTOR = '[data-slot="sheet-content"]';

Given("the mobile nav drawer is open at a {int} pixel viewport", async ({ page }, viewportWidth: number) => {
  await page.setViewportSize({ width: viewportWidth, height: 800 });
  await page.goto(DOCS_PAGE);
  await page.getByRole("button", { name: "Open navigation menu" }).click();
  await expect(page.locator(MOBILE_DRAWER_SELECTOR)).toBeVisible();
});

When("the reader selects the wider preset", async ({ page }) => {
  await page.getByRole("button", { name: "Wide" }).click();
});

Then("the drawer renders at the wider preset width", async ({ page }) => {
  await expect(page.locator(MOBILE_DRAWER_SELECTOR)).toHaveCSS("width", "360px");
});
