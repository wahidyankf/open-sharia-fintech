# IAM service / module (authentication & authorization)

One-line summary: a shared Identity and Access Management service or module providing authentication
and authorization for platform products.

> Idea, added 2026-07-21 (original capture undated).

## Problem / context

There is no shared IAM capability in the platform: authentication and authorization would have to be
reinvented per product. **Data point:** 0 products require shared auth today — the current
OrganicLever productivity work has not forced a concrete auth requirement, so there is no baseline
to measure against. This is a placeholder for a real need that has not yet materialized.

## Why now

Not yet. This idea is deliberately early and mostly open questions; it is captured so the need is not
forgotten, not because it is ready to build.

## Prior art / precedents

- **OpenID Connect / OAuth 2.0** — the standard authentication protocol a shared IAM would likely adopt
  rather than reinvent. [openid.net](https://openid.net/developers/how-connect-works/)
- **Keycloak** — established open-source IAM providing the auth(n/z) the "build vs. adopt an IdP" open
  question weighs. [keycloak.org](https://www.keycloak.org/)
- **Monorepo Structure reference** — frames the open "`apps/` service vs. `libs/` module" placement
  question. [monorepo-structure](../../docs/reference/monorepo-structure.md)

## Proposed direction (sketch)

- A dedicated IAM capability handling authentication and authorization, consumed by multiple products
  rather than each product rolling its own.
- Whether that is a service, a library, or an adopted external IdP is explicitly undecided.

## Rough scope & non-goals

In scope: shared auth(n/z) for platform products, eventually.

Out of scope (for now): everything, until a concrete product requirement exists to design against.

## Risks & open questions

- Which product drives the first real auth requirement? (open — this determines the whole shape)
- Build vs. adopt an existing identity provider? (open)
- Where does it live in the monorepo — an `apps/` service or a `libs/` module? (open)

## What success looks like + promotion signal

Success: platform products share one auth(n/z) capability instead of duplicating it. Ready to promote
only when a product has a concrete authentication/authorization requirement to design against — until
then it correctly stays an under-specified idea.
