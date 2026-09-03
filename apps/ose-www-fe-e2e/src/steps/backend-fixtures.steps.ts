import { createBdd } from "playwright-bdd";

const { Given } = createBdd();

// Shared Background step for every backend feature — the live server is already up via this
// project's `webServer` (playwright.config.ts).
Given("the API is running", async () => {});

// Content retrieval fixtures (no-op — real data comes from the running app's seeded content).
Given("the content repository contains a page with slug {string}", async ({}, _slug: string) => {});
Given("the content repository contains multiple update posts", async () => {});
Given("the content repository contains a draft page", async () => {});
Given("the OSE_WEB_SHOW_DRAFTS environment variable is not set", async () => {});
Given("the content repository contains no page with slug {string}", async ({}, _slug: string) => {});

// Search fixtures (no-op — the running app's real search index already has this content).
Given("the search index contains pages about {string} and {string}", async ({}, _t1: string, _t2: string) => {});
Given("the search index contains {int} pages matching {string}", async ({}, _count: number, _term: string) => {});

// RSS feed fixtures (no-op).
Given("the content repository contains update posts", async () => {});
Given(
  "the content repository contains an update post with title {string} and date {string}",
  async ({}, _title: string, _date: string) => {},
);

// SEO fixtures (no-op).
Given("the content repository contains public pages", async () => {});
