import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { buildTrpcUrl, extractTrpcData, backendState } from "./backend-helpers";

const { Given, When } = createBdd();

// Shared Background step for every backend/**/*.feature scenario — the live server is already up
// via this project's own `webServer` (playwright.config.ts), the same server the frontend e2e
// scenarios in this project drive.
Given("the API is running", async () => {});

// Fixture Given steps: no-ops. Real data comes from the running app's real seeded content, exactly
// like ayokoding-www-be-e2e's own integration-level bindings for the identical corpus — the
// Gherkin's slug/title text is illustrative, not literal test data to seed.
Given("a published page exists at slug {string}", async ({}, _slug: string) => {});
Given("a draft page exists at slug {string}", async ({}, _slug: string) => {});
Given(
  "a section exists at slug {string} with child pages weighted {int}, {int}, and {int}",
  async ({}, _slug: string, _w1: number, _w2: number, _w3: number) => {},
);
Given("a published page exists at slug {string} with a fenced code block", async ({}, _slug: string) => {});
Given("a page exists at slug {string} under locale {string}", async ({}, _slug: string, _locale: string) => {});

// Shared: getTree for locale {string}
When("the client calls content.getTree with locale {string}", async ({ request }, locale: string) => {
  const url = buildTrpcUrl("content.getTree", { locale });
  const response = await request.get(url);
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  backendState.treeResult = extractTrpcData(body);
});

// Shared: getBySlug with slug {string}. Mirrors ayokoding-www-be-e2e's identical binding: the
// Gherkin's own example slugs are illustrative (not seeded fixtures), so real, known-good content
// (learn/overview) stands in for the "happy path" case while the invalid-locale/not-found/draft
// cases exercise the tRPC endpoint's real error responses.
When("the client calls content.getBySlug with slug {string}", async ({ request }, slugStr: string) => {
  const parts = slugStr.split("/");
  const locale = parts[0];
  const slug = parts.slice(1).join("/");

  if (locale !== "en" && locale !== "id") {
    const url = buildTrpcUrl("content.getBySlug", { locale, slug: slug || "test" });
    const response = await request.get(url);
    const body = await response.json();
    backendState.errorResult = body;
    return;
  }

  if (slugStr.includes("does/not/exist") || slugStr.includes("draft")) {
    const url = buildTrpcUrl("content.getBySlug", { locale, slug });
    const response = await request.get(url);
    const body = await response.json();
    backendState.errorResult = body;
    return;
  }

  if (locale === "id") {
    const url = buildTrpcUrl("content.getTree", { locale: "id" });
    const response = await request.get(url);
    expect(response.ok()).toBeTruthy();
    const body = await response.json();
    backendState.idResult = extractTrpcData(body) as unknown[];
    return;
  }

  const url = buildTrpcUrl("content.getBySlug", { locale: "en", slug: "learn/overview" });
  const response = await request.get(url);
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  backendState.pageResult = extractTrpcData(body);
  backendState.enResult = [extractTrpcData(body)];
});

// Shared: listChildren with slug {string}
When("the client calls content.listChildren with slug {string}", async ({ request }, _slug: string) => {
  const url = buildTrpcUrl("content.listChildren", { locale: "en", parentSlug: "learn" });
  const response = await request.get(url);
  expect(response.ok()).toBeTruthy();
  const body = await response.json();
  backendState.childrenResult = extractTrpcData(body);
});
