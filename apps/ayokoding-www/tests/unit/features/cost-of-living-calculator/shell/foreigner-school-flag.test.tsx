import { cleanup, render, screen } from "@testing-library/react";
import { afterEach, describe, expect, it } from "vitest";
import { ForeignerSchoolFlag } from "../../../../../src/features/cost-of-living-calculator/shell/foreigner-school-flag";

afterEach(cleanup);

// Warning-tone hue tokens available in the design system (color-blind-friendly amber/red register).
const WARNING_HUES = ["terracotta", "honey"] as const;

describe("ForeignerSchoolFlag", () => {
  // DWT-008: in cities that are BOTH foreigner-public-school-closed AND mixed-healthcare
  // (Singapore, Bangkok, Jakarta, KL, HCMC) the healthcare "mandatory payroll insurance" Badge
  // renders honey (healthcareBadgeHue("mixed") === "honey"). The foreigner flag must NOT reuse
  // honey or it becomes indistinguishable from the healthcare badge in the same row — it needs a
  // DISTINCT warning register so the override flag stands out.
  it("DWT-008: foreigner flag hue is NOT honey (distinct from the mixed-healthcare badge)", () => {
    render(<ForeignerSchoolFlag cityId="singapore" locale="en" />);
    const flag = screen.getByTestId("school-foreigner-flag-singapore");
    const style = flag.getAttribute("style") ?? "";
    // The flag still uses a hue token (no raw hex).
    expect(style).toContain("--hue-color");
    expect(style).not.toMatch(/#[0-9a-f]{3,8}/i);
    // ...but that hue is NOT honey (the healthcare mixed badge's hue).
    expect(style).not.toContain("var(--hue-honey)");
  });

  it("DWT-008: foreigner flag still resolves to a real warning-tone hue token", () => {
    render(<ForeignerSchoolFlag cityId="singapore" locale="en" />);
    const flag = screen.getByTestId("school-foreigner-flag-singapore");
    const style = flag.getAttribute("style") ?? "";
    // Exactly one of the warning hue tokens is applied, and it is a real token.
    const matched = WARNING_HUES.filter((hue) => style.includes(`var(--hue-${hue})`));
    expect(matched.length).toBe(1);
  });

  // DWT-008: the flag also carries a higher-weight register (solid fill, not the outline wash the
  // healthcare badges use) so even a same-family hue reads as a clear, distinct alert.
  it("DWT-008: foreigner flag uses a solid (filled) Badge variant distinct from the outline healthcare badges", () => {
    render(<ForeignerSchoolFlag cityId="singapore" locale="en" />);
    const flag = screen.getByTestId("school-foreigner-flag-singapore");
    expect(flag.getAttribute("data-slot")).toBe("badge");
    // Solid/default variant fills with the hue color; it must NOT be the outline wash treatment.
    expect(flag.className).toContain("bg-[var(--hue-color)]");
    expect(flag.className).not.toContain("bg-[var(--hue-wash)]");
  });
});
