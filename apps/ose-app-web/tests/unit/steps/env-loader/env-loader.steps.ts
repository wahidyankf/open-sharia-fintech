/**
 * Step definitions for specs/apps/ose/app-web/behaviors/env-loader/env-loader.feature.
 *
 * Each scenario drives `loadTierEnv()` with an isolated `appDir` (a throwaway temp directory
 * holding fixture `.env.*` files) and an isolated `env` object (a plain record, not the real
 * `process.env`) so the suite never touches this app's real environment or filesystem tier files.
 */
import { mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import path from "node:path";
import { expect } from "vitest";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { loadTierEnv } from "@open-sharia-enterprise/ts-env-loader";

const feature = await loadFeature(
  path.resolve(process.cwd(), "../../specs/apps/ose/app-web/behaviors/env-loader/env-loader.feature"),
);

const tmpDirs: string[] = [];

function makeTmpAppDir(): string {
  const dir = mkdtempSync(join(tmpdir(), "ose-app-web-env-loader-test-"));
  tmpDirs.push(dir);
  return dir;
}

function writeEnvFile(appDir: string, fileName: string, contents: string): void {
  writeFileSync(join(appDir, fileName), contents, "utf-8");
}

describeFeature(feature, ({ Scenario, ScenarioOutline, AfterEachScenario }) => {
  // Every Given/When/Then/And step below runs as its own vitest `test()` (via
  // `@amiceli/vitest-cucumber`'s `test.for`), so a plain `vitest` `afterEach()` would fire
  // BETWEEN steps and delete the temp appDir before the later steps of the same scenario get to
  // use it. `AfterEachScenario` instead wraps the whole scenario's step run in a single
  // `afterAll()`, firing once the scenario's steps have all executed — must be registered before
  // any `Scenario`/`ScenarioOutline` call below, since it's captured by value at that point.
  AfterEachScenario(() => {
    for (const dir of tmpDirs.splice(0)) {
      rmSync(dir, { recursive: true, force: true });
    }
  });

  Scenario("ose-app-web builds against the staging tier", ({ Given, When, Then }) => {
    let appDir: string;
    let env: Record<string, string | undefined>;

    Given('only ".env.stag" exists in the app directory', () => {
      appDir = makeTmpAppDir();
      writeEnvFile(appDir, ".env.stag", "SHARED_VAR=stag-value\nSTAG_ONLY_VAR=stag-only\n");
    });

    When('"next build" runs with APP_ENV set to "stag"', () => {
      env = { APP_ENV: "stag" };
      loadTierEnv({ appDir, env });
    });

    Then('every variable consumed by the build resolves to its ".env.stag" value', () => {
      expect(env["SHARED_VAR"]).toBe("stag-value");
      expect(env["STAG_ONLY_VAR"]).toBe("stag-only");
    });
  });

  Scenario("ose-app-web process env wins over the local tier file", ({ Given, When, Then, And }) => {
    let appDir: string;
    let env: Record<string, string | undefined>;

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

    And('the ".env.local" value is not applied over it', () => {
      expect(env["SOME_VAR"]).not.toBe("file-value");
    });
  });

  Scenario("ose-app-web tolerates a missing tier file", ({ Given, When, Then, And }) => {
    let appDir: string;
    let env: Record<string, string | undefined>;

    Given('no ".env.stag" file exists in the app directory', () => {
      appDir = makeTmpAppDir(); // no .env.stag written
    });

    When('the loader runs with APP_ENV set to "stag"', () => {
      env = { APP_ENV: "stag", EXISTING_VAR: "already-set" };
      expect(() => loadTierEnv({ appDir, env })).not.toThrow();
    });

    Then("the loader does not throw", () => {
      // Assertion already performed at the When step, since throwing must be observed at the
      // moment the loader runs. This step exists to keep the Gherkin narrative intact.
      expect(env).toBeDefined();
    });

    And("startup proceeds using whatever the process environment already supplies", () => {
      expect(env["EXISTING_VAR"]).toBe("already-set");
    });
  });

  ScenarioOutline("ose-app-web fails loudly on a stray auto-loaded env file", ({ Given, When, Then }, variables) => {
    let appDir: string;
    let strayFile: string;

    Given('a stray "<file>" sits beside the app\'s tier file', () => {
      strayFile = String(variables["file"]);
      appDir = makeTmpAppDir();
      writeEnvFile(appDir, ".env.stag", "VAR=value\n");
      writeEnvFile(appDir, strayFile, "VAR=other\n");
    });

    When("the loader runs with APP_ENV set to a non-local tier", () => {
      // The actual invocation happens in the Then step below, so the thrown error can be
      // captured and asserted on in the same place.
    });

    Then('the loader throws, naming "<file>" and the correct ".env.<tier>" replacement', () => {
      const env: Record<string, string | undefined> = { APP_ENV: "stag" };
      let thrown: unknown;
      try {
        loadTierEnv({ appDir, env });
      } catch (error) {
        thrown = error;
      }

      expect(thrown).toBeInstanceOf(Error);
      expect((thrown as Error).message).toContain(strayFile);
      expect((thrown as Error).message).toContain(".env.stag");
    });
  });
});
