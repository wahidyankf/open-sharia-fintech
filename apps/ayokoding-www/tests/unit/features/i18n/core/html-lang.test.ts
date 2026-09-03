import { describe, expect, it } from "vitest";
import { htmlLang } from "../../../../../src/features/i18n/core/html-lang";

// Gherkin (binds): "Indonesian locale page declares lang='id'"
// Gherkin (binds): "English locale page declares lang='en'"
describe("htmlLang", () => {
  it("returns 'id' for Indonesian locale", () => {
    expect(htmlLang("id")).toBe("id");
  });

  it("returns 'en' for English locale", () => {
    expect(htmlLang("en")).toBe("en");
  });
});
