import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

// RED anchor for Phase 1 of the `ayokoding-www-tools-ai-benchmark` plan.
//
// The AI Benchmark feature renders a "band" UI (one band per AI model tier) whose colour is
// derived from a named CSS custom property. Phase 1 introduces four band design tokens that
// name the four benchmark tiers:
//
//   --chart-band-opus     (Opus tier)
//   --chart-band-sonnet   (Sonnet tier)
//   --chart-band-haiku    (_HAIKU / "fast" tier)
//   --chart-band-unrated  (models that have no tier rating)
//
// Token home: `libs/web-ui-token/src/ayokoding.css` (the AyoKoding theme that
// `@open-sharia-enterprise/web-ui-token` ships). They must be declared BOTH in the light
// `@theme` block (the default theme) AND in the dark-override block whose selector is
// `[data-theme="dark"], .dark` — so the chart bands render with theme-appropriate colours in
// both modes. This test pins the four token names and their presence in BOTH blocks BEFORE
// the tokens exist (T-1 RED). T-2 GREEN will add the four declarations to the CSS, at which
// point this test goes green. T-1's RED contract: this file must NOT add the tokens — it only
// asserts they exist, and currently they do not, so this test fails.
//
// Block identification (inspected in `libs/web-ui-token/src/ayokoding.css` at RED time):
//   - Light block: the `@theme { ... }` block starting near the top of the file. The opener
//     `@theme` is used as the literal anchor.
//   - Dark block: the selector whose normalized form is
//     `[data-theme="dark"], .dark { ... }` later in the file. In the SOURCE today the
//     selector is split across two lines as:
//         [data-theme="dark"],
//         .dark {
//     CSS treats the newline between the `,` and `.dark` as whitespace, so the selector is
//     semantically `[data-theme="dark"], .dark` (the exact text the plan expects). Because
//     the opener spans a newline, the extractor anchors on the substring
//     `[data-theme="dark"]` and then finds the NEXT `{` — that brace belongs to the dark
//     block. This is the selector we actually find in the file today.
//
// The file is read as TEXT (no CSS parser) so the assertions are resilient to formatting
// churn and comment placement. Block content is extracted by brace matching from the
// opener anchor to its matching close brace, so a token declared OUTSIDE the block does
// not satisfy the assertion.

// Resolve the CSS file from the vitest CWD. Nx's `test:unit` target sets
// `cwd = {projectRoot}` (apps/ayokoding-www), so the workspace-relative path to the token
// library is `../../libs/web-ui-token/src/ayokoding.css`. Using `process.cwd()` is robust
// to wherever vitest launches from inside the project; `__dirname`-relative walking would
// break if the test file ever moves.
const tokensPath = join(process.cwd(), "..", "..", "libs", "web-ui-token", "src", "ayokoding.css");

const css = readFileSync(tokensPath, "utf8");

// The four Phase 1 band design tokens. Order matches the plan's verbatim list.
const bandTokenNames = [
  "--chart-band-opus",
  "--chart-band-sonnet",
  "--chart-band-haiku",
  "--chart-band-unrated",
] as const;

// Extract the body of a CSS block that opens with `opener` (which must include the opening
// `{`) by counting braces to the matching closer. Returns the block body WITHOUT the outer
// braces, or `null` if the opener is not found / the block is malformed.
function extractBlockBody(opener: string): string | null {
  const start = css.indexOf(opener);
  if (start === -1) return null;
  const openBrace = css.indexOf("{", start);
  if (openBrace === -1) return null;
  let depth = 1;
  let i = openBrace + 1;
  while (i < css.length && depth > 0) {
    const ch = css[i];
    if (ch === "{") depth++;
    else if (ch === "}") depth--;
    if (depth === 0) break;
    i++;
  }
  if (depth !== 0) return null;
  return css.slice(openBrace + 1, i);
}

describe("ayokoding.css — Phase 1 band design tokens (RED anchor)", () => {
  describe("light @theme block", () => {
    // Anchor on `@theme {` (with space + brace) so `indexOf` skips the `@theme` mention
    // in the line-4 comment (`/* ... referenced by @theme and dark block */`) and finds
    // the actual `@theme {` directive. Anchoring on bare `@theme` would match the comment
    // first, then grab the next `{` — which opens `:root {`, not `@theme {`.
    const lightBlock = extractBlockBody("@theme {");

    it("the light @theme block exists in ayokoding.css", () => {
      expect(lightBlock).not.toBeNull();
    });

    it.each(bandTokenNames)("light @theme block declares `%s` as a CSS custom property", (tokenName) => {
      expect(lightBlock).not.toBeNull();
      // Assert the token is declared as `--chart-band-<name>:` inside the @theme block.
      expect(lightBlock ?? "").toContain(`${tokenName}:`);
    });
  });

  describe('dark override block — selector `[data-theme="dark"], .dark`', () => {
    // Normalized selector text the plan expects: `[data-theme="dark"], .dark`. In the source
    // today the selector spans two lines (`[data-theme="dark"],\n.dark {`), so we anchor on
    // the substring `[data-theme="dark"]` and let `extractBlockBody` find the next `{`.
    // See the file header comment for the full rationale.
    const darkAnchor = '[data-theme="dark"]';
    const darkBlock = extractBlockBody(darkAnchor);

    it('the dark override block with selector `[data-theme="dark"], .dark` exists in ayokoding.css', () => {
      expect(darkBlock).not.toBeNull();
    });

    it.each(bandTokenNames)("dark override block declares `%s` as a CSS custom property", (tokenName) => {
      expect(darkBlock).not.toBeNull();
      expect(darkBlock ?? "").toContain(`${tokenName}:`);
    });
  });
});
