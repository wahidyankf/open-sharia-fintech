import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

const setOpenMock = vi.fn();

vi.mock("@/features/app-shell/shell/use-mobile-nav-open", () => ({
  useMobileNavOpen: () => ({ open: false, setOpen: setOpenMock }),
}));

// eslint-disable-next-line import/first
import { PathBanner } from "./path-banner";

afterEach(cleanup);

describe("PathBanner (Cycle 2.9 — collapses the rail into the shipped drawer on a phone)", () => {
  it("has an accessible name 'Open path course list — {Path}, course {k} of {N}'", () => {
    render(<PathBanner pathTitle="Python Fundamentals" courseIndex={2} totalCourses={5} />);

    expect(
      screen.getByRole("button", { name: "Open path course list — Python Fundamentals, course 2 of 5" }),
    ).toBeTruthy();
  });

  it("carries aria-expanded and aria-controls, and flips aria-expanded on activation", async () => {
    const { default: userEvent } = await import("@testing-library/user-event");
    const user = userEvent.setup();

    render(<PathBanner pathTitle="Python Fundamentals" courseIndex={2} totalCourses={5} />);

    const button = screen.getByRole("button", { name: /Open path course list/i });
    expect(button.getAttribute("aria-expanded")).toBe("false");
    expect(button.hasAttribute("aria-controls")).toBe(true);

    await user.click(button);
    expect(button.getAttribute("aria-expanded")).toBe("true");
  });

  it("activating the trigger opens the shared mobile nav drawer (single sheet, not a second overlay)", async () => {
    const { default: userEvent } = await import("@testing-library/user-event");
    const user = userEvent.setup();

    render(<PathBanner pathTitle="Python Fundamentals" courseIndex={2} totalCourses={5} />);
    const trigger = screen.getByRole("button", { name: /Open path course list/i });
    await user.click(trigger);

    // Passes the trigger element explicitly (Cycle 3.4 regression fix) — WebKit does not focus a
    // clicked <button> by default, so `document.activeElement` alone is not a reliable stand-in for
    // "the element the reader just activated" (see `use-mobile-nav-open.ts`).
    expect(setOpenMock).toHaveBeenCalledWith(true, trigger);
  });

  it("renders the compact 'on path · course k of N' readout", () => {
    render(<PathBanner pathTitle="Python Fundamentals" courseIndex={2} totalCourses={5} />);

    expect(screen.getByText(/on path/i).textContent).toMatch(/2 of 5/);
  });

  it("is hidden at md: and up (md:hidden) — the rail itself covers that breakpoint", () => {
    const { container } = render(<PathBanner pathTitle="Python Fundamentals" courseIndex={2} totalCourses={5} />);

    expect(container.firstElementChild?.className).toContain("md:hidden");
  });
});
