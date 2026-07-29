import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { cleanup, render, screen } from "@testing-library/react";
import { expect, vi } from "vitest";
import React from "react";

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

import "./helpers/test-setup";
import ToolsIndexPage from "@/app/[locale]/tools/page";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/tools-index.feature"),
);

describeFeature(feature, ({ Scenario, AfterEachScenario }) => {
  AfterEachScenario(() => {
    cleanup();
  });

  // AC-13 (UWT-009) — Tools index calculator entry has a description distinct from its link text.
  Scenario("The calculator entry shows a description distinct from its link text", async ({ Given, When, Then }) => {
    let link: HTMLElement;

    Given("I am on the tools index page", async () => {
      const jsx = await ToolsIndexPage({ params: Promise.resolve({ locale: "en" as const }) });
      render(jsx);
    });

    When("the calculator entry renders", () => {
      link = screen.getByRole("link", { name: /cost of living calculator/i });
      expect(link).toBeTruthy();
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/tools-index.feature:The calculator entry shows a description distinct from its link text
    Then("the calculator entry shows a description distinct from its link text", () => {
      const desc = screen.getByTestId("tool-desc-calculator");
      expect((desc.textContent ?? "").trim()).not.toBe("");
      expect((desc.textContent ?? "").trim()).not.toBe((link.textContent ?? "").trim());
    });
  });

  // AC-3 — Phase 10 reveal: the AI benchmark tool gets its own tools-index entry.
  Scenario("The AI benchmark entry shows a description distinct from its link text", async ({ Given, When, Then }) => {
    let link: HTMLElement;

    Given("I am on the tools index page", async () => {
      const jsx = await ToolsIndexPage({ params: Promise.resolve({ locale: "en" as const }) });
      render(jsx);
    });

    When("the AI benchmark entry renders", () => {
      link = screen.getByRole("link", { name: /ai (model )?benchmark/i });
      expect(link).toBeTruthy();
    });

    // @covers specs/apps/ayokoding/behavior/ayokoding-www/gherkin/tools/tools-index.feature:The AI benchmark entry shows a description distinct from its link text
    Then("the AI benchmark entry shows a description distinct from its link text", () => {
      const desc = screen.getByTestId("tool-desc-ai-benchmark");
      expect((desc.textContent ?? "").trim()).not.toBe("");
      expect((desc.textContent ?? "").trim()).not.toBe((link.textContent ?? "").trim());
    });
  });
});
