# Make BeaverNest local full-stack development one command

One-line summary: make the advertised BeaverNest development command own its safe local data,
start the same-origin Flutter and F# runtime, and provide a practical edit-and-verify loop.

> Idea, added 2026-08-18 after manually verifying the Week 39 BeaverNest runtime.

## Problem / context

`npm run beavernest:dev` delegates directly to a full Docker Compose build. On 2026-08-18, both
default bind sources (`/tmp/beavernest-unconfigured-data` and
`/tmp/beavernest-unconfigured-backups`) were absent while Compose declared
`create_host_path: false`, so the advertised command did not own its startup prerequisites. The
Flutter project exposed 14 Nx targets but no `dev` or `serve` target. Its cold image build also
downloaded the pinned Flutter builder and then started a separate FVM local-mirror clone. The
verified fallback required building Flutter on the host, generating and publishing the backend,
copying `build/web` into a temporary `wwwroot`, setting four runtime variables, and starting the
published DLL. The resulting UI and three API probes returned HTTP 200, and the hosted-bundle
Chromium E2E scenario passed: the product path works, but the developer path is fragmented.

## Why now

BeaverNest now has a real hosted Flutter client and an active browser-chat plan, so frontend and
backend iteration will become routine rather than occasional. This does not block current work—the
combined runtime is functional—but leaving the setup implicit makes each new worktree rediscover
the same lifecycle and encourages unreviewed local launch recipes.

## Prior art / precedents

- [`run-e2e.sh`](../../../apps/beavernest-be/scripts/run-e2e.sh) already creates isolated data and
  backup directories, selects a free port, owns cleanup, waits for readiness, and can reuse an
  existing runtime.
- [`organiclever-app-web`](../../../apps/organiclever-app-web/README.md) exposes a documented Nx
  `dev` target and a direct first-run path, while keeping build and quality commands separate.
- [The current BeaverNest client README](../../../apps/beavernest-app/README.md) preserves the
  important production invariant: Flutter uses relative API routes and the F# host serves the
  bundle as one same-origin runtime.

## Proposed direction (sketch)

- Give the root development command ownership of safe data/backup directory creation, environment
  setup, readiness reporting, shutdown, and cleanup or retention semantics.
- Define one supported edit loop for Flutter plus F#: either a same-origin development proxy with
  hot reload or a bounded rebuild/restart path that remains visibly different from production.
- Keep the reproducible combined image, but avoid duplicate Flutter acquisition in the common local
  loop and document when developers should choose host, container, or existing-runtime modes.

## Rough scope & non-goals

In scope: the BeaverNest root/Nx development entry point, local directory lifecycle, same-origin
frontend/backend serving, focused regression coverage, and one complete local-run guide.

Out of scope (for now): production Compose or deployment behavior, product features, changing the
relative API contract, and a repository-wide development-server abstraction.

## Risks & open questions

- Can Flutter Web hot reload sit behind the F# same-origin boundary without weakening the behavior
  that production and browser E2E currently verify?
- Should local SQLite data persist across runs by default, or should the command require an explicit
  durable path and otherwise use disposable storage?
- Is the duplicate SDK acquisition best removed from the Dockerfile, bypassed only in a host-fast
  path, or retained as a deliberate reproducibility cost?
- Should one command own both watch processes, or should a small launcher coordinate independently
  invokable frontend and backend targets?

## What success looks like + promotion signal

Success means a clean worktree can run one documented command without pre-creating bind directories,
open the Flutter UI and ready API on the documented URL, observe a supported source-edit loop, and
stop without orphaning listeners or ambiguous data. Promote this idea once the maintainer chooses
the host-versus-container development architecture and the default persistence policy; those two
decisions determine the regression scenarios and delivery boundary.
