import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { SectionCard } from "../../../../../src/features/content/shell/section-card";

afterEach(cleanup);

describe("SectionCard", () => {
  it("renders the section title as a link to its content URL", () => {
    render(<SectionCard href="/en/learn" title="Software Engineering" description="Languages, architecture." />);
    const link = screen.getByRole("link", { name: /Software Engineering/ });
    expect(link.getAttribute("href")).toBe("/en/learn");
  });

  it("renders the description blurb", () => {
    render(<SectionCard href="/en/learn" title="Software Engineering" description="Languages, architecture." />);
    expect(screen.getByText("Languages, architecture.")).toBeTruthy();
  });

  it("reuses the shared Card token surface (rounded border)", () => {
    const { container } = render(<SectionCard href="/en/learn" title="Learn" description="x" />);
    // Card primitive applies the rounded-xl border bg-card token surface.
    expect(container.querySelector('[data-slot="card"]')).not.toBeNull();
  });

  it("renders the meta line with a decorative (aria-hidden) trailing arrow, locking in the current contract", () => {
    // swe-ui audit b06d32 Finding 4 flagged the trailing ArrowRight icon as missing an
    // explicit aria-hidden="true" prop (unlike hero.tsx/tools-teaser.tsx, which pass it
    // explicitly for the identical icon). Re-validated as FALSE_POSITIVE: lucide-react's
    // Icon primitive already defaults to aria-hidden="true" whenever no children/aria-*/
    // role/title prop is supplied, so the rendered DOM is already correctly hidden from
    // assistive tech. No source fix applied — this test locks in that already-correct
    // behaviour. Also fills a previously-uncovered code path: no prior test in this file
    // rendered SectionCard with the `meta` prop supplied.
    const { container } = render(<SectionCard href="/en/learn" title="Learn" description="x" meta="12 topics" />);
    expect(screen.getByText("12 topics")).toBeTruthy();
    const icon = container.querySelector("svg");
    expect(icon).not.toBeNull();
    expect(icon?.getAttribute("aria-hidden")).toBe("true");
  });
});
