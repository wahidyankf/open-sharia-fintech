import { createBdd } from "playwright-bdd";
import { expect, type Page } from "@playwright/test";
import { appPath } from "./_app-shell";
import { journalEntryCount } from "./_journal-db";

const { Given, When, Then } = createBdd();
let expectedSavedEntry: { name: string; payloadText: string } | null = null;

async function openAddEntrySheet(page: Page) {
  await page.goto(appPath("home"));
  await page.waitForLoadState("domcontentloaded");
  const fab = page.getByRole("button", { name: "Log entry" });
  await expect(fab).toBeVisible();
  await fab.click();
  await expect(page.getByText("Log an entry")).toBeVisible();
}

async function openLogger(page: Page, kind: "Reading" | "Learning" | "Meal" | "Focus") {
  await openAddEntrySheet(page);
  const button = page.getByRole("button", { name: kind }).nth(1);
  await expect(button).toBeVisible();
  await button.click();
}

Given("the user has opened the Add Entry sheet", async ({ page }) => {
  await openAddEntrySheet(page);
});

When("the user taps the FAB", async ({ page }) => {
  const fab = page.getByRole("button", { name: "Log entry" });
  await expect(fab).toBeVisible();
  await fab.click();
});

Then("the Add Entry sheet is open with all entry kinds", async ({ page }) => {
  await expect(page.getByText("Log an entry")).toBeVisible();
  for (const label of ["Workout", "Reading", "Learning", "Meal", "Focus"]) {
    await expect(page.getByRole("button", { name: label }).nth(1)).toBeVisible();
  }
  await expect(page.getByRole("button", { name: /New custom type/ })).toBeVisible();
});

When("the user selects the Reading entry kind", async ({ page }) => {
  await page.getByRole("button", { name: "Reading" }).nth(1).click();
});

Then("the reading logger is open", async ({ page }) => {
  await expect(page.getByText("Log reading")).toBeVisible();
});

Given("the user has opened the reading logger", async ({ page }) => {
  await openLogger(page, "Reading");
  expectedSavedEntry = { name: "reading", payloadText: "Atomic Habits" };
});

When("the user enters title {string}", async ({ page }, title: string) => {
  await page.getByPlaceholder("e.g. Thinking Fast and Slow").fill(title);
});

When("the user saves the entry", async ({ page }) => {
  const save = page.getByRole("button", { name: "Save" });
  await expect(save).toBeEnabled();
  await save.click();
});

Then("the entry is saved and the logger closes", async ({ page }) => {
  expect(expectedSavedEntry).not.toBeNull();
  await expect(page.getByRole("button", { name: "Save" })).not.toBeVisible();
  await expect
    .poll(() => journalEntryCount(page, expectedSavedEntry!.name, expectedSavedEntry!.payloadText))
    .toBeGreaterThan(0);
});

When("the user has not entered a title", async ({ page }) => {
  await page.getByPlaceholder("e.g. Thinking Fast and Slow").clear();
});

Then("the save button is disabled", async ({ page }) => {
  await expect(page.getByRole("button", { name: "Save" })).toBeDisabled();
});

When("the user selects the Learning entry kind", async ({ page }) => {
  await page.getByRole("button", { name: "Learning" }).nth(1).click();
});

Then("the learning logger is open", async ({ page }) => {
  await expect(page.getByText("Log learning")).toBeVisible();
});

Given("the user has opened the learning logger", async ({ page }) => {
  await openLogger(page, "Learning");
  expectedSavedEntry = { name: "learning", payloadText: "TypeScript generics" };
});

When("the user enters subject {string}", async ({ page }, subject: string) => {
  await page.getByPlaceholder(/React hooks/).fill(subject);
});

When("the user selects the Meal entry kind", async ({ page }) => {
  await page.getByRole("button", { name: "Meal" }).nth(1).click();
});

Then("the meal logger is open", async ({ page }) => {
  await expect(page.getByText("Log meal")).toBeVisible();
});

Given("the user has opened the meal logger", async ({ page }) => {
  await openLogger(page, "Meal");
  expectedSavedEntry = { name: "meal", payloadText: "Oatmeal with berries" };
});

When("the user enters meal name {string}", async ({ page }, mealName: string) => {
  await page.getByPlaceholder(/Oatmeal with berries/).fill(mealName);
});

When("the user selects the Focus entry kind", async ({ page }) => {
  await page.getByRole("button", { name: "Focus" }).nth(1).click();
});

Then("the focus logger is open", async ({ page }) => {
  await expect(page.getByText("Log focus session")).toBeVisible();
});

Given("the user has opened the focus logger", async ({ page }) => {
  await openLogger(page, "Focus");
  expectedSavedEntry = { name: "focus", payloadText: "25" };
});

When("the user selects the 25min preset", async ({ page }) => {
  await page.getByRole("button", { name: "25" }).click();
});

When("the user has not entered task or duration", async ({ page }) => {
  await page.getByPlaceholder(/Feature design/).clear();
  await page.getByPlaceholder("or enter custom minutes").clear();
});

When("the user selects the custom entry kind", async ({ page }) => {
  await page.getByRole("button", { name: /New custom type/ }).click();
});

Then("the custom entry logger is open", async ({ page }) => {
  await expect(page.getByText("New custom entry")).toBeVisible();
});

Given("the user has opened the custom entry logger", async ({ page }) => {
  await openAddEntrySheet(page);
  await page.getByRole("button", { name: /New custom type/ }).click();
  expectedSavedEntry = { name: "custom-evening-walk", payloadText: "Evening walk" };
});

When("the user enters custom entry name {string}", async ({ page }, name: string) => {
  await page.getByPlaceholder(/Evening walk/).fill(name);
});

When("the user saves the custom entry", async ({ page }) => {
  const save = page.getByRole("button", { name: "Save", exact: true });
  await expect(save).toBeEnabled();
  await save.click();
});

Then("the custom entry is saved and the logger closes", async ({ page }) => {
  expect(expectedSavedEntry).not.toBeNull();
  await expect(page.getByText("New custom entry")).not.toBeVisible();
  await expect
    .poll(() => journalEntryCount(page, expectedSavedEntry!.name, expectedSavedEntry!.payloadText))
    .toBeGreaterThan(0);
});
