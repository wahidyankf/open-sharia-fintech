import type { Page } from "@playwright/test";

export const readinessReady = {
  status: "ready",
  components: { database: "ready", schema: "current" },
} as const;

export const readinessUnavailable = {
  status: "not-ready",
  components: { database: "unavailable", schema: "unknown" },
} as const;

export async function routeReadiness(
  page: Page,
  responses: Array<typeof readinessReady | typeof readinessUnavailable>,
) {
  let index = 0;
  await page.route("**/api/v1/readiness", async (route) => {
    const response = responses[Math.min(index, responses.length - 1)] ?? readinessUnavailable;
    index += 1;
    await route.fulfill({
      status: response.status === "ready" ? 200 : 503,
      contentType: "application/json",
      body: JSON.stringify(response),
    });
  });
}

export async function routeDelayedReadiness(page: Page) {
  await page.route("**/api/v1/readiness", async (route) => {
    await new Promise((resolve) => setTimeout(resolve, 250));
    await route.fulfill({ contentType: "application/json", body: JSON.stringify(readinessReady) });
  });
}
