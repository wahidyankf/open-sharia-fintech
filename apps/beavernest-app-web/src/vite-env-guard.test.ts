import { execSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { loadEnv } from "vite";
import { afterEach, describe, expect, it } from "vitest";
import { guardStrayEnvFiles } from "./vite-env-guard";

// The Nx target commands are static config, not code — reading project.json
// directly is the only way to assert what flags each target passes to Vite.
const projectJsonPath = resolve(import.meta.dirname, "../project.json");
const projectJson = JSON.parse(readFileSync(projectJsonPath, "utf8")) as {
  targets: Record<string, { options: { command?: string } }>;
};

// Vite's own `loadEnv()` hard-rejects the literal mode name "local" — it
// collides with the `.env.<mode>.local` override postfix Vite itself
// defines. Empirically confirmed 2026-08-12: `vite build --mode local`
// throws `"local" cannot be used as a mode name because it conflicts with
// the .local postfix for .env files.` So every Nx target resolves the
// `local` tier to Vite's own conventional "development" mode name instead —
// `.env.local` still loads either way, because Vite always auto-loads it
// regardless of mode. Every other APP_ENV tier passes straight through as
// its own mode name.
const VITE_MODE_FRAGMENT = "VITE_MODE=$([ ${APP_ENV:-local} = local ] && echo development || echo ${APP_ENV:-local})";

function resolveViteModeFor(appEnv: string | undefined): string {
  const env: NodeJS.ProcessEnv = { ...process.env };
  delete env.APP_ENV;
  if (appEnv !== undefined) {
    env.APP_ENV = appEnv;
  }

  return execSync(`${VITE_MODE_FRAGMENT}; echo $VITE_MODE`, { encoding: "utf8", env }).trim();
}

// @covers specs/apps/beavernest/behavior/beavernest-app-web/gherkin/configuration/env-tier-loading.feature:beavernest-app-web builds with the tier selected via --mode
describe.each(["dev", "build", "test:unit"] as const)("the %s Nx target", (targetName) => {
  it("invokes Vite with a --mode flag derived from APP_ENV", () => {
    const command = projectJson.targets[targetName]?.options.command;

    expect(command).toBeDefined();
    expect(command).toContain(VITE_MODE_FRAGMENT);
    expect(command).toMatch(/--mode\s+\$VITE_MODE\b/);
  });
});

describe("APP_ENV resolution to Vite's --mode value", () => {
  it.each([
    [undefined, "development"],
    ["local", "development"],
    ["test", "test"],
    ["stag", "stag"],
    ["prod", "prod"],
  ] as const)("resolves APP_ENV=%s to Vite mode %s", (appEnv, expectedMode) => {
    expect(resolveViteModeFor(appEnv)).toBe(expectedMode);
  });
});

describe("process env precedence at the local tier", () => {
  const createdDirs: string[] = [];

  afterEach(() => {
    delete process.env.VITE_BEAVERNEST_ENV_GUARD_TEST_VAR;
    for (const dir of createdDirs.splice(0)) {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  // @covers specs/apps/beavernest/behavior/beavernest-app-web/gherkin/configuration/env-tier-loading.feature:beavernest-app-web process env wins at the local tier
  it("keeps the exported process value over .env.local at the local tier's Vite mode", () => {
    const envDir = mkdtempSync(join(tmpdir(), "beavernest-app-web-env-guard-"));
    createdDirs.push(envDir);
    writeFileSync(join(envDir, ".env.local"), "VITE_BEAVERNEST_ENV_GUARD_TEST_VAR=from-file\n");
    process.env.VITE_BEAVERNEST_ENV_GUARD_TEST_VAR = "from-process";

    // Vite's native loadEnv already implements process-env-wins — this
    // asserts that documented behavior, it does not exercise our own code.
    // "development" is the local tier's resolved Vite mode (see
    // VITE_MODE_FRAGMENT above); .env.local loads unconditionally regardless
    // of the mode name.
    const resolved = loadEnv("development", envDir, "");

    expect(resolved.VITE_BEAVERNEST_ENV_GUARD_TEST_VAR).toBe("from-process");
  });
});

describe("stray auto-loaded env file guard", () => {
  const createdDirs: string[] = [];

  afterEach(() => {
    for (const dir of createdDirs.splice(0)) {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  // @covers specs/apps/beavernest/behavior/beavernest-app-web/gherkin/configuration/env-tier-loading.feature:beavernest-app-web guards against a stray auto-loaded env file
  it.each([".env", ".env.local"] as const)("throws when a stray %s file exists at a non-local tier", (fileName) => {
    const envDir = mkdtempSync(join(tmpdir(), "beavernest-app-web-env-guard-"));
    createdDirs.push(envDir);
    writeFileSync(join(envDir, fileName), "VITE_UNUSED=stray\n");

    expect(() => guardStrayEnvFiles("stag", envDir)).toThrow();
  });

  it("does not throw at the local tier even when a stray file exists", () => {
    const envDir = mkdtempSync(join(tmpdir(), "beavernest-app-web-env-guard-"));
    createdDirs.push(envDir);
    writeFileSync(join(envDir, ".env"), "VITE_UNUSED=stray\n");

    expect(() => guardStrayEnvFiles("local", envDir)).not.toThrow();
  });

  it("does not throw at a non-local tier when no stray file exists", () => {
    const envDir = mkdtempSync(join(tmpdir(), "beavernest-app-web-env-guard-"));
    createdDirs.push(envDir);

    expect(() => guardStrayEnvFiles("stag", envDir)).not.toThrow();
  });
});
