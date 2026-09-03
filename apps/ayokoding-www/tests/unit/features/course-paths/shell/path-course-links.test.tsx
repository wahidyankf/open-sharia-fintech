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
import { PathCourseLinks } from "../../../../../src/features/course-paths/shell/path-course-links";

afterEach(cleanup);

describe("PathCourseLinks", () => {
  it("renders one badge link per path, to the path landing page, carrying the path context", () => {
    render(
      <PathCourseLinks locale="en" paths={[{ pathId: "skills/python-fundamentals", title: "Python Fundamentals" }]} />,
    );

    expect(screen.getByRole("link", { name: "Python Fundamentals" }).getAttribute("href")).toBe(
      "/en/learn/paths/skills/python-fundamentals?path=skills/python-fundamentals",
    );
  });

  // Two fixture manifests sharing a course ID — the multi-badge case (Cycle 2.5's RED note).
  it("renders one badge for every path that includes the course, sharing a course ID across two manifests", () => {
    render(
      <PathCourseLinks
        locale="en"
        paths={[
          { pathId: "skills/python-fundamentals", title: "Python Fundamentals" },
          { pathId: "careers/interview-ready/software-engineer", title: "Interview-Ready Software Engineer" },
        ]}
      />,
    );

    expect(screen.getByRole("link", { name: "Python Fundamentals" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "Interview-Ready Software Engineer" })).toBeTruthy();
    expect(screen.getAllByRole("link")).toHaveLength(2);
  });

  it("renders nothing when the course belongs to no path", () => {
    const { container } = render(<PathCourseLinks locale="en" paths={[]} />);

    expect(container.textContent).toBe("");
  });
});
