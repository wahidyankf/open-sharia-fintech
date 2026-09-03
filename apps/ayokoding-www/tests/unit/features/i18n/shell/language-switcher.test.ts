import { describe, expect, it } from "vitest";
import { buildLocaleSwitchHref } from "../../../../../src/features/i18n/shell/language-switcher";

// Regression test for Rule-15 EWT-002: a locale switch previously rewrote the URL from
// `usePathname()` alone, silently dropping any active query-string filter (e.g. the AI benchmark
// tool's `?harness=`/`?class=` filters) on every locale switch. `buildLocaleSwitchHref` is the
// extracted pure URL-builder now exercised directly by `switchLocale`.
describe("buildLocaleSwitchHref", () => {
  it("replaces only the locale segment when there is no query string", () => {
    const href = buildLocaleSwitchHref("/en/tools/ai-benchmark", new URLSearchParams(), "id");
    expect(href).toBe("/id/tools/ai-benchmark");
  });

  it("preserves an active query string across the locale switch (EWT-002 fix)", () => {
    const href = buildLocaleSwitchHref(
      "/en/tools/ai-benchmark",
      new URLSearchParams("harness=claude-code&class=opus"),
      "id",
    );
    expect(href).toBe("/id/tools/ai-benchmark?harness=claude-code&class=opus");
  });

  it("preserves the query string for a single filter param too", () => {
    const href = buildLocaleSwitchHref("/en/tools/ai-benchmark", new URLSearchParams("harness=claude-code"), "id");
    expect(href).toBe("/id/tools/ai-benchmark?harness=claude-code");
  });

  it("produces a bare root-locale path when the pathname has no further segments", () => {
    const href = buildLocaleSwitchHref("/en", new URLSearchParams(), "id");
    expect(href).toBe("/id");
  });
});
