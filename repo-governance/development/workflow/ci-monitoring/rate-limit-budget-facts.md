---
description: The GitHub API rate-limit quota, reset window, and why a tight poll loop or gh run watch exhausts it.
when_to_use: Use when estimating whether a polling approach will exhaust the GitHub API rate limit.
---

# Rate Limit Budget Facts

Understanding the budget prevents accidental exhaustion.

| Parameter          | Value                                                                         |
| ------------------ | ----------------------------------------------------------------------------- |
| Primary quota      | Depends on the authenticated account and GitHub API resource                  |
| When limited       | GitHub reports the applicable limit and reset coordinates in response headers |
| Single status read | One bounded, inspectable command invocation                                   |
| `gh run watch`     | Refreshes every 3s by default; **prohibited for CI monitoring**               |

A tight loop or stream watcher performs many unnecessary refreshes and can contribute to primary or
secondary API limits when combined with other automation. At its default cadence, `gh run watch`
refreshes about 20 times per minute, or about 600 times during a 30-minute run; the repository's
2-minute cadence needs only about 15 status reads. The prohibition is therefore a resource and
observability rule, not a claim that one watcher necessarily exhausts a particular quota.
