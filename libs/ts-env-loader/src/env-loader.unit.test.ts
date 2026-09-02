/**
 * Step definitions for ts-env-loader's own APP_ENV tier loader feature.
 *
 * Covers: specs/libs/ts-env-loader/behaviors/env-loader/env-loader.feature
 *
 * Each scenario drives `loadTierEnv()` with an isolated `appDir` (a throwaway temp directory
 * holding fixture `.env.*` files) and an isolated `env` object (a plain record, not the real
 * `process.env`) so the suite never touches this process's real environment or filesystem.
 */
import path from "path";
import { mkdtempSync, rmSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { describe, expect, it } from "vitest";
import { loadTierEnv, resolveTier, type EnvRecord } from "./index";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../specs/libs/ts-env-loader/behaviors/env-loader/env-loader.feature"),
);

const tmpDirs: string[] = [];

function makeTmpAppDir(): string {
  const dir = mkdtempSync(path.join(tmpdir(), "ts-env-loader-test-"));
  tmpDirs.push(dir);
  return dir;
}

function writeEnvFile(appDir: string, fileName: string, contents: string): void {
  writeFileSync(path.join(appDir, fileName), contents, "utf-8");
}

function cleanupTmpDirs(): void {
  for (const dir of tmpDirs.splice(0)) {
    rmSync(dir, { recursive: true, force: true });
  }
}

describeFeature(feature, ({ Scenario, ScenarioOutline, AfterEachScenario }) => {
  AfterEachScenario(() => {
    cleanupTmpDirs();
  });

  Scenario("Loads the selected tier's file", ({ Given, When, Then }) => {
    let appDir = "";
    let env: EnvRecord = {};

    Given('only ".env.stag" exists in the app directory', () => {
      appDir = makeTmpAppDir();
      writeEnvFile(appDir, ".env.stag", "SHARED_VAR=stag-value\nSTAG_ONLY_VAR=stag-only\n");
    });

    When('the loader runs with APP_ENV set to "stag"', () => {
      env = { APP_ENV: "stag" };
      loadTierEnv({ appDir, env });
    });

    // @covers specs/libs/ts-env-loader/behaviors/env-loader/env-loader.feature:Loads the selected tier's file
    Then('every variable defined in ".env.stag" is applied', () => {
      expect(env["SHARED_VAR"]).toBe("stag-value");
      expect(env["STAG_ONLY_VAR"]).toBe("stag-only");
    });
  });

  Scenario("Process env always wins over the tier file", ({ Given, When, Then, And }) => {
    let appDir = "";
    let env: EnvRecord = {};

    Given('".env.local" sets a variable to a file value', () => {
      appDir = makeTmpAppDir();
      writeEnvFile(appDir, ".env.local", "SOME_VAR=file-value\n");
    });

    When('the process already has that variable set at tier "local"', () => {
      env = { APP_ENV: "local", SOME_VAR: "process-value" };
      loadTierEnv({ appDir, env });
    });

    Then("the process value is used", () => {
      expect(env["SOME_VAR"]).toBe("process-value");
    });

    // @covers specs/libs/ts-env-loader/behaviors/env-loader/env-loader.feature:Process env always wins over the tier file
    And('the ".env.local" value is not applied over it', () => {
      expect(env["SOME_VAR"]).toBe("process-value");
    });
  });

  Scenario("Tolerates a missing tier file", ({ Given, When, Then, And }) => {
    let appDir = "";
    let env: EnvRecord = {};
    let thrown: unknown;

    Given('no ".env.stag" file exists in the app directory', () => {
      appDir = makeTmpAppDir();
      expect(existsSync(path.join(appDir, ".env.stag"))).toBe(false);
    });

    When('the loader runs with APP_ENV set to "stag"', () => {
      env = { APP_ENV: "stag", EXISTING_VAR: "already-set" };
      try {
        loadTierEnv({ appDir, env });
      } catch (error) {
        thrown = error;
      }
    });

    Then("the loader does not throw", () => {
      expect(thrown).toBeUndefined();
    });

    // @covers specs/libs/ts-env-loader/behaviors/env-loader/env-loader.feature:Tolerates a missing tier file
    And("the process environment is left otherwise untouched", () => {
      expect(env["EXISTING_VAR"]).toBe("already-set");
    });
  });

  ScenarioOutline("Fails loudly on a stray auto-loaded env file", ({ Given, When, Then }, examples) => {
    const file = String(examples["file"] ?? "");
    let appDir = "";
    let thrown: unknown;

    Given('a stray "<file>" sits beside the tier file', () => {
      appDir = makeTmpAppDir();
      writeEnvFile(appDir, ".env.stag", "VAR=value\n");
      writeEnvFile(appDir, file, "VAR=other\n");
    });

    When("the loader runs with APP_ENV set to a non-local tier", () => {
      try {
        loadTierEnv({ appDir, env: { APP_ENV: "stag" } });
      } catch (error) {
        thrown = error;
      }
    });

    // @covers specs/libs/ts-env-loader/behaviors/env-loader/env-loader.feature:Fails loudly on a stray auto-loaded env file
    Then('the loader throws, naming "<file>" and the correct ".env.<tier>" replacement', () => {
      expect(thrown).toBeInstanceOf(Error);
      expect((thrown as Error).message).toContain(file);
      expect((thrown as Error).message).toContain(".env.stag");
    });
  });

  Scenario("Tolerates a stray file at the local tier", ({ Given, When, Then }) => {
    let appDir = "";
    let thrown: unknown;

    Given('a stray ".env" sits beside ".env.local"', () => {
      appDir = makeTmpAppDir();
      writeEnvFile(appDir, ".env.local", "VAR=value\n");
      writeEnvFile(appDir, ".env", "VAR=other\n");
    });

    When('the loader runs with APP_ENV set to "local"', () => {
      try {
        loadTierEnv({ appDir, env: { APP_ENV: "local" } });
      } catch (error) {
        thrown = error;
      }
    });

    // @covers specs/libs/ts-env-loader/behaviors/env-loader/env-loader.feature:Tolerates a stray file at the local tier
    Then("the loader does not throw", () => {
      expect(thrown).toBeUndefined();
    });
  });
});

// Rule 1 of the loader contract (APP_ENV unset defaults to "local") is exercised directly against
// the pure `resolveTier` function rather than through a Gherkin scenario — every scenario above
// always supplies a concrete APP_ENV, so this is the sole place the default branch executes.
describe("resolveTier", () => {
  it("defaults to local when APP_ENV is unset", () => {
    expect(resolveTier({})).toBe("local");
  });

  it("defaults to local when APP_ENV is an empty string", () => {
    expect(resolveTier({ APP_ENV: "" })).toBe("local");
  });
});
