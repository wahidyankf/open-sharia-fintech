import { readFileSync } from "node:fs";
import { resolve } from "node:path";
import { describe, expect, it } from "vitest";

const routes = [
  { pathname: "/", source: "page.tsx" },
  { pathname: "/cv", source: "cv/page.tsx" },
  { pathname: "/personal-projects", source: "personal-projects/page.tsx" },
] as const;

const declaresSearchParams = /function\s+\w+\s*\(\s*{\s*searchParams\b/;
const awaitsSearchParams = /\bawait\s+searchParams\b/;

describe("static portfolio routes", () => {
  for (const route of routes) {
    it(`${route.pathname} neither declares nor awaits searchParams`, () => {
      const source = readFileSync(resolve(__dirname, route.source), "utf8");

      expect({
        declaresSearchParams: declaresSearchParams.test(source),
        awaitsSearchParams: awaitsSearchParams.test(source),
      }).toEqual({ declaresSearchParams: false, awaitsSearchParams: false });
    });
  }
});
