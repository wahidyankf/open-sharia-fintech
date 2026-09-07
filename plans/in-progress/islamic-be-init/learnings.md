# Learnings — islamic-be-init

Transient running log. Append an entry the moment something generalizable is noticed during
execution — never reconstruct this file from memory afterwards. The Knowledge Capture phase
(`delivery.md` Phase 7) drains it before archival, and nothing durable may depend on it surviving.

## Format

Each entry records what was observed, why it generalizes beyond this plan, and — once Phase 7 runs —
its terminal disposition.

```markdown
### <short title>

- **Observed**: <what happened, with the file or command that surfaced it>
- **Generalizes because**: <why this matters outside this plan>
- **Disposition**: _pending Phase 7_
```

## Entries

### Pre-execution: Go was half-provisioned, and the gap was invisible

- **Observed**: `Brewfile`, `repo-config.yml`'s gofmt gates, `scripts/verify-gofmt.sh`, and
  `rhino-cli`'s `TestCoverage.Format.Go` all survived the deletion of `a-demo-be-golang-gin`, while
  the CI job, the behaviour-coverage extractor, the tag vocabulary, and the env scanner did not.
  Nothing in the repository reported the partial state.
- **Generalizes because**: deleting the last project in a language leaves orphaned platform
  machinery that reads as working support. A future language removal or reintroduction faces the
  same trap, and a `lang:` value with no CI job routes silently into another language's job rather
  than failing loudly.
- **Disposition**: _pending Phase 7_

### Pre-execution: exclude-list CI routing fails open, not closed

- **Observed**: `pr-quality-gate.yml`'s `typescript` and `flutter` jobs select projects by
  _excluding_ known language tags rather than _including_ their own. An unrecognised `lang:` value is
  therefore picked up by both jobs instead of neither.
- **Generalizes because**: this is a fail-open default in a merge-blocking gate. Any future language
  addition inherits the same defect unless the selection is inverted to an allowlist.
- **Disposition**: _pending Phase 7_
