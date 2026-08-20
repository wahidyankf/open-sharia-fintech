# Executor-Tagging and Phase-Gate Fixes (Part 2)

**6. Missing Handoff/Resume Signal on a `[HUMAN]` Step** — a merge step is exempt (its human gate
IS the signal — adding a resume signal here must never become the route by which a merge step
acquires a scripted git command). Every other `[HUMAN]` step needs (a) what the human does and (b)
the observable resume signal:

```markdown
- [ ] [HUMAN] <existing step description>. Observable resume signal: <describe signal>;
      verify with `<runnable command>`.
```

**7. Missing Legend When `[HUMAN]` Markers Are Present** — insert immediately after the
`# Delivery…` heading (or after `## Worktree` if present):

```markdown
> **Legend** — `[AI]`: an agent performs the step (the default; unmarked steps are `[AI]`).
> `[HUMAN]`: reserved for steps only a human can perform — physical/hardware actions,
> out-of-band approvals (sign a contract, pay an invoice), or interactive credential/SSO gates
> an agent cannot script. `[AI+HUMAN]`: agent prepares, human approves or finishes. Every
> `[HUMAN]` step states what the human does and the observable signal the agent checks to resume.
>
> **Phase Gate** — every phase ends with a `### Phase N Gate`: a must-pass verification
> checklist plus a **Pause Safety** note (the safe-to-stop state after the phase and the
> single command to resume). A phase is **not complete until its gate is green**; do not start
> phase N+1 while any check in phase N's gate is failing.
```

**Confidence**: **HIGH** — missing legend/gate/Pause-Safety note, unambiguous human-only step
mis-tagged `[AI]`, unjustified `[HUMAN]` on a mechanical step — all mechanically derivable.
**MEDIUM** — sanctioned-channel ambiguity, or a gate/note that can't be derived without authoring
judgment. **FALSE_POSITIVE** — a documented sanctioned-channel exception, or a legend/gate under
different wording.
