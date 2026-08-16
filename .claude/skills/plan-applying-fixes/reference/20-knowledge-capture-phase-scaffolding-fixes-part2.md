# Knowledge Capture Phase Scaffolding Fixes (Part 2)

**How to scaffold the Knowledge Capture phase** — insert as the FINAL substantive phase in
`delivery.md`, immediately before Plan Archival:

```markdown
## Phase N: Knowledge Capture

> _Triage every surviving `learnings.md` entry before archival. See the
> [Knowledge Capture Convention](../../../../repo-governance/development/quality/knowledge-capture.md)._

- [ ] [AI] Apply the litmus test to every `learnings.md` entry — keep only if a durable surface
      would catch this automatically next time; discard the rest with a one-line reason
- [ ] [AI] Apply the secret/sensitivity gate — sanitize any secret, credential, token, or private
      hostname to a `<placeholder>` token, or discard if unsanitizable
- [ ] [AI] Apply the repo-relevance gate — infra-private content stays in `ose-private` only and is
      NEVER cross-routed into `ose-public`
- [ ] [AI] Route each surviving learning to exactly one durable home per the open-ended routing
      matrix; code homes (`apps/`, `libs/`, tests) are ALWAYS filed as a separate
      `plans/backlog/<slug>/` plan, NEVER landed inline (the only carve-out is a genuine blocker
      required to finish this plan's own scope)
- [ ] [AI] For any entry routed to `plans/ideas/`, scan `plans/ideas/README.md` and the existing
      two-pagers FIRST for a brief already covering the same area — fold in rather than creating a
      new file
- [ ] [AI] If no generalizable learning surfaced, record `No generalizable learnings — <reason>`
      in `learnings.md`

### Phase N Gate

> All checks below must pass before Plan Archival.

- [ ] [AI] Every `learnings.md` entry is terminal (routed inline / filed as backlog / discarded
      with reason), or the explicit "none" escape is recorded
- [ ] [AI] No code-homed learning landed inline in this plan's own commits/PR

> **Pause Safety**: `learnings.md` is fully triaged (or explicitly empty). Safe to stop. To
> resume: re-read `learnings.md` and confirm every entry is terminal.
```

After scaffolding, re-read both the inserted phase and `learnings.md`; confirm the phase sits
immediately before Plan Archival and the file exists at the plan-folder root. Do not auto-tick any
scaffolded checkbox — they are the author's/executor's remaining work.
