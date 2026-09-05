import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import { testCaller } from "./helpers/test-caller";
import type { SearchResult } from "@/features/content/core/types";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviours/backend/search/search-api.feature"),
);

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the API is running", async () => {
      await expect(testCaller.meta.health()).resolves.toEqual({ status: "ok" });
    });
  });

  Scenario("Search returns matching results with title, slug, and excerpt", ({ Given, When, Then, And }) => {
    let results: SearchResult[];

    Given('published pages indexed under locale "en" include a page titled "Beginner Examples"', async () => {
      await expect(testCaller.search.query({ query: "goroutines", locale: "en" })).resolves.toEqual(
        expect.arrayContaining([expect.objectContaining({ title: "Beginner Examples" })]),
      );
    });

    When('the client calls search.query with locale "en" and query "goroutines"', async () => {
      results = await testCaller.search.query({ query: "goroutines", locale: "en" });
    });

    Then("the response should contain at least one result", () => {
      expect(results.length).toBeGreaterThan(0);
    });

    And('each result should include a "title" field', () => {
      const first = results[0]!;
      expect(first).toHaveProperty("title");
    });

    And('each result should include a "slug" field', () => {
      const first = results[0]!;
      expect(first).toHaveProperty("slug");
    });

    And('each result should include an "excerpt" field', () => {
      const first = results[0]!;
      expect(first).toHaveProperty("excerpt");
    });
  });

  Scenario("Search results include locale information", ({ Given, When, Then }) => {
    let results: SearchResult[];

    Given('published pages indexed under locale "en" include content about "programming"', async () => {
      expect((await testCaller.search.query({ query: "programming", locale: "en" })).length).toBeGreaterThan(0);
    });

    When('the client calls search.query with locale "en" and query "programming"', async () => {
      results = await testCaller.search.query({ query: "programming", locale: "en" });
    });

    Then('each result should include a "locale" field matching "en"', () => {
      for (const result of results) {
        expect(result).toHaveProperty("locale");
        expect(result.locale).toBe("en");
      }
    });
  });

  Scenario("Search is scoped to the requested locale", ({ Given, When, Then, And }) => {
    let results: SearchResult[];

    Given('a page exists in locale "en" with title "Spring Security Basics"', async () => {
      await expect(testCaller.search.query({ query: "Security Basics", locale: "en" })).resolves.toEqual(
        expect.arrayContaining([expect.objectContaining({ title: "Spring Security Basics", locale: "en" })]),
      );
    });

    And('no equivalent page exists in locale "id"', async () => {
      await expect(testCaller.search.query({ query: "Spring Security Basics", locale: "id" })).resolves.toEqual([]);
    });

    When('the client calls search.query with locale "id" and query "Spring Security Basics"', async () => {
      results = await testCaller.search.query({ query: "Spring Security Basics", locale: "id" });
    });

    Then("the response should contain no results", () => {
      expect(results.length).toBe(0);
    });
  });

  Scenario("Empty query returns an error", ({ When, Then }) => {
    let error: unknown = null;

    When('the client calls search.query with locale "en" and an empty query', async () => {
      try {
        await testCaller.search.query({ query: "", locale: "en" });
      } catch (e) {
        error = e;
      }
    });

    Then("the response should indicate an invalid input error", () => {
      expect(error).toBeTruthy();
    });
  });
});
