import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { expect } from "vitest";

import { HomeContent } from "@/features/home";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/apps/organiclever/www/behaviors/frontend/home/home.feature"),
);

describeFeature(feature, ({ Scenario, Background, AfterEachScenario }) => {
  AfterEachScenario(() => {
    cleanup();
  });

  Background(({ Given }) => {
    Given("I navigate to the marketing home page", () => {});
  });

  Scenario("Hero heading visible", ({ Then, And }) => {
    Then('I see text "Your life,"', () => {
      cleanup();
      render(<HomeContent />);
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

  Scenario("Primary call-to-action button present", ({ Then }) => {
    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Primary call-to-action button present
    Then('I see a button "Open the app"', () => {
      cleanup();
      render(<HomeContent />);
      expect(screen.getByRole("button", { name: /Open the app/i })).toBeDefined();
    });
  });

  Scenario("Footer link present", ({ Then }) => {
    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Footer link present
    Then('I see text "Open app →"', () => {
      cleanup();
      render(<HomeContent />);
      expect(screen.getByText(/Open app →/)).toBeDefined();
    });
  });

  Scenario("Pre-Alpha badge visible in nav", ({ Then }) => {
    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Pre-Alpha badge visible in nav
    Then('I see text "Pre-Alpha"', () => {
      cleanup();
      render(<HomeContent />);
      expect(screen.getAllByText(/Pre-Alpha/i).length).toBeGreaterThan(0);
    });
  });

  Scenario("Alpha warning banner visible", ({ Then }) => {
    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Alpha warning banner visible
    Then('I see text "Pre-Alpha — expect bugs, rough edges, and breaking changes"', () => {
      cleanup();
      render(<HomeContent />);
      expect(screen.getByText(/Pre-Alpha — expect bugs, rough edges, and breaking changes/i)).toBeDefined();
    });
  });

  Scenario("All five event type cards visible", ({ Then, And }) => {
    Then('I see text "Workouts"', () => {
      cleanup();
      render(<HomeContent />);
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

  Scenario("Custom event card visible", ({ Then }) => {
    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Custom event card visible
    Then('I see text "Plus your own."', () => {
      cleanup();
      render(<HomeContent />);
      expect(screen.getByText(/Plus your own\./i)).toBeDefined();
    });
  });

  Scenario("Weekly rhythm demo visible", ({ Then }) => {
    // @covers specs/apps/organiclever/www/behaviors/frontend/home/home.feature:Weekly rhythm demo visible
    Then('I see text "Last 7 days"', () => {
      cleanup();
      render(<HomeContent />);
      expect(screen.getByText("Last 7 days")).toBeDefined();
    });
  });

  Scenario("All six principles visible", ({ Then, And }) => {
    Then('I see text "Local-first"', () => {
      cleanup();
      render(<HomeContent />);
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
