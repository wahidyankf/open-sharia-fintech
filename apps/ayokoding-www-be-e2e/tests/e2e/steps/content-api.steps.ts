import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { state } from "./helpers";

const { Then } = createBdd();

Then('the response should contain a non-null "html" field', async () => {
  expect((state.pageResult as { html: string }).html).toBeTruthy();
});

Then("the response should contain the page metadata for the requested slug", async () => {
  expect(state.pageResult).toMatchObject({
    title: "Beginner Examples",
    slug: "learn/courses/just-enough-go/learning/beginner",
    locale: "en",
    weight: 10,
    draft: false,
    isSection: false,
  });
});

Then('the response should contain a non-null "headings" field', async () => {
  expect((state.pageResult as { headings: unknown[] }).headings).toBeInstanceOf(Array);
});

Then('the response should contain a "prev" navigation link', async () => {
  expect(state.pageResult).toMatchObject({
    prev: { title: "Overview", slug: "learn/courses/just-enough-go/learning/overview" },
  });
});

Then('the response should contain a "next" navigation link', async () => {
  expect(state.pageResult).toMatchObject({
    next: {
      title: "Intermediate Examples",
      slug: "learn/courses/just-enough-go/learning/intermediate",
    },
  });
});

Then("the response should indicate the page was not found", async () => {
  const errors = state.errorResult as { error?: { json?: { data?: { code?: string } } } }[];
  expect(errors[0]?.error?.json?.data?.code).toBe("NOT_FOUND");
});

Then("the response should reject the invalid locale as a bad request", async () => {
  const errors = state.errorResult as { error?: { json?: { data?: { code?: string } } } }[];
  expect(errors[0]?.error?.json?.data?.code).toBe("BAD_REQUEST");
});

Then("the response should contain 5 child pages", async () => {
  expect(state.childrenResult).toHaveLength(5);
});

Then("the child pages should be ordered by weight ascending", async () => {
  const weights = (state.childrenResult as { weight: number }[]).map(({ weight }) => weight);
  expect(weights).toEqual([...weights].sort((a, b) => a - b));
});

Then("the response should contain a tree with top-level section nodes", async () => {
  const tree = state.treeResult as { slug: string; children: unknown[] }[];
  expect(tree.find(({ slug }) => slug === "")?.children.length).toBeGreaterThan(0);
});

Then("every node should include a slug and title", async () => {
  type Node = { slug: string; title: string; children: Node[] };
  const visit = (nodes: Node[]) => {
    for (const node of nodes) {
      expect(node).toMatchObject({ slug: expect.any(String), title: expect.any(String) });
      visit(node.children);
    }
  };
  visit(state.treeResult as Node[]);
});

Then('the response "html" field should contain a rendered code element', async () => {
  expect((state.pageResult as { html: string }).html).toContain("<code");
});
