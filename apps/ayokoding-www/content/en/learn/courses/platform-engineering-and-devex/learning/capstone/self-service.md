---
title: "Self-service contract"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

## Artifact: Development database capability

**Internal customer**: a Harbor product team that needs a routine development database without an
operations ticket.

| Contract field      | Filled decision                                                                                                          |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Capability          | Provision a development database from an approved profile.                                                               |
| Eligible input      | Catalog owner, approved development data class, size within quota, private network selection, and expiry.                |
| Default outcome     | Tagged private database, standard backup posture, ownership record, and a link to support guidance.                      |
| Guard-rails         | No public endpoint, capped size, approved data class, mandatory owner, default expiry, and protected production profile. |
| Service expectation | Status visible to the requester; documented support channel; published change notice for material default changes.       |
| Non-goals           | It does not decide a product's data model, waive data policy, or provision an unbounded production system.               |

## Escape hatch and exception record

| Field                 | Required entry                                                                                        |
| --------------------- | ----------------------------------------------------------------------------------------------------- |
| Trigger               | The request exceeds a published profile or needs a different data, availability, or network boundary. |
| Rationale             | Why the common capability cannot meet the customer need.                                              |
| Accountable owner     | Product and, where relevant, data or risk owner.                                                      |
| Compensating boundary | Proposed controls and a review or expiry date.                                                        |
| Decision              | Named reviewer, response expectation, and link back to the catalog record.                            |

## Verification

- [ ] A normal request is ticket-free and results in an owned resource within documented limits.
- [ ] An invalid request explains the failing guard-rail and points to a safe alternative or exception.
- [ ] The contract lists inputs, defaults, support expectation, non-goals, and an escape hatch.
- [ ] The exception produces a reviewable learning signal; it is not an untracked private agreement.

## Why this artifact matters

The contract turns a recurring approval into a product interface. It makes the safe case fast while
preserving judgment for a request that genuinely has different consequences. These guard-rails are
platform mechanisms; they should implement shared safety boundaries, not become a way for the
platform team to dictate every product decision.
