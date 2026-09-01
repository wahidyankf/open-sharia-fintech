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
