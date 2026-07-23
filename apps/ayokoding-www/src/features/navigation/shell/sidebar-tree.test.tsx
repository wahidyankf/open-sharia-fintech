import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

vi.mock("next/navigation", () => ({
  usePathname: () => "/en/learn",
}));

// eslint-disable-next-line import/first
import { SidebarTree } from "./sidebar-tree";

afterEach(cleanup);

const nodes = [
  { slug: "learn", title: "Learn", weight: 0, isSection: true, children: [] },
  { slug: "rants", title: "Rants", weight: 1, isSection: true, children: [] },
];

describe("SidebarTree", () => {
  it("emits bare hrefs for content nodes (contentUrl uniform join, DD-48)", () => {
    render(<SidebarTree nodes={nodes} locale="en" />);
    expect(screen.getByRole("link", { name: "Learn" }).getAttribute("href")).toBe("/en/learn");
    expect(screen.getByRole("link", { name: "Rants" }).getAttribute("href")).toBe("/en/rants");
  });

  it("emits bare hrefs for Indonesian locale", () => {
    render(
      <SidebarTree
        nodes={[{ slug: "belajar", title: "Belajar", weight: 0, isSection: true, children: [] }]}
        locale="id"
      />,
    );
    expect(screen.getByRole("link", { name: "Belajar" }).getAttribute("href")).toBe("/id/belajar");
  });
});
