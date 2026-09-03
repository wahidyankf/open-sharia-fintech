import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";

import { Callout } from "../../../../../src/features/content/shell/callout";

afterEach(cleanup);

describe("Callout", () => {
  it("maps type='warning' to the Alert warning variant, not destructive — HIGH-3 fix (contrast)", () => {
    // Regression for swe-ui audit b06d32 Finding 3: `warning` previously mapped to
    // `variant="destructive"` (3.05:1 contrast), instead of the dedicated `warning`
    // variant (6.90:1). Assert on the resolved `data-variant` token, not a screenshot.
    render(<Callout type="warning">Watch out.</Callout>);
    const alert = screen.getByRole("alert");
    expect(alert.getAttribute("data-variant")).toBe("warning");
  });

  it("maps type='info' to the Alert info variant", () => {
    render(<Callout type="info">FYI.</Callout>);
    const alert = screen.getByRole("alert");
    expect(alert.getAttribute("data-variant")).toBe("info");
  });

  it("maps type='tip' to the default variant", () => {
    render(<Callout type="tip">Pro tip.</Callout>);
    const alert = screen.getByRole("alert");
    expect(alert.getAttribute("data-variant")).toBe("default");
  });

  it("unknown types fall back to the default variant", () => {
    render(<Callout type="unknown">Fallback.</Callout>);
    const alert = screen.getByRole("alert");
    expect(alert.getAttribute("data-variant")).toBe("default");
  });

  it.each(["warning", "info", "tip"])(
    "renders the '%s' type icon as decorative (aria-hidden), locking in the current contract",
    (type) => {
      // swe-ui audit b06d32 Finding 4 flagged iconMap icons as missing an explicit
      // aria-hidden="true" prop (unlike hero.tsx/tools-teaser.tsx, which pass it
      // explicitly). Re-validated as FALSE_POSITIVE: lucide-react's Icon primitive
      // (node_modules/lucide-react/dist/esm/Icon.js) already defaults to
      // aria-hidden="true" whenever no children/aria-*/role/title prop is supplied,
      // so the rendered DOM is already correctly hidden from assistive tech. No
      // source fix applied for Finding 4 — this test locks in that already-correct
      // behavior so a future prop addition (e.g. an accidental aria-label) that
      // would silently disable the library default gets caught.
      const { container } = render(<Callout type={type}>Body text.</Callout>);
      const icon = container.querySelector("svg");
      expect(icon).not.toBeNull();
      expect(icon?.getAttribute("aria-hidden")).toBe("true");
    },
  );

  it("renders the children inside AlertDescription", () => {
    render(<Callout type="info">Body text.</Callout>);
    expect(screen.getByText("Body text.")).toBeTruthy();
  });
});
