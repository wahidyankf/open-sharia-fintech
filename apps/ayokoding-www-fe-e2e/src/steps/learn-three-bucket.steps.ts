import { createBdd } from "playwright-bdd";
import { expect } from "@playwright/test";
import { getResilient } from "../support/resilient-request";

const { Then } = createBdd();

// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:A relocated legacy domain URL redirects to its legacy address in one hop
// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:A stale /c-bookmarked legacy domain URL redirects to its legacy address in two hops
// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:A historical learn-reorg source chains through to its legacy address
// @covers specs/apps/ayokoding/www/behaviors/frontend/navigation/learn-three-bucket.feature:A deep legacy path keeps its sub-taxonomy verbatim
Then("the response status should not be a client or server error", async ({ page }) => {
  // Re-fetch whatever URL the browser landed on after following every redirect hop, so this
  // check is independent of how many hops the prior "a visitor navigates to" step's own
  // page.goto() Response object already discarded.
  const response = await getResilient(page, page.url());
  expect(response.status(), `${page.url()} responded ${response.status()}`).toBeLessThan(400);
});
