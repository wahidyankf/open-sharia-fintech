import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { axe } from "vitest-axe";
import { expect } from "vitest";

import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "../../../../src/components/card/card";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/card/card.feature"),
);

function renderCard() {
  return render(
    <Card>
      <CardHeader>
        <CardTitle>Card Title</CardTitle>
        <CardDescription>Card description text</CardDescription>
      </CardHeader>
      <CardContent>Card content here</CardContent>
      <CardFooter>Card footer here</CardFooter>
    </Card>,
  );
}

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders card with header, title, description, content, and footer", ({ When, Then, And }) => {
    let title: HTMLElement;
    let description: HTMLElement;
    let content: HTMLElement;
    let footer: HTMLElement;

    When(
      'the Card is rendered with title "Card Title", description "Card description text", content "Card content here", and footer "Card footer here"',
      () => {
        cleanup();
        renderCard();
        title = screen.getByText("Card Title");
        description = screen.getByText("Card description text");
        content = screen.getByText("Card content here");
        footer = screen.getByText("Card footer here");
      },
    );

    Then('the card title "Card Title" should have data-slot "card-title"', () => {
      expect(title.getAttribute("data-slot")).toBe("card-title");
    });

    And('the card description "Card description text" should have data-slot "card-description"', () => {
      expect(description.getAttribute("data-slot")).toBe("card-description");
    });

    And('the card content "Card content here" should have data-slot "card-content"', () => {
      expect(content.getAttribute("data-slot")).toBe("card-content");
    });

    And('the card footer "Card footer here" should have data-slot "card-footer"', () => {
      expect(footer.getAttribute("data-slot")).toBe("card-footer");
    });
  });

  Scenario("Has no accessibility violations", ({ When, Then }) => {
    let container: HTMLElement;

    When(
      'the Card is rendered with title "Card Title", description "Card description text", content "Card content here", and footer "Card footer here"',
      () => {
        cleanup();
        container = renderCard().container;
      },
    );

    Then("the card should have no accessibility violations", async () => {
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });
});
