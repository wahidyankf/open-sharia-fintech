# Idea Grooming — Procedure

## Procedure

Run the workflow's ten steps in order. The ordering constraints that actually matter:

1. **Inventory** every repo before deciding anything.
2. **Within-repo dedup** first, then **cross-repo dedup** — and resolve **residency before merging**,
   so a merge lands in the correct repo rather than wherever the pair was compared.
3. **Residency**, three rules, first match wins:
   - **R1** the idea needs a real secret, credential, or live infra-state value to be actionable →
     the infra-private repo, and no other.
   - **R2** it names a file, app, or concern that **provably** exists in exactly one repo → that repo
     only. Verify with `Glob` / `test -f` against each tree; **never** infer this from the brief's prose.
   - **R3** otherwise → the generalizable cross-cutting-governance default repo.
     Log the matched rule for **every** surviving idea, including "already correctly resident".
4. **Relocation** is fail-safe-toward-duplication: write the final file at the destination, commit
   and push, **verify it on the destination's `origin/main`**, and only then delete the source. If
   verification fails, stop before the delete and log the duplication in both repos' logs.
5. **Reshape** every survivor to the eight-section two-pager template, preserving content.
6. **Provenance**: append `Relocated from …` / `Renamed from …` to the file's **existing** blockquote,
   never overwriting it. Record every action in the repo's own `## Grooming Log`.
7. **Classify** with both rubrics — urgency from _Why now_ only; importance from the full content.
8. **Link rewrite** covers move, rename, and move-plus-rename as one mechanism: fix the moved file's
   own links, then grep the repo for inbound links to the old path. Cross-repo references become
   absolute `https://github.com/<org>/<repo>/blob/main/…` URLs.
9. Append `> Last groomed: YYYY-MM-DD` so the recurrence trigger stays armed.
