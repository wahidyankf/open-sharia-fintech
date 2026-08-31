import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";

const { Given, When, Then } = createBdd();

Given("the app is running", async () => {});

When("a visitor opens the home page", async ({ page }) => {
  await page.goto("/");
  await page.waitForLoadState("load");
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the welcome heading
Then('the H1 shows "Welcome to My Portfolio"', async ({ page }) => {
  await expect(page.getByRole("heading", { level: 1, name: /Welcome to My Portfolio/ })).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the About Me card
Then("an About Me card is visible", async ({ page }) => {
  await expect(page.getByRole("heading", { name: /About Me/i })).toBeVisible();
});

Then("a Skills & Expertise card is visible", async ({ page }) => {
  await expect(page.getByRole("heading", { name: /Skills & Expertise/i })).toBeVisible();
});

Then('the card has a "Top Skills Used in The Last 5 Years" subsection', async ({ page }) => {
  await expect(page.getByText(/Top Skills Used in The Last 5 Years/i)).toBeVisible();
});

Then('the card has a "Top Programming Languages Used in The Last 5 Years" subsection', async ({ page }) => {
  await expect(page.getByText(/Top Programming Languages Used in The Last 5 Years/i)).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the Skills & Expertise card with three subsections
Then('the card has a "Top Frameworks & Libraries Used in The Last 5 Years" subsection', async ({ page }) => {
  await expect(page.getByText(/Top Frameworks & Libraries Used in The Last 5 Years/i)).toBeVisible();
});

Then("a Quick Links card is visible", async ({ page }) => {
  await expect(page.getByRole("heading", { name: /Quick Links/i })).toBeVisible();
});

Then('the card contains a "View My CV" link to \\/cv', async ({ page }) => {
  const link = page.getByRole("link", { name: /View My CV/i });
  await expect(link).toBeVisible();
  await expect(link).toHaveAttribute("href", "/cv");
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the Quick Links card with two internal links
Then('the card contains a "Browse My Independent Projects" link to \\/personal-projects', async ({ page }) => {
  const link = page.getByRole("link", { name: /Browse My Independent Projects/i });
  await expect(link).toBeVisible();
  await expect(link).toHaveAttribute("href", "/personal-projects");
});

Then("a Connect With Me card is visible", async ({ page }) => {
  await expect(page.getByRole("heading", { name: /Connect With Me/i })).toBeVisible();
});

// @covers specs/apps/wahidyankf/behavior/wahidyankf-www/gherkin/home/home.feature:Home renders the Connect With Me card with five external links
Then("the card has Github, GithubOrg, Linkedin, Website, and Email links", async ({ page }) => {
  for (const name of [/Github/i, /GithubOrg/i, /Linkedin/i, /Website/i, /Email/i]) {
    await expect(page.getByRole("link", { name }).first()).toBeVisible();
  }
});
