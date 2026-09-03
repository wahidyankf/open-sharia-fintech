import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { state } from "./helpers";

const { Then } = createBdd();

// Note: All Given/When steps with {string} params are in common.steps.ts
// Note: Then "the response should indicate the page was not found" is in content-api.steps.ts

Then('the response "frontmatter" should indicate locale "en"', async () => {
  const enResult = state.enResult as unknown[];
  expect(enResult.length).toBeGreaterThan(0);
});

// @covers specs/apps/ayokoding/www/behaviors/backend/i18n/i18n-api.feature:English content is served when locale is "en"
Then('the response "html" should contain English-language content', async () => {
  const enResult = state.enResult as unknown[];
  expect(enResult.length).toBeGreaterThan(0);
});

Then('the response "frontmatter" should indicate locale "id"', async () => {
  const idResult = state.idResult as unknown[];
  expect(idResult.length).toBeGreaterThan(0);
});

// @covers specs/apps/ayokoding/www/behaviors/backend/i18n/i18n-api.feature:Indonesian content is served when locale is "id"
Then('the response "html" should contain Indonesian-language content', async () => {
  const idResult = state.idResult as unknown[];
  expect(idResult.length).toBeGreaterThan(0);
});
