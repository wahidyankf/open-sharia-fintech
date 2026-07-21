import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

// Regression guard for swe-ui audit b06d32 Finding 2 (re-validated FALSE_POSITIVE, not fixed):
// the audit assumed `--color-primary` resolves to the honey/amber `--hue-honey` token from
// `@open-sharia-enterprise/web-ui-token/src/ayokoding.css`, computing `prose-a:text-primary`
// (markdown-renderer.tsx) and the `text-primary` meta link (section-card.tsx) at 2.13:1 —
// below the 4.5:1 WCAG AA minimum. In the LIVE app this is not what renders: this file
// declares its own local `@theme` block (light) and `.dark` block (dark), both AFTER the
// `ayokoding.css` import, which redeclare `--color-primary` to blue
// (`hsl(221.2 83.2% 53.3%)` light / `hsl(217.2 91.2% 59.8%)` dark). Because `@import` is
// inlined before subsequent same-file rules and CSS custom properties cascade "last
// declaration for a matching selector wins," this local override — not the honey token —
// is what `text-primary` actually resolves to. Verified against the compiled Tailwind
// output (`--color-primary: #2563eb` in `:root`, `#3b82f6` in the winning `.dark` block)
// and WCAG luminance math: ~5.04:1 (light) / ~5.44:1 (dark) against `--color-background`,
// both clearing the 4.5:1 AA bar.
//
// This test pins the override's presence and its position AFTER the import. If either is
// ever removed, the honey token becomes live again and silently reintroduces the 2.13:1
// contrast failure without any other test catching it (jsdom does not resolve Tailwind
// `@theme`/CSS-custom-property cascade, so no component-level test can observe this).
describe("ayokoding-www globals.css — --color-primary override (WCAG AA guard)", () => {
  const css = readFileSync(join(__dirname, "globals.css"), "utf8");

  it("imports ayokoding.css (the source of the honey --color-primary token)", () => {
    expect(css).toContain('@import "@open-sharia-enterprise/web-ui-token/src/ayokoding.css"');
  });

  it("redeclares --color-primary to blue in a local @theme block, positioned after the import", () => {
    const importIndex = css.indexOf('@import "@open-sharia-enterprise/web-ui-token/src/ayokoding.css"');
    const lightOverrideIndex = css.indexOf("--color-primary: hsl(221.2 83.2% 53.3%)");

    expect(importIndex).toBeGreaterThan(-1);
    expect(lightOverrideIndex).toBeGreaterThan(-1);
    expect(lightOverrideIndex).toBeGreaterThan(importIndex);
  });

  it("redeclares --color-primary to blue in a local .dark block, positioned after the import", () => {
    const importIndex = css.indexOf('@import "@open-sharia-enterprise/web-ui-token/src/ayokoding.css"');
    const darkOverrideIndex = css.indexOf("--color-primary: hsl(217.2 91.2% 59.8%)");

    expect(importIndex).toBeGreaterThan(-1);
    expect(darkOverrideIndex).toBeGreaterThan(-1);
    expect(darkOverrideIndex).toBeGreaterThan(importIndex);
  });
});
