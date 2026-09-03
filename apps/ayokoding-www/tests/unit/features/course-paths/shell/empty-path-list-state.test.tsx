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
import { EmptyPathListState } from "../../../../../src/features/course-paths/shell/empty-path-list-state";

afterEach(cleanup);

describe("EmptyPathListState (Cycle 3.1a — shared empty state, R7)", () => {
  it("renders a stated 'being written, check back soon' message", () => {
    render(<EmptyPathListState fallbackHref="/en/learn/paths/careers" fallbackLabel="Careers" />);

    expect(screen.getByText(/being written/i)).toBeTruthy();
    expect(screen.getByText(/check back soon/i)).toBeTruthy();
  });

  it("renders a <Link> CTA to the caller-supplied fallback category", () => {
    render(<EmptyPathListState fallbackHref="/en/learn/paths/careers" fallbackLabel="Careers" />);

    const link = screen.getByRole("link", { name: /Careers/i });
    expect(link.getAttribute("href")).toBe("/en/learn/paths/careers");
  });

  it("is not a bare empty <div> — it has real text content and a real landmark role", () => {
    render(<EmptyPathListState fallbackHref="/en/learn/paths/careers" fallbackLabel="Careers" />);

    const status = screen.getByRole("alert");
    expect(status.textContent?.trim().length).toBeGreaterThan(0);
  });

  it("takes no hardcoded 'careers' string — a different fallback renders verbatim", () => {
    render(<EmptyPathListState fallbackHref="/en/learn/paths/skills" fallbackLabel="Skills" />);

    expect(screen.getByRole("link", { name: /Skills/i }).getAttribute("href")).toBe("/en/learn/paths/skills");
    expect(screen.queryByText(/careers/i)).toBeNull();
  });
});
