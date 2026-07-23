import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

// Mock next/link as a simple <a> tag.
vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// Import after mocks are registered.
// eslint-disable-next-line import/first
import { Breadcrumb } from "./breadcrumb";

afterEach(cleanup);

const segments = [
  { label: "Home", slug: "" },
  { label: "Tools", slug: "tools" },
  { label: "Cost of Living Calculator", slug: "tools/cost-of-living-calculator" },
];

describe("Breadcrumb", () => {
  it("by default excludes the last (current-page) segment", () => {
    render(<Breadcrumb locale="en" slug="tools/cost-of-living-calculator" segments={segments} />);
    // Final segment is not rendered when showCurrent is absent (legacy behaviour).
    expect(screen.queryByText("Cost of Living Calculator")).toBeNull();
    expect(screen.getByRole("link", { name: "Home" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Tools" })).toBeTruthy();
  });

  it("with showCurrent renders the final segment as a non-link aria-current='page' crumb", () => {
    render(<Breadcrumb locale="en" slug="tools/cost-of-living-calculator" segments={segments} showCurrent />);
    const current = screen.getByText("Cost of Living Calculator");
    expect(current.getAttribute("aria-current")).toBe("page");
    // The current crumb must not be a link.
    expect(current.closest("a")).toBeNull();
    // Ancestor segments remain links.
    expect(screen.getByRole("link", { name: "Home" }).getAttribute("href")).toBe("/en");
    expect(screen.getByRole("link", { name: "Tools" }).getAttribute("href")).toBe("/en/tools");
  });

  it("with showCurrent uses ChevronRight separators, never a literal '/'", () => {
    const { container } = render(
      <Breadcrumb locale="en" slug="tools/cost-of-living-calculator" segments={segments} showCurrent />,
    );
    // lucide-react ChevronRight renders an <svg>; one separator between each of 3 crumbs.
    expect(container.querySelectorAll("svg").length).toBe(2);
    expect(container.textContent).not.toContain("/");
  });

  it("ChevronRight separators are decorative (aria-hidden), locking in the current contract", () => {
    // swe-ui audit b06d32 Finding 4 flagged the separator icon as missing an explicit
    // aria-hidden="true" prop. Re-validated as FALSE_POSITIVE: lucide-react's Icon
    // primitive already defaults to aria-hidden="true" whenever no children/aria-*/
    // role/title prop is supplied, so the rendered DOM is already correctly hidden
    // from assistive tech. No source fix applied — this test locks in that
    // already-correct behavior.
    const { container } = render(
      <Breadcrumb locale="en" slug="tools/cost-of-living-calculator" segments={segments} showCurrent />,
    );
    const separators = container.querySelectorAll("svg");
    expect(separators.length).toBeGreaterThan(0);
    separators.forEach((svg) => {
      expect(svg.getAttribute("aria-hidden")).toBe("true");
    });
  });
});

const contentSegments = [
  { label: "Learn", slug: "learn" },
  { label: "Software Engineering", slug: "learn/software-engineering" },
  { label: "Data Structures", slug: "learn/software-engineering/data-structures" },
];

describe("Breadcrumb with explicit href override", () => {
  it("when segment has href field, uses that href instead of computed one — UWT-002 fix", () => {
    const segments = [
      { label: "Home", slug: "" },
      { label: "Browse", slug: "browse", href: "/en/browse" },
      { label: "Learn", slug: "learn" },
    ];
    render(<Breadcrumb locale="en" slug="learn" segments={segments} showCurrent />);
    expect(screen.getByRole("link", { name: "Browse" }).getAttribute("href")).toBe("/en/browse");
    expect(screen.getByRole("link", { name: "Home" }).getAttribute("href")).toBe("/en");
  });
});

describe("Breadcrumb content hrefs", () => {
  it("resolves content ancestor segments through contentUrl (uniform bare join, DD-48)", () => {
    render(
      <Breadcrumb
        locale="en"
        slug="learn/software-engineering/data-structures"
        segments={contentSegments}
        showCurrent
      />,
    );
    // contentUrl() is a uniform bare join post-de-namespacing — no /c/ prefix.
    expect(screen.getByRole("link", { name: "Learn" }).getAttribute("href")).toBe("/en/learn");
    expect(screen.getByRole("link", { name: "Software Engineering" }).getAttribute("href")).toBe(
      "/en/learn/software-engineering",
    );
    // Final segment is non-link aria-current.
    const current = screen.getByText("Data Structures");
    expect(current.getAttribute("aria-current")).toBe("page");
    expect(current.closest("a")).toBeNull();
  });

  it("emits bare hrefs for non-content segments too", () => {
    render(<Breadcrumb locale="en" slug="tools" segments={segments} showCurrent />);
    expect(screen.getByRole("link", { name: "Tools" }).getAttribute("href")).toBe("/en/tools");
  });
});
