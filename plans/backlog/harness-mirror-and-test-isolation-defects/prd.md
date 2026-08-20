# Product Requirements — Harness Mirror and Test-Isolation Defects

## User Stories

### US-1 — A binding directory contains only what the harness should load

**As a** developer opening OpenCode in this repository
**I want** the agent picker to list only real agents
**So that** the roster I see matches the roster this repository claims to publish.

```gherkin
Feature: Binding directories carry no non-agent files

  Scenario: The generated OpenCode agent directory holds only agent definitions
    Given the bindings have been generated
    When every tracked file under ".opencode/agents" is enumerated
    Then each one carries agent frontmatter with a "name" key

  Scenario: An index file emitted into a globbed agent directory is a finding
    Given a file "README.md" exists under a harness's globbed agent directory
    When rhino-cli harness bindings validate runs
    Then the command exits with a failure code
    And the output names that file and states that the directory is globbed by the harness
```

### US-2 — Every test states its own repository root

**As a** developer adding a test to `rhino-cli`
**I want** each test to declare the tree it operates on
**So that** adding a test cannot make an unrelated sibling fail.

```gherkin
Feature: Command smoke tests are independent of the process working directory

  Scenario: A generate smoke test names its own root
    Given a temporary repository fixture
    When the generate command runs against that fixture explicitly
    Then it operates on the fixture and not on the process working directory

  Scenario: The suite is order-independent
    Given the full rhino-cli test suite
    When it runs under the default parallel runner three times
    Then every run reports the same set of passing tests
```

### US-3 — Skill-tree links resolve

**As an** agent loading a skill
**I want** every anchor in that skill to resolve
**So that** a reference does not send me to a heading that no longer exists.

```gherkin
Feature: Skill trees carry no dangling anchors

  Scenario: The skill sources validate with the exemption lifted
    Given the skill-tree link exemption is temporarily disabled
    When rhino-cli md links validate runs over ".claude/skills"
    Then it reports zero dangling anchors

  Scenario: The repo-wide baseline is not made worse
    Given the repair has landed
    When rhino-cli md links validate runs with the registered exclusions
    Then the broken-link count is no greater than the recorded baseline
```

## Acceptance Criteria

| ID   | Criterion                                                                          | Pre-change                                | Post-change                      |
| ---- | ---------------------------------------------------------------------------------- | ----------------------------------------- | -------------------------------- |
| AC-1 | `opencode agent list` names no agent called `README`                               | one such entry among 94 repository agents | zero                             |
| AC-2 | A non-agent file under a globbed agent directory fails `harness bindings validate` | exits 0                                   | exits 1 naming the file          |
| AC-3 | Two `run(...)` generate smoke tests coexist with `harness_unknown_name_is_error`   | sibling fails under parallelism           | all pass, three consecutive runs |
| AC-4 | `md links validate` over `.claude/skills` with the exemption lifted                | 47 dangling anchors across 22 files       | 0                                |
| AC-5 | Repo-wide broken-link count with registered exclusions                             | 312                                       | no greater than 312              |

Each criterion states both directions: a criterion that cannot fail before the change is not a
criterion. AC-4's pre-change figure is reproducible by disabling `SKILL_TREE_MARKERS` in
`apps/rhino-cli/src/application/docs/links.rs` and re-running the validator.

## Out of Scope

The `.agents/skills/` mirror layout — Codex reads it as a skill root and it carries no index file of
the shape WS-H1 describes. The eight vendored plugin skill directories, which this repository
neither authors nor regenerates.
