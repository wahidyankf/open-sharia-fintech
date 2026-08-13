import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";

const { Given, When, Then } = createBdd();

Given("version two of the F# hosted Flutter bundle is available", async () => undefined);

When("I navigate normally to the workspace root", async ({ page }) => {
  await page.goto("/");
});

Then("the browser loads the coherent version two bundle without a service worker", async ({ page }) => {
  const bundle = await page.request.get("/main.dart.js");
  expect(bundle.ok()).toBe(true);
  expect(await bundle.text()).toContain("Build v2");
  await expect
    .poll(() => page.evaluate(async () => (await navigator.serviceWorker.getRegistration()) ?? null))
    .toBeNull();
});

Then("un-hashed Flutter entrypoints revalidate before reuse", async ({ page }) => {
  const bootstrap = await page.request.get("/flutter_bootstrap.js");
  const entrypoint = await page.request.get("/main.dart.js");

  expect(bootstrap.headers()["cache-control"]).toBe("no-cache");
  expect(entrypoint.headers()["cache-control"]).toBe("no-cache");
});
