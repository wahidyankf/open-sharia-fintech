# Anti-Hallucination Fixes (Part 2)

**Confidence**: **HIGH** — verification recipe passes after replacement, mechanically derived.
**MEDIUM** — replacement value can't be mechanically derived (interpretation/judgment/multi-page
research needed) — write to `## Manual Review Required`. **FALSE_POSITIVE** — claim WAS verifiable
but the checker missed the confidence label or recipe context (e.g. inside a code-fence quoting a
repo file) — document per the Skip-List protocol.

**Refuse-on-uncertainty applies to fixes too**: (1) skip the line if the surrounding content stays
coherent; (2) add `[Unverified]`, classify MEDIUM, escalate; (3) convert to `_Judgment call:_` when
genuinely subjective; (4) convert to `_Unknown — verify before authoring_` placeholder with an Open
Questions delivery item. Forbidden: a more-plausible-sounding hallucination.

**Never apply refusal option 1 — or any option here — to a merge step.** Removing a merge step's
line to resolve an unverified claim inside it deletes the plan's human-gate opt-in as a side effect
of an unrelated fix — merge steps commonly carry a relative link to the PR Merge Protocol, and plan
folders sit deep enough that such links break routinely, so this path is reached in normal operation.
On a merge step, fix the claim in place or classify MEDIUM; never remove the line.
