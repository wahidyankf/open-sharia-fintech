import { afterEach, beforeEach, describe, expect, it } from "vitest";
import fs from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { loadManifests } from "./manifest-repository";

describe("loadManifests", () => {
  let tmpDir: string;

  beforeEach(async () => {
    tmpDir = await fs.mkdtemp(path.join(os.tmpdir(), "manifest-repository-test-"));
  });

  afterEach(async () => {
    await fs.rm(tmpDir, { recursive: true, force: true });
  });

  async function writeManifest(relPath: string, data: unknown): Promise<void> {
    const fullPath = path.join(tmpDir, relPath);
    await fs.mkdir(path.dirname(fullPath), { recursive: true });
    await fs.writeFile(fullPath, JSON.stringify(data), "utf-8");
  }

  it("loads a fixture manifest into a PathManifest[] validated through the upstream zod schema", async () => {
    await writeManifest("careers/interview-ready/software-engineer.json", {
      pathId: "careers/interview-ready/software-engineer",
      arc: "interview-ready",
      title: "Interview-Ready Software Engineer",
      description: "Interview-first track for an experienced engineer re-entering the market.",
      courseOrder: ["just-enough-python", "capstone-forge-ready"],
    });

    const manifests = await loadManifests(tmpDir, ["just-enough-python", "capstone-forge-ready"]);

    expect(manifests).toHaveLength(1);
    expect(manifests[0]?.pathId).toBe("careers/interview-ready/software-engineer");
    expect(manifests[0]?.courseOrder).toEqual(["just-enough-python", "capstone-forge-ready"]);
  });

  it("walks nested category/arc directories (variable-depth pathId, R2)", async () => {
    await writeManifest("skills/conventional-accounting.json", {
      pathId: "skills/conventional-accounting",
      arc: "immediately-effective",
      title: "Conventional Accounting",
      description: "desc",
      courseOrder: ["just-enough-python"],
    });

    const manifests = await loadManifests(tmpDir, ["just-enough-python"]);

    expect(manifests).toHaveLength(1);
    expect(manifests[0]?.pathId).toBe("skills/conventional-accounting");
  });

  it("throws when a manifest's courseOrder names an unresolvable course ID", async () => {
    await writeManifest("careers/interview-ready/software-engineer.json", {
      pathId: "careers/interview-ready/software-engineer",
      arc: "interview-ready",
      title: "Interview-Ready Software Engineer",
      description: "desc",
      courseOrder: ["just-enough-python", "does-not-exist-anywhere"],
    });

    await expect(loadManifests(tmpDir, ["just-enough-python"])).rejects.toThrow(/does-not-exist-anywhere/);
  });

  it("throws when a manifest fails the upstream zod schema (no validation of its own)", async () => {
    await writeManifest("skills/broken.json", { pathId: "skills/broken" });

    await expect(loadManifests(tmpDir, [])).rejects.toThrow();
  });

  it("returns an empty array for a directory with no manifest files (today's real, unpopulated dir)", async () => {
    const manifests = await loadManifests(tmpDir, []);

    expect(manifests).toEqual([]);
  });

  it("returns an empty array for a manifests directory that does not exist yet", async () => {
    const manifests = await loadManifests(path.join(tmpDir, "does-not-exist"), []);

    expect(manifests).toEqual([]);
  });
});
