import { readFileSync } from "node:fs";
import { join } from "node:path";
import { describe, expect, it } from "vitest";

const appDirectory = __dirname;
const staticServerEntries = [
  join(appDirectory, "[locale]", "layout.tsx"),
  join(appDirectory, "[locale]", "(content)", "layout.tsx"),
  join(appDirectory, "[locale]", "(content)", "[...slug]", "page.tsx"),
];

describe("ayokoding-www static course-path data boundary", () => {
  it("does not serialize the complete course-path catalog into ordinary page client boundaries", () => {
    for (const entry of staticServerEntries) {
      expect(readFileSync(entry, "utf8")).not.toContain("toCoursePathClientData");
    }
  });
});
