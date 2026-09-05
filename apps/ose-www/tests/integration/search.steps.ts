import path from "node:path";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import type { SearchResult } from "@/features/content/core/types";
import { FileSystemContentRepository } from "@/features/content/shell/repository-fs";
import { ContentService } from "@/features/content/shell/service";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ose/www/behaviours/backend/search/search.feature"),
);
const contentDirectory = path.resolve(process.cwd(), "tests/e2e-fixtures/content");
const searchDataPath = path.resolve(process.cwd(), "tests/e2e-fixtures/search-data.json");

function realSearchService(): ContentService {
  return new ContentService(new FileSystemContentRepository(contentDirectory, false), searchDataPath, {
    showDrafts: false,
  });
}

describeFeature(feature, ({ Background, Scenario }) => {
  Background(({ Given }) => {
    Given("the API is running", () => {
      expect(realSearchService()).toBeInstanceOf(ContentService);
    });
  });

  Scenario("Search returns matching results", ({ Given, When, Then, And }) => {
    const service = realSearchService();
    let results: SearchResult[] = [];

    Given('the search index contains pages about "enterprise" and "compliance"', async () => {
      expect(await service.search("enterprise")).not.toHaveLength(0);
      expect(await service.search("compliance")).not.toHaveLength(0);
    });
    When('a search query "enterprise" is executed', async () => {
      results = await service.search("enterprise");
    });
    Then('the results contain pages matching "enterprise"', () => {
      expect(results.some(({ title, excerpt }) => `${title} ${excerpt}`.toLowerCase().includes("enterprise"))).toBe(
        true,
      );
    });
    And("each result contains a title, slug, and excerpt", () => {
      for (const result of results) {
        expect(result.title).not.toBe("");
        expect(result.slug).not.toBe("");
        expect(result.excerpt).not.toBe("");
      }
    });
  });

  Scenario("Search with no matches returns empty results", ({ Given, When, Then }) => {
    const service = realSearchService();
    let results: SearchResult[] = [];

    Given('the search index contains pages about "enterprise" and "compliance"', async () => {
      expect(await service.search("enterprise")).not.toHaveLength(0);
      expect(await service.search("compliance")).not.toHaveLength(0);
    });
    When('a search query "nonexistent-term-xyz" is executed', async () => {
      results = await service.search("nonexistent-term-xyz");
    });
    Then("the results are empty", () => {
      expect(results).toHaveLength(0);
    });
  });

  Scenario("Search results respect the limit parameter", ({ Given, When, Then }) => {
    const service = realSearchService();
    let results: SearchResult[] = [];

    Given('the search index contains 5 pages matching "phase"', async () => {
      expect(await service.search("phase", 10)).toHaveLength(5);
    });
    When('a search query "phase" is executed with limit 2', async () => {
      results = await service.search("phase", 2);
    });
    Then("at most 2 results are returned", () => {
      expect(results).toHaveLength(2);
    });
  });
});
