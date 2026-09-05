import { expect, type APIRequestContext } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { buildTrpcUrl, extractTrpcData, state } from "./helpers";

type TreeNode = { slug: string; title: string; weight: number; children: TreeNode[] };

const { Given, Then } = createBdd();

function findNode(nodes: TreeNode[], slug: string): TreeNode | undefined {
  for (const node of nodes) {
    if (node.slug === slug) return node;
    const nested = findNode(node.children, slug);
    if (nested) return nested;
  }
  return undefined;
}

async function getTree(request: APIRequestContext): Promise<TreeNode[]> {
  const response = await request.get(buildTrpcUrl("content.getTree", { locale: "en" }));
  expect(response.ok()).toBeTruthy();
  return extractTrpcData(await response.json()) as TreeNode[];
}

Given('content exists in locale "en" with sections "about-ayokoding", "learn", and "rants"', async ({ request }) => {
  const localeRoot = (await getTree(request)).find(({ slug }) => slug === "");
  expect(localeRoot?.children.map(({ slug }) => slug)).toEqual(
    expect.arrayContaining(["about-ayokoding", "learn", "rants"]),
  );
});

Given(
  "a section {string} in locale {string} has child nodes with weights {int}, {int}, {int}, {int}, and {int}",
  async ({ request }, section: string, locale: string, ...declaredWeights: number[]) => {
    const response = await request.get(
      buildTrpcUrl("content.listChildren", {
        locale,
        parentSlug: section,
      }),
    );
    expect(response.ok()).toBeTruthy();
    const children = extractTrpcData(await response.json()) as TreeNode[];
    expect(children.map(({ weight }) => weight)).toEqual([...declaredWeights].sort((a, b) => a - b));
  },
);

Given(
  "a section {string} in locale {string} contains at least one child page",
  async ({ request }, section: string, locale: string) => {
    expect(locale).toBe("en");
    expect(findNode(await getTree(request), section)?.children.length).toBeGreaterThan(0);
  },
);

Then('the response tree should contain top-level nodes for "about-ayokoding", "learn", and "rants"', async () => {
  const localeRoot = (state.treeResult as TreeNode[]).find(({ slug }) => slug === "");
  expect(localeRoot?.children.map(({ slug }) => slug)).toEqual(
    expect.arrayContaining(["about-ayokoding", "learn", "rants"]),
  );
});

Then("each node should reflect its position in the directory hierarchy", async () => {
  expect(findNode(state.treeResult as TreeNode[], "learn/courses/just-enough-go/learning/beginner")?.slug).toBe(
    "learn/courses/just-enough-go/learning/beginner",
  );
});

Then(
  "the children of {string} should appear in order: weight {int}, weight {int}, weight {int}, weight {int}, weight {int}",
  async ({}, section: string, ...expectedWeights: number[]) => {
    const node = findNode(state.treeResult as TreeNode[], section);
    expect(node?.children.map(({ weight }) => weight)).toEqual(expectedWeights);
  },
);

Then("the {string} node should have a non-empty {string} array", async ({}, section: string, field: string) => {
  expect(field).toBe("children");
  const node = findNode(state.treeResult as TreeNode[], section);
  expect(node?.children.length).toBeGreaterThan(0);
});

Then('each child should include a "slug" and "title"', async () => {
  const node = findNode(state.treeResult as TreeNode[], "learn/courses/just-enough-go/learning");
  expect(node).toBeDefined();
  for (const child of node!.children) {
    expect(child).toMatchObject({ slug: expect.any(String), title: expect.any(String) });
  }
});
