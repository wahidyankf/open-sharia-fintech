/**
 * Step definitions for the APP_ENV tier env-file loader feature.
 *
 * Covers: specs/apps/organiclever/app-web/behaviors/env-loader/env-loader.feature
 *
 * Each scenario drives `loadTierEnv()` with an isolated `appDir` (a throwaway temp directory
 * holding fixture `.env.*` files) and an isolated `env` object (a plain record, not the real
 * `process.env`) so the suite never touches this app's real environment or filesystem tier files.
 */
import path from "path";
import { mkdtempSync, rmSync, writeFileSync, existsSync } from "node:fs";
import { tmpdir } from "node:os";
import { loadFeature, describeFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import { loadTierEnv } from "@open-sharia-enterprise/ts-env-loader";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../../specs/apps/organiclever/app-web/behaviors/env-loader/env-loader.feature"),
);

type EnvRecord = Record<string, string | undefined>;

const tmpDirs: string[] = [];

function makeTmpAppDir(): string {
  const dir = mkdtempSync(path.join(tmpdir(), "organiclever-app-web-env-loader-test-"));
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

  Scenario("organiclever-app-web builds against the staging tier", ({ Given, When, Then }) => {
    let appDir = "";
    let env: EnvRecord = {};

    Given('only ".env.stag" exists in the app directory', () => {
      appDir = makeTmpAppDir();
      writeEnvFile(appDir, ".env.stag", "SHARED_VAR=stag-value\nSTAG_ONLY_VAR=stag-only\n");
    });

    When('"next build" runs with APP_ENV set to "stag"', () => {
      env = { APP_ENV: "stag" };
      loadTierEnv({ appDir, env });
    });

    // @covers specs/apps/organiclever/app-web/behaviors/env-loader/env-loader.feature:organiclever-app-web builds against the staging tier
    Then('every variable consumed by the build resolves to its ".env.stag" value', () => {
      expect(env["SHARED_VAR"]).toBe("stag-value");
      expect(env["STAG_ONLY_VAR"]).toBe("stag-only");
    });
  });

  Scenario("organiclever-app-web process env wins over the local tier file", ({ Given, When, Then, And }) => {
    let appDir = "";
    let env: EnvRecord = {};

    Given('".env.local" sets an app variable to a file value', () => {
      appDir = makeTmpAppDir();
      writeEnvFile(appDir, ".env.local", "SOME_VAR=file-value\n");
    });

    When('the process starts with that variable already exported at tier "local"', () => {
      env = { APP_ENV: "local", SOME_VAR: "process-value" };
      loadTierEnv({ appDir, env });
    });

    Then("the exported process value is used", () => {
      expect(env["SOME_VAR"]).toBe("process-value");
    });

    // @covers specs/apps/organiclever/app-web/behaviors/env-loader/env-loader.feature:organiclever-app-web process env wins over the local tier file
    And('the ".env.local" value is not applied over it', () => {
      expect(env["SOME_VAR"]).toBe("process-value");
    });
  });

  Scenario("organiclever-app-web tolerates a missing tier file", ({ Given, When, Then, And }) => {
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

    // @covers specs/apps/organiclever/app-web/behaviors/env-loader/env-loader.feature:organiclever-app-web tolerates a missing tier file
    And("startup proceeds using whatever the process environment already supplies", () => {
      expect(env["EXISTING_VAR"]).toBe("already-set");
    });
  });

  ScenarioOutline(
    "organiclever-app-web fails loudly on a stray auto-loaded env file",
    ({ Given, When, Then }, examples) => {
      const file = String(examples["file"] ?? "");
      let appDir = "";
      let thrown: unknown;

      Given('a stray "<file>" sits beside the app\'s tier file', () => {
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

      // @covers specs/apps/organiclever/app-web/behaviors/env-loader/env-loader.feature:organiclever-app-web fails loudly on a stray auto-loaded env file
      Then('the loader throws, naming "<file>" and the correct ".env.<tier>" replacement', () => {
        expect(thrown).toBeInstanceOf(Error);
        expect((thrown as Error).message).toContain(file);
        expect((thrown as Error).message).toContain(".env.stag");
      });
    },
  );
});
