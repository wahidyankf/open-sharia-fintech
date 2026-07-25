import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("@/lib/trpc/client", () => ({
  trpcClient: {
    content: {
      getTree: { query: vi.fn().mockResolvedValue([]) },
    },
  },
}));

vi.mock("next/navigation", () => ({
  usePathname: () => "/en",
  useRouter: () => ({ push: vi.fn() }),
  useSearchParams: () => new URLSearchParams(),
}));

vi.mock("next-themes", () => ({
  useTheme: () => ({ theme: "light", setTheme: vi.fn() }),
}));

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

afterEach(cleanup);

// Phase 3 — header primary nav (Learn / Tools) matching chrome-1280 mockup
describe("Phase 3 — Header primary nav", () => {
  it("renders a Learn link pointing to /en/browse", async () => {
    const { Header } = await import("./header");
    render(<Header locale="en" />);

    const learn = screen.getByRole("link", { name: "Learn" });
    expect(learn.getAttribute("href")).toBe("/en/browse");
  });

  it("renders a Tools link pointing to /en/tools", async () => {
    const { Header } = await import("./header");
    render(<Header locale="en" />);

    const tools = screen.getByRole("link", { name: "Tools" });
    expect(tools.getAttribute("href")).toBe("/en/tools");
  });

  it("renders localized Indonesian primary-nav labels for locale=id", async () => {
    const { Header } = await import("./header");
    render(<Header locale="id" />);

    expect(screen.getByRole("link", { name: "Belajar" }).getAttribute("href")).toBe("/id/browse");
    expect(screen.getByRole("link", { name: "Alat" }).getAttribute("href")).toBe("/id/tools");
  });
});
