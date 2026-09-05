import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { TRPCError } from "@trpc/server";
import { expect } from "vitest";
import { testCaller } from "./helpers/test-caller";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviours/backend/i18n/i18n-api.feature"),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the API is running", async () => {
      await expect(testCaller.meta.health()).resolves.toEqual({ status: "ok" });
    });
  });

  Scenario('English content is served when locale is "en"', ({ Given, When, Then, And }) => {
    let result: Awaited<ReturnType<typeof testCaller.content.getBySlug>>;

    Given('a page exists at slug "en/learn/courses/just-enough-go/learning/beginner" under locale "en"', async () => {
      await expect(
        testCaller.content.getBySlug({ locale: "en", slug: "learn/courses/just-enough-go/learning/beginner" }),
      ).resolves.toMatchObject({ locale: "en" });
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

    Then('the response "frontmatter" should indicate locale "en"', () => {
      expect(result.locale).toBe("en");
    });

    And('the response "html" should contain English-language content', () => {
      expect(result.html).toContain("Goroutines come later");
    });
  });

  Scenario('Indonesian content is served when locale is "id"', ({ Given, When, Then, And }) => {
    let result: Awaited<ReturnType<typeof testCaller.content.getBySlug>>;

    Given('a page exists at slug "id/belajar/ikhtisar" under locale "id"', async () => {
      await expect(testCaller.content.getBySlug({ locale: "id", slug: "belajar/ikhtisar" })).resolves.toMatchObject({
        locale: "id",
      });
    });

    When('the client calls content.getBySlug with slug "id/belajar/ikhtisar"', async () => {
      result = await testCaller.content.getBySlug({ locale: "id", slug: "belajar/ikhtisar" });
    });

    Then('the response "frontmatter" should indicate locale "id"', () => {
      expect(result.locale).toBe("id");
    });

    And('the response "html" should contain Indonesian-language content', () => {
      expect(result.html).toContain("Ini adalah halaman ikhtisar");
    });
  });

  Scenario("Requesting a slug prefixed with an invalid locale is rejected", ({ When, Then }) => {
    let error: unknown = null;

    When(
      'the client calls content.getBySlug with slug "fr/learn/courses/just-enough-go/learning/beginner"',
      async () => {
        try {
          const invalidInput = {
            locale: "fr",
            slug: "learn/courses/just-enough-go/learning/beginner",
          } as unknown as Parameters<typeof testCaller.content.getBySlug>[0];
          await testCaller.content.getBySlug(invalidInput);
        } catch (e) {
          error = e;
        }
      },
    );

    Then("the response should reject the invalid locale as a bad request", () => {
      expect(error).toBeInstanceOf(TRPCError);
      expect((error as TRPCError).code).toBe("BAD_REQUEST");
    });
  });
});
