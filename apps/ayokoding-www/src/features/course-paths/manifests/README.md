# Path Manifests

This directory is the machine-consumed source of truth for path manifests: nested
`<path-id>.yaml` data files, one per path. A slash in a path ID becomes a nested directory — for
example, `careers/interview-ready/software-engineer` lands at
`manifests/careers/interview-ready/software-engineer.yaml`.

Every `.yaml` file in this directory is owned by
`ayokoding-learning-path-05-manifests` and by no other plan. This plan
(`ayokoding-learning-path-02-schema-and-prerequisite-dag`) creates this directory and nothing else
in it — no manifest data file ships here as part of this plan.

Each manifest must validate against `PathManifestSchema` in
[`../core/schemas.ts`](../core/schemas.ts).
