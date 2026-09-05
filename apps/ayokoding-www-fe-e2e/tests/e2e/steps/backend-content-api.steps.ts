import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { backendState } from "./backend-helpers";

const { Then } = createBdd();

// Note: All Given/When steps with {string} params are in backend-common.steps.ts

Then('the response should contain a non-null "html" field', async () => {
  const pageResult = backendState.pageResult as Record<string, unknown>;
  expect(pageResult.html).toBeTruthy();
});

Then("the response should contain the page metadata for the requested slug", async () => {
  expect(backendState.pageResult).toMatchObject({
    title: "Beginner Examples",
    slug: "learn/courses/just-enough-go/learning/beginner",
    locale: "en",
    weight: 10,
    draft: false,
    isSection: false,
  });
});

Then('the response should contain a non-null "headings" field', async () => {
  const pageResult = backendState.pageResult as Record<string, unknown>;
  expect(Array.isArray(pageResult.headings)).toBe(true);
});

Then('the response should contain a "prev" navigation link', async () => {
  expect(backendState.pageResult).toMatchObject({
    prev: { title: "Overview", slug: "learn/courses/just-enough-go/learning/overview" },
  });
});

Then('the response should contain a "next" navigation link', async () => {
  expect(backendState.pageResult).toMatchObject({
    next: {
      title: "Intermediate Examples",
      slug: "learn/courses/just-enough-go/learning/intermediate",
    },
  });
});

Then("the response should indicate the page was not found", async () => {
  const errors = backendState.errorResult as { error?: { json?: { data?: { code?: string } } } }[];
  expect(errors[0]?.error?.json?.data?.code).toBe("NOT_FOUND");
});

Then("the response should reject the invalid locale as a bad request", async () => {
  const errors = backendState.errorResult as { error?: { json?: { data?: { code?: string } } } }[];
  expect(errors[0]?.error?.json?.data?.code).toBe("BAD_REQUEST");
});

Then("the response should contain 5 child pages", async () => {
  const children = backendState.childrenResult as { weight: number }[];
  expect(children).toHaveLength(5);
});

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

Then("every node should include a slug and title", async () => {
  const tree = backendState.treeResult as Array<{ slug: string; title: string; children: unknown[] }>;
  const visit = (nodes: typeof tree): void => {
    for (const node of nodes) {
      expect(node.slug).toEqual(expect.any(String));
      expect(node.title).toEqual(expect.any(String));
      expect(Array.isArray(node.children)).toBe(true);
      visit(node.children as typeof tree);
    }
  };
  visit(tree);
});

Then('the response "html" field should contain a rendered code element', async () => {
  const pageResult = backendState.pageResult as Record<string, unknown>;
  expect(pageResult.html).toEqual(expect.stringContaining("<code"));
});
