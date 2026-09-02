import path from "path";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { render, screen, cleanup, fireEvent, act, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { axe } from "vitest-axe";
import { expect, vi } from "vitest";

import { CopyButton } from "../../../../src/primitives/code-block/copy-button";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../../specs/libs/web-ui/behaviors/code-block/copy-button.feature"),
);

/** Installs a mock `navigator.clipboard.writeText` (jsdom lacks it). Returns the spy. */
function stubClipboard(resolves: boolean): ReturnType<typeof vi.fn> {
  const writeText = vi.fn(() => (resolves ? Promise.resolve() : Promise.reject(new Error("denied"))));
  Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
  return writeText;
}

function getButton(): HTMLButtonElement {
  return screen.getByRole("button") as HTMLButtonElement;
}

describeFeature(feature, ({ Scenario }) => {
  Scenario("Clicking the copy button writes its value to the clipboard", ({ Given, When, Then }) => {
    let writeText: ReturnType<typeof vi.fn>;

    Given('a CopyButton rendered with the value "npm install"', () => {
      // render + click happen together in the When step (steps run as sequential tests)
    });

    When("the user clicks the button", () => {
      cleanup();
      writeText = stubClipboard(true);
      render(<CopyButton value="npm install" />);
      fireEvent.click(getButton());
    });

    Then('the clipboard receives the exact text "npm install"', () => {
      expect(writeText).toHaveBeenCalledWith("npm install");
    });
  });

  Scenario(
    "A successful copy swaps to the success icon and announces via a live region",
    ({ Given, When, Then, And }) => {
      let showsCheck = false;
      let announced = "";

      Given("a CopyButton rendered with a value and a stubbed clipboard that resolves", () => {
        // render + click happen together in the When step
      });

      When("the user clicks the button", async () => {
        cleanup();
        stubClipboard(true);
        render(<CopyButton value="npm install" copiedLabel="Copied" />);
        fireEvent.click(getButton());
        await waitFor(() => expect(getButton().querySelector(".lucide-check")).not.toBeNull());
        showsCheck = getButton().querySelector(".lucide-check") !== null;
        announced = screen.getByRole("status").textContent ?? "";
      });

      Then("the button shows the success (Check) icon", () => {
        expect(showsCheck).toBe(true);
      });

      And("a polite live region announces the copied label", () => {
        expect(announced).toBe("Copied");
      });
    },
  );

  Scenario("The success state reverts to the resting state after the timeout", ({ Given, When, Then, And }) => {
    let showsCopy = false;
    let announced = "unset";

    Given("a CopyButton that has just shown its success state", () => {
      // render + copy + timeout happen together in the When step
    });

    When("the revert timeout elapses", async () => {
      cleanup();
      vi.useFakeTimers();
      stubClipboard(true);
      render(<CopyButton value="npm install" resetMs={2000} />);
      fireEvent.click(getButton());
      await act(async () => {
        await vi.advanceTimersByTimeAsync(0);
      });
      // precondition: success is showing
      expect(getButton().querySelector(".lucide-check")).not.toBeNull();
      await act(async () => {
        await vi.advanceTimersByTimeAsync(2000);
      });
      showsCopy = getButton().querySelector(".lucide-copy") !== null;
      announced = screen.getByRole("status").textContent ?? "";
      vi.useRealTimers();
    });

    Then("the button shows the resting (Copy) icon again", () => {
      expect(showsCopy).toBe(true);
    });

    And("the live region no longer announces the copied label", () => {
      expect(announced).toBe("");
    });
  });

  Scenario("A failed clipboard write does not show a false success state", ({ Given, When, Then, And }) => {
    let showsCheck = false;
    let announced = "unset";

    Given("a CopyButton rendered with a stubbed clipboard that rejects", () => {
      // render + click happen together in the When step
    });

    When("the user clicks the button", async () => {
      cleanup();
      stubClipboard(false);
      render(<CopyButton value="npm install" copiedLabel="Copied" />);
      fireEvent.click(getButton());
      await act(async () => {
        await Promise.resolve();
      });
      showsCheck = getButton().querySelector(".lucide-check") !== null;
      announced = screen.getByRole("status").textContent ?? "";
    });

    Then("the button does not show the success (Check) icon", () => {
      // No false success: the rejected write never flips to the Check icon (it shows the error cue
      // instead — asserted by the dedicated error scenario).
      expect(showsCheck).toBe(false);
    });

    And("no copied confirmation is announced", () => {
      // The live region may carry the error label, but never the copied confirmation.
      expect(announced).not.toBe("Copied");
    });
  });

  Scenario("The copy button is operable by keyboard", ({ Given, When, Then }) => {
    let writeText: ReturnType<typeof vi.fn>;

    Given("a CopyButton is focused", () => {
      // render + focus + keypress happen together in the When step
    });

    When("the user presses Enter", async () => {
      cleanup();
      // create the user session before installing our spy so `userEvent`'s own clipboard stub
      // doesn't shadow the spy the button calls
      const user = userEvent.setup();
      writeText = stubClipboard(true);
      render(<CopyButton value="npm install" />);
      getButton().focus();
      await user.keyboard("{Enter}");
    });

    Then("the clipboard receives the button's value", () => {
      expect(writeText).toHaveBeenCalledWith("npm install");
    });
  });

  Scenario("The copy button exposes an accessible name", ({ Given, When, Then }) => {
    let accessibleName: string | null = null;

    Given("a CopyButton rendered with the default labels", () => {
      // render + inspection happen together in the When step
    });

    When("the accessibility tree is inspected", () => {
      cleanup();
      stubClipboard(true);
      render(<CopyButton value="npm install" />);
      accessibleName = getButton().getAttribute("aria-label");
    });

    Then('the button has an accessible name of "Copy"', () => {
      expect(accessibleName).toBe("Copy");
    });
  });

  Scenario("The copy button's accessible name can be localized", ({ Given, When, Then }) => {
    let accessibleName: string | null = null;

    Given('a CopyButton rendered with copyLabel "Salin"', () => {
      // render + inspection happen together in the When step
    });

    When("the accessibility tree is inspected", () => {
      cleanup();
      stubClipboard(true);
      render(<CopyButton value="npm install" copyLabel="Salin" />);
      accessibleName = getButton().getAttribute("aria-label");
    });

    Then('the button has an accessible name of "Salin"', () => {
      expect(accessibleName).toBe("Salin");
    });
  });

  Scenario("The copy button has no accessibility violations", ({ Given, When, Then }) => {
    let results: Awaited<ReturnType<typeof axe>>;

    Given("a CopyButton is rendered in its resting state", () => {
      // render + scan happen together in the When step
    });

    When("an automated accessibility scan runs", async () => {
      cleanup();
      stubClipboard(true);
      const { container } = render(<CopyButton value="npm install" />);
      results = await axe(container);
    });

    Then("no accessibility violations are reported", () => {
      expect(results).toHaveNoViolations();
    });
  });

  Scenario("The copy button meets the minimum target size", ({ Given, When, Then }) => {
    let dataSize: string | null = null;
    let className = "";

    Given("a CopyButton rendered at its default size", () => {
      // render + measurement happen together in the When step
    });

    When("its rendered box is measured", () => {
      cleanup();
      stubClipboard(true);
      render(<CopyButton value="npm install" />);
      dataSize = getButton().getAttribute("data-size");
      className = getButton().className;
    });

    Then("both dimensions are at least 24 CSS pixels", () => {
      // jsdom performs no layout, so the size is asserted through the `icon-sm`/`size-8` class the
      // Button primitive applies: size-8 = 2rem = 32 CSS px, clearing WCAG 2.5.8's 24x24 minimum.
      expect(dataSize).toBe("icon-sm");
      expect(className).toContain("size-8");
    });
  });

  Scenario("Re-clicking during the success window resets the revert timer", ({ Given, When, Then, And }) => {
    let stillSuccessPastFirstWindow = false;
    let revertedAfterSecondWindow = false;

    Given("a CopyButton has just shown its success state from a first click", () => {
      // first click + re-click + timer advances all happen together in the When step
    });

    When("the user clicks the button again before the revert timeout elapses", async () => {
      cleanup();
      vi.useFakeTimers();
      stubClipboard(true);
      render(<CopyButton value="npm install" resetMs={2000} />);
      fireEvent.click(getButton());
      await act(async () => {
        await vi.advanceTimersByTimeAsync(0);
      });
      // t=1000ms: still within the first success window; re-click resets the pending revert.
      await act(async () => {
        await vi.advanceTimersByTimeAsync(1000);
      });
      fireEvent.click(getButton());
      await act(async () => {
        await vi.advanceTimersByTimeAsync(0);
      });
      // t=2500ms overall — past the FIRST click's 2000ms window. Still success ⇒ the first timer was
      // cleared, not left to fire independently.
      await act(async () => {
        await vi.advanceTimersByTimeAsync(1500);
      });
      stillSuccessPastFirstWindow = getButton().querySelector(".lucide-check") !== null;
      // Advance to 2000ms after the SECOND click ⇒ now it reverts.
      await act(async () => {
        await vi.advanceTimersByTimeAsync(500);
      });
      revertedAfterSecondWindow = getButton().querySelector(".lucide-copy") !== null;
      vi.useRealTimers();
    });

    Then("the button remains in the success (Check) state", () => {
      expect(stillSuccessPastFirstWindow).toBe(true);
    });

    And("the revert timeout is measured from the second click, not the first", () => {
      expect(revertedAfterSecondWindow).toBe(true);
    });
  });

  Scenario("A retry after a failed clipboard write succeeds normally", ({ Given, When, Then, And }) => {
    let showsCheck = false;
    let announced = "";

    Given("a CopyButton whose previous click failed to write to the clipboard", () => {
      // the failing first click + the resolving retry happen together in the When step
    });

    When("the user clicks the button again and the clipboard write resolves", async () => {
      cleanup();
      // First attempt rejects → error state, no false success.
      stubClipboard(false);
      render(<CopyButton value="npm install" copiedLabel="Copied" />);
      fireEvent.click(getButton());
      await act(async () => {
        await Promise.resolve();
      });
      // Retry now resolves.
      stubClipboard(true);
      fireEvent.click(getButton());
      await waitFor(() => expect(getButton().querySelector(".lucide-check")).not.toBeNull());
      showsCheck = getButton().querySelector(".lucide-check") !== null;
      announced = screen.getByRole("status").textContent ?? "";
    });

    Then("the button shows the success (Check) icon", () => {
      expect(showsCheck).toBe(true);
    });

    And("a polite live region announces the copied label", () => {
      expect(announced).toBe("Copied");
    });
  });

  Scenario("The copy button is operable by keyboard via the Space key", ({ Given, When, Then }) => {
    let writeText: ReturnType<typeof vi.fn>;

    Given("a CopyButton is focused", () => {
      // render + focus + keypress happen together in the When step
    });

    When("the user presses Space", async () => {
      cleanup();
      // create the user session before installing our spy so `userEvent`'s own clipboard stub
      // doesn't shadow the spy the button calls
      const user = userEvent.setup();
      writeText = stubClipboard(true);
      render(<CopyButton value="npm install" />);
      getButton().focus();
      await user.keyboard(" ");
    });

    Then("the clipboard receives the button's value", () => {
      expect(writeText).toHaveBeenCalledWith("npm install");
    });
  });

  Scenario("A failed clipboard write shows an error cue and announces it", ({ Given, When, Then, And }) => {
    let showsX = false;
    let announced = "";

    Given("a CopyButton rendered with a stubbed clipboard that rejects", () => {
      // render + click happen together in the When step
    });

    When("the user clicks the button", async () => {
      cleanup();
      stubClipboard(false);
      render(<CopyButton value="npm install" errorLabel="Copy failed" />);
      fireEvent.click(getButton());
      await waitFor(() => expect(getButton().querySelector(".lucide-x")).not.toBeNull());
      showsX = getButton().querySelector(".lucide-x") !== null;
      announced = screen.getByRole("status").textContent ?? "";
    });

    Then("the button shows the error (X) icon", () => {
      expect(showsX).toBe(true);
    });

    And("a polite live region announces the error label", () => {
      expect(announced).toBe("Copy failed");
    });
  });

  Scenario("The copy button exposes a native tooltip title", ({ Given, When, Then }) => {
    let title: string | null = null;
    let accessibleName: string | null = null;

    Given("a CopyButton rendered with the default labels", () => {
      // render + inspection happen together in the When step
    });

    When("the button's attributes are inspected", () => {
      cleanup();
      stubClipboard(true);
      render(<CopyButton value="npm install" />);
      title = getButton().getAttribute("title");
      accessibleName = getButton().getAttribute("aria-label");
    });

    Then("the button carries a title matching its accessible name", () => {
      expect(title).toBe("Copy");
      expect(title).toBe(accessibleName);
    });
  });
});
