import assert from "node:assert/strict";
import { mkdtemp, mkdir, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import {
  extractBindings,
  parseCliOptions,
  runCli,
  validateCoverage,
  validateFeatureSource,
  validateProjectTargetContract,
} from "./behaviour-coverage.mjs";

const validFeature = `Feature: Static coverage

  Scenario: A covered behaviour
    Given a configured subject
    When the subject is exercised
    Then independent evidence is observed
`;

async function fixture(files) {
  const root = await mkdtemp(path.join(os.tmpdir(), "ose-behaviour-coverage-"));
  await Promise.all(
    Object.entries(files).map(async ([relativePath, contents]) => {
      const target = path.join(root, relativePath);
      await mkdir(path.dirname(target), { recursive: true });
      await writeFile(target, contents, "utf8");
    }),
  );
  return root;
}

function tsBindings(extra = "") {
  return `
const { Given, When, Then } = createBdd();
Given("a configured subject", () => {});
When("the subject is exercised", () => {});
Then("independent evidence is observed", () => {});
${extra}`;
}

test("accepts independently documented Integration and E2E exemptions", () => {
  const source = validFeature.replace(
    "  Scenario: A covered behaviour",
    "  # Exemption(integration): the local boundary cannot inject the private invariant failure; alternative-proof: example:test:unit / A covered behaviour\n" +
      "  @integration-exempt\n" +
      "  # Exemption(e2e): no public trigger can inject the private invariant failure; alternative-proof: example:test:unit / A covered behaviour\n" +
      "  @e2e-exempt\n" +
      "  Scenario: A covered behaviour",
  );

  assert.deepEqual(validateFeatureSource("example.feature", source).errors, []);
});

test("requires each exemption on its own tag line with its own adjacent comment", () => {
  const sharedTagLine = validFeature.replace(
    "  Scenario: A covered behaviour",
    "  # Exemption(integration): local state is not observable at the public boundary; alternative-proof: example:test:unit / A covered behaviour\n" +
      "  @integration-exempt @e2e-exempt\n" +
      "  Scenario: A covered behaviour",
  );
  const sharedComment = validFeature.replace(
    "  Scenario: A covered behaviour",
    "  # Exemption(integration): local state is not observable at the public boundary; alternative-proof: example:test:unit / A covered behaviour\n" +
      "  @integration-exempt\n" +
      "  @e2e-exempt\n" +
      "  Scenario: A covered behaviour",
  );

  assert.ok(
    validateFeatureSource("example.feature", sharedTagLine).errors.some((error) => error.includes("separate tag line")),
  );
  assert.ok(
    validateFeatureSource("example.feature", sharedComment).errors.some((error) =>
      error.includes("immediately preceding comment"),
    ),
  );
});

test("rejects difficulty, runtime, flakiness, cost, and unfinished-work reasons", () => {
  for (const reason of [
    "hard to build",
    "slow runtime",
    "flaky in CI",
    "costly to maintain",
    "too expensive",
    "TODO",
    "not-yet-implemented",
    "unfinished",
    "missing implementation",
  ]) {
    const source = validFeature.replace(
      "  Scenario: A covered behaviour",
      `  # Exemption(e2e): ${reason}; alternative-proof: example:test:unit / A covered behaviour\n` +
        "  @e2e-exempt\n" +
        "  Scenario: A covered behaviour",
    );
    assert.ok(
      validateFeatureSource("example.feature", source).errors.some((error) => error.includes("cannot be justified")),
      reason,
    );
  }
});

test("requires boundary language and a canonical alternative proof", () => {
  const weakReason = validFeature.replace(
    "  Scenario: A covered behaviour",
    "  # Exemption(e2e): this is enough; alternative-proof: example:test:unit / A covered behaviour\n" +
      "  @e2e-exempt\n" +
      "  Scenario: A covered behaviour",
  );
  const invalidProof = validFeature.replace(
    "  Scenario: A covered behaviour",
    "  # Exemption(e2e): no public boundary exposes this invariant; alternative-proof: unit suite\n" +
      "  @e2e-exempt\n" +
      "  Scenario: A covered behaviour",
  );

  assert.ok(
    validateFeatureSource("example.feature", weakReason).errors.some((error) => error.includes("boundary mismatch")),
  );
  assert.ok(
    validateFeatureSource("example.feature", invalidProof).errors.some((error) => error.includes("alternative-proof")),
  );
});

test("rejects forbidden exemption, WIP, no-layer, and positive selection tags", () => {
  for (const tag of ["@unit-exempt", "@wip", "@no-network", "@unit", "@integration", "@e2e"]) {
    const source = validFeature.replace("  Scenario: A covered behaviour", `  ${tag}\n  Scenario: A covered behaviour`);
    assert.ok(
      validateFeatureSource("example.feature", source).errors.some((error) => error.includes("is forbidden")),
      tag,
    );
  }
});

test("does not interpret doc-string content as tags", () => {
  const source = `Feature: Doc strings

  Scenario: Literal tags are documented
    Given documentation containing:
      """
      @wip
      @unit-exempt
      """
    When the documentation is inspected
    Then the literal tags are preserved
`;

  assert.deepEqual(validateFeatureSource("doc-string.feature", source).errors, []);
});

test("rejects malformed and empty features and scenarios without explicit When and Then", () => {
  assert.ok(
    validateFeatureSource("malformed.feature", "Scenario: orphan").errors.some((error) => error.includes("parse")),
  );
  assert.ok(
    validateFeatureSource("empty.feature", "Feature: Empty").errors.some((error) =>
      error.includes("at least one scenario"),
    ),
  );
  const noAction = validFeature
    .replace("    When the subject is exercised\n", "")
    .replace("    Then independent evidence is observed\n", "");
  const errors = validateFeatureSource("no-action.feature", noAction).errors;
  assert.ok(errors.some((error) => error.includes("explicit When")));
  assert.ok(errors.some((error) => error.includes("explicit Then")));
});

test("expands every Scenario Outline example row", () => {
  const source = `Feature: Outline coverage

  Scenario Outline: A value is covered
    Given value <value>
    When the value is inspected
    Then result <result> is observed

    Examples:
      | value | result |
      | one   | first  |
      | two   | second |
`;

  const result = validateFeatureSource("outline.feature", source);
  assert.deepEqual(result.errors, []);
  assert.equal(result.pickles.length, 2);
  assert.deepEqual(
    result.pickles.map(({ steps }) => steps.map(({ text }) => text)),
    [
      ["value one", "the value is inspected", "result first is observed"],
      ["value two", "the value is inspected", "result second is observed"],
    ],
  );
});

test("extracts TypeScript, TSX, and F# TickSpec bindings", () => {
  const typescript = `
const { Given, When } = createBdd();
Given("a value {string}", () => {});
When(/^the value (\\d+) is inspected$/, () => {});
`;
  const fsharp = `
[<Then>]
let \`\`result "([^"]*)" is observed\`\` (result: string) = result
[<Given>]
member _.\`\`a member-bound subject\`\`() = ()
`;

  const bindings = [...extractBindings("steps.tsx", typescript), ...extractBindings("Steps.fs", fsharp)];
  assert.equal(bindings.length, 4);
  assert.equal(bindings[0].keyword, "Given");
  assert.match(bindings[0].pattern, /a value/u);
  assert.equal(bindings[2].keyword, "Then");
  assert.match(bindings[2].pattern, /result/u);
  assert.equal(bindings[3].keyword, "Given");
  assert.equal(bindings[3].pattern, "a member-bound subject");
});

test("ignores commented-out TypeScript and F# bindings", () => {
  const typescript = `
// Given("a disabled step", () => {});
/* When("another disabled step", () => {}); */
Then("an active step", () => {});
`;
  const fsharp = `
(*
[<Given>]
let \`\`a disabled F sharp step\`\` () = ()
*)
[<Then>]
let \`\`an active F sharp step\`\` () = ()
`;

  assert.deepEqual(
    extractBindings("steps.ts", typescript).map(({ pattern }) => pattern),
    ["an active step"],
  );
  assert.deepEqual(
    extractBindings("Steps.fs", fsharp).map(({ pattern }) => pattern),
    ["an active F sharp step"],
  );
});

test("scopes duplicate F# TickSpec bindings to explicit feature literals", async () => {
  const feature = (name, action, outcome) => `Feature: ${name}

  Scenario: ${name} works
    Given shared setup
    When ${action}
    Then ${outcome}
`;
  const root = await fixture({
    "specs/alpha.feature": feature("Alpha", "alpha runs", "alpha is observed"),
    "specs/beta.feature": feature("Beta", "beta runs", "beta is observed"),
    "unit/AlphaSteps.fs": `
let private featurePath = "specs/alpha.feature"
[<Given>]
let \`\`shared setup\`\` () = ()
[<When>]
let \`\`alpha runs\`\` () = ()
[<Then>]
let \`\`alpha is observed\`\` () = ()
`,
    "unit/BetaSteps.fs": `
let private featurePath = "specs\\\\beta.feature"
[<Given>]
let \`\`shared setup\`\` () = ()
[<When>]
let \`\`beta runs\`\` () = ()
[<Then>]
let \`\`beta is observed\`\` () = ()
`,
    "unit/driver.fsproj": "<Project />",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "specs")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.fsproj"),
  });

  assert.deepEqual(result.errors, []);
});

test("keeps duplicate F# TickSpec bindings ambiguous without explicit feature ownership", async () => {
  const root = await fixture({
    "specs/alpha.feature": validFeature,
    "unit/AlphaSteps.fs": `
[<Given>]
let \`\`a configured subject\`\` () = ()
[<When>]
let \`\`the subject is exercised\`\` () = ()
[<Then>]
let \`\`independent evidence is observed\`\` () = ()
`,
    "unit/BetaSteps.fs": `
[<Given>]
let \`\`a configured subject\`\` () = ()
`,
    "unit/driver.fsproj": "<Project />",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "specs")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.fsproj"),
  });

  assert.ok(result.errors.some((error) => error.includes("ambiguous Unit binding")));
});

test("matches standard and custom Cucumber expression parameters", async () => {
  const feature = `Feature: Parameter bindings

  Scenario: Values are covered
    Given a value "alpha"
    When 42 items are inspected
    Then result accepted is observed
`;
  const root = await fixture({
    "behaviours/parameters.feature": feature,
    "unit/parameters.steps.ts": `
Given("a value {string}", () => {});
When("{int} items are inspected", () => {});
Then("result {any} is observed", () => {});
`,
    "unit/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.ts"),
  });

  assert.deepEqual(result.errors, []);
});

test("matches vitest-cucumber Scenario Outline placeholders after pickle expansion", async () => {
  const feature = `Feature: Outline adapter

  Scenario Outline: A route redirects
    Given route <source>
    When the route is resolved
    Then destination <destination> is returned

    Examples:
      | source | destination |
      | old    | new         |
`;
  const root = await fixture({
    "behaviours/routes.feature": feature,
    "unit/routes.steps.ts": `
Given("route <source>", () => {});
When("the route is resolved", () => {});
Then("destination <destination> is returned", () => {});
`,
    "unit/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.ts"),
  });

  assert.deepEqual(result.errors, []);
});

test("matches escaped literal Cucumber metacharacters in Playwright-BDD strings", async () => {
  const feature = `Feature: Escaped literals

  Scenario: Literal punctuation
    Given a touch (no-hover) viewport
    When prev/next is inspected
    Then active/selected is observed
`;
  const root = await fixture({
    "behaviours/literals.feature": feature,
    "e2e/literals.steps.ts": String.raw`
Given("a touch \\(no-hover\\) viewport", () => {});
When("prev\\/next is inspected", () => {});
Then("active\\/selected is observed", () => {});
`,
    "e2e/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    adapter: "e2e",
    bindingRoots: [path.join(root, "e2e")],
    driver: path.join(root, "e2e/driver.ts"),
  });

  assert.deepEqual(result.errors, []);
});

test("treats TypeScript Cucumber registration keywords as matching synonyms", async () => {
  const feature = `Feature: Keyword synonyms

  Scenario: Playwright registration
    Given setup exists
    When the public page opens
    Then the result is visible
`;
  const root = await fixture({
    "behaviours/synonyms.feature": feature,
    "e2e/synonyms.steps.ts": `
Given("setup exists", () => {});
Given("the public page opens", () => {});
Given("the result is visible", () => {});
`,
    "e2e/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    adapter: "e2e",
    bindingRoots: [path.join(root, "e2e")],
    driver: path.join(root, "e2e/driver.ts"),
  });

  assert.deepEqual(result.errors, []);
});

test("requires Unit coverage even when both higher layers are exempt", async () => {
  const feature = validFeature.replace(
    "  Scenario: A covered behaviour",
    "  # Exemption(integration): the local boundary cannot inject the private invariant failure; alternative-proof: example:test:unit / A covered behaviour\n" +
      "  @integration-exempt\n" +
      "  # Exemption(e2e): no public boundary exposes the private invariant failure; alternative-proof: example:test:unit / A covered behaviour\n" +
      "  @e2e-exempt\n" +
      "  Scenario: A covered behaviour",
  );
  const root = await fixture({
    "behaviours/example.feature": feature,
    "unit/empty.steps.ts": "export {};",
    "unit/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.ts"),
  });

  assert.ok(result.errors.some((error) => error.includes("undefined Unit binding")));
});

test("exempts only the named adapter", async () => {
  const feature = validFeature.replace(
    "  Scenario: A covered behaviour",
    "  # Exemption(integration): a browser public boundary is required to observe layout; alternative-proof: example-e2e:test:e2e / A covered behaviour\n" +
      "  @integration-exempt\n" +
      "  Scenario: A covered behaviour",
  );
  const root = await fixture({
    "behaviours/example.feature": feature,
    "adapter/empty.steps.ts": "export {};",
    "adapter/driver.ts": "export const driver = {};",
  });
  const input = {
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    bindingRoots: [path.join(root, "adapter")],
    driver: path.join(root, "adapter/driver.ts"),
  };

  const integration = await validateCoverage({ ...input, adapter: "integration" });
  const e2e = await validateCoverage({ ...input, adapter: "e2e" });

  assert.equal(integration.errors.filter((error) => error.includes("undefined")).length, 0);
  assert.ok(e2e.errors.some((error) => error.includes("undefined E2E binding")));
});

test("reports ambiguous and unused bindings", async () => {
  const root = await fixture({
    "behaviours/example.feature": validFeature,
    "unit/one.steps.ts": tsBindings('Given("an unused boundary", () => {});'),
    "unit/two.steps.ts": 'When("the subject is exercised", () => {});',
    "unit/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.ts"),
  });

  assert.ok(result.errors.some((error) => error.includes("ambiguous Unit binding")));
  assert.ok(result.errors.some((error) => error.includes("unused Unit binding")));
});

test("validates scoped vitest-cucumber scenarios without cross-scenario ambiguity", async () => {
  const feature = `Feature: Scoped bindings

  Scenario: First case
    Given shared setup
    When first action
    Then success is observed

  Scenario: Second case
    Given shared setup
    When second action
    Then success is observed
`;
  const bindings = `
describeFeature(feature, ({ Scenario }) => {
  Scenario("First case", ({ Given, When, Then }) => {
    Given("shared setup", () => {});
    When("first action", () => {});
    Then("success is observed", () => {});
  });
  Scenario("Second case", ({ Given, When, Then }) => {
    Given("shared setup", () => {});
    When("second action", () => {});
    Then("success is observed", () => {});
  });
});
`;
  const root = await fixture({
    "behaviours/scoped.feature": feature,
    "unit/scoped.steps.tsx": bindings,
    "unit/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.ts"),
  });

  assert.deepEqual(result.errors, []);
});

test("scopes duplicate TypeScript Background bindings to their loaded feature", async () => {
  const feature = (name, action, outcome) => `Feature: ${name}

  Background:
    Given the API is running

  Scenario: ${name} works
    When ${action}
    Then ${outcome}
`;
  const root = await fixture({
    "specs/alpha.feature": feature("Alpha", "alpha runs", "alpha is observed"),
    "specs/beta.feature": feature("Beta", "beta runs", "beta is observed"),
    "unit/alpha.steps.ts": `
const feature = loadFeature(path.resolve(process.cwd(), "specs/alpha.feature"));
Given("the API is running", () => {});
When("alpha runs", () => {});
Then("alpha is observed", () => {});
`,
    "unit/beta.steps.ts": `
const feature = loadFeature(path.resolve(process.cwd(), "specs/beta.feature"));
Given("the API is running", () => {});
When("beta runs", () => {});
Then("beta is observed", () => {});
`,
    "unit/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "specs")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.ts"),
  });

  assert.deepEqual(result.errors, []);
});

test("does not report feature-scoped bindings outside a manifest corpus as unused", async () => {
  const root = await fixture({
    "specs/in-scope.feature": validFeature,
    "unit/in-scope.steps.ts": `
const feature = loadFeature(path.resolve(process.cwd(), "specs/in-scope.feature"));
${tsBindings()}
`,
    "unit/out-of-scope.steps.ts": `
const feature = loadFeature(path.resolve(process.cwd(), "specs/out-of-scope.feature"));
Given("an unrelated setup", () => {});
`,
    "unit/driver.ts": "export const driver = {};",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "specs/in-scope.feature")],
    adapter: "unit",
    bindingRoots: [path.join(root, "unit")],
    driver: path.join(root, "unit/driver.ts"),
  });

  assert.deepEqual(result.errors, []);
});

test("requires a non-empty recursive corpus and an existing driver", async () => {
  const root = await fixture({ "nested/README.md": "nothing here" });
  const result = await validateCoverage({
    project: "example",
    corpusRoots: [root],
    adapter: "unit",
    bindingRoots: [root],
    driver: path.join(root, "missing-driver.ts"),
  });

  assert.ok(result.errors.some((error) => error.includes("no .feature files")));
  assert.ok(result.errors.some((error) => error.includes("driver does not exist")));
});

test("aggregate behaviour mode checks every configured adapter without executing tests", async () => {
  const root = await fixture({
    "behaviours/example.feature": validFeature,
    "unit/steps.ts": tsBindings(),
    "unit/driver.ts": "throw new Error('the static validator executed the driver');",
  });

  const result = await validateCoverage({
    project: "example",
    corpusRoots: [path.join(root, "behaviours")],
    adapter: "behaviour",
    adapters: {
      unit: {
        bindingRoots: [path.join(root, "unit")],
        driver: path.join(root, "unit/driver.ts"),
      },
    },
  });

  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.stats.adapters, ["unit"]);
});

test("loads a project-local aggregate config with paths relative to that config", async () => {
  const root = await fixture({
    "config/behaviour-coverage.json": JSON.stringify({
      project: "example",
      corpus: ["../behaviours"],
      adapters: {
        unit: { bindings: ["../unit"], driver: "../unit/driver.ts" },
      },
    }),
    "behaviours/example.feature": validFeature,
    "unit/example.steps.ts": tsBindings(),
    "unit/driver.ts": "export const driver = {};",
  });

  const options = await parseCliOptions(["--config", "config/behaviour-coverage.json", "--adapter", "behaviour"], root);

  assert.equal(options.project, "example");
  assert.deepEqual(options.corpusRoots, [path.join(root, "behaviours")]);
  assert.deepEqual(options.adapters.unit.bindingRoots, [path.join(root, "unit")]);
});

test("CLI is deterministic and never invokes a configured runtime", async () => {
  const root = await fixture({
    "behaviours/example.feature": validFeature,
    "unit/example.steps.ts": tsBindings(),
    "unit/driver.ts": "throw new Error('runtime execution is forbidden');",
  });
  const output = { logs: [], errors: [] };
  const io = {
    log: (message) => output.logs.push(message),
    error: (message) => output.errors.push(message),
  };
  const argv = [
    "--adapter",
    "unit",
    "--project",
    "example",
    "--corpus",
    path.join(root, "behaviours"),
    "--bindings",
    path.join(root, "unit"),
    "--driver",
    path.join(root, "unit/driver.ts"),
  ];

  assert.equal(await runCli(argv, io), 0);
  assert.equal(await runCli(argv, io), 0);
  assert.deepEqual(output.errors, []);
  assert.equal(output.logs[0], output.logs[1]);
});

test("accepts the closed project target contract", async () => {
  const root = await fixture({
    "project.json": JSON.stringify({
      name: "example",
      targets: {
        "test:unit": { options: { command: "npx vitest run --coverage --coverage.thresholds.lines=99" } },
        "test:integration": { options: { command: "node integration-runner.mjs" } },
        "test:coverage:unit": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter unit" },
        },
        "test:coverage:integration": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter integration" },
        },
        "test:coverage:behaviour": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter behaviour" },
        },
        "test:coverage": {
          options: {
            commands: [
              "npx nx run example:test:coverage:unit",
              "npx nx run example:test:coverage:integration",
              "npx nx run example:test:coverage:behaviour",
            ],
            parallel: false,
          },
        },
        "test:quick": {
          options: {
            commands: ["npx nx run example:test:unit", "npx nx run example:test:coverage"],
            parallel: false,
          },
        },
      },
    }),
  });

  assert.deepEqual(
    await validateProjectTargetContract(path.join(root, "project.json"), "example", {
      unit: {},
      integration: {},
    }),
    [],
  );
});

test("rejects runtime coverage, incomplete quick composition, and missing adapter pairs", async () => {
  const root = await fixture({
    "project.json": JSON.stringify({
      name: "example",
      targets: {
        "test:unit": { options: { command: "npx vitest run" } },
        "test:coverage:unit": { options: { command: "npx vitest run --coverage" } },
        "test:coverage:behaviour": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter behaviour" },
        },
        "test:coverage": {
          options: { command: "npx nx run example:test:unit" },
        },
        "test:quick": {
          options: {
            commands: ["npx nx run example:lint", "npx nx run example:test:unit"],
            parallel: true,
          },
        },
      },
    }),
  });

  const errors = await validateProjectTargetContract(path.join(root, "project.json"), "example", {
    unit: {},
    integration: {},
  });
  assert.ok(errors.some((error) => error.includes("requires test:integration")));
  assert.ok(errors.some((error) => error.includes("at least 99% line coverage")));
  assert.ok(errors.some((error) => error.includes("requires test:coverage:integration")));
  assert.ok(errors.some((error) => error.includes("must be static")));
  assert.ok(errors.some((error) => error.includes("must include aggregate test:coverage")));
  assert.ok(errors.some((error) => error.includes("parallel to false")));
});

test("rejects a Unit line coverage threshold below the 99% hard minimum", async () => {
  const root = await fixture({
    "project.json": JSON.stringify({
      name: "example",
      targets: {
        "test:unit": { options: { command: "npx vitest run --coverage --coverage.thresholds.lines=98" } },
        "test:coverage:unit": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter unit" },
        },
        "test:coverage:behaviour": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter behaviour" },
        },
        "test:coverage": {
          options: {
            commands: ["npx nx run example:test:coverage:unit", "npx nx run example:test:coverage:behaviour"],
            parallel: false,
          },
        },
        "test:quick": {
          options: {
            commands: ["npx nx run example:test:unit", "npx nx run example:test:coverage"],
            parallel: false,
          },
        },
      },
    }),
  });

  const errors = await validateProjectTargetContract(path.join(root, "project.json"), "example", { unit: {} });
  assert.ok(errors.some((error) => error.includes("98% is below the 99% minimum")));
});

test("accepts a 99% Coverlet Unit line coverage hard gate", async () => {
  const root = await fixture({
    "project.json": JSON.stringify({
      name: "example",
      targets: {
        "test:unit": {
          options: {
            command: "dotnet test tests/unit.fsproj /p:CollectCoverage=true /p:Threshold=99 /p:ThresholdType=line",
          },
        },
        "test:coverage:unit": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter unit" },
        },
        "test:coverage:behaviour": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter behaviour" },
        },
        "test:coverage": {
          options: {
            commands: ["npx nx run example:test:coverage:unit", "npx nx run example:test:coverage:behaviour"],
            parallel: false,
          },
        },
        "test:quick": {
          options: {
            commands: ["npx nx run example:test:unit", "npx nx run example:test:coverage"],
            parallel: false,
          },
        },
      },
    }),
  });

  assert.deepEqual(await validateProjectTargetContract(path.join(root, "project.json"), "example", { unit: {} }), []);
});

test("accepts a 99% XPlat collector Unit line coverage hard gate", async () => {
  const root = await fixture({
    "project.json": JSON.stringify({
      name: "example",
      targets: {
        "test:unit": {
          options: {
            command:
              "node scripts/dotnet-unit-coverage.mjs --project tests/unit.fsproj --results coverage --line-threshold 99",
          },
        },
        "test:coverage:unit": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter unit" },
        },
        "test:coverage:behaviour": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter behaviour" },
        },
        "test:coverage": {
          options: {
            commands: ["npx nx run example:test:coverage:unit", "npx nx run example:test:coverage:behaviour"],
            parallel: false,
          },
        },
        "test:quick": {
          options: {
            commands: ["npx nx run example:test:unit", "npx nx run example:test:coverage"],
            parallel: false,
          },
        },
      },
    }),
  });

  assert.deepEqual(await validateProjectTargetContract(path.join(root, "project.json"), "example", { unit: {} }), []);
});

test("rejects a bare line-threshold argument without the XPlat hard-gate helper", async () => {
  const root = await fixture({
    "project.json": JSON.stringify({
      name: "example",
      targets: {
        "test:unit": { options: { command: "dotnet test tests/unit.fsproj --line-threshold 99" } },
        "test:coverage:unit": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter unit" },
        },
        "test:coverage:behaviour": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter behaviour" },
        },
        "test:coverage": {
          options: {
            commands: ["npx nx run example:test:coverage:unit", "npx nx run example:test:coverage:behaviour"],
            parallel: false,
          },
        },
        "test:quick": {
          options: {
            commands: ["npx nx run example:test:unit", "npx nx run example:test:coverage"],
            parallel: false,
          },
        },
      },
    }),
  });

  const errors = await validateProjectTargetContract(path.join(root, "project.json"), "example", { unit: {} });
  assert.ok(errors.some((error) => error.includes("must enforce at least 99% line coverage")));
});

test("dedicated E2E projects do not need to own the Unit runtime", async () => {
  const root = await fixture({
    "project.json": JSON.stringify({
      name: "example-e2e",
      targets: {
        "test:e2e": { options: { command: "npx playwright test" } },
        "test:coverage:e2e": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter e2e" },
        },
        "test:coverage:behaviour": {
          options: { command: "node scripts/behaviour-coverage.mjs --adapter behaviour" },
        },
        "test:coverage": {
          options: {
            commands: ["npx nx run example-e2e:test:coverage:e2e", "npx nx run example-e2e:test:coverage:behaviour"],
            parallel: false,
          },
        },
        "test:quick": {
          options: { command: "npx nx run example-e2e:test:coverage" },
        },
      },
    }),
  });

  assert.deepEqual(
    await validateProjectTargetContract(path.join(root, "project.json"), "example-e2e", {
      unit: {},
      e2e: {},
    }),
    [],
  );
});
