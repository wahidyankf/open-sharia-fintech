import { vi } from "vitest";

// Polyfill IntersectionObserver for jsdom
if (typeof globalThis.IntersectionObserver === "undefined") {
  globalThis.IntersectionObserver = class IntersectionObserver {
    constructor() {}
    observe() {}
    unobserve() {}
    disconnect() {}
  } as unknown as typeof globalThis.IntersectionObserver;
}

// next/navigation is mocked per-step-file (hoisted vi.mock) so each file controls its own mock.
// navigation.steps.tsx renders no next/navigation-dependent components, so no mock needed there.

// Mock next/link
vi.mock("next/link", () => ({
  default: ({ children, href, ...props }: { children: React.ReactNode; href: string; [key: string]: unknown }) => {
    const React = require("react");
    return React.createElement("a", { href, ...props }, children);
  },
}));
