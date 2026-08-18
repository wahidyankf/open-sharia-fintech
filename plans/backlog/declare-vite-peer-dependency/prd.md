# Product Requirements — Declare the `vite` Every Vitest Config Already Imports

## User Stories

### US-1 — A maintainer adding a package gets told, not surprised

**As** a maintainer adding a workspace package with a `vitest` config,
**I want** CI to fail immediately if the config imports something the package does not declare,
**so that** I learn it at review time rather than months later on an unrelated branch.

### US-2 — A reviewer can trust the manifests

**As** a reviewer,
**I want** each `package.json` to list what its own code imports,
**so that** reading the manifest tells me what the package needs without simulating npm's hoisting.

### US-3 — Declaring changes nothing that runs

**As** a maintainer applying WS-V1,
**I want** proof that adding ten declarations installs no different version anywhere,
**so that** a hygiene change cannot silently become a dependency upgrade.

### US-4 — The two repositories stay aligned

**As** a maintainer of both repositories,
**I want** the same gate in each,
**so that** the repository without it does not quietly re-accumulate what the other just cleared.

## Acceptance Criteria

### AC-1 — Every matching package declares `vite`

```gherkin
Feature: vite is a declared dependency of every package whose config imports it

  Scenario: no matching package is left undeclared
    Given every "package.json" that sits beside a "vite*.config.*" file and declares "vitest"
    When I read its dependency and devDependency maps
    Then each one declares "vite"

  Scenario: the declared range matches what the repository already resolves
    Given a package that newly declares "vite"
    When I compare the declared range against the version in that repository's lockfile
    Then the resolved version satisfies the declared range
    And the resolved version is unchanged from before the declaration
```

### AC-2 — Declaring installs nothing new

```gherkin
Feature: WS-V1 is inert

  Scenario: the lockfile gains declarations and nothing else
    Given the ten packages have been declared
    When I inspect the "package-lock.json" diff
    Then every changed line adds a "vite" declaration to a workspace package entry
    And no line changes a resolved version, integrity hash, or dependency tree

  Scenario: the test suites behave identically
    Given the ten packages have been declared
    When I run each affected package's unit tests
    Then each passes with the same test count as before the declaration
```

### AC-3 — The gate catches an undeclared config import

```gherkin
Feature: a config file may not import an undeclared module

  Scenario: an undeclared import fails the gate
    Given a workspace package whose "vitest.config.ts" imports "vite"
    And that package's "package.json" does not declare "vite"
    When the gate runs
    Then it exits non-zero
    And its output names the package and the undeclared module

  Scenario: a declared import passes the gate
    Given the same package now declares "vite"
    When the gate runs
    Then it exits zero

  Scenario: a Node builtin is not reported
    Given a config file that imports "node:path"
    When the gate runs
    Then "node:path" is not reported as undeclared

  Scenario: a relative import is not reported
    Given a config file that imports "./vitest.setup"
    When the gate runs
    Then that import is not reported as undeclared
```

### AC-4 — Both repositories carry the gate

```gherkin
Feature: cross-repository parity

  Scenario: the gate is registered in both repositories
    Given "repo-config.yml" in each repository
    When I read the gate registry
    Then both register the config-import gate with identical arguments

  Scenario: the shared implementation is byte-identical
    Given the gate's source under "apps/rhino-cli/"
    When the parity manifest is validated in both repositories
    Then it reports zero diverging files
```

## Out of Scope

- Upgrading `vite` in either repository.
- Reconciling the `vite` 7.x/8.x split between `ose-public` and `ose-private`.
- Extending the gate beyond config files to application source.
- Any change to a `vite*.config.*` file's contents.
