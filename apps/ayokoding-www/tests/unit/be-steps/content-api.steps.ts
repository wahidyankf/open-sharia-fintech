import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import { testCaller } from "./helpers/test-caller";
import { draftFixture } from "./helpers/test-service";
import { TRPCError } from "@trpc/server";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviours/backend/content/content-api.feature"),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the API is running", async () => {
      await expect(testCaller.meta.health()).resolves.toEqual({ status: "ok" });
    });
  });

  Scenario(
    "Get existing page by slug returns HTML, page metadata, headings, and prev/next links",
    ({ Given, When, Then, And }) => {
      let result: Awaited<ReturnType<typeof testCaller.content.getBySlug>>;

      Given('a published page exists at slug "en/learn/courses/just-enough-go/learning/beginner"', async () => {
        await expect(
          testCaller.content.getBySlug({ locale: "en", slug: "learn/courses/just-enough-go/learning/beginner" }),
        ).resolves.toMatchObject({ title: "Beginner Examples", draft: false });
      });

      When(
        'the client calls content.getBySlug with slug "en/learn/courses/just-enough-go/learning/beginner"',
        async () => {
          result = await testCaller.content.getBySlug({
            locale: "en",
            slug: "learn/courses/just-enough-go/learning/beginner",
          });
        },
      );

      Then('the response should contain a non-null "html" field', () => {
        expect(result.html).toContain("<h2");
      });

      And("the response should contain the page metadata for the requested slug", () => {
        expect(result).toMatchObject({
          title: "Beginner Examples",
          slug: "learn/courses/just-enough-go/learning/beginner",
          locale: "en",
          weight: 10,
          draft: false,
          isSection: false,
        });
      });

      And('the response should contain a non-null "headings" field', () => {
        expect(result.headings.length).toBeGreaterThan(0);
      });

      And('the response should contain a "prev" navigation link', () => {
        expect(result.prev).toEqual({ title: "Overview", slug: "learn/courses/just-enough-go/learning/overview" });
      });

      And('the response should contain a "next" navigation link', () => {
        expect(result.next).toEqual({
          title: "Intermediate Examples",
          slug: "learn/courses/just-enough-go/learning/intermediate",
        });
      });
    },
  );

  Scenario("Get non-existent page by slug returns 404", ({ When, Then }) => {
    let error: TRPCError | null = null;

    When('the client calls content.getBySlug with slug "en/does/not/exist"', async () => {
      try {
        await testCaller.content.getBySlug({ locale: "en", slug: "does-not-exist" });
      } catch (e) {
        error = e as TRPCError;
      }
    });

    Then("the response should indicate the page was not found", () => {
      expect(error).toBeInstanceOf(TRPCError);
      expect(error?.code).toBe("NOT_FOUND");
    });
  });

  Scenario("Draft pages are excluded from content retrieval", ({ Given, When, Then }) => {
    let error: TRPCError | null = null;

    Given('a draft page exists at slug "en/learn/paths/skills/e2e-fixture-alpha"', () => {
      expect(draftFixture).toMatchObject({ slug: "learn/paths/skills/e2e-fixture-alpha", locale: "en", draft: true });
    });

    When('the client calls content.getBySlug with slug "en/learn/paths/skills/e2e-fixture-alpha"', async () => {
      try {
        await testCaller.content.getBySlug({ locale: "en", slug: "learn/paths/skills/e2e-fixture-alpha" });
      } catch (e) {
        error = e as TRPCError;
      }
    });

    Then("the response should indicate the page was not found", () => {
      expect(error).toBeInstanceOf(TRPCError);
      expect(error?.code).toBe("NOT_FOUND");
    });
  });

  Scenario("List children of a section returns pages ordered by weight ascending", ({ Given, When, Then, And }) => {
    let result: Awaited<ReturnType<typeof testCaller.content.listChildren>>;

    Given(
      'a section exists at slug "en/learn/courses/just-enough-go/learning" with child pages weighted 30, 1, 100, 20, and 10',
      async () => {
        const children = await testCaller.content.listChildren({
          locale: "en",
          parentSlug: "learn/courses/just-enough-go/learning",
        });
        expect(children.map(({ weight }) => weight)).toEqual([1, 10, 20, 30, 100]);
      },
    );

    When('the client calls content.listChildren with slug "en/learn/courses/just-enough-go/learning"', async () => {
      result = await testCaller.content.listChildren({
        locale: "en",
        parentSlug: "learn/courses/just-enough-go/learning",
      });
    });

    Then("the response should contain 5 child pages", () => {
      expect(result).toHaveLength(5);
    });

    And("the child pages should be ordered by weight ascending", () => {
      for (let i = 1; i < result.length; i++) {
        expect(result[i]!.weight).toBeGreaterThanOrEqual(result[i - 1]!.weight);
      }
    });
  });

  Scenario("Get navigation tree returns full hierarchy for the requested locale", ({ When, Then, And }) => {
    let result: Awaited<ReturnType<typeof testCaller.content.getTree>>;

    When('the client calls content.getTree with locale "en"', async () => {
      result = await testCaller.content.getTree({ locale: "en" });
    });

    Then("the response should contain a tree with top-level section nodes", () => {
      expect(result.length).toBeGreaterThan(0);
    });

    And("every node should include a slug and title", () => {
      const firstNode = result[0]!;
      expect(firstNode).toHaveProperty("slug");
      expect(firstNode).toHaveProperty("weight");
      expect(firstNode).toHaveProperty("children");
    });
  });

  Scenario("Page content includes rendered HTML with code blocks preserved", ({ Given, When, Then }) => {
    let result: Awaited<ReturnType<typeof testCaller.content.getBySlug>>;

    Given(
      'a published page exists at slug "en/learn/courses/just-enough-go/learning/beginner" with a fenced code block',
      async () => {
        const page = await testCaller.content.getBySlug({
          locale: "en",
          slug: "learn/courses/just-enough-go/learning/beginner",
        });
        expect(page?.html).toContain("<code");
      },
    );

    When(
      'the client calls content.getBySlug with slug "en/learn/courses/just-enough-go/learning/beginner"',
      async () => {
        result = await testCaller.content.getBySlug({
          locale: "en",
          slug: "learn/courses/just-enough-go/learning/beginner",
        });
      },
    );

    Then('the response "html" field should contain a rendered code element', () => {
      expect(result.html).toContain("<code");
    });
  });
});
