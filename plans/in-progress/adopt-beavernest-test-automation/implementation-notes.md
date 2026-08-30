# Implementation Notes

This is the plan's only tracked execution-evidence aggregate. Raw command output, fixtures produced
only for inspection, lifecycle controls, GitHub responses, and audit manifests remain under the
ignored `local-tmp/adopt-beavernest-test-automation/evidence/runtime/` roots defined in
[delivery.md](./delivery.md).

During delivery, append one tab-separated `EVIDENCE` row for each completed action:

```text
EVIDENCE<TAB>binding<TAB>task-id<TAB>command-or-manual-proof<TAB>exit-or-terminal-state<TAB>raw-evidence-path<TAB>head-or-working-tree-SHA
```

Rows are replaced only by the same `binding + task-id`; a later binding never rewrites an earlier
binding's row. Do not place secrets, raw private content, or copied command output here. Phase 22
adds only sanitized public/private lifecycle hashes and counts. `delivery.md` and this file are
mandatory changed plan-state paths in every public delivery. `learnings.md` is reserved in every
prospective allocation and is included in the actual Git union only when that delivery records a
new as-you-go learning.
