import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { axe } from "vitest-axe";
import { expect } from "vitest";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogTrigger,
} from "../../../../src/components/dialog/dialog";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/dialog/dialog.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders dialog with trigger button", ({ When, Then, And }) => {
    let trigger: HTMLElement;

    When('the Dialog is rendered with a trigger labeled "Open"', () => {
      cleanup();
      render(
        <Dialog>
          <DialogTrigger>Open</DialogTrigger>
        </Dialog>,
      );
      trigger = screen.getByText("Open");
    });

    Then('the dialog trigger element with label "Open" should be present', () => {
      expect(trigger.textContent).toBe("Open");
    });

    And('the trigger should have data-slot "dialog-trigger"', () => {
      expect(trigger.getAttribute("data-slot")).toBe("dialog-trigger");
    });
  });

  Scenario("Has no accessibility violations", ({ When, Then }) => {
    let container: HTMLElement;

    When('the Dialog is rendered open with title "Test Dialog"', () => {
      cleanup();
      container = render(
        <Dialog open>
          <DialogContent showCloseButton={false}>
            <DialogHeader>
              <DialogTitle>Test Dialog</DialogTitle>
              <DialogDescription>Dialog description text</DialogDescription>
            </DialogHeader>
          </DialogContent>
        </Dialog>,
      ).container;
    });

    Then("the dialog should have no accessibility violations", async () => {
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });
});
