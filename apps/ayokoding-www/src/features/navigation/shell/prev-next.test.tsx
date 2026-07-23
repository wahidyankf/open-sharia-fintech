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
import { PrevNext } from "./prev-next";

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
});
