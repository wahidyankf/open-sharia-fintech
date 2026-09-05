import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import type { ContentMeta } from "@/features/content/core/types";
import { InMemoryContentRepository } from "@/features/content/core/repository-memory";
import { ContentService } from "@/features/content/shell/service";
import { buildFeedResponse } from "@/features/rss-feed/core/feed";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ose/www/behaviours/backend/rss-feed/rss-feed.feature"),
);

const SITE_URL = "https://oseplatform.com";

describeFeature(feature, ({ Scenario, Background }) => {
  Background(({ Given }) => {
    Given("the API is running", async () => {
      expect(await buildFeedResponse([]).text()).toContain("<rss");
    });
  });

  Scenario("RSS feed contains valid structure", ({ Given, When, Then, And }) => {
    let updates: ContentMeta[];
    let feedXml: string;

    Given("the content repository contains update posts", async () => {
      const repo = new InMemoryContentRepository([
        {
          meta: {
            title: "Phase 0 Week 4",
            slug: "updates/2025-12-14-phase-0-week-4",
            date: new Date("2025-12-14T00:00:00Z"),
            draft: false,
            description: "Week 4",
            tags: [],
            summary: "Initial setup",
            weight: 0,
            isSection: false,
            filePath: "/mock/updates/week-4.md",
            readingTime: 5,
            category: "updates",
          },
          content: "## Week 4\n\nInitial setup.",
        },
      ]);
      const service = new ContentService(repo);
      updates = await service.listUpdates();
    });

    When("the RSS feed is generated", async () => {
      feedXml = await buildFeedResponse(updates).text();
    });

    Then('the feed has a channel with title "OSE Platform Updates"', () => {
      expect(feedXml).toContain("<title>OSE Platform Updates</title>");
    });

    And("the feed has a channel link to the site URL", () => {
      expect(feedXml).toContain(`<link>${SITE_URL}/updates/</link>`);
    });

    And("the feed contains item elements for each update", () => {
      expect(feedXml).toContain("<item>");
      expect(feedXml).toContain("</item>");
    });
  });

  Scenario("RSS feed entries contain required fields", ({ Given, When, Then, And }) => {
    let updates: ContentMeta[];
    let feedXml: string;

    Given('the content repository contains an update post with title "Phase 0 End" and date "2026-02-08"', async () => {
      const repo = new InMemoryContentRepository([
        {
          meta: {
            title: "Phase 0 End",
            slug: "updates/2026-02-08-phase-0-end",
            date: new Date("2026-02-08T00:00:00Z"),
            draft: false,
            description: "End of phase 0",
            tags: [],
            summary: "Phase 0 complete",
            weight: 0,
            isSection: false,
            filePath: "/mock/updates/phase-0-end.md",
            readingTime: 5,
            category: "updates",
          },
          content: "## Phase 0 End\n\nPhase complete.",
        },
      ]);
      const service = new ContentService(repo);
      updates = await service.listUpdates();
    });

    When("the RSS feed is generated", async () => {
      feedXml = await buildFeedResponse(updates).text();
    });

    Then('the feed entry has the title "Phase 0 End"', () => {
      expect(feedXml).toContain("<![CDATA[Phase 0 End]]>");
    });

    And("the feed entry has a publication date", () => {
      expect(feedXml).toContain("<pubDate>");
    });

    And("the feed entry has a link to the update page", () => {
      expect(feedXml).toContain(`<link>${SITE_URL}/updates/2026-02-08-phase-0-end/</link>`);
    });

    And("the feed entry has a description", () => {
      expect(feedXml).toContain("<description>");
    });
  });
});
