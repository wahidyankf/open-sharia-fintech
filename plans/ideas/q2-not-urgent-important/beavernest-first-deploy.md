# BeaverNest first deploy (provision prod/stag targets)

One-line summary: provision the first real deploy targets for `beavernest-app`/`beavernest-be` —
today the deployer agents and CI caller workflows ship wired but dormant, with nothing on the
other end.

> Idea, added 2026-07-31, filed from `beaver-nest`'s `baseerah-repo-reset` plan's Product Scope §
> Out of scope. Carried into `ose-public` 2026-08-10 by the `beaver-nest-repo-consolidation` plan's
> idea-triage step as part of the BeaverNest product port; renamed from `beaver-nest-first-deploy` to
> `beavernest-first-deploy` to match this repo's single-token domain naming
> ([File Naming Convention](../../../repo-governance/conventions/structure/file-naming.md)).
> Retargeted 2026-08-18 by the `repo-clean-up` plan: the client is the Flutter `beavernest-app`, not
> the retired `beavernest-app-web` React shell.

## Problem / context

`beaver-nest`'s `baseerah-repo-reset` shipped `apps-beaver-nest-fe-deployer` and
`apps-beaver-nest-be-deployer`, plus CI caller workflows — but deliberately did not provision
anything: no Vercel project, no GHCR repository consumer, no `prod-*`/`stag-*` branch existed yet.
Now that BeaverNest lives in `ose-public` as `beavernest-app`/`beavernest-be`
(`apps-beavernest-app-deployer`, `apps-beavernest-be-deployer`), the same gap persists here:
pushing to a `prod-beavernest-app`/`stag-beavernest-be` branch today reaches nothing, because no
such branch, hosting project, or GHCR consumer exists in `ose-public` either. Both deployer agents
currently only trigger `beavernest-app-test-local-deploy-stag.yml`, which tests and stops.

## Why now

Not yet — provisioning a real deploy target is an infrastructure decision (hosting account, DNS, k3s
wiring via `ose-private`'s `coralpolyp`) that belongs to its own plan once BeaverNest has something
worth deploying beyond a readiness walking skeleton.

## Prior art / precedents

- `apps/beavernest-app/README.md` and `apps/beavernest-be/README.md` document the intended
  framework/deployment per app, per `AGENTS.md`'s Web Sites section convention.
- `.github/workflows/_reusable-be-build-deploy.yml`'s own comment already documents that the actual
  k3s rollout is orchestrated by `ose-private`'s `coralpolyp` — out of scope for this repo, and
  `coralpolyp` does not yet know about `beavernest-be` at all.
- [`beaver-nest`'s own `stag-beaver-nest-fe`](https://github.com/wahidyankf/beaver-nest/blob/main/apps/beaver-nest-fe/README.md)
  (a scheduled Vercel **preview** deploy, not production) was the only deploy-like branch wired up in
  the source repo — that was a smoke-test workflow, not a real staging environment, and did not carry
  forward into the port.

## Proposed direction (sketch)

- For `beavernest-app`: pick and provision a host for the Flutter Web build, fed by a
  `prod-beavernest-app` branch. The hosting choice is open — the Flutter client never had a Vercel
  project, so this is not a carry-over decision.
- For `beavernest-be`: provision a running consumer of the `ghcr.io/wahidyankf/ose-public` image for
  `beavernest-be` — most likely wiring `coralpolyp` (in `ose-private`) to know about `beavernest-be`
  and roll it out to k3s on push to `stag-beavernest-be`.
- Only after provisioning, re-verify both deployer agents' "Current State" sections no longer
  describe a dormant target.

## Rough scope & non-goals

In scope: the first real `prod-beavernest-app` hosting target and the first real
`stag-beavernest-be` k3s rollout via `coralpolyp`.

Out of scope (for now): any change to the deployer agents' push-based mechanism itself — that part
already works and is real; only the receiving end is missing.

## Risks & open questions

- Does `coralpolyp` need BeaverNest-specific changes, or just a config entry? (open)
- Which host serves the Flutter Web build, and is it provisioned manually (a `[HUMAN]` step) or can
  it be automated? Account/billing implications likely make this a human step.
- Does the current readiness-only content warrant a real deploy yet, or should this wait for the
  first real feature (see [beavernest-persistence-layer](../q4-not-urgent-not-important/beavernest-persistence-layer.md))?

## What success looks like + promotion signal

Success: a real, working `prod-beavernest-app` URL and a real running `beavernest-be` staging
server, with both deployer agents' files updated to drop their "no target provisioned" caveats.
Ready to promote once a maintainer decides BeaverNest is ready for a first live deploy — until then
it correctly stays an under-specified idea.
