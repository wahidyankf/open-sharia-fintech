import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup } from "@testing-library/react";
import { axe } from "vitest-axe";
import { expect } from "vitest";

import { Button } from "../../../../src/components/button/button";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviours/button/button.feature"),
);

describeFeature(feature, ({ Scenario }) => {
  Scenario("Renders with default variant and size", ({ When, Then, And }) => {
    let button: HTMLElement;

    When('the Button is rendered with label "Click me"', () => {
      cleanup();
      render(<Button>Click me</Button>);
      button = screen.getByRole("button", { name: "Click me" });
    });

    Then("the button element should be present in the document", () => {
      expect(button.textContent).toBe("Click me");
    });

    And('the button should have data-variant "default"', () => {
      expect(button.getAttribute("data-variant")).toBe("default");
    });

    And('the button should have data-size "default"', () => {
      expect(button.getAttribute("data-size")).toBe("default");
    });
  });

  Scenario("Renders variant default", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with variant "default" and label "default"', () => {
      cleanup();
      render(<Button variant="default">default</Button>);
      button = screen.getByRole("button", { name: "default" });
    });

    Then('the button element with label "default" should be present', () => {
      expect(button.getAttribute("data-variant")).toBe("default");
    });
  });

  Scenario("Renders variant destructive", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with variant "destructive" and label "destructive"', () => {
      cleanup();
      render(<Button variant="destructive">destructive</Button>);
      button = screen.getByRole("button", { name: "destructive" });
    });

    Then('the button element with label "destructive" should be present', () => {
      expect(button.getAttribute("data-variant")).toBe("destructive");
    });
  });

  Scenario("Renders variant outline", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with variant "outline" and label "outline"', () => {
      cleanup();
      render(<Button variant="outline">outline</Button>);
      button = screen.getByRole("button", { name: "outline" });
    });

    Then('the button element with label "outline" should be present', () => {
      expect(button.getAttribute("data-variant")).toBe("outline");
    });
  });

  Scenario("Renders variant secondary", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with variant "secondary" and label "secondary"', () => {
      cleanup();
      render(<Button variant="secondary">secondary</Button>);
      button = screen.getByRole("button", { name: "secondary" });
    });

    Then('the button element with label "secondary" should be present', () => {
      expect(button.getAttribute("data-variant")).toBe("secondary");
    });
  });

  Scenario("Renders variant ghost", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with variant "ghost" and label "ghost"', () => {
      cleanup();
      render(<Button variant="ghost">ghost</Button>);
      button = screen.getByRole("button", { name: "ghost" });
    });

    Then('the button element with label "ghost" should be present', () => {
      expect(button.getAttribute("data-variant")).toBe("ghost");
    });
  });

  Scenario("Renders variant link", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with variant "link" and label "link"', () => {
      cleanup();
      render(<Button variant="link">link</Button>);
      button = screen.getByRole("button", { name: "link" });
    });

    Then('the button element with label "link" should be present', () => {
      expect(button.getAttribute("data-variant")).toBe("link");
    });
  });

  Scenario("Renders size default", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with size "default" and aria-label "button-default"', () => {
      cleanup();
      render(
        <Button size="default" aria-label="button-default">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-default" });
    });

    Then('the button element with aria-label "button-default" should be present', () => {
      expect(button.getAttribute("data-size")).toBe("default");
    });
  });

  Scenario("Renders size xs", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with size "xs" and aria-label "button-xs"', () => {
      cleanup();
      render(
        <Button size="xs" aria-label="button-xs">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-xs" });
    });

    Then('the button element with aria-label "button-xs" should be present', () => {
      expect(button.getAttribute("data-size")).toBe("xs");
    });
  });

  Scenario("Renders size sm", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with size "sm" and aria-label "button-sm"', () => {
      cleanup();
      render(
        <Button size="sm" aria-label="button-sm">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-sm" });
    });

    Then('the button element with aria-label "button-sm" should be present', () => {
      expect(button.getAttribute("data-size")).toBe("sm");
    });
  });

  Scenario("Renders size lg", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with size "lg" and aria-label "button-lg"', () => {
      cleanup();
      render(
        <Button size="lg" aria-label="button-lg">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-lg" });
    });

    Then('the button element with aria-label "button-lg" should be present', () => {
      expect(button.getAttribute("data-size")).toBe("lg");
    });
  });

  Scenario("Renders size icon", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with size "icon" and aria-label "button-icon"', () => {
      cleanup();
      render(
        <Button size="icon" aria-label="button-icon">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-icon" });
    });

    Then('the button element with aria-label "button-icon" should be present', () => {
      expect(button.getAttribute("data-size")).toBe("icon");
    });
  });

  Scenario("Renders size icon-xs", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with size "icon-xs" and aria-label "button-icon-xs"', () => {
      cleanup();
      render(
        <Button size="icon-xs" aria-label="button-icon-xs">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-icon-xs" });
    });

    Then('the button element with aria-label "button-icon-xs" should be present', () => {
      expect(button.getAttribute("data-size")).toBe("icon-xs");
    });
  });

  Scenario("Renders size icon-sm", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with size "icon-sm" and aria-label "button-icon-sm"', () => {
      cleanup();
      render(
        <Button size="icon-sm" aria-label="button-icon-sm">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-icon-sm" });
    });

    Then('the button element with aria-label "button-icon-sm" should be present', () => {
      expect(button.getAttribute("data-size")).toBe("icon-sm");
    });
  });

  Scenario("Renders size icon-lg", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered with size "icon-lg" and aria-label "button-icon-lg"', () => {
      cleanup();
      render(
        <Button size="icon-lg" aria-label="button-icon-lg">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-icon-lg" });
    });

    Then('the button element with aria-label "button-icon-lg" should be present', () => {
      expect(button.getAttribute("data-size")).toBe("icon-lg");
    });
  });

  Scenario("Supports disabled state", ({ When, Then }) => {
    let button: HTMLElement;

    When('the Button is rendered as disabled with label "Disabled"', () => {
      cleanup();
      render(<Button disabled>Disabled</Button>);
      button = screen.getByRole("button", { name: "Disabled" });
    });

    Then("the button element should have the disabled attribute", () => {
      expect(button.hasAttribute("disabled")).toBe(true);
    });
  });

  Scenario("Renders as child element when asChild is true", ({ When, Then, And }) => {
    let link: HTMLElement;

    When('the Button is rendered with asChild wrapping an anchor to "/test" with label "Link Button"', () => {
      cleanup();
      render(
        <Button asChild>
          <a href="/test">Link Button</a>
        </Button>,
      );
      link = screen.getByRole("link", { name: "Link Button" });
    });

    Then('a link element with label "Link Button" should be present', () => {
      expect(link.textContent).toBe("Link Button");
    });

    And('the link should have href "/test"', () => {
      expect(link.getAttribute("href")).toBe("/test");
    });
  });

  Scenario("Has no accessibility violations", ({ When, Then }) => {
    let container: HTMLElement;

    When('the Button is rendered with label "Accessible Button"', () => {
      cleanup();
      container = render(<Button>Accessible Button</Button>).container;
    });

    Then("the button should have no accessibility violations", async () => {
      const results = await axe(container);
      expect(results).toHaveNoViolations();
    });
  });

  Scenario("Renders variant teal", ({ When, Then }) => {
    let button: HTMLElement;

    When('I render a Button with variant "teal"', () => {
      cleanup();
      render(<Button variant="teal">teal</Button>);
      button = screen.getByRole("button", { name: "teal" });
    });

    Then('the button should have data-variant "teal"', () => {
      expect(button.getAttribute("data-variant")).toBe("teal");
    });
  });

  Scenario("Renders variant sage", ({ When, Then }) => {
    let button: HTMLElement;

    When('I render a Button with variant "sage"', () => {
      cleanup();
      render(<Button variant="sage">sage</Button>);
      button = screen.getByRole("button", { name: "sage" });
    });

    Then('the button should have data-variant "sage"', () => {
      expect(button.getAttribute("data-variant")).toBe("sage");
    });
  });

  Scenario("Renders size xl", ({ When, Then }) => {
    let button: HTMLElement;

    When('I render a Button with size "xl"', () => {
      cleanup();
      render(
        <Button size="xl" aria-label="button-xl">
          X
        </Button>,
      );
      button = screen.getByRole("button", { name: "button-xl" });
    });

    Then('the button should have data-size "xl"', () => {
      expect(button.getAttribute("data-size")).toBe("xl");
    });
  });
});
