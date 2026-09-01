# Learnings

Transient execution log. Add a candidate only when a durable repository surface could prevent the
same gap for a future contributor.

Every future entry uses a stable `L-<number>` heading and includes exactly one repository-relevance
field before routing:

```text
## L-<number>: <short title>
Repository relevance: <public|private-only|discard>
Observation: <sanitized execution fact>
Durable prevention: <candidate rule, documentation, test, or automation surface>
Route: <filled only after Phase 21 safety and overlap gates>
```

`public` may enter an authorized public durable surface after the overlap scan. `private-only` may
be reported or routed only inside `ose-private`; it never enters a public idea, plan, rule, or
export. `discard` records a one-line reason and is not routed.

Before archival, every surviving entry must be routed inline to a non-code home, filed as a
literally authorized follow-up plan, reported without plan authorization with handoff evidence, or
discarded with a one-line reason after both safety gates are applied.

## L-1: An Nx project name is inferred from its directory when `project.json` omits `name`

Repository relevance: public
Observation: `test-contract registry validate` reported `ose-www is absent from the Nx project
list` even though `apps/ose-www/project.json` exists, because that file — like most app projects
here — declares no `name` key and relies on Nx inferring the name from the containing directory.
A reader that only trusts an explicit `name` silently loses those projects, and the resulting
diagnostic blames the registry rather than the reader.
Durable prevention: any repository tool that enumerates Nx projects from `project.json` must fall
back to the containing directory name, and should be checked against `nx show projects --json`
rather than against a hand-listed project set.
Route:

## L-2: The local F# analyzer run does not reproduce every CI analyzer diagnostic

Repository relevance: public
Observation: `rhino-cli:lint` passed locally — with the Nx cache skipped, and again when the
offending expression was deliberately restored — while the same target in CI failed with
`GRA-TYPE-ANNOTATE-001 : Please annotate your type when using the 'string' function`. Both sides
load g-research.fsharp.analyzers 0.22.0 through the same command, and the verbose local log shows
the file being analyzed, so a green local lint is not evidence that the analyzer gate will pass.
Durable prevention: treat CI as the only authority for the G-Research analyzer rules, and avoid the
constructs those rules police in the first place — never apply `string` to an unannotated
expression in `apps/rhino-cli` F# sources; parse and compare typed values instead.
Route:

## L-3: Captured tool transcripts leak the absolute worktree path

Repository relevance: public
Observation: `dotnet test` prints each built assembly and the test-run target as a fully resolved
path, so an evidence file captured verbatim from `nx run <project>:test:unit` carried six lines of
`/Users/<user>/.../worktrees/<name>/...` into a tracked file. The leak review caught it; no local
gate did, because absolute paths are neither a lint nor a formatting failure. The same pattern is
already present in several merged `plans/done/**` evidence files, so this is a class rather than a
one-off slip.
Durable prevention: normalize the repository-root prefix to a portable placeholder when capturing
any build, test, or coverage transcript into a tracked evidence file, and scan a candidate evidence
file for an absolute home-directory path before staging it rather than relying on the leak review
to find it.
Route:
