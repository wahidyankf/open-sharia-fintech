import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

// ---------------------------------------------------------------------------
// course-paths plan (ayokoding-learning-path-03-navigation-ui), Phase 3 — e2e step definitions.
//
// Every scenario below runs against the fixture manifest set at
// `apps/ayokoding-www-fe-e2e/fixtures/manifests/` (see that directory's own README.md) — the
// running server's `AYOKODING_WEB_MANIFESTS_DIR` is pointed there by `playwright.config.ts`
// (local) and `infra/dev/ayokoding-www/docker-compose.yml` (CI), so every "Given a fixture ..."
// step below is a no-op: the fixture data is already loaded server-side before any scenario runs.
// ---------------------------------------------------------------------------

const PHONE_VIEWPORT = { width: 375, height: 812 };

// ---------------------------------------------------------------------------
// Cycle 3.1 — path landing renders its courses in manifest order, path-context query param
// (breadcrumb.feature)
// ---------------------------------------------------------------------------

Given("a fixture path manifest is loaded by the manifest repository", async () => {
  // No-op — see file header.
});

When("a reader opens that fixture path's landing page under \\/en\\/learn\\/paths\\/", async ({ page }) => {
  await page.goto("/en/learn/paths/careers/interview-ready/backend-track");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/breadcrumb.feature:A path landing page lists its courses in manifest order
Then("the courses appear in the fixture manifest's courseOrder", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: /backend track \(interview-ready\) syllabus/i });
  const links = nav.getByRole("link");
  await expect(links).toHaveCount(2);
  await expect(links.nth(0)).toContainText("Just Enough Python");
  await expect(links.nth(1)).toContainText("Data Structures");
});

Then("every course link carries the path context query parameter", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: /backend track \(interview-ready\) syllabus/i });
  const links = nav.getByRole("link");
  const count = await links.count();
  expect(count).toBeGreaterThan(0);
  for (let i = 0; i < count; i++) {
    const href = await links.nth(i).getAttribute("href");
    expect(href).toContain("?path=careers/interview-ready/backend-track");
  }
});

// ---------------------------------------------------------------------------
// Cycle 3.1b-i — careers category landing arc chooser (category-landing-arc-chooser.feature)
// ---------------------------------------------------------------------------

Given("a fixture careers manifest set with three arcs is loaded", async () => {
  // No-op — the fixture set has exactly three careers arcs (interview-ready,
  // immediately-effective, fundamentally-strong).
});

When("a reader opens the careers category landing at \\/en\\/learn\\/paths\\/careers\\/", async ({ page }) => {
  await page.goto("/en/learn/paths/careers");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/category-landing-arc-chooser.feature:The careers category landing offers an arc chooser
// The literal parentheses in the Gherkin step text ("role(s)") must be escaped (`\\(`/`\\)`) —
// Cucumber Expressions otherwise parse unescaped `(text)` as optional-text syntax, which would
// match "role" or "roles" but never the literal characters "role(s)" the feature file contains.
Then("the page renders one arc card per arc with its member role\\(s\\) previewed", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "Careers arcs" });
  const arcCards = nav.getByRole("link");
  await expect(arcCards).toHaveCount(3);
});

Then("the immediately-effective arc card previews exactly two member roles", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "Careers arcs" });
  // Exact humanized casing (no `i` flag): the arc card's accessible name renders the arc's
  // humanized/authored title (UWT-001 fix, phase-5 rule-15 retest — `category-landing.tsx`'s
  // `ArcCard` builds its `aria-label` from `arcTitle`, not the raw `arc` slug), e.g. "Explore the
  // Immediately-Effective arc — …", never the raw kebab-case slug this regex originally matched.
  // A case-insensitive flag here would pass identically for either the pre-fix raw slug or the
  // post-fix humanized title (they differ only in case), so it must stay case-sensitive to detect
  // a regression back to the raw-slug defect this assertion exists to catch.
  const arcCard = nav.getByRole("link", { name: /Explore the Immediately-Effective arc/ });
  await expect(arcCard).toBeVisible();
  const roleBadges = arcCard.getByRole("listitem");
  await expect(roleBadges).toHaveCount(2);
});

// ---------------------------------------------------------------------------
// Cycle 3.1b-ii — skills category landing fixed-arc statement (skills-fixed-arc-statement.feature)
// ---------------------------------------------------------------------------

Given("a fixture skills manifest set is loaded", async () => {
  // No-op — the fixture set has two skills paths (e2e-fixture-alpha, e2e-fixture-beta).
});

When("a reader opens the skills category landing at \\/en\\/learn\\/paths\\/skills\\/", async ({ page }) => {
  await page.goto("/en/learn/paths/skills");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/skills-fixed-arc-statement.feature:The skills category landing states its fixed arc once, with no chooser
Then("the page renders the ramp promise once as a statement, not a question", async ({ page }) => {
  const promise = page.getByText("Get up and running fast on the ramp", { exact: false });
  await expect(promise).toHaveCount(1);
  const text = await promise.textContent();
  expect(text?.trim().endsWith("?")).toBe(false);
});

Then("no arc-selection control is present anywhere on the page", async ({ page }) => {
  await expect(page.getByRole("navigation", { name: "Careers arcs" })).toHaveCount(0);
  await expect(page.getByRole("link", { name: /Explore the .* arc/ })).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// Cycle 3.1c-i — arc landing, two-role state (arc-landing-two-role.feature)
// ---------------------------------------------------------------------------

Given("the fixture immediately-effective arc manifest lists two roles", async () => {
  // No-op — immediately-effective has frontend-track (2 courses) and backend-track (3 courses).
});

When(
  "a reader opens the arc landing at \\/en\\/learn\\/paths\\/careers\\/immediately-effective\\/",
  async ({ page }) => {
    await page.goto("/en/learn/paths/careers/immediately-effective");
    await page.waitForLoadState("networkidle");
  },
);

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/arc-landing-two-role.feature:An arc landing with two paths renders both role cards without a placeholder
Then("both role cards render side by side with their own course counts", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "immediately-effective paths" });
  const cards = nav.getByRole("link");
  await expect(cards).toHaveCount(2);
  await expect(page.getByText("~2 courses")).toBeVisible();
  await expect(page.getByText("~3 courses")).toBeVisible();
});

Then("neither card is a placeholder or an empty grid cell", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "immediately-effective paths" });
  await expect(nav.getByRole("link", { name: /Start the Frontend Track/ })).toBeVisible();
  await expect(nav.getByRole("link", { name: /Start the Backend Track/ })).toBeVisible();
});

// ---------------------------------------------------------------------------
// Cycle 3.1c-ii — arc landing, single-role state (arc-landing-one-role.feature)
// ---------------------------------------------------------------------------

Given("a fixture arc manifest lists exactly one role", async () => {
  // No-op — interview-ready has exactly one role (backend-track).
});

When("a reader opens that arc's landing page", async ({ page }) => {
  await page.goto("/en/learn/paths/careers/interview-ready");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/arc-landing-one-role.feature:An arc landing with one path renders a full card, not a sparse stub
Then("the single role card renders with an inline first-phase syllabus preview", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "interview-ready paths" });
  await expect(nav.getByRole("link")).toHaveCount(1);
  await expect(page.getByText("Starts with:")).toBeVisible();
});

Then("the layout does not reserve or render a visibly empty second card", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "interview-ready paths" });
  const items = nav.locator("> ul > li");
  await expect(items).toHaveCount(1);
});

// ---------------------------------------------------------------------------
// Cycle 3.1d — skills path landing body content (skills-path-landing-body.feature)
// ---------------------------------------------------------------------------

Given(
  "two fixture skills paths whose landing bodies declare different runway-justification paragraphs for their differing first boundaries",
  async () => {
    // No-op — e2e-fixture-alpha's and e2e-fixture-beta's `_index.md` fixture content declare
    // distinct authored paragraphs (see apps/ayokoding-www/content/en/learn/paths/skills/
    // e2e-fixture-{alpha,beta}/_index.md).
  },
);

When("a reader opens either skills path's landing page", async () => {
  // No-op — each Then step below navigates to both fixture paths itself, since this scenario
  // compares one path's page against the other's.
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/skills-path-landing-body.feature:A skills path's authored runway-justification content renders on its own landing
Then(
  "that path's landing renders its own authored runway-justification paragraph between the title and the syllabus",
  async ({ page }) => {
    await page.goto("/en/learn/paths/skills/e2e-fixture-alpha");
    await page.waitForLoadState("networkidle");
    await expect(page.getByText("never opened a terminal", { exact: false })).toBeVisible();

    await page.goto("/en/learn/paths/skills/e2e-fixture-beta");
    await page.waitForLoadState("networkidle");
    await expect(page.getByText("never touched a database", { exact: false })).toBeVisible();
  },
);

Then("the other path's justification paragraph never appears on this page", async ({ page }) => {
  await page.goto("/en/learn/paths/skills/e2e-fixture-alpha");
  await page.waitForLoadState("networkidle");
  await expect(page.getByText("never touched a database", { exact: false })).toHaveCount(0);

  await page.goto("/en/learn/paths/skills/e2e-fixture-beta");
  await page.waitForLoadState("networkidle");
  await expect(page.getByText("never opened a terminal", { exact: false })).toHaveCount(0);
});

// ---------------------------------------------------------------------------
// Cycle 3.2 — landing hero (landing-hero.feature)
// ---------------------------------------------------------------------------

Given("a first-time visitor opens the site landing page at \\/en", async ({ page }) => {
  await page.goto("/en");
  await page.waitForLoadState("networkidle");
});

When("the hero section renders", async () => {
  // No-op — the navigation above already waited for the hero's Server Component render.
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/landing-hero.feature:The landing hero surfaces the four goal paths directly
Then("the hero shows a goal-labeled path card for each published path", async ({ page }) => {
  const hero = page.locator("section").first();
  await expect(hero.getByText("Choose your path")).toBeVisible();
  const cards = hero.getByRole("link", { name: /^Start the / });
  await expect(cards).toHaveCount(4);
});

Then('a "Compare all paths" link to \\/en\\/learn\\/paths is visible below the cards', async ({ page }) => {
  const link = page.getByRole("link", { name: "Compare all paths →" });
  await expect(link).toBeVisible();
  expect(await link.getAttribute("href")).toBe("/en/learn/paths");
});

// ---------------------------------------------------------------------------
// Cycle 3.4 — aggregate feature binder (canonical-fallback / invalid-path-fallback /
// omitted-course / path-order-nav / paths-hub-category-grouping)
// ---------------------------------------------------------------------------

// canonical-fallback.feature, scenario 1 — production manifests place
// just-enough-python in four career paths.
Given(
  "a reader opens a course URL \\/en\\/learn\\/courses\\/<course-id> with no path context query parameter",
  async ({ page }) => {
    await page.goto("/en/learn/courses/just-enough-python");
  },
);

When("the course page renders", async ({ page }) => {
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/canonical-fallback.feature:A course deep-linked without path context renders the canonical view
Then("the course body renders in full with the content-tree breadcrumb and its prerequisite list", async ({ page }) => {
  await expect(page.getByRole("navigation", { name: "Breadcrumb" })).toBeVisible();
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});

Then('a "this course is part of" affordance lists every path that includes the course', async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "This course is part of" });
  const paths = [
    {
      pathId: "careers/fundamentally-strong/software-engineer",
      title: "Fundamentally Strong Software Engineer",
    },
    {
      pathId: "careers/immediately-effective/ai-engineer",
      title: "Immediately Effective AI Engineer",
    },
    {
      pathId: "careers/immediately-effective/software-engineer",
      title: "Immediately Effective Software Engineer",
    },
    {
      pathId: "careers/interview-ready/software-engineer",
      title: "Interview-Ready Software Engineer",
    },
  ];

  await expect(nav).toBeVisible();
  await expect(nav.getByRole("link")).toHaveCount(paths.length);

  for (const path of paths) {
    await expect(nav.getByRole("link", { name: path.title })).toHaveAttribute(
      "href",
      `/en/learn/paths/${path.pathId}?path=${path.pathId}`,
    );
  }
});

// canonical-fallback.feature, scenario 2 — generic sidebar unchanged.
// "When the page renders" is shared with `cost-of-living-calculator.steps.ts` (identical
// `page.waitForLoadState("networkidle")` semantics) — not redefined here.
Given("a reader opens a canonical course URL with no path context query parameter", async ({ page }) => {
  await page.goto("/en/learn/courses/just-enough-python");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/canonical-fallback.feature:A course opened without path context renders the generic sidebar unchanged
Then("the left sidebar shows the generic content tree exactly as it does elsewhere in the site", async ({ page }) => {
  await expect(page.getByRole("navigation", { name: "Sidebar navigation" })).toBeVisible();
});

Then("no path rail, path readout, or path breadcrumb segment appears", async ({ page }) => {
  await expect(page.getByRole("navigation", { name: /course list$/ })).toHaveCount(0);
  await expect(page.getByRole("button", { name: /Open path course list/ })).toHaveCount(0);
});

// invalid-path-fallback.feature.
Given("a reader opens a course URL with a path context that names no known path", async ({ page }) => {
  await page.goto("/en/learn/courses/just-enough-python?path=careers/does-not-exist/no-such-role");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/invalid-path-fallback.feature:An invalid path context falls back to the canonical view
// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/omitted-course.feature:A course omitted from a path shows no path nav for that path
Then("the course renders the canonical standalone view", async ({ page }) => {
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
  await expect(page.getByRole("navigation", { name: /course list$/ })).toHaveCount(0);
  await expect(page.getByRole("button", { name: /Open path course list/ })).toHaveCount(0);
});

Then("no error is shown", async ({ page }) => {
  await expect(page.locator("body")).not.toContainText("Application error");
  await expect(page.getByRole("heading", { level: 1 })).toBeVisible();
});

// omitted-course.feature — sql-essentials is not in the interview-ready/backend-track manifest.
Given("a course is not listed in a given path's manifest", async () => {
  // No-op — sql-essentials belongs to careers/immediately-effective/backend-track only.
});

When("a reader opens that course with that path's context", async ({ page }) => {
  await page.goto("/en/learn/courses/sql-essentials?path=careers/interview-ready/backend-track");
  await page.waitForLoadState("networkidle");
});

Then("neither the path rail nor the path banner is shown for that path", async ({ page }) => {
  await expect(page.getByRole("navigation", { name: /course list$/ })).toHaveCount(0);
  await expect(page.getByRole("button", { name: /Open path course list/ })).toHaveCount(0);
});

// path-order-nav.feature, scenario 2 — desktop rail.
Given("a reader opens a course in path context on a desktop-width viewport", async ({ page }) => {
  await page.goto("/en/learn/courses/backend-essentials?path=careers/immediately-effective/backend-track");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/path-order-nav.feature:The path rail shows the whole ordered arc beside a course at desktop width
Then("the left rail lists that path's courses in manifest order with the current course marked", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "Backend Track (Immediately-Effective) course list" });
  const items = nav.getByRole("listitem");
  await expect(items).toHaveCount(3);
  await expect(items.nth(1).getByRole("link")).toHaveAttribute("aria-current", "page");
});

Then("the current course is distinguished by a marker and weight, not by colour alone", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "Backend Track (Immediately-Effective) course list" });
  // Playwright's `getByRole` does not support a `current` filter option — filter by the actual
  // `aria-current="page"` DOM attribute instead.
  const current = nav.locator('a[aria-current="page"]');
  await expect(current).toContainText("▸");
});

Then("the rail offers a link back to the full path and to the whole course library", async ({ page }) => {
  const nav = page.getByRole("navigation", { name: "Backend Track (Immediately-Effective) course list" });
  await expect(nav.getByRole("link", { name: "View full path" })).toBeVisible();
  await expect(nav.getByRole("link", { name: "Browse all courses" })).toBeVisible();
});

// path-order-nav.feature, scenario 3 — phone drawer.
Given("a reader opens a course in path context on a phone-width viewport", async ({ page }) => {
  await page.setViewportSize(PHONE_VIEWPORT);
  await page.goto("/en/learn/courses/backend-essentials?path=careers/immediately-effective/backend-track");
  await page.waitForLoadState("networkidle");
});

When('they activate the path readout\'s "open path course list" control', async ({ page }) => {
  await page.getByRole("button", { name: /Open path course list/ }).click();
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/path-order-nav.feature:The path rail collapses into the existing navigation drawer on a phone
Then("the existing left navigation drawer opens showing that path's ordered courses", async ({ page }) => {
  const drawer = page.locator("#mobile-nav-drawer");
  await expect(drawer).toBeVisible();
  await expect(
    drawer.getByRole("navigation", { name: "Backend Track (Immediately-Effective) course list" }),
  ).toBeVisible();
});

Then("focus moves into the drawer and returns to the control when the drawer is dismissed", async ({ page }) => {
  const drawer = page.locator("#mobile-nav-drawer");
  const isFocusInsideDrawer = await drawer.evaluate((el) => el.contains(document.activeElement));
  expect(isFocusInsideDrawer).toBe(true);

  await page.keyboard.press("Escape");
  await expect(drawer).toBeHidden();

  const trigger = page.getByRole("button", { name: /Open path course list/ });
  await expect(trigger).toBeFocused();
});

// paths-hub-category-grouping.feature.
Given("a fixture manifest set covers both a careers-shaped and a skills-shaped fixture", async () => {
  // No-op — the fixture set has both careers and skills manifests.
});

When("a reader opens the paths hub at \\/en\\/learn\\/paths", async ({ page }) => {
  await page.goto("/en/learn/paths");
  await page.waitForLoadState("networkidle");
});

// @covers specs/apps/ayokoding/www/behaviors/frontend/course-paths/paths-hub-category-grouping.feature:The paths hub groups paths by category, not a flat grid
Then("the hub renders a Careers section grouped by arc and a separate Skills section", async ({ page }) => {
  const careersHeading = page.getByRole("heading", { level: 2, name: "Careers" });
  const skillsHeading = page.getByRole("heading", { level: 2, name: "Skills" });
  await expect(careersHeading).toBeVisible();
  await expect(skillsHeading).toBeVisible();
  // `exact: true` disambiguates the arc-group's own `<h3>` (its full accessible name is exactly
  // the arc's humanized/authored title — UWT-001 fix, phase-5 rule-15 retest — never the raw arc
  // slug) from a `PathCard`'s `<h3 data-slot="card-title">` whose title text merely contains the
  // arc name as a substring (e.g. "Backend Track (Interview-Ready)").
  await expect(page.getByRole("heading", { level: 3, name: "Interview-Ready", exact: true })).toBeVisible();
  await expect(page.getByRole("heading", { level: 3, name: "Immediately-Effective", exact: true })).toBeVisible();
});

Then("no path card from either category is rendered outside its category's section", async ({ page }) => {
  // `CategorySection` (path-card.tsx) sets `aria-labelledby="{id}-heading"` on its own `<section>`
  // — scope directly to that, rather than `section:has(h2)`, which would also match the hub's
  // outer wrapping `<section>` (itself a `has`-match ancestor of both category sections).
  const careersSection = page.locator("section[aria-labelledby='careers-heading']");
  const skillsSection = page.locator("section[aria-labelledby='skills-heading']");

  await expect(careersSection.getByText("E2E Fixture Alpha")).toHaveCount(0);
  await expect(careersSection.getByText("E2E Fixture Beta")).toHaveCount(0);
  await expect(skillsSection.getByText("Backend Track")).toHaveCount(0);
  await expect(skillsSection.getByText("Frontend Track")).toHaveCount(0);
  await expect(skillsSection.getByText("Generalist Track")).toHaveCount(0);
});
