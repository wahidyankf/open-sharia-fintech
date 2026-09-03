import { cleanup, render, screen, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";

vi.mock("next/link", () => ({
  default: ({ href, children, ...rest }: { href: string; children: React.ReactNode; [key: string]: unknown }) => (
    <a href={href} {...rest}>
      {children}
    </a>
  ),
}));

afterEach(cleanup);

// Cluster K: tools index renders localized text, not raw i18n keys
describe("Phase 9K — Tools index renders localized text", () => {
  it("Phase9K: en locale renders 'Tools' heading and 'Cost of Living Calculator' link", async () => {
    const ToolsPage = (await import("@/app/[locale]/tools/page")).default;
    // async server component — call directly, render returned JSX
    const jsx = await ToolsPage({ params: Promise.resolve({ locale: "en" as const }) });
    render(jsx);
    expect(screen.getByRole("heading", { level: 1 }).textContent).toMatch(/tools/i);
    expect(screen.getByRole("link", { name: /cost of living calculator/i })).toBeTruthy();
    expect(document.body.textContent).not.toMatch(/toolsPageTitle|toolsPageCalcLink/);
  });

  it("Phase9K: id locale renders 'Alat' heading and 'Kalkulator Biaya Hidup' link", async () => {
    const ToolsPage = (await import("@/app/[locale]/tools/page")).default;
    const jsx = await ToolsPage({ params: Promise.resolve({ locale: "id" as const }) });
    render(jsx);
    expect(screen.getByRole("heading", { level: 1 }).textContent).toMatch(/alat/i);
    expect(screen.getByRole("link", { name: /kalkulator biaya hidup/i })).toBeTruthy();
    expect(document.body.textContent).not.toMatch(/toolsPageTitle|toolsPageCalcLink/);
  });
});

// UWT-009: the tools index calculator entry must carry a description that is
// distinct from the link text, so the entry is not "link-text only".
describe("UWT-009 — tools index calculator entry has a distinct description", () => {
  it("renders a description element whose text differs from the calculator link text (en)", async () => {
    const ToolsPage = (await import("@/app/[locale]/tools/page")).default;
    const jsx = await ToolsPage({ params: Promise.resolve({ locale: "en" as const }) });
    render(jsx);

    const link = screen.getByRole("link", { name: /cost of living calculator/i });
    const desc = screen.getByTestId("tool-desc-calculator");

    expect((desc.textContent ?? "").trim()).not.toBe("");
    expect((desc.textContent ?? "").trim()).not.toBe((link.textContent ?? "").trim());
    expect(document.body.textContent).not.toMatch(/toolsPageCalcDesc/);
  });

  it("associates the description with the calculator list item in the id locale", async () => {
    const ToolsPage = (await import("@/app/[locale]/tools/page")).default;
    const jsx = await ToolsPage({ params: Promise.resolve({ locale: "id" as const }) });
    render(jsx);

    const item = screen.getByRole("link", { name: /kalkulator biaya hidup/i }).closest("li")!;
    const desc = within(item).getByTestId("tool-desc-calculator");
    expect((desc.textContent ?? "").trim()).not.toBe("");
    expect(document.body.textContent).not.toMatch(/toolsPageCalcDesc/);
  });
});
