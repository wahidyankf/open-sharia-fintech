# Claude Code agent catalog

This directory is the canonical catalog of the AI agents that help maintain Open
Sharia Enterprise. It exists to make a large workspace easier to navigate: pick
the outcome you need, then open the agent whose filename matches that job. 🤖

Start with [AGENTS.md](../../AGENTS.md) for repository rules and
[the skills catalog](../skills/README.md) for reusable guidance. Agents execute
work; skills provide the focused knowledge they use.

## Choose an agent by outcome

| If you need to…                                | Start with                                                                | Then use when needed                                                                        |
| ---------------------------------------------- | ------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Create or improve reader-facing material       | [`docs-maker`](docs-maker.md) or [`readme-maker`](readme-maker.md)        | A tutorial, site-content, or social-content maker for the specific format                   |
| Verify an artifact before it moves forward     | The matching `*-checker` agent                                            | A `*-fixer` agent after a concrete finding exists                                           |
| Plan a multi-step delivery                     | [`plan-maker`](plan-maker.md)                                             | [`plan-checker`](plan-checker.md) and [`plan-execution-checker`](plan-execution-checker.md) |
| Change application or test code                | The matching `swe-*-dev` agent                                            | [`swe-code-checker`](swe-code-checker.md) or a focused UI/E2E agent                         |
| Research a changing external fact              | [`web-researcher`](web-researcher.md)                                     | A domain maker to apply the cited result                                                    |
| Evaluate a live experience without changing it | A `web-*-tester` or [`api-exploratory-tester`](api-exploratory-tester.md) | A plan agent to turn durable findings into work                                             |
| Review a pull request                          | [`pr-review-scout-maker`](pr-review-scout-maker.md)                       | The PR-review specialists, synthesis agent, then [`pr-review-fixer`](pr-review-fixer.md)    |

The filenames in this directory are the live catalog. Do not treat this table
as a complete roster: new focused agents can be added without making this
overview stale.

## How the roles fit together

Most delivery work follows a small, understandable loop:

```text
maker or dev → checker → fixer (only when a finding needs a change)
```

- A **maker** creates a document, plan, or other content artifact.
- A **dev** changes an application, test, or implementation surface.
- A **checker** validates an artifact against its documented standard.
- A **fixer** addresses validated findings instead of reopening the whole task.
- A **tester** explores a running product and reports what a reader or user
  experiences; it does not silently change the product.
- A **researcher** gathers current external evidence and returns it with
  sources; it does not edit the workspace.

## Naming and definition format

Each agent filename follows `<scope>(-<qualifier>)*-<role>`. The allowed roles
and their meanings live in the
[Agent Naming Convention](../../repo-governance/conventions/structure/agent-naming.md).
Use the existing neighbor agent as the starting point for a new definition and
follow [the agent-development skill](../skills/agent-developing-agents/SKILL.md).

Agent files use YAML frontmatter for their name, purpose, allowed tools, model
tier, color, and skills. Keep the description practical: it should tell a
reader when the agent is the right choice, not merely restate its filename.

## Source and generated bindings

Edit agent definitions in this directory only. Platform-specific mirrors are
generated from the primary binding; never hand-edit a mirror. After a
definition changes, run `npm run generate:bindings` and then
`npm run validate:sync`. Keep generated files in the same commit as their
source change.

This README is a navigation aid, not an agent definition. The complete
cross-harness model is documented in
[Platform bindings](../../docs/reference/platform-bindings.md).

## Useful references

- [AI agents](../../repo-governance/development/agents/ai-agents.md) — roles,
  ownership, and operating expectations
- [Maker–Checker–Fixer](../../repo-governance/development/pattern/maker-checker-fixer.md)
  — the delivery pattern
- [Agent catalog convention](../../repo-governance/conventions/structure/agent-naming.md)
  — naming rules and schema
- [Skills catalog](../skills/README.md) — reusable on-demand guidance

## Complete catalog

The outcome guide above is the quickest way to choose an agent. This complete
linked catalog keeps every definition discoverable without making the guide
pretend that a short list is the whole roster.

- [agent-maker](agent-maker.md)
- [api-exploratory-tester](api-exploratory-tester.md)
- [apps-ayokoding-www-annotated-concept-checker](apps-ayokoding-www-annotated-concept-checker.md)
- [apps-ayokoding-www-annotated-concept-fixer](apps-ayokoding-www-annotated-concept-fixer.md)
- [apps-ayokoding-www-annotated-concept-maker](apps-ayokoding-www-annotated-concept-maker.md)
- [apps-ayokoding-www-by-example-checker](apps-ayokoding-www-by-example-checker.md)
- [apps-ayokoding-www-by-example-fixer](apps-ayokoding-www-by-example-fixer.md)
- [apps-ayokoding-www-by-example-maker](apps-ayokoding-www-by-example-maker.md)
- [apps-ayokoding-www-deployer](apps-ayokoding-www-deployer.md)
- [apps-ayokoding-www-facts-checker](apps-ayokoding-www-facts-checker.md)
- [apps-ayokoding-www-facts-fixer](apps-ayokoding-www-facts-fixer.md)
- [apps-ayokoding-www-general-checker](apps-ayokoding-www-general-checker.md)
- [apps-ayokoding-www-general-fixer](apps-ayokoding-www-general-fixer.md)
- [apps-ayokoding-www-general-maker](apps-ayokoding-www-general-maker.md)
- [apps-ayokoding-www-in-the-field-checker](apps-ayokoding-www-in-the-field-checker.md)
- [apps-ayokoding-www-in-the-field-fixer](apps-ayokoding-www-in-the-field-fixer.md)
- [apps-ayokoding-www-in-the-field-maker](apps-ayokoding-www-in-the-field-maker.md)
- [apps-ayokoding-www-link-checker](apps-ayokoding-www-link-checker.md)
- [apps-ayokoding-www-link-fixer](apps-ayokoding-www-link-fixer.md)
- [apps-ayokoding-www-primer-checker](apps-ayokoding-www-primer-checker.md)
- [apps-ayokoding-www-primer-fixer](apps-ayokoding-www-primer-fixer.md)
- [apps-ayokoding-www-primer-maker](apps-ayokoding-www-primer-maker.md)
- [apps-organiclever-app-web-deployer](apps-organiclever-app-web-deployer.md)
- [apps-organiclever-www-deployer](apps-organiclever-www-deployer.md)
- [apps-ose-app-web-deployer](apps-ose-app-web-deployer.md)
- [apps-ose-www-content-checker](apps-ose-www-content-checker.md)
- [apps-ose-www-content-fixer](apps-ose-www-content-fixer.md)
- [apps-ose-www-content-maker](apps-ose-www-content-maker.md)
- [apps-ose-www-deployer](apps-ose-www-deployer.md)
- [apps-wahidyankf-www-deployer](apps-wahidyankf-www-deployer.md)
- [apps-web-ui-storybook-deployer](apps-web-ui-storybook-deployer.md)
- [ci-checker](ci-checker.md)
- [ci-fixer](ci-fixer.md)
- [docs-checker](docs-checker.md)
- [docs-file-manager](docs-file-manager.md)
- [docs-fixer](docs-fixer.md)
- [docs-link-checker](docs-link-checker.md)
- [docs-maker](docs-maker.md)
- [docs-software-engineering-separation-checker](docs-software-engineering-separation-checker.md)
- [docs-software-engineering-separation-fixer](docs-software-engineering-separation-fixer.md)
- [docs-tutorial-checker](docs-tutorial-checker.md)
- [docs-tutorial-fixer](docs-tutorial-fixer.md)
- [docs-tutorial-maker](docs-tutorial-maker.md)
- [pdf-to-md-checker](pdf-to-md-checker.md)
- [pdf-to-md-fixer](pdf-to-md-fixer.md)
- [pdf-to-md-maker](pdf-to-md-maker.md)
- [plan-checker](plan-checker.md)
- [plan-execution-checker](plan-execution-checker.md)
- [plan-fixer](plan-fixer.md)
- [plan-maker](plan-maker.md)
- [pr-review-architecture-maker](pr-review-architecture-maker.md)
- [pr-review-docs-maker](pr-review-docs-maker.md)
- [pr-review-fixer](pr-review-fixer.md)
- [pr-review-governance-maker](pr-review-governance-maker.md)
- [pr-review-instruction-maker](pr-review-instruction-maker.md)
- [pr-review-integrity-maker](pr-review-integrity-maker.md)
- [pr-review-logic-maker](pr-review-logic-maker.md)
- [pr-review-performance-maker](pr-review-performance-maker.md)
- [pr-review-scout-maker](pr-review-scout-maker.md)
- [pr-review-security-maker](pr-review-security-maker.md)
- [pr-review-synthesis-maker](pr-review-synthesis-maker.md)
- [pr-review-types-maker](pr-review-types-maker.md)
- [readme-checker](readme-checker.md)
- [readme-fixer](readme-fixer.md)
- [readme-maker](readme-maker.md)
- [repo-harness-compatibility-checker](repo-harness-compatibility-checker.md)
- [repo-harness-compatibility-fixer](repo-harness-compatibility-fixer.md)
- [repo-rules-checker](repo-rules-checker.md)
- [repo-rules-fixer](repo-rules-fixer.md)
- [repo-rules-maker](repo-rules-maker.md)
- [repo-setup-manager](repo-setup-manager.md)
- [repo-workflow-checker](repo-workflow-checker.md)
- [repo-workflow-fixer](repo-workflow-fixer.md)
- [repo-workflow-maker](repo-workflow-maker.md)
- [social-linkedin-post-maker](social-linkedin-post-maker.md)
- [specs-checker](specs-checker.md)
- [specs-fixer](specs-fixer.md)
- [specs-maker](specs-maker.md)
- [swe-code-checker](swe-code-checker.md)
- [swe-csharp-dev](swe-csharp-dev.md)
- [swe-e2e-dev](swe-e2e-dev.md)
- [swe-fsharp-dev](swe-fsharp-dev.md)
- [swe-golang-dev](swe-golang-dev.md)
- [swe-rust-dev](swe-rust-dev.md)
- [swe-typescript-dev](swe-typescript-dev.md)
- [swe-ui-checker](swe-ui-checker.md)
- [swe-ui-fixer](swe-ui-fixer.md)
- [swe-ui-maker](swe-ui-maker.md)
- [web-design-tester](web-design-tester.md)
- [web-exploratory-tester](web-exploratory-tester.md)
- [web-researcher](web-researcher.md)
- [web-usability-tester](web-usability-tester.md)
