import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { SkipLink } from "../../../../../src/features/app-shell/shell/skip-link";

afterEach(cleanup);

// Gherkin (binds): "Skip-to-content link is translated in the ID locale"
describe("SkipLink", () => {
  it("renders Indonesian skip-to-content text for locale=id", () => {
    render(<SkipLink locale="id" />);
    expect(screen.getByRole("link", { name: "Langsung ke konten" })).toBeTruthy();
  });

  it("renders English skip-to-content text for locale=en", () => {
    render(<SkipLink locale="en" />);
    expect(screen.getByRole("link", { name: "Skip to content" })).toBeTruthy();
  });

  // UWT-005: activating the link must move focus to #main-content (not just scroll it into view), so
  // the next Tab continues from the main content instead of dumping the user back into the header.
  it("moves keyboard focus to #main-content when activated", () => {
    const main = document.createElement("main");
    main.id = "main-content";
    main.tabIndex = -1;
    document.body.appendChild(main);

    render(<SkipLink locale="en" />);
    fireEvent.click(screen.getByRole("link", { name: "Skip to content" }));

    expect(document.activeElement).toBe(main);
    main.remove();
  });
});
