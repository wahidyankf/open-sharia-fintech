import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { PathManifest } from "../core/schemas";

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { PathCard, CategorySection, ArcGroup } from "./path-card";

afterEach(cleanup);

const manifest: PathManifest = {
  pathId: "careers/interview-ready/example-role",
  arc: "interview-ready",
  title: "Interview-Ready Example Role",
  description: "An interview-first track.",
  courseOrder: ["just-enough-python", "just-enough-bash", "capstone-forge-ready"],
};

describe("PathCard", () => {
  it("is a single <a> wrapping the card content (no link-in-link)", () => {
    render(<PathCard locale="en" manifest={manifest} context="hub" />);

    const link = screen.getByRole("link");
    expect(link.getAttribute("href")).toBe("/en/learn/paths/careers/interview-ready/example-role");
    expect(link.querySelector("a")).toBeNull();
  });

  it("hub context renders the formal path title and description", () => {
    render(<PathCard locale="en" manifest={manifest} context="hub" />);

    expect(screen.getByText("Interview-Ready Example Role")).toBeTruthy();
    expect(screen.getByText("An interview-first track.")).toBeTruthy();
  });

  it("shows a course-count badge derived from courseOrder length by default", () => {
    render(<PathCard locale="en" manifest={manifest} context="hub" />);

    expect(screen.getByText("~3 courses")).toBeTruthy();
  });

  it("omits the course-count badge when showCourseCount is false (pre-manifest skills cards)", () => {
    render(<PathCard locale="en" manifest={manifest} context="hub" showCourseCount={false} />);

    expect(screen.queryByText(/courses/)).toBeNull();
  });

  it("the link's accessible name states the goal and course count", () => {
    render(<PathCard locale="en" manifest={manifest} context="hero" />);

    expect(screen.getByRole("link", { name: /Start the Interview-Ready Example Role path.*3 courses/i })).toBeTruthy();
  });
});

describe("CategorySection", () => {
  it("is a <section aria-labelledby> with a real <h2> heading", () => {
    render(
      <CategorySection id="careers" heading="Careers" strapline="Converging within your role">
        <p>content</p>
      </CategorySection>,
    );

    const heading = screen.getByRole("heading", { level: 2, name: "Careers" });
    const section = heading.closest("section");
    expect(section?.getAttribute("aria-labelledby")).toBe(heading.id);
  });
});

describe("ArcGroup", () => {
  it("renders an <h3> arc heading followed by a <ul> of its children", () => {
    render(
      <ArcGroup arc="interview-ready">
        <li>role card</li>
      </ArcGroup>,
    );

    const heading = screen.getByRole("heading", { level: 3, name: "interview-ready" });
    expect(heading).toBeTruthy();
    expect(screen.getByRole("list").textContent).toContain("role card");
  });
});
