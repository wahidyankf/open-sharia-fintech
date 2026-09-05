import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { buildTrpcUrl, extractTrpcData, backendState } from "./backend-helpers";

const { Given, When, Then } = createBdd();

async function querySearch(
  request: { get(url: string): Promise<{ ok(): boolean; json(): Promise<unknown> }> },
  locale: "en" | "id",
  query: string,
) {
  const response = await request.get(buildTrpcUrl("search.query", { locale, query, limit: 20 }));
  expect(response.ok()).toBe(true);
  return extractTrpcData(await response.json()) as Array<{
    title: string;
    slug: string;
    excerpt: string;
    locale: string;
  }>;
}

Given('published pages indexed under locale "en" include a page titled "Beginner Examples"', async ({ request }) => {
  expect(await querySearch(request, "en", "goroutines")).toEqual(
    expect.arrayContaining([expect.objectContaining({ title: "Beginner Examples", locale: "en" })]),
  );
});
Given('published pages indexed under locale "en" include content about "programming"', async ({ request }) => {
  expect((await querySearch(request, "en", "programming")).length).toBeGreaterThan(0);
});
Given('a page exists in locale "en" with title "Spring Security Basics"', async ({ request }) => {
  expect(await querySearch(request, "en", "Spring Security Basics")).toEqual(
    expect.arrayContaining([expect.objectContaining({ title: "Spring Security Basics", locale: "en" })]),
  );
});
Given('no equivalent page exists in locale "id"', async ({ request }) => {
  expect(await querySearch(request, "id", "Spring Security Basics")).toEqual([]);
});

When('the client calls search.query with locale "en" and query "programming"', async ({ request }) => {
  backendState.searchResults = await querySearch(request, "en", "programming");
});

Then("the response should contain at least one result", async () => {
  const results = backendState.searchResults as unknown[];
  expect(results.length).toBeGreaterThan(0);
});

Then('each result should include a "title" field', async () => {
  const results = backendState.searchResults as unknown[];
  expect(results.length).toBeGreaterThan(0);
  for (const result of results) expect(result).toHaveProperty("title");
});

Then('each result should include a "slug" field', async () => {
  const results = backendState.searchResults as unknown[];
  expect(results.length).toBeGreaterThan(0);
  for (const result of results) expect(result).toHaveProperty("slug");
});

Then('each result should include an "excerpt" field', async () => {
  const results = backendState.searchResults as unknown[];
  expect(results.length).toBeGreaterThan(0);
  for (const result of results) expect(result).toHaveProperty("excerpt");
});

When('the client calls search.query with locale "en" and query "goroutines"', async ({ request }) => {
  backendState.searchResults = await querySearch(request, "en", "goroutines");
});

Then('each result should include a "locale" field matching "en"', async () => {
  const results = backendState.searchResults as { locale: string }[];
  for (const result of results) {
    expect(result).toHaveProperty("locale");
    expect(result.locale).toBe("en");
  }
});

When('the client calls search.query with locale "id" and query "Spring Security Basics"', async ({ request }) => {
  backendState.searchResults = await querySearch(request, "id", "Spring Security Basics");
});

Then("the response should contain no results", async () => {
  const results = backendState.searchResults as unknown[];
  expect(results.length).toBe(0);
});

When('the client calls search.query with locale "en" and an empty query', async ({ request }) => {
  const url = buildTrpcUrl("search.query", { locale: "en", query: "", limit: 10 });
  const response = await request.get(url);
  const body = await response.json();
  backendState.errorResult = body;
});

Then("the response should indicate an invalid input error", async () => {
  const arr = backendState.errorResult as unknown[];
  expect(arr[0]).toHaveProperty("error");
});
