import React from "react";
import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import RootLayout, { metadata } from "./layout";

vi.mock("@open-sharia-enterprise/web-ui", () => ({
  ScrollToTop: () => <div data-testid="scroll-to-top">ScrollToTop</div>,
  ThemeToggle: () => <div data-testid="theme-toggle">ThemeToggle</div>,
}));

// Mock the Inter font
vi.mock("next/font/google", () => ({
  Inter: () => ({ className: "inter-font" }),
}));

describe("RootLayout", () => {
  it("renders children correctly", () => {
    render(
      <RootLayout>
        <div>Test content</div>
      </RootLayout>,
    );

    const bodyContent = screen.getByText("Test content").closest(".body-content");
    expect(bodyContent).toBeInTheDocument();
    expect(bodyContent).toHaveClass("body-content flex-grow");

    expect(screen.getByTestId("theme-toggle")).toBeInTheDocument();
    expect(screen.getByText("Test content")).toBeInTheDocument();
  });

  it("includes ScrollToTop component", () => {
    render(
      <RootLayout>
        <div>Test content</div>
      </RootLayout>,
    );

    expect(screen.getByTestId("scroll-to-top")).toBeInTheDocument();
  });

  it("references the og-image.jpg asset for OpenGraph and Twitter previews", () => {
    expect(metadata.openGraph?.images).toEqual([
      { url: "https://www.wahidyankf.com/og-image.jpg", width: 1200, height: 630 },
    ]);
    expect(metadata.twitter?.images).toEqual(["https://www.wahidyankf.com/og-image.jpg"]);
  });

  it("does not reference a Twitter handle", () => {
    expect(metadata.twitter?.creator).toBeUndefined();
  });

  it("uses the canonical public URL for OpenGraph metadata", () => {
    expect(metadata.openGraph?.url).toBe("https://www.wahidyankf.com");
  });
});
