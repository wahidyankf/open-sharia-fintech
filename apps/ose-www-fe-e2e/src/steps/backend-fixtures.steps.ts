import { readFile } from "node:fs/promises";
import path from "node:path";
import { expect, type APIRequestContext } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { buildTrpcUrl, extractTrpcData } from "./backend-helpers";

const { Given } = createBdd();

async function query(request: APIRequestContext, procedure: string, input: unknown): Promise<unknown> {
  const response = await request.get(buildTrpcUrl(procedure, input));
  expect(response.ok()).toBeTruthy();
  return extractTrpcData(await response.json());
}

Given("the API is running", async ({ request }) => {
  const result = (await query(request, "health.check", undefined)) as { status?: string };
  expect(result.status).toBe("ok");
});

Given("the content repository contains a page with slug {string}", async ({ request }, slug: string) => {
  const page = (await query(request, "content.getBySlug", { slug })) as { slug?: string } | null;
  expect(page).not.toBeNull();
  expect(page?.slug).toBe(slug);
});
Given("the content repository contains multiple update posts", async ({ request }) => {
  const updates = (await query(request, "content.listUpdates", undefined)) as unknown[];
  expect(updates.length).toBeGreaterThan(1);
});
Given("the content repository contains a draft page", async ({ request }) => {
  const fixture = await readFile(
    path.resolve(process.cwd(), "../ose-www/tests/e2e-fixtures/content/updates/2026-02-03-hidden-draft.md"),
    "utf8",
  );
  expect(fixture).toMatch(/^draft:\s*true$/mu);
  const updates = (await query(request, "content.listUpdates", undefined)) as Array<{ draft?: boolean }>;
  expect(updates.every((update) => update.draft !== true)).toBe(true);
});
Given("the OSE_WEB_SHOW_DRAFTS environment variable is not set", async ({ request }) => {
  const updates = (await query(request, "content.listUpdates", undefined)) as Array<{ draft?: boolean }>;
  expect(updates.every((update) => update.draft !== true)).toBe(true);
});
Given("the content repository contains no page with slug {string}", async ({ request }, slug: string) => {
  expect(await query(request, "content.getBySlug", { slug })).toBeNull();
});

Given("the search index contains pages about {string} and {string}", async ({ request }, t1: string, t2: string) => {
  const first = (await query(request, "search.query", { query: t1, limit: 10 })) as unknown[];
  const second = (await query(request, "search.query", { query: t2, limit: 10 })) as unknown[];
  expect(first.length).toBeGreaterThan(0);
  expect(second.length).toBeGreaterThan(0);
});
Given("the search index contains {int} pages matching {string}", async ({ request }, count: number, term: string) => {
  const results = (await query(request, "search.query", { query: term, limit: count + 5 })) as unknown[];
  expect(results.length).toBeGreaterThanOrEqual(count);
});

Given("the content repository contains update posts", async ({ request }) => {
  const response = await request.get("/feed.xml");
  expect(response.ok()).toBeTruthy();
  expect(await response.text()).toContain("<item>");
});
Given(
  "the content repository contains an update post with title {string} and date {string}",
  async ({ request }, title: string, date: string) => {
    const response = await request.get("/feed.xml");
    expect(response.ok()).toBeTruthy();
    const feed = await response.text();
    for (const word of title.split(/\s+/)) expect(feed.toLowerCase()).toContain(word.toLowerCase());
    expect(feed).toContain(new Date(`${date}T00:00:00Z`).toUTCString().slice(5, 16));
  },
);

Given("the content repository contains public pages", async ({ request }) => {
  const response = await request.get("/sitemap.xml");
  expect(response.ok()).toBeTruthy();
  const sitemap = await response.text();
  expect(sitemap).toContain("<loc>");
  expect(sitemap).toContain("/about");
});
