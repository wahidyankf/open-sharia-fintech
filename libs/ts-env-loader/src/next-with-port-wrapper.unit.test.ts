/**
 * Contract tests for `scripts/next-with-port.mjs`.
 *
 * The wrapper lives at the repository root, outside any Nx project, so nothing would otherwise
 * execute it. It is tested from here because it exists solely to apply this library's `resolvePort`
 * to a Next.js server, and this is the target that already runs on every change to that resolver.
 *
 * Only the `--server` form is exercised. It is the branch four of the six container images use, and
 * unlike the `dev`/`start` form it needs no Next.js installation — the wrapper simply sets
 * `process.env.PORT` and imports whatever path it is handed, so a few lines of fixture stand in for
 * the generated standalone server faithfully.
 */
import { spawn } from "node:child_process";
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { afterAll, beforeAll, describe, expect, it } from "vitest";

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
const wrapper = path.join(repoRoot, "scripts/next-with-port.mjs");

let fixtureDir: string;
let fixtureServer: string;

beforeAll(() => {
  fixtureDir = mkdtempSync(path.join(tmpdir(), "next-with-port-"));
  fixtureServer = path.join(fixtureDir, "server.js");
  // Mirrors Next's standalone server: parses no flags, reads only process.env.PORT.
  writeFileSync(fixtureServer, 'console.log("PORT=" + process.env.PORT);\n');
});

afterAll(() => {
  rmSync(fixtureDir, { recursive: true, force: true });
});

interface RunResult {
  code: number | null;
  stdout: string;
  stderr: string;
}

function runWrapper(args: string[], env: Record<string, string> = {}): Promise<RunResult> {
  return new Promise((resolve) => {
    const child = spawn("node", [wrapper, ...args, "--server", fixtureServer], {
      cwd: repoRoot,
      env: { ...process.env, ...env },
    });

    let stdout = "";
    let stderr = "";
    child.stdout.on("data", (chunk) => (stdout += String(chunk)));
    child.stderr.on("data", (chunk) => (stderr += String(chunk)));
    child.on("close", (code) => resolve({ code, stdout, stderr }));
  });
}

describe("next-with-port.mjs", () => {
  it("falls back to --default when nothing overrides it", async () => {
    const result = await runWrapper(["--env", "PROBE_PORT", "--default", "3100"], { PROBE_PORT: "" });

    expect(result.code).toBe(0);
    expect(result.stdout).toContain("PORT=3100");
  });

  it("lets the prefixed variable outrank the default", async () => {
    const result = await runWrapper(["--env", "PROBE_PORT", "--default", "3100"], { PROBE_PORT: "4321" });

    expect(result.code).toBe(0);
    expect(result.stdout).toContain("PORT=4321");
  });

  it("lets an explicit --port outrank the variable", async () => {
    const result = await runWrapper(["--env", "PROBE_PORT", "--default", "3100", "--port", "5000"], {
      PROBE_PORT: "4321",
    });

    expect(result.code).toBe(0);
    expect(result.stdout).toContain("PORT=5000");
  });

  it("accepts the joined --port=N spelling", async () => {
    const result = await runWrapper(["--env", "PROBE_PORT", "--default", "3100", "--port=5001"]);

    expect(result.code).toBe(0);
    expect(result.stdout).toContain("PORT=5001");
  });

  it("exits non-zero on a malformed value instead of falling back to the default", async () => {
    const result = await runWrapper(["--env", "PROBE_PORT", "--default", "3100"], { PROBE_PORT: "notaport" });

    expect(result.code).toBe(1);
    expect(result.stderr).toContain("PROBE_PORT");
    expect(result.stdout).not.toContain("PORT=3100");
  });

  it("rejects the numeric-literal forms the F# resolver also rejects", async () => {
    for (const value of ["0x10", "1e3", "+3100", "0b1010"]) {
      const result = await runWrapper(["--env", "PROBE_PORT", "--default", "3100"], { PROBE_PORT: value });

      expect(result.code, `${value} should be rejected`).toBe(1);
      expect(result.stderr).toContain("PROBE_PORT");
    }
  });
});
