import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { MobileNavOpenProvider } from "../../../../../src/features/app-shell/shell/mobile-nav-open-provider";
import { useMobileNavOpen } from "../../../../../src/features/app-shell/shell/use-mobile-nav-open";

afterEach(cleanup);

function Probe() {
  const { open, setOpen } = useMobileNavOpen();
  return (
    <div>
      <span data-testid="open-state">{String(open)}</span>
      <button type="button" onClick={() => setOpen(true)}>
        open
      </button>
    </div>
  );
}

describe("MobileNavOpenProvider / useMobileNavOpen", () => {
  it("defaults to closed outside a provider", () => {
    render(<Probe />);
    expect(screen.getByTestId("open-state").textContent).toBe("false");
  });

  it("shares open state between two consumers under the same provider (Cycle 2.9 — single sheet, single state)", async () => {
    const { default: userEvent } = await import("@testing-library/user-event");
    const user = userEvent.setup();

    render(
      <MobileNavOpenProvider>
        <Probe />
        <Probe />
      </MobileNavOpenProvider>,
    );

    const states = screen.getAllByTestId("open-state");
    expect(states[0]?.textContent).toBe("false");
    expect(states[1]?.textContent).toBe("false");

    const buttons = screen.getAllByRole("button", { name: "open" });
    await user.click(buttons[0]!);

    for (const state of screen.getAllByTestId("open-state")) {
      expect(state.textContent).toBe("true");
    }
  });
});
