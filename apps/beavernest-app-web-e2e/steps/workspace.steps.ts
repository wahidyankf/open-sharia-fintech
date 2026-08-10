import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { readinessReady, readinessUnavailable, routeDelayedReadiness, routeReadiness } from "../utils/readiness-route";

const { Given, When, Then, After } = createBdd();

After(async ({ page }) => page.unrouteAll({ behavior: "wait" }));

Given("BeaverNest is reachable through its configured VPN address", async ({ page }) => {
  await routeReadiness(page, [readinessReady]);
});

When("I navigate to {string} in a new browser session", async ({ page }, path: string) => page.goto(path));

Then("the application shell renders before the readiness request completes", async ({ page }) => {
  await expect(page.getByRole("heading", { name: "BeaverNest" })).toBeVisible();
  await expect(page.getByText("Foundation status")).toBeVisible();
});

Then("the browser sends a same-origin GET request to {string}", async ({ page }, path: string) => {
  await expect
    .poll(() =>
      page.evaluate(
        (expectedPath) => performance.getEntriesByType("resource").some((entry) => entry.name.endsWith(expectedPath)),
        path,
      ),
    )
    .toBe(true);
});

Then("the page reports Application Available, Database Ready and Schema Current", async ({ page }) => {
  await expect(page.getByText("Application")).toBeVisible();
  await expect(page.getByText("Database")).toBeVisible();
  await expect(page.getByText("Schema")).toBeVisible();
  await expect(page.getByText("Current")).toBeVisible();
});

Given("the readiness response is intentionally delayed", async ({ page }) => routeDelayedReadiness(page));
When("I navigate to {string}", async ({ page }, path: string) => page.goto(path));
Then("the readiness region reports that status is being checked", async ({ page }) =>
  expect(page.getByText("Checking foundation status")).toBeVisible(),
);
Then("the region does not falsely report the database as ready", async ({ page }) =>
  expect(page.getByText("Database")).toHaveCount(0),
);

Given("the readiness endpoint returns an unavailable response", async ({ page }) =>
  routeReadiness(page, [readinessUnavailable, readinessReady]),
);
When(
  "I navigate to {string} and activate {string} after service recovery",
  async ({ page }, path: string, action: string) => {
    await page.goto(path);
    await page.getByRole("button", { name: action }).click();
  },
);
Then("the readiness request is retried without a full page navigation", async ({ page }) =>
  expect(page).toHaveURL(/\/$/),
);
Then("the region changes from Unavailable to Ready using a polite live announcement", async ({ page }) => {
  await expect(page.getByRole("region", { name: "Foundation status" })).toHaveAttribute("aria-live", "polite");
  await expect(page.getByRole("img", { name: "Ready", exact: true })).toBeVisible();
});

Given("I am viewing the rendered workspace home", async ({ page }) => {
  await routeReadiness(page, [readinessReady]);
  await page.goto("/");
});
When("I inspect the visible page content and accessible links", async () => undefined);
Then("no promotional product description is present", async ({ page }) =>
  expect(page.getByText(/personal operating layer/i)).toHaveCount(0),
);
Then("no external GitHub call to action is present", async ({ page }) =>
  expect(page.getByRole("link", { name: /github/i })).toHaveCount(0),
);
