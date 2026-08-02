import { existsSync, readFileSync, readdirSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

const appDirectory = __dirname;
const rootLayoutPath = join(appDirectory, "layout.tsx");
const layoutPaths = readdirSync(appDirectory, { recursive: true })
  .filter((path): path is string => typeof path === "string" && path.endsWith("layout.tsx"))
  .map((path) => join(appDirectory, path));
const dynamicApiPattern = /\b(?:headers|cookies|draftMode|connection|noStore)\s*\(/;

describe("ayokoding-www layouts remain statically renderable", () => {
  it("does not retain a root app layout", () => {
    expect(existsSync(rootLayoutPath)).toBe(false);
  });

  it("does not read a Next.js dynamic API from any layout", () => {
    const dynamicLayouts = layoutPaths.filter((layoutPath) =>
      dynamicApiPattern.test(readFileSync(layoutPath, "utf8")),
    );

    expect(dynamicLayouts).toEqual([]);
  });
});
