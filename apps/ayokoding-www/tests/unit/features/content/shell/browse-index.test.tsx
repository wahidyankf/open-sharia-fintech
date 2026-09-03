import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { TreeNode } from "@/features/content/core/types";

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

// eslint-disable-next-line import/first
import { BrowseIndex } from "../../../../../src/features/content/shell/browse-index";

afterEach(cleanup);

function section(slug: string, title: string): TreeNode {
  return { slug, title, weight: 0, isSection: true, children: [] };
}

const sections: TreeNode[] = [section("learn", "Software Engineering"), section("rants", "Rants")];

describe("BrowseIndex", () => {
  it("renders a section card for every top-level section", () => {
    render(<BrowseIndex locale="en" sections={sections} />);
    expect(screen.getByRole("link", { name: /Software Engineering/ })).toBeTruthy();
    expect(screen.getByRole("link", { name: /Rants/ })).toBeTruthy();
  });

  it("links each section card through contentUrl (bare join, DD-48)", () => {
    render(<BrowseIndex locale="en" sections={sections} />);
    expect(screen.getByRole("link", { name: /Software Engineering/ }).getAttribute("href")).toBe("/en/learn");
    expect(screen.getByRole("link", { name: /Rants/ }).getAttribute("href")).toBe("/en/rants");
  });

  it("renders a Home > Browse breadcrumb starting at Home", () => {
    render(<BrowseIndex locale="en" sections={sections} />);
    const nav = screen.getByRole("navigation", { name: "Breadcrumb" });
    expect(nav.querySelector("a")?.getAttribute("href")).toBe("/en");
    expect(nav.textContent).toContain("Home");
    expect(nav.textContent).toContain("Browse");
  });

  it("renders the localized browse title and intro", () => {
    render(<BrowseIndex locale="en" sections={sections} />);
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("Browse");
    expect(screen.getByText("Browse every AyoKoding section in one place.")).toBeTruthy();
  });

  it("uses id slugs and labels for the id locale", () => {
    const idSections = [section("belajar", "Belajar"), section("celoteh", "Celoteh")];
    render(<BrowseIndex locale="id" sections={idSections} />);
    expect(screen.getByRole("link", { name: /Belajar/ }).getAttribute("href")).toBe("/id/belajar");
    expect(screen.getByRole("heading", { level: 1 }).textContent).toBe("Jelajahi");
  });
});
