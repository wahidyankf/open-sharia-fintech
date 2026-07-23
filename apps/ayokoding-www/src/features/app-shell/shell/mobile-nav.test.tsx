import { act, cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

const getTreeMock = vi.fn().mockResolvedValue([
  {
    slug: "",
    title: "English Content",
    href: "/en",
    children: [
      { slug: "by-example", title: "By Example", href: "/en/by-example", children: [] },
      { slug: "in-the-field", title: "In the Field", href: "/en/in-the-field", children: [] },
    ],
  },
]);

vi.mock("@/lib/trpc/client", () => ({
  trpcClient: {
    content: {
      getTree: { query: getTreeMock },
    },
  },
}));

vi.mock("next/navigation", () => ({
  usePathname: () => "/en",
}));

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

afterEach(cleanup);

// Phase 9 Cluster O — mobile nav drawer shows site nav without raw root node
describe("Phase 9O — mobile nav drawer", () => {
  it("Phase9O: does NOT show raw root node title ('English Content') in the nav", async () => {
    render(
      await (async () => {
        const { MobileNav } = await import("./mobile-nav");
        return <MobileNav locale="en" open={true} onOpenChange={() => {}} />;
      })(),
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    const nav = document.querySelector("nav");
    expect(nav?.textContent).not.toMatch(/English Content/i);
  });

  it("Phase9O: shows child nav links (By Example, In the Field) in the drawer", async () => {
    render(
      await (async () => {
        const { MobileNav } = await import("./mobile-nav");
        return <MobileNav locale="en" open={true} onOpenChange={() => {}} />;
      })(),
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    expect(screen.getByText("By Example")).toBeTruthy();
    expect(screen.getByText("In the Field")).toBeTruthy();
  });
});

// Phase 3 — mobile nav drawer shows primary Learn/Tools links (chrome-375 open drawer)
describe("Phase 3 — mobile nav primary links", () => {
  it("shows Learn link to /en/browse and Tools link to /en/tools", async () => {
    render(
      await (async () => {
        const { MobileNav } = await import("./mobile-nav");
        return <MobileNav locale="en" open={true} onOpenChange={() => {}} />;
      })(),
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    expect(screen.getByRole("link", { name: "Learn" }).getAttribute("href")).toBe("/en/browse");
    expect(screen.getByRole("link", { name: "Tools" }).getAttribute("href")).toBe("/en/tools");
  });

  it("shows localized Indonesian primary links for locale=id", async () => {
    render(
      await (async () => {
        const { MobileNav } = await import("./mobile-nav");
        return <MobileNav locale="id" open={true} onOpenChange={() => {}} />;
      })(),
    );

    await act(async () => {
      await new Promise((r) => setTimeout(r, 0));
    });

    expect(screen.getByRole("link", { name: "Belajar" }).getAttribute("href")).toBe("/id/browse");
    expect(screen.getByRole("link", { name: "Alat" }).getAttribute("href")).toBe("/id/tools");
  });
});
