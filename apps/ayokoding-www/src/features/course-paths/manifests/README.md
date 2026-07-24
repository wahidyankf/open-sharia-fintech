# Path Manifests

This directory is the machine-consumed source of truth for path manifests: nested
`<path-id>.yaml` data files, one per path. A slash in a path ID becomes a nested directory — for
example, `careers/interview-ready/software-engineer` lands at
`manifests/careers/interview-ready/software-engineer.yaml`.

Ownership is split per category, not directory-wide: `ayokoding-learning-path-05-manifests` owns
every `.yaml` under `careers/`; `ayokoding-learning-path-06-skills-accounting` and
`ayokoding-learning-path-07-skills-erp` together own the sibling `skills/` subtree. See
`ayokoding-learning-path-05-manifests`'s own README for the full, authoritative ruling. This plan
(`ayokoding-learning-path-02-schema-and-prerequisite-dag`) creates this directory and nothing else
in it — no manifest data file ships here as part of this plan.

Each manifest must validate against `PathManifestSchema` in
[`../core/schemas.ts`](../core/schemas.ts).
