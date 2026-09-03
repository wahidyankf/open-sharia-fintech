import { describe, it, expect } from "vitest";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

describe("be status page env reads", () => {
  const src = readFileSync(resolve(__dirname, "../../../../../../src/app/system/status/be/page.tsx"), "utf-8");

  it("reads ORGANICLEVER_BE_URL via env object not process.env", () => {
    expect(src).toMatch(/env\.ORGANICLEVER_BE_URL/);
  });
});
