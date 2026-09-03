import { describe, expect, it } from "vitest";
import { metadata } from "../../../../../../src/app/system/status/be/page";

describe("backend status page metadata", () => {
  it("excludes the health-check from search indexes", () => {
    expect(metadata.robots).toMatchObject({ index: false });
  });
});
