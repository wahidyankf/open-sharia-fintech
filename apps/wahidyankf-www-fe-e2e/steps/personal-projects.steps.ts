import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { When, Then } = createBdd();

When("a visitor opens the personal projects page", async ({ page }) => {
  await page.goto("/personal-projects");
  await page.waitForLoadState("load");
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Personal projects page renders the heading
Then('the H1 shows "Independent Projects"', async ({ page }) => {
  await expect(page.getByRole("heading", { level: 1, name: /Independent Projects/ })).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Personal projects page renders a search input
Then('a search input with placeholder "Search projects..." is visible', async ({ page }) => {
  await expect(page.getByPlaceholder(/Search projects/i)).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Personal projects page lists at least one project card
Then("at least one project card is visible", async ({ page }) => {
  const cardCount = await page.locator("h2, h3").count();
  expect(cardCount).toBeGreaterThan(0);
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Each project card exposes external links where applicable
Then(
  "every project card exposes a Repository, Website, or YouTube link where the project has that resource",
  async ({ page }) => {
    const externalLinks = await page.getByRole("link", { name: /Repository|Website|YouTube/i }).count();
    expect(externalLinks).toBeGreaterThan(0);
  },
);

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Each project card shows how long the project has been running
Then("every project card shows a duration next to its start date", async ({ page }) => {
  const cards = page.locator('[id^="project-"]');
  const count = await cards.count();
  expect(count).toBeGreaterThan(0);
  for (let i = 0; i < count; i += 1) {
    await expect(cards.nth(i).getByText(/\(\d+\s+(year|month)/i).first()).toBeVisible();
  }
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Each project card exposes clickable skill tags
Then("every project card exposes at least one clickable skill tag", async ({ page }) => {
  const cards = page.locator('[id^="project-"]');
  const count = await cards.count();
  expect(count).toBeGreaterThan(0);
  for (let i = 0; i < count; i += 1) {
    const buttonCount = await cards.nth(i).getByRole("button").count();
    expect(buttonCount).toBeGreaterThan(0);
  }
});

When('a visitor opens the personal projects page and clicks the "TypeScript" skill tag', async ({ page }) => {
  await page.goto("/personal-projects");
  await page.waitForLoadState("load");
  await page.getByRole("button", { name: "TypeScript" }).first().click();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/personal-projects/personal-projects.feature:Clicking a skill tag filters the project list
Then("the URL becomes \\/personal-projects?search=TypeScript", async ({ page }) => {
  await expect(page).toHaveURL(/\/personal-projects\?search=TypeScript/);
});
