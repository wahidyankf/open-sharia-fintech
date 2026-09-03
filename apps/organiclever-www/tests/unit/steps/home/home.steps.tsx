import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { expect } from "vitest";

import { HomeContent } from "@/features/home";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/apps/organiclever/www/behaviors/frontend/home/home.feature"),
);

describeFeature(feature, ({ Scenario, AfterEachScenario }) => {
  AfterEachScenario(() => {
    cleanup();
  });

  Scenario("Hero heading visible", ({ When, Then, And }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    Then('I see text "Your life,"', () => {
      expect(screen.getByText(/Your life,/i)).toBeDefined();
    });

    And('I see text "tracked."', () => {
      expect(screen.getByText(/tracked\./i)).toBeDefined();
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Hero heading visible
    And('I see text "Analyzed."', () => {
      expect(screen.getByText(/Analyzed\./)).toBeDefined();
    });
  });

  Scenario("Primary call-to-action button present", ({ When, Then }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Primary call-to-action button present
    Then('I see a button "Open the app"', () => {
      expect(screen.getByRole("button", { name: /Open the app/i })).toBeDefined();
    });
  });

  Scenario("Footer link present", ({ When, Then }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Footer link present
    Then('I see text "Open app →"', () => {
      expect(screen.getByText(/Open app →/)).toBeDefined();
    });
  });

  Scenario("Pre-Alpha badge visible in nav", ({ When, Then }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Pre-Alpha badge visible in nav
    Then('I see text "Pre-Alpha"', () => {
      expect(screen.getAllByText(/Pre-Alpha/i).length).toBeGreaterThan(0);
    });
  });

  Scenario("Alpha warning banner visible", ({ When, Then }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Alpha warning banner visible
    Then('I see text "Pre-Alpha — expect bugs, rough edges, and breaking changes"', () => {
      expect(screen.getByText(/Pre-Alpha — expect bugs, rough edges, and breaking changes/i)).toBeDefined();
    });
  });

  Scenario("All five event type cards visible", ({ When, Then, And }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    Then('I see text "Workouts"', () => {
      expect(screen.getByText("Workouts")).toBeDefined();
    });

    And('I see text "Reading"', () => {
      expect(screen.getAllByText("Reading").length).toBeGreaterThan(0);
    });

    And('I see text "Learning"', () => {
      expect(screen.getAllByText("Learning").length).toBeGreaterThan(0);
    });

    And('I see text "Meals"', () => {
      expect(screen.getByText("Meals")).toBeDefined();
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:All five event type cards visible
    And('I see text "Focus"', () => {
      expect(screen.getAllByText("Focus").length).toBeGreaterThan(0);
    });
  });

  Scenario("Custom event card visible", ({ When, Then }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Custom event card visible
    Then('I see text "Plus your own."', () => {
      expect(screen.getByText(/Plus your own\./i)).toBeDefined();
    });
  });

  Scenario("Weekly rhythm demo visible", ({ When, Then }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Weekly rhythm demo visible
    Then('I see text "Last 7 days"', () => {
      expect(screen.getByText("Last 7 days")).toBeDefined();
    });
  });

  Scenario("All six principles visible", ({ When, Then, And }) => {
    When("I navigate to the marketing home page", () => {
      cleanup();
      render(<HomeContent />);
    });

    Then('I see text "Local-first"', () => {
      expect(screen.getByText("Local-first")).toBeDefined();
    });

    And('I see text "Yours to take"', () => {
      expect(screen.getByText("Yours to take")).toBeDefined();
    });

    And('I see text "Flexible"', () => {
      expect(screen.getByText("Flexible")).toBeDefined();
    });

    And('I see text "Quiet"', () => {
      expect(screen.getByText("Quiet")).toBeDefined();
    });

    And('I see text "Open"', () => {
      expect(screen.getByText("Open")).toBeDefined();
    });

    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:All six principles visible
    And('I see text "Multilingual"', () => {
      expect(screen.getByText("Multilingual")).toBeDefined();
    });
  });
});
