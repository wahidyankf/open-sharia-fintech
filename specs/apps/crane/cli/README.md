# Crane CLI — Specification Corpus

Audience: engineers and technical product managers working on
[`apps/crane-cli`](../../../../apps/crane-cli/README.md) — the Content Retrieval And Normalization
Engine.

This corpus is the single source of truth for what `crane-cli` does. A scenario here defines the
command's accepted arguments, the JSON it writes to stdout, and its exit code.

## Contents

- [Architecture](./architecture.md) — the current as-built system: its context, the one binary it
  ships, its ports-and-adapters interior, and the constraints that bind them.
- [Behaviours](./behaviours/README.md) — the recursive Gherkin corpus, grouped by command family.

## Consumers

Crane's output is read by the `pdf-to-md` agents and by the quality-gate workflow, so a change to
the shape of a command's JSON is a change to a contract, not an implementation detail. A scenario
that asserts a field is the record of that contract.

## Related

- [`apps/crane-cli/README.md`](../../../../apps/crane-cli/README.md) — the implementing project.
- [BDD Spec-to-Test Mapping Convention](../../../../repo-governance/development/infra/bdd-spec-test-mapping.md) —
  the repository-wide rule this corpus follows.
