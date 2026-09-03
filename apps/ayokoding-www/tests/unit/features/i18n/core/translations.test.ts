import { describe, expect, it } from "vitest";
import { t } from "../../../../../src/features/i18n/core/translations";

// Gherkin (underpins): "A non-mermaid code block renders a copy button"; "The copy button is
// labelled in Indonesian on the Indonesian site" — a pure-data key test that supplies the
// localized copy/copied labels those scenarios rely on, without binding either scenario's steps
// itself (see specs/apps/ayokoding/www/behaviors/frontend/content/code-block-copy.feature).
describe("t — code-block copy button keys", () => {
  it("returns the English copy label", () => {
    expect(t("en", "copy")).toBe("Copy");
  });

  it("returns the Indonesian copy label", () => {
    expect(t("id", "copy")).toBe("Salin");
  });

  it("returns the English copied label", () => {
    expect(t("en", "copied")).toBe("Copied");
  });

  it("returns the Indonesian copied label", () => {
    expect(t("id", "copied")).toBe("Tersalin");
  });

  it("returns the English copy-failed label", () => {
    expect(t("en", "copyFailed")).toBe("Copy failed");
  });

  it("returns the Indonesian copy-failed label", () => {
    expect(t("id", "copyFailed")).toBe("Gagal menyalin");
  });
});
