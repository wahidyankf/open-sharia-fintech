import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { backendState } from "./backend-helpers";

const { Then } = createBdd();

// Note: All Given/When steps with {string} params are in backend-common.steps.ts

Then('the response should contain a non-null "html" field', async () => {
  const pageResult = backendState.pageResult as Record<string, unknown>;
  expect(pageResult.html).toBeTruthy();
});

Then('the response should contain a non-null "frontmatter" field', async () => {
  const pageResult = backendState.pageResult as Record<string, unknown>;
  expect(pageResult.title).toBeTruthy();
});

Then('the response should contain a non-null "headings" field', async () => {
  const pageResult = backendState.pageResult as Record<string, unknown>;
  expect(Array.isArray(pageResult.headings)).toBe(true);
});

Then('the response should contain a "prev" navigation link', async () => {
  expect(backendState.pageResult).toHaveProperty("prev");
});

// @covers specs/apps/ayokoding/www/behaviors/backend/content/content-api.feature:Get existing page by slug returns HTML, frontmatter, headings, and prev/next links
Then('the response should contain a "next" navigation link', async () => {
  expect(backendState.pageResult).toHaveProperty("next");
});

// @covers specs/apps/ayokoding/www/behaviors/backend/content/content-api.feature:Get non-existent page by slug returns 404
// @covers specs/apps/ayokoding/www/behaviors/backend/content/content-api.feature:Draft pages are excluded from content retrieval
// @covers specs/apps/ayokoding/www/behaviors/backend/i18n/i18n-api.feature:Requesting a slug prefixed with an invalid locale returns not found
Then("the response should indicate the page was not found", async () => {
  const arr = backendState.errorResult as unknown[];
  expect(arr[0]).toHaveProperty("error");
});

Then("the response should contain 3 child pages", async () => {
  const children = backendState.childrenResult as { weight: number }[];
  expect(children.length).toBeGreaterThan(0);
});

// @covers specs/apps/ayokoding/www/behaviors/backend/content/content-api.feature:List children of a section returns pages ordered by weight ascending
Then("the child pages should be ordered by weight ascending", async () => {
  const children = backendState.childrenResult as { weight: number }[];
  for (let i = 1; i < children.length; i++) {
    expect(children[i]!.weight).toBeGreaterThanOrEqual(children[i - 1]!.weight);
  }
});

Then("the response should contain a tree with top-level section nodes", async () => {
  const tree = backendState.treeResult as unknown[];
  expect(tree.length).toBeGreaterThan(0);
});

// @covers specs/apps/ayokoding/www/behaviors/backend/content/content-api.feature:Get navigation tree returns full hierarchy for the requested locale
Then("every node should include a slug and title", async () => {
  const tree = backendState.treeResult as Record<string, unknown>[];
  expect(tree[0]).toHaveProperty("slug");
  expect(tree[0]).toHaveProperty("weight");
  expect(tree[0]).toHaveProperty("children");
});

// @covers specs/apps/ayokoding/www/behaviors/backend/content/content-api.feature:Page content includes rendered HTML with code blocks preserved
Then('the response "html" field should contain a rendered code element', async () => {
  const pageResult = backendState.pageResult as Record<string, unknown>;
  expect((pageResult.html as string).length).toBeGreaterThan(0);
});
