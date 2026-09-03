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
import { PrerequisiteList } from "../../../../../src/features/course-paths/shell/prerequisite-list";

afterEach(cleanup);

const prerequisites = [{ title: "Version Control and Git", slug: "learn/courses/version-control-and-git" }];

describe("PrerequisiteList", () => {
  it("renders each declared prerequisite as a link to its canonical URL — canonical (no path) view", () => {
    render(<PrerequisiteList locale="en" prerequisites={prerequisites} />);

    expect(screen.getByRole("link", { name: "Version Control and Git" }).getAttribute("href")).toBe(
      "/en/learn/courses/version-control-and-git",
    );
  });

  it("renders each declared prerequisite as a link to its canonical URL — path-aware view, preserving the path context", () => {
    // EWT-002 fix: `pathId` is now carried per-item (set only when that prerequisite is itself a
    // member of the active manifest) rather than as a blanket prop applied to every prerequisite.
    const pathAwarePrerequisites = [
      {
        title: "Version Control and Git",
        slug: "learn/courses/version-control-and-git",
        pathId: "skills/python-fundamentals",
      },
    ];
    render(<PrerequisiteList locale="en" prerequisites={pathAwarePrerequisites} />);

    expect(screen.getByRole("link", { name: "Version Control and Git" }).getAttribute("href")).toBe(
      "/en/learn/courses/version-control-and-git?path=skills/python-fundamentals",
    );
  });

  it("renders nothing at all — not an empty 'Prerequisites' label — for a course with no prerequisites", () => {
    const { container } = render(<PrerequisiteList locale="en" prerequisites={[]} />);

    expect(container.textContent).toBe("");
  });

  it("renders multiple declared prerequisites in declaration order", () => {
    const many = [
      { title: "Version Control and Git", slug: "learn/courses/version-control-and-git" },
      { title: "Just Enough Python", slug: "learn/courses/just-enough-python" },
    ];
    render(<PrerequisiteList locale="en" prerequisites={many} />);

    const links = screen.getAllByRole("link");
    expect(links.map((l) => l.textContent)).toEqual(["Version Control and Git", "Just Enough Python"]);
  });

  it("localizes the 'Prerequisites' heading and landmark label on the id locale (DWT-003 fix, phase-5 rule-15 design-tester retest)", () => {
    render(<PrerequisiteList locale="id" prerequisites={prerequisites} />);

    expect(screen.getByRole("heading", { level: 2, name: "Prasyarat" })).toBeTruthy();
    expect(screen.getByRole("navigation", { name: "Prasyarat" })).toBeTruthy();
  });
});
