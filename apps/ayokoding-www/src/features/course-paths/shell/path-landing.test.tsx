import { cleanup, render, screen, within } from "@testing-library/react";
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
import { PathLanding } from "./path-landing";

afterEach(cleanup);

const manifest: PathManifest = {
  pathId: "careers/interview-ready/example-role",
  arc: "interview-ready",
  title: "Interview-Ready Example Role",
  description: "An interview-first track.",
  courseOrder: ["just-enough-python", "just-enough-bash", "version-control-and-git"],
};

const courseTitles = {
  "just-enough-python": "Just Enough Python",
  "just-enough-bash": "Just Enough Bash",
  "version-control-and-git": "Version Control & Git",
};

describe("PathLanding (Cycle 3.1 — Screen 2)", () => {
  it("renders the path title as the H1", () => {
    render(<PathLanding locale="en" manifest={manifest} courseTitles={courseTitles} />);

    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("Interview-Ready Example Role");
  });

  it("lists the courses in manifest courseOrder inside a semantic <ol>", () => {
    const { container } = render(<PathLanding locale="en" manifest={manifest} courseTitles={courseTitles} />);

    const ol = container.querySelector("ol");
    expect(ol).not.toBeNull();
    const items = within(ol as HTMLElement).getAllByRole("listitem");
    expect(items.map((item) => item.textContent)).toEqual([
      "Just Enough Python",
      "Just Enough Bash",
      "Version Control & Git",
    ]);
  });

  it("every course link carries the path context query parameter", () => {
    render(<PathLanding locale="en" manifest={manifest} courseTitles={courseTitles} />);

    const link = screen.getByRole("link", { name: "Just Enough Python" });
    expect(link.getAttribute("href")).toBe(
      "/en/learn/courses/just-enough-python?path=careers/interview-ready/example-role",
    );
  });

  it("renders no body content when bodyHtml is not supplied (careers paths, no regression)", () => {
    const { container } = render(<PathLanding locale="en" manifest={manifest} courseTitles={courseTitles} />);

    expect(container.querySelector(".prose")).toBeNull();
  });

  it("renders the supplied body html between the title and the syllabus (Cycle 3.1d)", () => {
    render(
      <PathLanding
        locale="en"
        manifest={manifest}
        courseTitles={courseTitles}
        bodyHtml="<p>A distinct runway-justification paragraph.</p>"
      />,
    );

    expect(screen.getByText("A distinct runway-justification paragraph.")).toBeTruthy();
  });
});
