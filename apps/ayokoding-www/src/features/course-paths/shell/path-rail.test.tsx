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
import { PathRail } from "./path-rail";

afterEach(cleanup);

const manifest: PathManifest = {
  pathId: "skills/python-fundamentals",
  arc: "python-fundamentals",
  title: "Python Fundamentals",
  description: "Learn Python from the ground up.",
  courseOrder: ["version-control-and-git", "just-enough-python", "data-structures-and-algorithms-essentials"],
};

const courseTitles = {
  "version-control-and-git": "Git",
  "just-enough-python": "Just Enough Python",
  "data-structures-and-algorithms-essentials": "Data Structures & Algorithms",
};

describe("PathRail (Cycle 2.8 — Screen 3 Option B)", () => {
  it("is a <nav> whose accessible name is '{Path} course list'", () => {
    render(
      <PathRail locale="en" manifest={manifest} currentCourseId="just-enough-python" courseTitles={courseTitles} />,
    );

    expect(screen.getByRole("navigation", { name: "Python Fundamentals course list" })).toBeTruthy();
  });

  it("renders a semantic <ol> listing every course in manifest order", () => {
    const { container } = render(
      <PathRail locale="en" manifest={manifest} currentCourseId="just-enough-python" courseTitles={courseTitles} />,
    );

    const ol = container.querySelector("ol");
    expect(ol).not.toBeNull();
    const items = ol!.querySelectorAll("li");
    expect(items.length).toBe(3);
    expect(items[0]?.textContent).toContain("Git");
    expect(items[1]?.textContent).toContain("Just Enough Python");
    expect(items[2]?.textContent).toContain("Data Structures");
  });

  it("marks the current course with aria-current='page' AND a non-colour signal (▸ marker + font-semibold)", () => {
    render(
      <PathRail locale="en" manifest={manifest} currentCourseId="just-enough-python" courseTitles={courseTitles} />,
    );

    const current = screen.getByRole("link", { name: /Just Enough Python/i });
    expect(current.getAttribute("aria-current")).toBe("page");
    expect(current.textContent).toContain("▸");
    expect(current.className).toContain("font-semibold");
  });

  it("every row link carries the path context, and the row's aria-label holds the untruncated title", () => {
    render(
      <PathRail locale="en" manifest={manifest} currentCourseId="just-enough-python" courseTitles={courseTitles} />,
    );

    const link = screen.getByRole("link", { name: /Data Structures & Algorithms/i });
    expect(link.getAttribute("href")).toBe(
      "/en/learn/courses/data-structures-and-algorithms-essentials?path=skills/python-fundamentals",
    );
    expect(link.getAttribute("aria-label")).toBe("Data Structures & Algorithms");
  });

  it("the footer offers 'view full path' and 'browse all courses' escape links", () => {
    render(
      <PathRail locale="en" manifest={manifest} currentCourseId="just-enough-python" courseTitles={courseTitles} />,
    );

    const viewFullPath = screen.getByRole("link", { name: /view full path/i });
    expect(viewFullPath.getAttribute("href")).toBe(
      "/en/learn/paths/skills/python-fundamentals?path=skills/python-fundamentals",
    );

    const browseAll = screen.getByRole("link", { name: /browse all courses/i });
    expect(browseAll.getAttribute("href")).toBe("/en/browse");
  });
});
