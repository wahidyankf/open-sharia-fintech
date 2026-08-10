import { expect, test } from "@playwright/test";
import { readinessReady, routeReadiness } from "../utils/readiness-route";

test.use({ colorScheme: "light" });

const viewports = [
  { name: "mobile-320", width: 320, height: 568 },
  { name: "mobile-375", width: 375, height: 812 },
  { name: "tablet", width: 768, height: 1024 },
  { name: "desktop", width: 1280, height: 800 },
] as const;

async function expectFoundationStatus(page: Parameters<typeof routeReadiness>[0]) {
  await expect(page.getByRole("heading", { name: "BeaverNest" })).toBeVisible();
  await expect(page.getByText("Foundation status")).toBeVisible();
  await expect(page.getByText("Current")).toBeVisible();
  await expect(page.getByRole("button", { name: "Refresh status" })).toBeVisible();
  expect(await page.locator("body").evaluate((body) => body.scrollWidth <= window.innerWidth)).toBe(true);
}

for (const viewport of viewports) {
  test(`foundation status fits ${viewport.name}`, async ({ page }) => {
    await page.setViewportSize(viewport);
    await routeReadiness(page, [readinessReady]);
    await page.goto("/");

    await expectFoundationStatus(page);
  });
}
