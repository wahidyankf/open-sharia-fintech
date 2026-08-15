# Path Manifests

This directory is the machine-consumed source of truth for path manifests: nested
`<path-id>.yaml` data files, one per path. A slash in a path ID becomes a nested directory — for
example, `careers/interview-ready/software-engineer` lands at
`manifests/careers/interview-ready/software-engineer.yaml`.

Ownership is split per category, not directory-wide: `ayokoding-learning-path-12-careers-se-manifests`
and `ayokoding-learning-path-13-careers-ai-manifest` jointly own the `careers/` subtree; plans
`ayokoding-learning-path-14` through `ayokoding-learning-path-18` own the sibling `skills/`
subtree. This plan (`ayokoding-learning-path-02-schema-and-prerequisite-dag`) creates this directory
and nothing else in it — no manifest data file ships here as part of this plan.

Each manifest must validate against `PathManifestSchema` in
[`../core/schemas.ts`](../core/schemas.ts).
