import { expect } from "@playwright/test";
import { createBdd } from "playwright-bdd";
import { state } from "./helpers";

const { Then } = createBdd();

Then('the response "frontmatter" should indicate locale "en"', async () => {
  expect((state.pageResult as { locale: string }).locale).toBe("en");
});

Then('the response "html" should contain English-language content', async () => {
  expect((state.pageResult as { html: string }).html).toContain("Examples 1–26 establish Go's daily toolchain");
});

Then('the response "frontmatter" should indicate locale "id"', async () => {
  expect((state.pageResult as { locale: string }).locale).toBe("id");
});

Then('the response "html" should contain Indonesian-language content', async () => {
  expect((state.pageResult as { html: string }).html).toContain("Selamat datang di pusat pembelajaran AyoKoding");
});
