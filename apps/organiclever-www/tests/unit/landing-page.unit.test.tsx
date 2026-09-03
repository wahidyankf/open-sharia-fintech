import { describe, it, expect, afterEach } from "vitest";
import { render, screen, cleanup, fireEvent } from "@testing-library/react";

import { LandingPage } from "@/features/home/components/landing-page";

describe("LandingPage", () => {
  afterEach(() => {
    cleanup();
  });

  it('navigates to "/app/home" when the primary call-to-action is clicked', () => {
    render(<LandingPage />);

    // jsdom does not implement real navigation, and its `location.href`
    // accessor is non-configurable, so the click handler's
    // `window.location.href = "/app/home"` assignment is observed by
    // swapping in a plain writable stand-in for the whole `location` object.
    const originalLocation = window.location;
    const stub = { href: "" } as unknown as Location;
    Object.defineProperty(window, "location", { configurable: true, writable: true, value: stub });

    try {
      fireEvent.click(screen.getByRole("button", { name: /Open the app/i }));

      expect(stub.href).toBe("/app/home");
    } finally {
      Object.defineProperty(window, "location", { configurable: true, writable: true, value: originalLocation });
    }
  });
});
