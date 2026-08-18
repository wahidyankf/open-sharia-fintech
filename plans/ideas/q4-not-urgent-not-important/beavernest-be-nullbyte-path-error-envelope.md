# beavernest-be null-byte-path error envelope

One-line summary: a request whose path contains an invalid percent-encoded byte (e.g. `%00`) gets a
bare, bodyless `400 Bad Request` from Kestrel instead of `beavernest-be`'s usual `{"error": "..."}`
envelope — fixing it requires replacing the ASP.NET Core server, which is out of proportion to the
defect.

> Idea, added 2026-08-01, filed from `beaver-nest`'s `beaver-nest-rebrand` plan's Phase 16 Rule-16
> API exploratory retest (finding AET-001). Carried into `ose-public` 2026-08-10 by the
> `beaver-nest-repo-consolidation` plan's idea-triage step as part of the BeaverNest product port;
> renamed from `beaver-nest-be-nullbyte-path-error-envelope` to
> `beavernest-be-nullbyte-path-error-envelope` to match this repo's single-token domain naming
> ([File Naming Convention](../../../repo-governance/conventions/structure/file-naming.md)).

## Problem / context

`GET /api/v1/hello%00` (a URL-encoded null byte in the path) returns `HTTP/1.1 400 Bad Request` with
an empty body, no `Content-Type` header, and `Connection: close` — every other non-2xx response this
API returns (unknown path, wrong method, malformed query, etc.) carries the uniform
`{"error": "<message>"}` envelope described in
`specs/apps/beavernest/containers/contracts/openapi.yaml › components.schemas.Error`. This one path
breaks that convention.

Root cause: the request is rejected by Kestrel's own HTTP/1.1 request-target parser
(`BadHttpRequestException`, `RequestRejectionReason.InvalidRequestTarget`) **before**
`IHttpApplication.ProcessRequestAsync` is ever invoked — i.e. before any ASP.NET Core middleware,
including `UseExceptionHandler` or a custom `app.Use(...)` wrapper registered in
`apps/beavernest-be/src/BeaverNestBe/WebApp.fs` / `Program.fs`, gets a chance to run for that
connection. Kestrel writes the raw 400 and closes the connection itself. This is documented,
version-independent Kestrel behavior — not specific to this app, Giraffe, or the originating
`beaver-nest-rebrand` plan.

## Why now

Not yet — Minor severity, Low priority. Reachable only via a hand-crafted malformed URL; no real
client (including `beavernest-app`'s generated OpenAPI contract client) can ever produce this
input.

## Prior art / precedents

- `specs/apps/beavernest/containers/contracts/openapi.yaml` — the `Error` schema this endpoint
  should (but currently cannot, for this one input class) conform to on every non-2xx path.
- `apps/beavernest-be/src/BeaverNestBe/WebApp.fs` — the existing `notFoundHandler` this defect's fix
  would need to somehow reach, if a fix is ever attempted.
- Well-known ASP.NET Core/Kestrel behavior (multiple public `dotnet/aspnetcore` GitHub issues)
  confirm requests with control characters in the request-target are rejected by the HTTP/1.1 parser
  itself, ahead of the middleware pipeline.

## Proposed direction (sketch)

Two options, neither obviously worth it at current severity:

1. Swap Kestrel for a different `IServer` implementation (e.g. `HttpSys` on platforms where it's
   available) that exposes a hook for this class of malformed request — large blast radius for a
   readiness-only walking-skeleton API.
2. Write a custom `IConnectionListenerFactory`/raw-stream interceptor ahead of HTTP/1.1 parsing —
   high engineering cost for a Minor/Low finding.

Neither is recommended unless a real client is ever found to produce this input class.

## Rough scope & non-goals

In scope: deciding whether this is worth fixing at all, and if so, which of the two directions above.

Out of scope: any change to `beavernest-app` or its generated contract client (neither can
produce this input).

## Risks & open questions

- Is there a lower-cost mitigation neither option above captures (e.g. a reverse proxy in front of
  Kestrel in production that normalizes malformed requests before they reach the app)? (open — no
  production deploy target exists yet for `beavernest-be`, see
  [beavernest-first-deploy](../q2-not-urgent-important/beavernest-first-deploy.md))
- Does this matter at all before `beavernest-be` has a real production deploy target and real
  clients? (open — leans toward "no")

## What success looks like + promotion signal

Success: `GET /api/v1/hello%00`-class requests return the standard `Error` envelope like every other
non-2xx response. Ready to promote only if a maintainer decides this edge case is worth the
engineering cost above — until then it correctly stays an under-specified, low-priority idea.
