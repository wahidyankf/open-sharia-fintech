import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, fireEvent, cleanup } from "@testing-library/react";
import { vi, expect } from "vitest";

import { SideNav } from "../../../../src/components/side-nav/side-nav";
import type { TabItem } from "../../../../src/components/tab-bar/tab-bar";

const tabs: TabItem[] = [
  { id: "home", label: "Home", icon: "home" },
  { id: "history", label: "History", icon: "history" },
];

const brand = { name: "OrganicLever", icon: "dumbbell", hue: "teal" as const };

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/side-nav/side-nav.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders brand name", ({ When, Then }) => {
    let brandName: HTMLElement;

    When('I render a SideNav with brand "OrganicLever" and tabs', () => {
      cleanup();
      render(<SideNav brand={brand} tabs={tabs} current="home" onChange={vi.fn()} />);
      brandName = screen.getByText("OrganicLever");
    });

    Then('the text "OrganicLever" should be visible', () => {
      expect(brandName.textContent).toBe("OrganicLever");
    });
  });

  Scenario("Renders tabs", ({ When, Then }) => {
    let homeTab: HTMLElement;

    When('I render a SideNav with brand "OrganicLever" and tabs', () => {
      cleanup();
      render(<SideNav brand={brand} tabs={tabs} current="home" onChange={vi.fn()} />);
      homeTab = screen.getByText("Home");
    });

    Then('the tab "Home" should be visible', () => {
      expect(homeTab.textContent).toBe("Home");
    });
  });

  Scenario("Tab click triggers onChange with tab id", ({ Given, When, Then }) => {
    const onChangeMock = vi.fn();

    Given('I render a SideNav with brand "OrganicLever" and tabs', () => {
      cleanup();
      render(<SideNav brand={brand} tabs={tabs} current="home" onChange={onChangeMock} />);
      expect(screen.getByText("History")).toBeDefined();
    });

    When('the user clicks the "History" tab', () => {
      cleanup();
      render(<SideNav brand={brand} tabs={tabs} current="home" onChange={onChangeMock} />);
      fireEvent.click(screen.getByText("History"));
    });

    Then('onChange should be called with "history"', () => {
      expect(onChangeMock).toHaveBeenCalledWith("history");
    });
  });

  Scenario("Active tab has active background", ({ When, Then }) => {
    let homeButton: HTMLButtonElement | null;

    When('I render a SideNav with brand "OrganicLever" current "home" and tabs', () => {
      cleanup();
      render(<SideNav brand={brand} tabs={tabs} current="home" onChange={vi.fn()} />);
      homeButton = screen.getByText("Home").closest("button");
    });

    Then('the "Home" button should have the active class', () => {
      expect(homeButton?.className).toContain("bg-[var(--hue-teal-wash)]");
    });
  });

  Scenario("Brand row click always calls onChange with home", ({ Given, When, Then }) => {
    const onChangeMock = vi.fn();

    Given('I render a SideNav with brand "OrganicLever" current "history" and tabs', () => {
      cleanup();
      render(<SideNav brand={brand} tabs={tabs} current="history" onChange={onChangeMock} />);
      expect(screen.getByText("OrganicLever")).toBeDefined();
    });

    When("the user clicks the brand row", () => {
      cleanup();
      render(<SideNav brand={brand} tabs={tabs} current="history" onChange={onChangeMock} />);
      fireEvent.click(screen.getByText("OrganicLever"));
    });

    Then('onChange should be called with "home"', () => {
      expect(onChangeMock).toHaveBeenCalledWith("home");
    });
  });
});
