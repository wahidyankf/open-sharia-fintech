# Bring `organiclever-www` and `wahidyankf-www` onto `output: "standalone"`

One-line summary: four of the six Next.js apps set `output: "standalone"` and two do not, so those
two images run `next start` under a resident wrapper parent — two Node processes instead of one, plus
a full `node_modules` in the final layer.

> Surfaced 2026-08-19 during the runtime-port-override delivery (PR #230), where the divergence was
> documented in `scripts/next-with-port.mjs` rather than fixed.

## Problem / context

`grep 'output.*standalone' apps/*/next.config.ts` returns 1 for `ose-www`, `ayokoding-www`,
`organiclever-app-web`, and `ose-app-web`, and 0 for `organiclever-www` and `wahidyankf-www`. That
single config line decides which of two different runtime shapes an image gets.

With `standalone`, the port wrapper runs its `--server` form: it sets `process.env.PORT` and then
`import`s the generated `server.js` into its own process, so the container holds exactly one Node
process. Without it, the wrapper must run its `start` form — Next's CLI is a separate binary and Node
has no `execve`, so the wrapper `spawn`s it and stays resident as the child's parent for the life of
the container. Both images' `CMD` show this directly: `organiclever-www` and `wahidyankf-www` pass
`"start", "-H", "0.0.0.0"`, while the four standalone images pass `"--server", "apps/<app>/server.js"`.

The cost is a second resident Node process per container and a final image carrying a full installed
`node_modules` rather than Next's traced subset. Neither is a defect — the wrapper forwards and
re-raises signals so `docker stop` still yields a conventional 128+N status, and both images serve
correctly. It is an unexplained inconsistency with a measurable price, in a set of apps that are
otherwise built the same way.

## Why now

No deadline and nothing is broken — this is filed so the divergence stops being invisible. PR #230
had to special-case it in the wrapper's own documentation to explain why two images behave
differently, which is the usual sign that an inconsistency has started costing explanation rather
than just bytes. It is also naturally bundled with the Dockerfile brief covering the same six files,
so whoever opens them next can settle both.

## Prior art / precedents

- **Next.js `output: "standalone"`** — the file-tracing mode that emits a self-contained `server.js`
  and the minimal `node_modules` subset it needs.
  [next output](https://nextjs.org/docs/app/api-reference/config/next-config-js/output)
- **Next.js official Dockerfile example** — uses `standalone` as the default containerisation path
  for exactly this reason.
  [with-docker](https://github.com/vercel/next.js/tree/canary/examples/with-docker)
- **`tini` / `dumb-init`** — the established answer to "a container has a parent process that must
  forward signals correctly", the problem the wrapper's `start` form takes on manually.
  [tini](https://github.com/krallin/tini)
- **The repo's own port wrapper** — `scripts/next-with-port.mjs`'s `PROCESS SHAPE` block already
  names these two apps as the exception.

## Proposed direction (sketch)

- Find out why the two apps diverge. It may be deliberate (a route or dependency incompatible with
  file tracing) or simply never done — and that answer decides whether this is a config change or a
  closed question.
- If nothing blocks it, add `output: "standalone"` to both configs and move their Dockerfiles onto
  the wrapper's `--server` form, matching the other four.
- If something does block it, record that reason next to the config so the divergence reads as a
  decision rather than an oversight, and close this brief.

## Rough scope & non-goals

In scope: the two `next.config.ts` files, their two Dockerfiles, and whatever verification proves
the images still serve correctly on all three viewports.

Out of scope (for now): the workspace-lib resolution failure that stops all six images building —
that is its own brief and must land first, since these images cannot currently be built to test;
changing the port contract; touching the four apps already on `standalone`.

## Risks & open questions

- Why do these two apps not set it? Unknown, and it is the question the whole brief rests on.
  (open — blocks promotion)
- Does either app depend on runtime files that Next's tracing would miss? `ose-www` needs explicit
  `outputFileTracingIncludes` for `content/` and `generated/`, so the risk is real and precedented.
  (open)
- Verification is currently impossible: the six images do not build. This brief is gated behind that
  fix regardless of its own merits.

## What success looks like + promotion signal

Success: either all six Next.js apps use `output: "standalone"` and one process shape, or the two
exceptions carry a written reason at the point of divergence — no silent third state. Ready to
promote once the image builds are fixed and the "why not" question has an answer; if the answer turns
out to be "a route genuinely cannot be traced", the right outcome is to document it and delete this
brief rather than promote it.
