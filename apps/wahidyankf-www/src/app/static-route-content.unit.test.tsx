import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import React from "react";
import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it, vi } from "vitest";
import Home from "./page";
import CV from "./cv/page";
import Projects from "./personal-projects/page";

vi.mock("next/navigation", () => ({
  useRouter: () => ({ push: vi.fn(), replace: vi.fn() }),
}));

vi.mock("@/features/app-shell/shell/Navigation", () => ({
  Navigation: () => <nav aria-label="Primary navigation" />,
}));

vi.mock("@open-sharia-enterprise/web-ui", () => ({
  SearchComponent: ({ placeholder }: { placeholder: string }) => <input placeholder={placeholder} readOnly />,
  HighlightText: ({ text }: { text: string }) => <>{text}</>,
}));

const routes = [
  {
    pathname: "/",
    source: "page.tsx",
    contentSource: "../features/home/shell/HomeContent.tsx",
    Component: Home,
    visibleContent: "Welcome to My Portfolio",
  },
  {
    pathname: "/cv",
    source: "cv/page.tsx",
    contentSource: "../features/cv/shell/CvContent.tsx",
    Component: CV,
    visibleContent: "Curriculum Vitae",
  },
  {
    pathname: "/personal-projects",
    source: "personal-projects/page.tsx",
    contentSource: "../features/personal-projects/shell/PersonalProjectsContent.tsx",
    Component: Projects,
    visibleContent: "Independent Projects",
  },
] as const;

describe("static portfolio route content", () => {
  for (const route of routes) {
    it(`${route.pathname} renders visible content before browser query seeding`, () => {
      const source = readFileSync(resolve(__dirname, route.source), "utf8");
      const contentSource = readFileSync(resolve(__dirname, route.contentSource), "utf8");

      expect(source).not.toContain("Suspense");
      expect(contentSource).not.toContain("useSearchParams");
      expect(renderToStaticMarkup(<route.Component />)).toContain(route.visibleContent);
    });
  }
});
