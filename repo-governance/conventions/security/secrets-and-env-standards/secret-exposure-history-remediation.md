---
description: The mandatory five-step incident procedure for a secret found in committed Git history — contain and rotate, inventory, rewrite, replace remote state, replace the PR.
when_to_use: Use immediately when a suspected or confirmed secret is found anywhere in committed Git history, including a PR diff.
---

# Secret-Exposure History Remediation

A suspected or confirmed secret in committed history is a security incident. Do not treat deleting a
file in a later commit, redacting a PR comment, or closing the PR as remediation: the secret remains
reachable in Git history and can remain visible in the PR diff.

Execute this procedure automatically under the repository's standing incident policy. Do not expose
the value while doing so; all evidence must use sanitized commit identifiers, ref names, paths, and
provider case references only.

1. **Contain and rotate.** Revoke, disable, or rotate the credential at its provider before relying
   on a Git rewrite. Treat the old value as compromised even if the repository is private.
2. **Inventory reachability.** Identify every affected reachable ref, including the PR head branch,
   target branches, tags, releases, and repository-owned mirrors or sibling refs that contain the
   contaminated commit. Keep unrelated concurrent branches out of the incident worktree.
3. **Rewrite all affected history.** From an isolated incident worktree, use a reviewed secret-removal
   tool to remove the exposure from every identified reachable ref. A partial branch-only rewrite is
   not complete when the commit is still reachable from a tag, target branch, or PR ref.
4. **Replace remote state.** Verify the rewritten objects contain neither the secret nor its exposed
   file/path representation, force-push affected refs with `--force-with-lease`, and delete
   contaminated remote branches and tags. The exception in
   [Git Push Safety](../../../development/workflow/git-push-safety/rule.md#secret-exposure-history-remediation-exception)
   authorizes only these necessary lease-protected pushes; never use `--no-verify`.
5. **Replace the PR and complete external cleanup.** Close the contaminated PR, open a replacement PR
   from clean history, and run its normal required checks. Request provider-side purge of cached PR
   diffs and repository views where available. State accurately that external clones, forks, mirrors,
   and third-party caches cannot be erased by the repository; rotation remains the real containment.

No normal merge proceeds while a contaminated ref or PR remains reachable. The remediation record
must never include a secret value, matching fragment, command line containing it, or copied diff.
