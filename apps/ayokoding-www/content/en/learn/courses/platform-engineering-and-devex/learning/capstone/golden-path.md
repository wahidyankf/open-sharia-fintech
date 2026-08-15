---
title: "Golden-path brief"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

## Artifact: Harbor service-start path

**Internal customer**: a stream-aligned Harbor team starting a standard customer-facing service.

**Customer problem**: today, a team copies an old repository, asks in several channels which delivery
checks apply, and separately discovers the owner record and operational evidence it needs. The
common safe first-release path should take less coordination than that DIY route.

| Artifact field       | Filled decision                                                                                                             |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| Outcome              | A team reaches a reviewable, deployable service record with one supported path.                                             |
| Inputs               | Service name, accountable owner group, data class, runtime profile, and business-domain link.                               |
| Opinionated defaults | Standard delivery checks, container metadata, approved deployment path, ownership entry, and operational-link placeholders. |
| Product-team choices | Domain design, service behavior, release timing, and a supported runtime profile appropriate to the product.                |
| Catalog result       | Service, owner, on-call route, data class, dependencies, lifecycle, and runbook location are discoverable.                  |
| Success evidence     | Compare time-to-first-review, setup handoffs, and a post-use confidence answer against a documented DIY baseline.           |

## Escape hatch

The path supports standard request-response services. A batch, unusual runtime, or exceptional data
need uses the self-service contract's escape-hatch route: state the need, accountable owner,
affected guard-rail, and intended review date. The platform team commits to a response expectation
and reviews exception patterns quarterly. It does not require the team to pretend its service fits
the default.

## Verification

- [ ] The path's inputs are sufficient to create a useful catalog record, not a general intake form.
- [ ] The default path includes delivery and ownership evidence without deciding product policy.
- [ ] A customer can name the DIY alternative and identify at least one reduced wait or handoff.
- [ ] The off-path route is documented, owned, and treated as product feedback.

## Why this artifact matters

This brief makes a golden path testable as a platform product. It avoids the common trap of calling
a repository template a platform while leaving all of the difficult discovery and support work
unchanged. The platform provides a reusable mechanism; the customer keeps the contextual decisions
that determine whether their service serves its users well.
