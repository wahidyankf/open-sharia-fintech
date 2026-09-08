---
description: "The narrow exceptions for CI-availability outages, not code defects."
when_to_use: "Use when CI itself is unavailable, not merely reporting a failure."
---

# Operational CI-Availability Exceptions

The code-quality carve-out above is not a blanket license to proceed on a red or missing CI gate.
It is narrow, and every use of it must independently satisfy all of the following before a merge
proceeds without a completed CI-gate confirmation:

1. **Root-cause the failure signature, don't assume.** Distinguish the actual shape before treating
   it as operational rather than a code regression. Observed signatures include:
   - **Job cancellation mid-run**, with a rerun stuck `queued` for an extended period.
   - **No workflow run created at all** (`total_count: 0` on the commit's combined status) --
     consistent with a webhook-delivery outage, not a cancelled run.
   - **A generic, identical failure across many otherwise-unrelated matrix legs**, traced to a
     shared setup step (a composite action, a provisioning script) rather than to the gate logic
     each leg actually exercises -- confirm the shared step was not touched by the change under
     review, and that the same workflow passed cleanly on the same branch recently.
2. **Verify the external cause live, every time -- never reuse a prior check's conclusion.** An
   outage that was active an hour ago may have resolved; a runner pool that was healthy an hour ago
   may not be now. Check the authoritative status source (e.g. `githubstatus.com` for GitHub-wide
   incidents, `gh api .../actions/runners` for self-hosted pool health) fresh, immediately before
   deciding to bypass -- not from memory of an earlier check in the same session.
3. **Confirm the higher-value gate still ran.** The CI-gate confirmation step is one layer; the
   review-cycle discipline (specialist review, fixer, thread resolution) is a separate, higher-value
   layer. This exception covers only the former. Never skip the latter to work around the former.
4. **Confirm no enforced required-status-check is actually bypassed.** If branch protection enforces
   the CI gate as a required check, this exception does not apply without an explicit admin override
   decision, which is a different (and more consequential) action than proceeding on an unenforced
   branch.
5. **Record the instance.** Each use of this exception is a discrete, justified decision, not a
   standing policy inferred from a prior instance -- document the failure signature, the live
   verification performed, and why the decision holds for this instance specifically.

A runner-host or provisioning-step failure that persists across otherwise-unrelated PRs or branches
(rather than resolving on its own) is not covered by this exception once identified as persistent --
it becomes an ordinary infrastructure defect requiring a `[HUMAN]` fix at the host/infra level, filed
and tracked like any other blocking issue, not repeatedly bypassed.
