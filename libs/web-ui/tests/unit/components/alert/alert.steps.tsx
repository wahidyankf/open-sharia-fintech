import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { axe } from "vitest-axe";
import { expect } from "vitest";

import { Alert, AlertTitle, AlertDescription } from "../../../../src/components/alert/alert";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/alert/alert.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders default alert with title and description", ({ When, Then, And }) => {
    let alert: HTMLElement;

    When('the Alert is rendered with title "Warning" and description "Something happened"', () => {
      cleanup();
      render(
        <Alert>
          <AlertTitle>Warning</AlertTitle>
          <AlertDescription>Something happened</AlertDescription>
        </Alert>,
      );
      alert = screen.getByRole("alert");
    });

    Then('an element with role "alert" should be present', () => {
      expect(alert).toBeDefined();
    });

    And('the alert title "Warning" should be present', () => {
      expect(alert.textContent).toContain("Warning");
    });

    And('the alert description "Something happened" should be present', () => {
      expect(alert.textContent).toContain("Something happened");
    });
  });

  Scenario("Renders destructive variant", ({ When, Then }) => {
    let alert: HTMLElement;

    When('the Alert is rendered with variant "destructive" and content "Error"', () => {
      cleanup();
      render(<Alert variant="destructive">Error</Alert>);
      alert = screen.getByRole("alert");
    });

    Then('the alert element should contain the class "text-destructive"', () => {
      expect(alert.className).toContain("text-destructive");
    });
  });

  Scenario("Has no accessibility violations", ({ When, Then }) => {
    let container: HTMLElement;

    When('the Alert is rendered with title "Warning" and description "Something happened"', () => {
      cleanup();
      container = render(
        <Alert>
          <AlertTitle>Warning</AlertTitle>
          <AlertDescription>Something happened</AlertDescription>
        </Alert>,
      ).container;
    });

    Then("the alert should have no accessibility violations", async () => {
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  Scenario("Renders variant success", ({ When, Then }) => {
    let alert: HTMLElement;

    When('I render an Alert with variant "success"', () => {
      cleanup();
      render(<Alert variant="success">Success content</Alert>);
      alert = screen.getByRole("alert");
    });

    Then('the alert should have data-variant "success"', () => {
      expect(alert.getAttribute("data-variant")).toBe("success");
    });
  });

  Scenario("Renders variant warning", ({ When, Then }) => {
    let alert: HTMLElement;

    When('I render an Alert with variant "warning"', () => {
      cleanup();
      render(<Alert variant="warning">Warning content</Alert>);
      alert = screen.getByRole("alert");
    });

    Then('the alert should have data-variant "warning"', () => {
      expect(alert.getAttribute("data-variant")).toBe("warning");
    });
  });

  Scenario("Renders variant info", ({ When, Then }) => {
    let alert: HTMLElement;

    When('I render an Alert with variant "info"', () => {
      cleanup();
      render(<Alert variant="info">Info content</Alert>);
      alert = screen.getByRole("alert");
    });

    Then('the alert should have data-variant "info"', () => {
      expect(alert.getAttribute("data-variant")).toBe("info");
    });
  });
});
