/** Real-filesystem adapter for the APP_ENV tier-loader behaviour. */
import { existsSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import { describeFeature, loadFeature } from "@amiceli/vitest-cucumber";
import { expect } from "vitest";
import { loadTierEnv, type EnvRecord } from "../../src/index";

const feature = await loadFeature(
  path.resolve(__dirname, "../../../../specs/libs/ts-env-loader/behaviours/env-loader/env-loader.feature"),
);

const temporaryDirectories: string[] = [];

function temporaryAppDirectory(): string {
  const directory = mkdtempSync(path.join(tmpdir(), "ts-env-loader-integration-"));
  temporaryDirectories.push(directory);
  return directory;
}

function writeEnvFile(appDirectory: string, name: string, contents: string): void {
  writeFileSync(path.join(appDirectory, name), contents, "utf8");
}

function capture(action: () => void): unknown {
  try {
    action();
    return undefined;
  } catch (error) {
    return error;
  }
}

describeFeature(feature, ({ Scenario, ScenarioOutline, AfterEachScenario }) => {
  AfterEachScenario(() => {
    for (const directory of temporaryDirectories.splice(0)) {
      rmSync(directory, { recursive: true, force: true });
    }
  });

  Scenario("Loads the selected tier's file", ({ Given, When, Then }) => {
    let appDirectory = "";
    let env: EnvRecord = {};

    Given('only ".env.stag" exists in the app directory', () => {
      appDirectory = temporaryAppDirectory();
      writeEnvFile(appDirectory, ".env.stag", "SHARED_VAR=stag-value\nSTAG_ONLY_VAR=stag-only\n");
    });

    When('the loader runs with APP_ENV set to "stag"', () => {
      env = { APP_ENV: "stag" };
      loadTierEnv({ appDir: appDirectory, env });
    });

    Then('every variable defined in ".env.stag" is applied', () => {
      expect(env["SHARED_VAR"]).toBe("stag-value");
      expect(env["STAG_ONLY_VAR"]).toBe("stag-only");
    });
  });

  Scenario("Process env always wins over the tier file", ({ Given, When, Then, And }) => {
    let appDirectory = "";
    let env: EnvRecord = {};

    Given('".env.local" sets a variable to a file value', () => {
      appDirectory = temporaryAppDirectory();
      writeEnvFile(appDirectory, ".env.local", "SOME_VAR=file-value\n");
    });

    When('the process already has that variable set at tier "local"', () => {
      env = { APP_ENV: "local", SOME_VAR: "process-value" };
      loadTierEnv({ appDir: appDirectory, env });
    });

    Then("the process value is used", () => {
      expect(env["SOME_VAR"]).toBe("process-value");
    });

    And('the ".env.local" value is not applied over it', () => {
      expect(env["SOME_VAR"]).toBe("process-value");
    });
  });

  Scenario("Tolerates a missing tier file", ({ Given, When, Then, And }) => {
    let appDirectory = "";
    let env: EnvRecord = {};
    let thrown: unknown;

    Given('no ".env.stag" file exists in the app directory', () => {
      appDirectory = temporaryAppDirectory();
      expect(existsSync(path.join(appDirectory, ".env.stag"))).toBe(false);
    });

    When('the loader runs with APP_ENV set to "stag"', () => {
      env = { APP_ENV: "stag", EXISTING_VAR: "already-set" };
      thrown = capture(() => loadTierEnv({ appDir: appDirectory, env }));
    });

    Then("the loader does not throw", () => {
      expect(thrown).toBeUndefined();
    });

    And("the process environment is left otherwise untouched", () => {
      expect(env["EXISTING_VAR"]).toBe("already-set");
    });
  });

  ScenarioOutline("Fails loudly on a stray auto-loaded env file", ({ Given, When, Then }, examples) => {
    const file = String(examples["file"] ?? "");
    let appDirectory = "";
    let thrown: unknown;

    Given("a stray {string} sits beside the tier file", () => {
      appDirectory = temporaryAppDirectory();
      writeEnvFile(appDirectory, ".env.stag", "VAR=value\n");
      writeEnvFile(appDirectory, file, "VAR=other\n");
    });

    When("the loader runs with APP_ENV set to a non-local tier", () => {
      thrown = capture(() => loadTierEnv({ appDir: appDirectory, env: { APP_ENV: "stag" } }));
    });

    Then('the loader throws, naming {string} and the correct ".env.<tier>" replacement', () => {
      expect(thrown).toBeInstanceOf(Error);
      expect((thrown as Error).message).toContain(file);
      expect((thrown as Error).message).toContain(".env.stag");
    });
  });

  Scenario("Tolerates a stray file at the local tier", ({ Given, When, Then }) => {
    let appDirectory = "";
    let thrown: unknown;

    Given('a stray ".env" sits beside ".env.local"', () => {
      appDirectory = temporaryAppDirectory();
      writeEnvFile(appDirectory, ".env.local", "VAR=value\n");
      writeEnvFile(appDirectory, ".env", "VAR=other\n");
    });

    When('the loader runs with APP_ENV set to "local"', () => {
      thrown = capture(() => loadTierEnv({ appDir: appDirectory, env: { APP_ENV: "local" } }));
    });

    Then("the loader does not throw", () => {
      expect(thrown).toBeUndefined();
    });
  });
});
