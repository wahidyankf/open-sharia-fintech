import "./helpers/test-setup";
import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render } from "@testing-library/react";
import { expect } from "vitest";

import { MarkdownRenderer } from "@/features/content/shell/markdown-renderer";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ose/www/behaviours/frontend/content/code-block-copy.feature"),
);

const luaFigureHtml = `<figure data-rehype-pretty-code-figure><pre data-language="lua"><code><span>print("hi")</span></code></pre></figure>`;
const mermaidFigureHtml = `<figure data-rehype-pretty-code-figure><pre data-language="mermaid"><code>graph TD; A-->B;</code></pre></figure>`;

// The content-rendering contract is verified at the renderer boundary.
describeFeature(feature, ({ Scenario }) => {
  Scenario("The renderer wraps a non-mermaid code figure in a CodeBlock", ({ Given, When, Then }) => {
    Given("the ose-www markdown renderer receives HTML with a non-mermaid code figure", () => {
      expect(luaFigureHtml).toContain('data-language="lua"');
      expect(luaFigureHtml).not.toContain('data-language="mermaid"');
    });

    When("the HTML is parsed to React", () => {
      cleanup();
      render(<MarkdownRenderer html={luaFigureHtml} />);
    });

    Then("the figure is wrapped in a CodeBlock exposing a copy button", () => {
      expect(document.querySelector('[data-slot="code-block"]')).toBeTruthy();
      expect(document.querySelector('[data-slot="code-block-copy"]')).toBeTruthy();
    });
  });

  Scenario("The renderer leaves a mermaid figure as a diagram", ({ Given, When, Then }) => {
    Given("the ose-www markdown renderer receives HTML with a mermaid code figure", () => {
      expect(mermaidFigureHtml).toContain('data-language="mermaid"');
    });

    When("the HTML is parsed to React", () => {
      cleanup();
      render(<MarkdownRenderer html={mermaidFigureHtml} />);
    });

    Then("the figure renders as a mermaid diagram with no copy button", () => {
      // Real SVG rendering needs browser APIs jsdom lacks (see mermaid.tsx); before the async
      // `mermaid.render()` resolves, MermaidDiagram renders its <pre><code> fallback — asserting that
      // plus the absence of the copy button is the exclusion regression guard.
      expect(document.querySelector("pre")).toBeTruthy();
      expect(document.querySelector('[data-slot="code-block-copy"]')).toBeNull();
    });
  });
});
