# Writing a Refutation Clause That Survives Its Own Fix

[The execution rules](../../pr-review-fixer-resolution/reference/refutation-clause-execution.md)
govern what the fixer may **run**. This file governs what the specialist may **write**: whether the
clause still discriminates once the fix lands.

## The Outcome Must Follow From the Finding

**A clause's outcome must be entailed by the finding — never by the pre-fix wording or position
that merely carried it.** A clause tests the defect, or it tests a carrier of the defect. Only the
first survives a fix.

Two measured instances on PR #249:

- **C10-F3** was clause `rg -c 'strip' <path>`. The fix added the sentence "No rule strips them", so
  the clause matched the fix's own text and reported the finding refuted **by the presence of its
  fix**.
- **C11-F7** was clause `sed -n '12,22p' <path>`. The correct fix moved the sentence to line 24, so
  the clause read a region that no longer held what it was checking.

The practical test: name a literal the fix is **logically required** to add or remove. If a correct
fix could leave the pattern's match state unchanged — or could flip it for a reason unrelated to the
defect — the clause is testing a carrier. Rewrite the claim until a literal exists, or the claim is
too vague to review.

This is also why a clause is never rewritten into compliance. Weakening a precise pattern to fit the
allowed shapes produced C10-F3. A clause that cannot be expressed in the shapes means the finding
needs restating, not the clause loosening.

## When the Subject Is Not a Tracked File

Some findings have no file to read. A defect in the **PR body** is the common case, and
[the scope rule](./finding-requirements-hard-rules.md) makes it mandatory: absent, vague, or
contradicted scope is raised against the body. Review history and CI state are the same shape. Every
allowed clause reads one git-tracked regular file, so none of them applies.

Such a finding is still posted. It carries `"refutation_check": null`, names the exact reproduction
(the command or API query that produced the true value) as evidence rather than as a clause, and
lands in the consolidated review's **body** — there is no file to anchor a thread to. Its
disposition is tracked in the audit record rather than by thread resolution.

Dropping it instead is what the rules used to require, and it silently exempted the one document
that bounds every other finding's scope.

## Enforcement

None automated. A violation is visible as a disposition recording `refuted` in the same cycle the
finding's own fix landed.
