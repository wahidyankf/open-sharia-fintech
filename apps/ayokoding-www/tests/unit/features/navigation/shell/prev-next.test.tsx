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
import { PrevNext } from "../../../../../src/features/navigation/shell/prev-next";

afterEach(cleanup);

describe("PrevNext", () => {
  it("emits a bare href for prev link (contentUrl uniform join, DD-48)", () => {
    render(
      <PrevNext locale="en" prev={{ slug: "learn/software-engineering", title: "Software Engineering" }} next={null} />,
    );
    const link = screen.getByRole("link", { name: /Software Engineering/i });
    expect(link.getAttribute("href")).toBe("/en/learn/software-engineering");
  });

  it("emits a bare href for next link (contentUrl uniform join, DD-48)", () => {
    render(<PrevNext locale="en" prev={null} next={{ slug: "learn/algorithms", title: "Algorithms" }} />);
    const link = screen.getByRole("link", { name: /Algorithms/i });
    expect(link.getAttribute("href")).toBe("/en/learn/algorithms");
  });

  it("emits a bare href for Indonesian locale", () => {
    render(
      <PrevNext
        locale="id"
        prev={{ slug: "belajar/rekayasa-perangkat-lunak", title: "Rekayasa Perangkat Lunak" }}
        next={null}
      />,
    );
    const link = screen.getByRole("link", { name: /Rekayasa Perangkat Lunak/i });
    expect(link.getAttribute("href")).toBe("/id/belajar/rekayasa-perangkat-lunak");
  });

  // Gherkin (binds) — course-paths/path-order-nav.feature: "Prev and next follow the active
  // path's order"
  it("carries the path context query parameter on both links when an active path context is given", () => {
    render(
      <PrevNext
        locale="en"
        prev={{ slug: "learn/courses/just-enough-python", title: "Just Enough Python" }}
        next={{ slug: "learn/courses/capstone-forge-ready", title: "Capstone: Forge Ready" }}
        pathId="careers/interview-ready/software-engineer"
      />,
    );

    const prevLink = screen.getByRole("link", { name: /Just Enough Python/i });
    const nextLink = screen.getByRole("link", { name: /Capstone: Forge Ready/i });

    expect(prevLink.getAttribute("href")).toBe(
      "/en/learn/courses/just-enough-python?path=careers/interview-ready/software-engineer",
    );
    expect(nextLink.getAttribute("href")).toBe(
      "/en/learn/courses/capstone-forge-ready?path=careers/interview-ready/software-engineer",
    );
  });

  it("omits the path context query parameter when no pathId is given (no-regression)", () => {
    render(
      <PrevNext
        locale="en"
        prev={{ slug: "learn/courses/just-enough-python", title: "Just Enough Python" }}
        next={null}
      />,
    );

    const link = screen.getByRole("link", { name: /Just Enough Python/i });
    expect(link.getAttribute("href")).toBe("/en/learn/courses/just-enough-python");
  });
});
