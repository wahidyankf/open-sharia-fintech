import { expect, type APIRequestContext } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { buildTrpcUrl, extractTrpcData, state } from "./helpers";

type SearchResult = { title: string; slug: string; excerpt: string; locale: string };

const { Given, When, Then } = createBdd();

async function search(request: APIRequestContext, locale: string, query: string): Promise<SearchResult[]> {
  const response = await request.get(buildTrpcUrl("search.query", { locale, query, limit: 10 }));
  expect(response.ok()).toBeTruthy();
  return extractTrpcData(await response.json()) as SearchResult[];
}

Given('published pages indexed under locale "en" include a page titled "Beginner Examples"', async ({ request }) => {
  expect(await search(request, "en", "goroutines")).toEqual(
    expect.arrayContaining([expect.objectContaining({ title: "Beginner Examples", locale: "en" })]),
  );
});

Given('published pages indexed under locale "en" include content about "programming"', async ({ request }) => {
  expect((await search(request, "en", "programming")).length).toBeGreaterThan(0);
});

Given('a page exists in locale "en" with title "Spring Security Basics"', async ({ request }) => {
  expect(await search(request, "en", "Spring Security Basics")).toEqual(
    expect.arrayContaining([expect.objectContaining({ title: "Spring Security Basics", locale: "en" })]),
  );
});

Given('no equivalent page exists in locale "id"', async ({ request }) => {
  expect(await search(request, "id", "Spring Security Basics")).toEqual([]);
});

When('the client calls search.query with locale "en" and query "goroutines"', async ({ request }) => {
  state.searchResults = await search(request, "en", "goroutines");
});

Then("the response should contain at least one result", async () => {
  expect((state.searchResults as SearchResult[]).length).toBeGreaterThan(0);
});

Then('each result should include a "title" field', async () => {
  expect((state.searchResults as SearchResult[]).every(({ title }) => title.length > 0)).toBe(true);
});

Then('each result should include a "slug" field', async () => {
  expect((state.searchResults as SearchResult[]).every(({ slug }) => slug.length > 0)).toBe(true);
});

Then('each result should include an "excerpt" field', async () => {
  expect((state.searchResults as SearchResult[]).every(({ excerpt }) => excerpt.length > 0)).toBe(true);
});

When('the client calls search.query with locale "en" and query "programming"', async ({ request }) => {
  state.searchResults = await search(request, "en", "programming");
});

Then('each result should include a "locale" field matching "en"', async () => {
  const results = state.searchResults as SearchResult[];
  expect(results.length).toBeGreaterThan(0);
  expect(results.every(({ locale }) => locale === "en")).toBe(true);
});

When('the client calls search.query with locale "id" and query "Spring Security Basics"', async ({ request }) => {
  state.searchResults = await search(request, "id", "Spring Security Basics");
});

Then("the response should contain no results", async () => {
  expect(state.searchResults).toEqual([]);
});

When('the client calls search.query with locale "en" and an empty query', async ({ request }) => {
  const response = await request.get(buildTrpcUrl("search.query", { locale: "en", query: "", limit: 10 }));
  state.errorResult = await response.json();
  expect(response.ok()).toBe(false);
});

Then("the response should indicate an invalid input error", async () => {
  const errors = state.errorResult as { error?: { json?: { data?: { code?: string } } } }[];
  expect(errors[0]?.error?.json?.data?.code).toBe("BAD_REQUEST");
});
