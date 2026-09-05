import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { backendState } from "./backend-helpers";

const { Then } = createBdd();

// Note: All Given/When steps with {string} params are in backend-common.steps.ts
// Note: Then "the response should indicate the page was not found" is in backend-content-api.steps.ts

Then('the response "frontmatter" should indicate locale "en"', async () => {
  expect(backendState.enResult).toMatchObject({ locale: "en" });
});

Then('the response "html" should contain English-language content', async () => {
  expect(backendState.enResult).toMatchObject({ html: expect.stringContaining("Examples 1–26 establish Go") });
});

Then('the response "frontmatter" should indicate locale "id"', async () => {
  expect(backendState.idResult).toMatchObject({ locale: "id" });
});

Then('the response "html" should contain Indonesian-language content', async () => {
  expect(backendState.idResult).toMatchObject({ html: expect.stringContaining("Selamat datang") });
});
