import { render, screen, cleanup, fireEvent, act, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { axe } from "vitest-axe";
import { describe, it, expect, afterEach, vi } from "vitest";

import { CopyButton } from "../../../../src/primitives/code-block/copy-button";

/** Installs a mock `navigator.clipboard.writeText` (jsdom lacks it). Returns the spy. */
function stubClipboard(resolves: boolean): ReturnType<typeof vi.fn> {
  const writeText = vi.fn(() => (resolves ? Promise.resolve() : Promise.reject(new Error("denied"))));
  Object.defineProperty(navigator, "clipboard", { value: { writeText }, configurable: true });
  return writeText;
}

function getButton(): HTMLButtonElement {
  return screen.getByRole("button") as HTMLButtonElement;
}

function hasCheckIcon(button: HTMLElement): boolean {
  return button.querySelector(".lucide-check") !== null;
}

function hasCopyIcon(button: HTMLElement): boolean {
  return button.querySelector(".lucide-copy") !== null;
}

describe("CopyButton", () => {
  afterEach(() => {
    cleanup();
    vi.restoreAllMocks();
  });

  // Cycle 1.2
  it("swaps to the success icon and announces via a live region on a resolved copy", async () => {
    stubClipboard(true);
    render(<CopyButton value="npm install" />);

    fireEvent.click(getButton());

    await waitFor(() => expect(hasCheckIcon(getButton())).toBe(true));
    expect(getButton().getAttribute("aria-label")).toBe("Copied");
    expect(screen.getByRole("status").textContent).toBe("Copied");
  });

  // Cycle 1.3
  it("reverts to the resting icon and clears the announcement after the timeout", async () => {
    vi.useFakeTimers();
    stubClipboard(true);
    render(<CopyButton value="npm install" resetMs={2000} />);

    fireEvent.click(getButton());
    await act(async () => {
      await vi.advanceTimersByTimeAsync(0);
    });
    expect(hasCheckIcon(getButton())).toBe(true);
    expect(screen.getByRole("status").textContent).toBe("Copied");

    await act(async () => {
      await vi.advanceTimersByTimeAsync(2000);
    });
    expect(hasCopyIcon(getButton())).toBe(true);
    expect(screen.getByRole("status").textContent).toBe("");

    vi.useRealTimers();
  });

  // Cycle 1.4 — the no-false-success invariant: a rejected write must never show success (Check
  // icon / "Copied" announcement). It now shows an explicit error cue instead of a silent no-op
  // (UWT-004), asserted separately below; here we only guard that it isn't a false success.
  it("never shows a false success when the write rejects", async () => {
    stubClipboard(false);
    render(<CopyButton value="npm install" copiedLabel="Copied" />);

    fireEvent.click(getButton());
    // allow the rejected promise microtask to settle
    await act(async () => {
      await Promise.resolve();
    });

    expect(hasCheckIcon(getButton())).toBe(false);
    expect(getButton().getAttribute("aria-label")).not.toBe("Copied");
    expect(screen.getByRole("status").textContent).not.toBe("Copied");
  });

  // UWT-004 — a rejected write gives the visitor an explicit failure cue (error icon + label +
  // polite announcement) rather than appearing to do nothing.
  it("shows an error cue and announces it when the write rejects", async () => {
    stubClipboard(false);
    render(<CopyButton value="npm install" errorLabel="Copy failed" />);

    fireEvent.click(getButton());
    await waitFor(() => expect(getButton().querySelector(".lucide-x")).not.toBeNull());

    expect(getButton().getAttribute("aria-label")).toBe("Copy failed");
    expect(getButton().getAttribute("title")).toBe("Copy failed");
    expect(screen.getByRole("status").textContent).toBe("Copy failed");
  });

  // Cycle 1.5
  it("copies its value when operated by the keyboard (Enter)", async () => {
    // `userEvent.setup()` installs its own `navigator.clipboard` stub, so create the user session
    // FIRST and install our spy AFTER, so the button's `copy()` calls the spy we assert on.
    const user = userEvent.setup();
    const writeText = stubClipboard(true);
    render(<CopyButton value="npm install" />);

    getButton().focus();
    await user.keyboard("{Enter}");

    expect(writeText).toHaveBeenCalledWith("npm install");
  });

  // Cycle 1.6
  it("exposes the default accessible name 'Copy'", () => {
    stubClipboard(true);
    render(<CopyButton value="npm install" />);

    expect(screen.getByRole("button", { name: "Copy" })).toBeTruthy();
  });

  // Cycle 1.7
  it("uses a localized accessible name when copyLabel is overridden", () => {
    stubClipboard(true);
    render(<CopyButton value="npm install" copyLabel="Salin" />);

    expect(screen.getByRole("button", { name: "Salin" })).toBeTruthy();
  });

  // Cycle 1.8
  it("has no accessibility violations in the resting state", async () => {
    stubClipboard(true);
    const { container } = render(<CopyButton value="npm install" />);

    const results = await axe(container);
    expect(results).toHaveNoViolations();
  });

  // Cycle 1.9
  it("meets the minimum target size (icon-sm = size-8 = 32 CSS px >= 24)", () => {
    stubClipboard(true);
    render(<CopyButton value="npm install" />);
    const button = getButton();

    // jsdom performs no layout (offsetWidth is 0), so the target size is asserted through the
    // size class the Button primitive applies: `size-8` = 2rem = 32 CSS px, clearing WCAG 2.5.8's
    // 24x24 minimum.
    expect(button.getAttribute("data-size")).toBe("icon-sm");
    expect(button.className).toContain("size-8");
    const sizePx = 32; // size-8
    expect(sizePx).toBeGreaterThanOrEqual(24);
  });

  it("merges a passthrough className onto the button", () => {
    stubClipboard(true);
    render(<CopyButton value="x" className="my-custom-class" />);
    expect(getButton().className).toContain("my-custom-class");
  });
});
