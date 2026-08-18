# Business Requirements — File Naming Convention Rework

## Business Goal

Make the two filename conventions say what the repository actually enforces, so that reading the rule
and running the gate produce the same answer.

## Why It Matters

A convention is only worth its enforcement. When the published rule is stricter than the gate, every
reader pays a tax the repository never intended to charge; when it is looser, the gate blocks work the
rule permitted. Both are live here, in the same document.

**The concrete failure is not hypothetical.** `file-naming.md` states "no underscores in the
basename". `_index.md` — the structurally-required Hugo section file used by every `apps/*-www` app in
this repository — begins with one. A careful reader auditing the content trees against the convention
would conclude the repository is in wholesale violation and would be wrong. The gate exempts the file;
no document says so.

**The scope clause makes the drift unfixable by reading.** The rule governs
"`docs/`, `repo-governance/`, and similar locations". Nothing can be checked against "similar". Worse,
the validator's own doc comment quotes the phrase as its justification for exempting root files — so
the code cites the convention, the convention cannot be evaluated, and the loop closes with nobody
able to say what the rule covers.

**The ordinal convention fails at exactly the point it is consulted.** Nobody reads a naming rule for
an easy case. Its worked-cases table exists for the hard ones, and the hard row it shows contradicts
the normative sentence three paragraphs above it.

**The collision gap already cost a repository-level deviation.** `repo-rules-sweep` swept both
repositories with one rule and got two answers — 8 numbered paths left in `ose-public`, 46 in
`ose-private` — because 40 files there differ only by an ordinal and the rule has no verdict for them.
That divergence is documented, not accidental, but it stands until WS-B3 rules on the case.

## Business Impact

| If fixed                                                       | If skipped                                                                             |
| -------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| A reader can name every exempt file and say why.               | Exemptions are discoverable only by reading Rust, which most contributors will not do. |
| A future sweep produces the same outcome in both repositories. | Each sweep re-litigates the collision case and may resolve it differently.             |
| The next word-budget split cannot create a collision.          | The 18 existing collision groups grow with every split.                                |
| The scope of the rule is a path set that can be listed.        | "Similar locations" continues to justify whatever the reader already believed.         |

## Affected Roles

- **Contributors** naming a new governance file — the direct audience of both conventions.
- **AI agents** — `repo-rules-checker`, `repo-rules-fixer`, and `repo-rules-maker` all restate these
  rules and will act on whatever the conventions say.
- **Sweep executors** — anyone running a bulk rename needs a verdict for the collision case before
  starting, not during.

## Success Metrics

1. Every basename the gate exempts is named in a convention, and every basename a convention exempts
   is exempted by the gate. Checkable by comparing two lists.
2. The convention states its scope as a path expression that can be evaluated against the tree.
3. The ordinal convention's worked-cases table contains no row whose verdict contradicts the rule
   stated above it.
4. A word-budget split cannot emit two filenames differing only by ordinal.
5. Both repositories' copies of both conventions state the same rule, with per-repository facts
   (exclude lists, instance counts) derived separately rather than copied.

## Non-Goals (business scope)

- Renaming the 40 existing collision files. That needs the verdict this plan produces, and is its own
  delivery unit.
- Re-opening the withdrawal of the agent role-suffix and workflow type-suffix rules. That decision
  stands.
- Extending the `md-naming` gate to non-`.md` extensions. This plan makes the convention **honest**
  about which extensions are enforced; widening enforcement is a separate decision with its own cost.
- Changing the kebab-case rule itself. The rule is right; its statement is incomplete.

## Risks and Mitigations

| Risk                                                                           | Mitigation                                                                                                         |
| ------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------ |
| Documenting eleven exemptions reads as blessing sprawl and invites a twelfth.  | State the admission criterion (an externally-mandated fixed filename), not just the list, so additions are judged. |
| The convention grows past its word budget while gaining content.               | Both files are already near the 500-word cap; plan for a child shard rather than discovering the need mid-edit.    |
| Fixing the ordinal table's row changes what a future sweep does to real files. | Any verdict change is checked against the current tree before landing, and the affected file count is stated.      |
| The two repositories' conventions drift again during the fix.                  | Apply to both in the same delivery unit, and re-derive per-repository facts by command in each.                    |
