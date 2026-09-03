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

/** `clampWidth`'s lower band bound, as a percentage of the viewport width — mirrors
 * `width-model.ts`'s `MIN_PCT` (see `MAX_WIDTH_PCT` above for why this is duplicated locally). */
const MIN_WIDTH_PCT = 15;

/** Sets the desktop rail's persisted width directly, mirroring a prior drag/keyboard commit. */
async function setPersistedSidebarWidth(page: Page, widthPx: number): Promise<void> {
  await page.evaluate(({ key, px }) => localStorage.setItem(key, String(px)), {
    key: SIDEBAR_STORAGE_KEY,
    px: widthPx,
  });
}

/**
 * Bridges "a resizable panel rendered at N pixels with a M to K pixel band" (which records the
 * panel's pre-drag width) to the mid-drag Then step that must confirm nothing new has persisted
 * yet — same per-page `WeakMap` technique as `keyboardScenarioStartWidth` below.
 */
const dragScenarioStartWidth = new WeakMap<Page, number>();

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
    dragScenarioStartWidth.set(page, startPx);
  },
);

/**
 * Presses down on the separator handle and drags it by `deltaPx`, releasing the mouse button
 * afterward unless `release` is `false` — the shared drag mechanics behind every drag-driven
 * Given/When step in this file.
 */
async function dragSeparatorHandle(page: Page, deltaPx: number, release = true): Promise<void> {
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
  if (release) {
    await page.mouse.up();
  }
}

When("the user drags the separator handle {int} pixels to the right", async ({ page }, deltaPx: number) => {
  await dragSeparatorHandle(page, deltaPx);
});

When(
  "the user drags the separator handle {int} pixels to the right without releasing",
  async ({ page }, deltaPx: number) => {
    await dragSeparatorHandle(page, deltaPx, false);
  },
);

Then("the panel width becomes {int} pixels", async ({ page }, expectedPx: number) => {
  const panel = page.locator(PANEL_SELECTOR);
  await expect(panel).toHaveCSS("width", `${expectedPx}px`);
});

Then(
  "the panel width becomes {int} pixels but nothing is yet persisted to localStorage",
  async ({ page }, expectedPx: number) => {
    const panel = page.locator(PANEL_SELECTOR);
    await expect(panel).toHaveCSS("width", `${expectedPx}px`);

    const startPx = dragScenarioStartWidth.get(page);
    if (startPx === undefined) {
      throw new Error("expected the panel's starting width to have been recorded by the Given step");
    }
    const persisted = await page.evaluate((key) => localStorage.getItem(key), SIDEBAR_STORAGE_KEY);
    expect(persisted).toBe(String(startPx));

    // Release the still-in-progress drag so it doesn't leak an active pointer-capture into
    // whatever this page does next.
    await page.mouse.up();
  },
);

Then("the width {int} pixels is persisted to localStorage", async ({ page }, expectedPx: number) => {
  const persisted = await page.evaluate((key) => localStorage.getItem(key), SIDEBAR_STORAGE_KEY);
  expect(persisted).toBe(String(expectedPx));
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

Given("a resizable panel is rendered", async ({ page }) => {
  await page.goto(DOCS_PAGE);
  await expect(page.locator(PANEL_SELECTOR)).toBeVisible();
});

// Shared by both "The handle exposes separator semantics" and "The handle's accessible label can
// be localized" — inspection happens directly in each scenario's own Then/And steps below, via
// role/attribute locators rather than a snapshot taken here.
When("the accessibility tree is inspected", async () => {});

Then('the handle has role "separator"', async ({ page }) => {
  await expect(page.getByRole("separator")).toBeVisible();
});

Then('the handle has aria-orientation "vertical"', async ({ page }) => {
  await expect(page.getByRole("separator")).toHaveAttribute("aria-orientation", "vertical");
});

Then("the handle prevents native text selection", async ({ page }) => {
  // `select-none` (`user-select: none`) is the Tailwind utility resizable-panel.tsx's handle
  // carries unconditionally — see resizable-panel.steps.tsx's own unit-level assertion of the
  // same className for the underlying mechanism this checks the real computed style for instead.
  // Playwright's bundled WebKit engine reports an empty string for the unprefixed `user-select`
  // computed style (it only resolves the `-webkit-user-select` longhand it actually implements),
  // so both are read directly here rather than relying on `toHaveCSS`'s single-property match.
  await expect
    .poll(() =>
      page.getByRole("separator").evaluate((el) => {
        const style = getComputedStyle(el);
        return style.userSelect || style.getPropertyValue("-webkit-user-select");
      }),
    )
    .toBe("none");
});

Given('a resizable panel is rendered with a custom handle label "Ubah ukuran panel"', async ({ page }) => {
  // AyoKoding's own "id" locale translation for `resizableSidebarHandleLabel` IS this exact
  // string (see apps/ayokoding-www/src/features/i18n/core/translations.ts) — the primitive's
  // generic "custom label" concept is exercised here via the real app's Indonesian locale route
  // rather than a synthetic prop, matching this file's "real browser, real docs page" convention.
  await page.goto("/id/belajar/ikhtisar");
  await expect(page.locator(PANEL_SELECTOR)).toBeVisible();
});

Then('the handle has aria-label "Ubah ukuran panel"', async ({ page }) => {
  await expect(page.getByRole("separator")).toHaveAttribute("aria-label", "Ubah ukuran panel");
});

Given(
  "a resizable panel rendered at {int} pixels has been dragged to {int} pixels",
  async ({ page }, startPx: number, draggedPx: number) => {
    await page.goto(DOCS_PAGE);
    await setPersistedSidebarWidth(page, startPx);
    await page.reload();

    const panel = page.locator(PANEL_SELECTOR);
    await expect(panel).toHaveCSS("width", `${startPx}px`);

    await dragSeparatorHandle(page, draggedPx - startPx);
    await expect(panel).toHaveCSS("width", `${draggedPx}px`);
  },
);

When("the user double-clicks the separator handle", async ({ page }) => {
  await page.getByRole("separator").dblclick();
});

Then("the panel width returns to {int} pixels", async ({ page }, expectedPx: number) => {
  const panel = page.locator(PANEL_SELECTOR);
  await expect(panel).toHaveCSS("width", `${expectedPx}px`);
});

Given(
  "the separator handle is focused on a panel at {int} pixels with a {int} to {int} pixel band",
  async ({ page }, startPx: number, _minPx: number, maxPx: number) => {
    const viewportWidth = Math.round(maxPx / (MAX_WIDTH_PCT / 100));
    await page.setViewportSize({ width: viewportWidth, height: 800 });
    await page.goto(DOCS_PAGE);
    await setPersistedSidebarWidth(page, startPx);
    await page.reload();

    const panel = page.locator(PANEL_SELECTOR);
    await expect(panel).toHaveCSS("width", `${startPx}px`);
    await page.getByRole("separator").focus();
  },
);

When("the user presses Home", async ({ page }) => {
  await page.keyboard.press("Home");
});

When("the user presses End", async ({ page }) => {
  await page.keyboard.press("End");
});

Given("a corrupted localStorage value of {int} pixels for the panel width", async ({ page }, corruptedPx: number) => {
  await page.goto(DOCS_PAGE);
  await setPersistedSidebarWidth(page, corruptedPx);
});

/** Bridges the re-clamp scenario's When (which knows the target band) to its Then (which asserts
 * against that band's max) — same per-page `WeakMap` technique used elsewhere in this file. */
const reclampMaxWidth = new WeakMap<Page, number>();

When(
  "a resizable panel with a {int} to {int} pixel band is rendered",
  async ({ page }, _minPx: number, maxPx: number) => {
    const viewportWidth = Math.round(maxPx / (MAX_WIDTH_PCT / 100));
    await page.setViewportSize({ width: viewportWidth, height: 800 });
    // The corrupted value was already written to localStorage by the Given step (against a page
    // that hadn't yet been sized to this band) — reloading now re-mounts under the right
    // viewport, so useResizableWidth's mount-time re-clamp runs against the intended band.
    await page.reload();
    reclampMaxWidth.set(page, maxPx);
  },
);

Then("the panel width renders at the maximum band width, not the corrupted value", async ({ page }) => {
  const maxPx = reclampMaxWidth.get(page);
  if (maxPx === undefined) {
    throw new Error("expected the clamp band's max width to have been recorded by the When step");
  }
  const panel = page.locator(PANEL_SELECTOR);
  await expect(panel).toHaveCSS("width", `${maxPx}px`);
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

/**
 * The courses index — a stable (not subject to this plan's learn-section relocation, DD-42)
 * page whose sidebar shows all 37 course titles at once, several long enough (e.g. "21 ·
 * Object-Oriented Design & Patterns") to force horizontal scroll, and numerous enough to force
 * vertical scroll even at a full-height viewport — unlike `DOCS_PAGE` (`/en/learn/overview`),
 * whose own sidebar now shows only the three top-level learn buckets (DD-40) plus itself, too
 * short/narrow for these two overflow scenarios after the six-domain relocation (DD-41/DD-42).
 */
const TALL_WIDE_SIDEBAR_PAGE = "/en/learn/courses";

Given(
  "a docs sidebar narrowed to {int} pixels containing a nav label wider than {int} pixels",
  async ({ page }, widthPx: number, _minLabelWidthPx: number) => {
    // `useResizableWidth` re-clamps a persisted width against MIN_WIDTH_PCT of the CURRENT
    // viewport on mount (see width-model.ts's `clampWidth`, wired since the primitive was
    // introduced). At Playwright's default 1280px-wide viewport, MIN_WIDTH_PCT (15%) is 192px —
    // above this scenario's literal 150px — so the persisted value silently got clamped upward
    // instead of applying. Size the viewport so `widthPx` sits exactly at the minimum band
    // bound and is therefore not clamped, mirroring the same technique already used by the
    // "resizable panel rendered at N pixels with a M to K pixel band" step above.
    const viewportWidth = Math.round(widthPx / (MIN_WIDTH_PCT / 100));
    await page.setViewportSize({ width: viewportWidth, height: 800 });
    await page.goto(TALL_WIDE_SIDEBAR_PAGE);
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

/**
 * The div `resizable-sidebar.tsx` renders as `ResizablePanel`'s sole child — the immediate
 * child of the primitive's `resizable-panel-content` slot — which owns the rail's vertical
 * scroll (see that file's docstring for why it, not `<aside>`, is the real scroll owner).
 */
const VERTICAL_SCROLL_CONTAINER_SELECTOR = `aside:has(${PANEL_SELECTOR}) [data-slot="resizable-panel-content"] > div`;

Given("a docs sidebar whose nav tree is taller than the visible rail height", async ({ page }) => {
  // Rather than fabricating tall content, shrink the viewport height enough that a real page's
  // nav tree exceeds the rail's `h-[calc(100vh-4rem)]` height — mirroring the "narrowed to N
  // pixels" technique above, which shrinks width instead for the horizontal scenario. Uses
  // `TALL_WIDE_SIDEBAR_PAGE` (the courses index, 37 titles) rather than `DOCS_PAGE`: after the
  // six-domain relocation (DD-40/DD-41) the `/en/learn/overview` sidebar shows only the three
  // top-level learn buckets plus itself, too short to overflow the rail even at a 300px viewport.
  await page.setViewportSize({ width: 1280, height: 300 });
  await page.goto(TALL_WIDE_SIDEBAR_PAGE);
});

Then("the sidebar content area is vertically scrollable", async ({ page }) => {
  const scrollContainer = page.locator(VERTICAL_SCROLL_CONTAINER_SELECTOR);
  await expect(scrollContainer).toHaveCount(1);
  await expect.poll(async () => scrollContainer.evaluate((el) => el.scrollHeight > el.clientHeight)).toBe(true);
});

Then("the horizontal scroll behavior is unaffected", async ({ page }) => {
  // This scenario's 1280px-wide viewport (see the Given step above, which only shrinks height)
  // means a real docs label is unlikely to overflow horizontally here, so asserting live
  // `scrollWidth > clientWidth` overflow (as the dedicated horizontal scenario at line 356-360
  // does) would be flaky at this viewport. Instead assert the container still carries the
  // `overflow-x: auto` computed style — proving the horizontal-scroll *capability* the vertical
  // fix must not remove, without depending on this viewport happening to trigger overflow.
  const scrollContainer = page.locator(SCROLL_CONTAINER_SELECTOR);
  await expect(scrollContainer).toHaveCount(1);
  await expect(scrollContainer).toHaveCSS("overflow-x", "auto");
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
