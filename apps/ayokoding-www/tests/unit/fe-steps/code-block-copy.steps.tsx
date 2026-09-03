import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen, fireEvent, waitFor } from "@testing-library/react";
import { expect, vi } from "vitest";

import { MarkdownRenderer } from "@/features/content/shell/markdown-renderer";
import { t } from "@/features/i18n/core/translations";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/www/behaviors/frontend/content/code-block-copy.feature"),
);

const luaHtml = `<figure data-rehype-pretty-code-figure><pre data-language="lua"><code><span>print("hi")</span></code></pre></figure>`;
const mermaidFigureHtml = `<figure data-rehype-pretty-code-figure><pre data-language="mermaid"><code>graph TD; A-->B;</code></pre></figure>`;
// A two-line annotated Lua block; the text nodes (including the newline between the lines) are what
// `getTextContent(pre)` concatenates into the verbatim clipboard value.
const annotatedLua = `local x = 1  -- => output\nprint(x)     -- => output`;
const annotatedLuaHtml = `<figure data-rehype-pretty-code-figure><pre data-language="lua"><code><span>local x = 1  -- => output</span>\n<span>print(x)     -- => output</span></code></pre></figure>`;

/** Installs a mock `navigator.clipboard.writeText` (jsdom lacks it). Returns the spy. */
function stubClipboard(): ReturnType<typeof vi.fn> {
  const writeText = vi.fn(() => Promise.resolve());
  Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
  return writeText;
}

function copyButton(): HTMLElement {
  const button = document.querySelector('[data-slot="code-block-copy"]');
  if (!(button instanceof HTMLElement)) {
    throw new Error("copy button not found");
  }
  return button;
}

// Every scenario in this feature is `@unit @e2e` (the ayokoding convention: content behaviours are
// verified BOTH as a jsdom unit render here AND as a live Playwright-BDD run in
// apps/ayokoding-www-fe-e2e). `includeTags: ["unit"]` runs them all at the unit tier; the same
// scenarios run against the real page in the e2e project. The three interaction scenarios
// (verbatim clipboard / success confirmation / touch reachability) get jsdom smoke bodies here that
// exercise the wiring the live e2e proves end-to-end.
describeFeature(
  feature,
  ({ Scenario, Background }) => {
    Background(({ Given }) => {
      Given("the app is running", () => {});
    });

    Scenario("A non-mermaid code block renders a copy button", ({ Given, When, Then }) => {
      Given("a visitor opens an English content page containing a fenced Lua code block", () => {
        // render happens in the When step
      });

      When("the page renders", () => {
        cleanup();
        stubClipboard();
        render(<MarkdownRenderer html={luaHtml} locale="en" />);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/content/code-block-copy.feature:A non-mermaid code block renders a copy button
      Then("the code block displays a copy button", () => {
        expect(document.querySelector('[data-slot="code-block-copy"]')).toBeTruthy();
      });
    });

    Scenario("A mermaid block renders no copy button", ({ Given, When, Then }) => {
      Given("a visitor opens a content page containing a mermaid fenced block", () => {
        // render happens in the When step
      });

      When("the page renders", () => {
        cleanup();
        render(<MarkdownRenderer html={mermaidFigureHtml} locale="en" />);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/content/code-block-copy.feature:A mermaid block renders no copy button
      Then("the mermaid block renders as a diagram with no copy button", () => {
        // Real SVG rendering requires browser APIs unavailable in jsdom (see mermaid.tsx); before
        // the async `mermaid.render()` resolves, MermaidDiagram renders its <pre><code> fallback —
        // asserting that plus the absence of the copy button is the exclusion regression guard.
        expect(document.querySelector("pre")).toBeTruthy();
        expect(document.querySelector('[data-slot="code-block-copy"]')).toBeNull();
      });
    });

    Scenario("The copy button is labelled in Indonesian on the Indonesian site", ({ Given, When, Then }) => {
      Given("a visitor opens an Indonesian content page containing a fenced code block", () => {
        // render happens in the When step
      });

      When("the accessibility tree is inspected", () => {
        cleanup();
        stubClipboard();
        render(<MarkdownRenderer html={luaHtml} locale="id" />);
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/content/code-block-copy.feature:The copy button is labelled in Indonesian on the Indonesian site
      Then('the copy button has the Indonesian accessible name "Salin"', () => {
        const button = screen.getByRole("button", { name: t("id", "copy") });
        expect(button.getAttribute("aria-label")).toBe("Salin");
      });
    });

    Scenario("Clicking copy places the verbatim annotated source on the clipboard", ({ Given, When, Then }) => {
      let writeText: ReturnType<typeof vi.fn>;

      Given('a visitor is on a page whose Lua block contains "-- => output" annotations', () => {
        cleanup();
        writeText = stubClipboard();
        render(<MarkdownRenderer html={annotatedLuaHtml} locale="en" />);
      });

      When("the visitor clicks that block's copy button", () => {
        fireEvent.click(copyButton());
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/content/code-block-copy.feature:Clicking copy places the verbatim annotated source on the clipboard
      Then('the clipboard contains the block\'s source verbatim including the "-- => output" annotations', () => {
        // Compared against the in-process value handed to writeText (pre-clipboard), per tech-docs.md's
        // Windows \r\n caveat; the live e2e reads navigator.clipboard on a real page.
        expect(writeText).toHaveBeenCalledWith(annotatedLua);
      });
    });

    Scenario("The copy button confirms success to the visitor", ({ Given, When, Then }) => {
      Given("a visitor has clicked a code block's copy button", () => {
        cleanup();
        stubClipboard();
        render(<MarkdownRenderer html={luaHtml} locale="en" />);
        fireEvent.click(copyButton());
      });

      When("the copy succeeds", async () => {
        // The clipboard stub resolves; the button flips to its success state on the microtask.
        await waitFor(() => expect(copyButton().getAttribute("aria-label")).toBe(t("en", "copied")));
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/content/code-block-copy.feature:The copy button confirms success to the visitor
      Then('the button shows a "Copied" confirmation before reverting', () => {
        // Success state: aria-label is the copied label and the polite live region carries it.
        expect(copyButton().getAttribute("aria-label")).toBe("Copied");
        expect(screen.getByText("Copied", { selector: "output" })).toBeTruthy();
      });
    });

    Scenario("The copy button is reachable on a touch viewport without hovering", ({ Given, When, Then }) => {
      Given("a visitor loads a content page on a touch (no-hover) viewport", () => {
        cleanup();
        stubClipboard();
        render(<MarkdownRenderer html={luaHtml} locale="en" />);
      });

      When("the code block is rendered", () => {
        // render happened in the Given step
      });

      // @covers specs/apps/ayokoding/www/behaviors/frontend/content/code-block-copy.feature:The copy button is reachable on a touch viewport without hovering
      Then("the copy button is visible without any hover interaction", () => {
        // jsdom cannot evaluate `@media (hover: none)`; assert the always-visible-on-touch utility is
        // present (the mechanism the live e2e proves under a real no-hover viewport) — no hover fired.
        expect(copyButton().className).toContain("[@media(hover:none)]:opacity-100");
      });
    });
  },
  { includeTags: ["unit"] },
);
