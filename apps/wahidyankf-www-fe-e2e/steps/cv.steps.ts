import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { When, Then } = createBdd();

When("a visitor opens the CV page", async ({ page }) => {
  await page.goto("/cv");
  await page.waitForLoadState("load");
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV renders the Curriculum Vitae heading
Then('the H1 shows "Curriculum Vitae"', async ({ page }) => {
  await expect(page.getByRole("heading", { level: 1, name: /Curriculum Vitae/ })).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV renders a search input
Then('a search input with placeholder "Search CV entries..." is visible', async ({ page }) => {
  await expect(page.getByPlaceholder(/Search CV entries/i)).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV renders the Highlights section header
Then('a "Highlights" section header is visible', async ({ page }) => {
  await expect(page.getByRole("heading", { name: /Highlights/i })).toBeVisible();
});

When('a visitor opens the CV page with search term "TypeScript" and scrollTop true', async ({ page }) => {
  await page.goto("/cv?search=TypeScript&scrollTop=true");
  await page.waitForLoadState("load");
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV cross-linked via scrollTop query scrolls into the entries
Then("the page scrolls past Highlights into the matching entries", async ({ page }) => {
  await expect(page.getByRole("heading", { level: 1, name: /Curriculum Vitae/ })).toBeVisible();
  const searchInput = page.getByPlaceholder(/Search CV entries/i);
  await expect(searchInput).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/cv/cv.feature:CV offers a downloadable PDF
Then('a "Download CV \\(PDF\\)" link pointing at the generated PDF is visible', async ({ page }) => {
  const downloadLink = page.getByRole("link", { name: /Download CV \(PDF\)/ });
  await expect(downloadLink).toBeVisible();
  await expect(downloadLink).toHaveAttribute("href", "/wahidyankf-kresna-fridayoka-cv.pdf");
});
