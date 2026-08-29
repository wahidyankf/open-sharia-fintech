<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: rewrite-rhino-cli-to-fsharp

## 2026-08-26 — Phase 1: B7 re-measurement documented skip

`benchmark.md`'s B2-B8 re-measurement step could not re-measure **B7** (CI critical path) in either
repository. B7 reads the `build-rhino` job duration from the three most recent green
`pr-quality-gate.yml` runs on `main`, and as of this date `main` in both `ose-public` and
`ose-private` still carries the pre-removal `Cargo.toml` (tree-sitter still listed, confirmed via
`git show main:apps/rhino-cli/Cargo.toml | grep -c tree-sitter` returning `1` in both repos) —
this Phase 1 removal has not merged to `main` yet, so no post-removal CI run of that job exists to
sample. B1 through B6 and B8 were successfully re-measured against the post-removal crate in both
worktrees and are recorded in `benchmark.md` without a `†` marker; only B7 keeps its `†` and its
pre-removal Before figure (70.67 s `ose-public`, 88.67 s `ose-private`). B7 must be re-measured once
this PR merges to `main` and three green post-merge `pr-quality-gate.yml` runs exist — Phase 10's
verdict step should treat B7 as provisional until then.

## 2026-08-26 — Phase 1: Size row confirmation

Re-ran Phase 0's exact source-line-count command
(`find apps/rhino-cli/src -name '*.rs' -type f -print0 | xargs -0 cat | awk '...' | wc -l`) in both
worktrees after the tree-sitter removal. Both report **49,460** lines, unchanged from Phase 0 — as
expected, since removing an unreferenced `Cargo.toml` dependency cannot change line counts under
`apps/rhino-cli/src/`. The Before figure in `benchmark.md`'s Size row is left as-is.

## 2026-08-26 — Phase 1: publish-mode spike (`local-tmp/publish-spike/`, `ose-public` only)

A throwaway F# console project targeting `net10.0` was created at `local-tmp/publish-spike/` and
exercised the four constructs the real `rhino-cli` binary needs: an `FSharp.Core` `Map`/`Set`
round-trip, a discriminated-union argument parse via `Argu` 6.2.5, a `System.Text.Json`
serialize+deserialize round-trip, and a recursive directory walk over `repo-governance/`. The JIT
build printed all four results and exited 0.

### Finding 1 — F#'s `sprintf`/`printfn` break under NativeAOT

The first AOT publish attempt (before the mitigations below) used `sprintf`/`printfn` to build the
result strings. It published successfully but **crashed at runtime** with
`System.NotSupportedException: ... is missing native code. MethodInfo.MakeGenericMethod() is not
compatible with AOT compilation`, thrown from `Microsoft.FSharp.Core.PrintfImpl`. F#'s printf engine
parses format strings via reflection at first use, which NativeAOT's static analysis cannot resolve.
The fix was to replace every `sprintf`/`printfn` call with F# string interpolation (`$"...{expr}..."`)
and `Console.WriteLine`, which does not go through `PrintfImpl`. This is a real, general finding for
the rewrite: **no wave's F# code may use `sprintf`/`printfn` if NativeAOT is ever adopted**, string
interpolation must be used instead.

### Finding 2 — `Argu` emits AOT/trim warnings and fails at runtime; `System.CommandLine` mitigates it

Publishing with AOT (`-p:PublishAot=true`) for `osx-arm64` produced, verbatim:

```text
/Users/wkf/.nuget/packages/argu/6.2.5/lib/netstandard2.0/Argu.dll : warning IL2104: Assembly 'Argu' produced trim warnings. For more information see https://aka.ms/il2104
/Users/wkf/.nuget/packages/argu/6.2.5/lib/netstandard2.0/Argu.dll : warning IL3053: Assembly 'Argu' produced AOT analysis warnings.
```

`FSharp.Core` itself also produced IL2104/IL3053. Per delivery.md's mitigation instruction, the parse
step was repeated with `System.CommandLine` (`3.0.0-preview.7.26381.103`, the current NuGet version)
in the same spike. Running the published AOT binary confirmed the warning was not noise: Argu's
`ArgumentParser<'T>.Parse` failed at runtime with
`Argu.ArguParseException: ERROR: unrecognized argument: '--name'` — Argu builds its argument spec by
reflecting over the DU case metadata, which NativeAOT's trimming removes by default. The
`System.CommandLine`-based parse of the identical `--name spike --verbose` input succeeded, published
with **zero** trim/AOT warnings of its own, and ran correctly in the AOT binary.
**`System.CommandLine` is the AOT-clean parser; this choice binds
[DD-2](./tech-docs.md#dd-2--reuse-the-gherkin-replace-only-the-harness) if NativeAOT is ever adopted
for the rewrite** — though see the publish-mode decision below, which does not select NativeAOT now.

### Finding 3 — `System.Text.Json`'s default reflection serializer is also disabled under NativeAOT

Not named as a mitigation trigger in delivery.md, but discovered in the same spike: the AOT publish
also emitted, verbatim:

```text
Program.fs(57): Trim analysis warning IL2026: ... JsonSerializer.Serialize<Program.Payload>(...) which has 'RequiresUnreferencedCodeAttribute' can break functionality when trimming application code.
Program.fs(57): AOT analysis warning IL3050: ... JsonSerializer.Serialize<Program.Payload>(...) which has 'RequiresDynamicCodeAttribute' can break functionality when AOT compiling.
```

and the published AOT binary crashed at runtime on the JSON round-trip with:

```text
Unhandled exception. System.InvalidOperationException: Reflection-based serialization has been
disabled for this application. Either use the source generator APIs or explicitly configure the
'JsonSerializerOptions.TypeInfoResolver' property.
```

This is a well-known, documented NativeAOT constraint (reflection-based `System.Text.Json` requires
a source-generated `JsonSerializerContext` per serialized type under full trimming) but delivery.md
names no mitigation for it, unlike Argu. Implementing source-generated JSON contexts for every type
serialized across all thirteen namespaces is a materially larger scope than swapping one argument
parser, and is not attempted in this throwaway spike. For the AOT run used in the startup
measurement below, both the Argu call and the JSON call were wrapped in `try`/`with` so the process
still exits 0 and the remaining constructs (`Map`/`Set`, `System.CommandLine`, directory walk) can be
proven in the same run — this decouples "does the process launch and exit cleanly" from "does every
required construct work", which the raw crash would otherwise conflate.

### Publish outcomes

| Publish mode            | RID         | Result                                                                                           |
| ----------------------- | ----------- | ------------------------------------------------------------------------------------------------ |
| NativeAOT               | `osx-arm64` | Publish succeeded, 11.6 s, 10 MB binary. Argu and default JSON fail at runtime (Findings 2 & 3). |
| NativeAOT               | `linux-x64` | Publish **failed** (cross-OS AOT from macOS) — see verbatim error below.                         |
| Self-contained, non-AOT | `osx-arm64` | Publish succeeded, 2.1 s, 87 MB (`du -sh`). All four constructs work correctly, unmodified.      |
| Self-contained, non-AOT | `linux-x64` | Publish succeeded, 3.95 s, 83 MB (`du -sh`).                                                     |

`linux-x64` NativeAOT verbatim failure (workstation is Apple silicon, matching delivery.md's own
expectation that cross-arch AOT figures cannot be taken from this machine):

```text
error : Symbol stripping tool ('llvm-objcopy' or 'objcopy') not found in PATH. Try installing
appropriate package for llvm-objcopy or objcopy to resolve the problem or set the StripSymbols
property to false to disable symbol stripping.
```

This is a macOS-hosted cross-OS toolchain gap (no Linux `objcopy` available), not evidence against
NativeAOT itself; CI runs on Linux runners and would not hit this specific error. It does mean this
spike cannot produce a Linux AOT startup figure from this machine, which is why the AOT startup
figure below is `osx-arm64` only, consistent with the rest of this plan's benchmarking being run on
this machine.

### Startup measurement (50 runs each, `osx-arm64`, exit code 0 asserted every iteration)

| Binary                                    | Total (50 runs) | Mean per invocation | Failures |
| ----------------------------------------- | --------------- | ------------------- | -------- |
| NativeAOT                                 | 0.762 s         | **15.23 ms**        | 0/50     |
| Self-contained, non-AOT                   | 10.042 s        | **200.84 ms**       | 0/50     |
| Rust, Phase 0 B5 baseline (`ose-public`)  | 0.562 s         | **11.2 ms**         | 0/50     |
| Rust, Phase 0 B5 baseline (`ose-private`) | 0.767 s         | **15.3 ms**         | 0/50     |

Commands used, both run from the repo root:

```bash
# AOT
dotnet publish local-tmp/publish-spike -c Release -r osx-arm64 -p:PublishAot=true -o local-tmp/publish-spike/out-aot
# self-contained
dotnet publish local-tmp/publish-spike -c Release -r osx-arm64 --self-contained true -o local-tmp/publish-spike/out-sc
```

followed by 50 timed invocations of each published binary, asserting exit code 0 on every iteration.
**Timing method note**: this plan's own `benchmark.md` already deviated from the delivery.md-literal
`/usr/bin/time -p` in Phase 0, documenting that `/usr/bin/time -p` "dropped its `real` line on
several runs" and standardizing on Python `time.time()` around `subprocess.run` for every measurement
on this page instead. This Phase 1 startup measurement follows that same established, documented
precedent rather than the literal `/usr/bin/time -p` text, for direct comparability with the Phase 0
B5 baseline it is measured against — both rows in the table above use the identical method.

**Reading these three figures together**: NativeAOT's startup (15.23 ms) is within noise of the Rust
baseline (11.2-15.3 ms) and roughly 13x faster than the self-contained fallback (200.84 ms). If AOT
worked correctly for all four constructs, it would be the clear, easy choice on this axis alone.

### Publish-mode decision

**Selected: self-contained, non-AOT.** Per the order NativeAOT, self-contained, framework-dependent,
NativeAOT is disqualified first: it does not work — out of the box, and even after applying the one
named mitigation (`System.CommandLine` for Argu) — for a second required construct
(`System.Text.Json`'s default reflection serializer), which has no mitigation named in this plan and
whose real fix (source-generated `JsonSerializerContext` for every serialized type, across all
thirteen namespaces) is a materially larger scope decision than this spike is chartered to make.
"Produces a runnable binary" is read here as producing a binary that correctly performs the
constructs the real CLI needs, not merely one that exits 0 after every failing call is caught and
swallowed — the try/with guards above were a **measurement device** to isolate the startup-time
question, not a claim that AOT is fit for purpose as tested.

Self-contained, non-AOT ran all four constructs correctly, unmodified, on both `osx-arm64` and
`linux-x64` publish targets. Its measured startup penalty (200.84 ms vs Rust's ~11-15 ms, roughly
185-190 ms slower per invocation) is real but bounded:
[tech-docs.md DD-1](./tech-docs.md#dd-1--nativeaot-is-preferred-not-mandatory) already costs the
self-contained fallback at "0.478 s per commit and 0.956 s per CI run" using an earlier, smaller
measured delta (47.8 ms) from a simpler test program; this spike's larger 185-190 ms delta, scaled
the same way (10 invocations/pre-commit, 20/CI run per that document), is roughly 1.85-1.9 s per
commit and 3.7-3.8 s per CI run — still small in absolute terms against gate jobs of 22-253 s and a
full CI run of ~380 s, but a materially larger number than DD-1's own headline figures, so it is
recorded here rather than silently inherited. This does not change the decision, since NativeAOT is
disqualified on correctness before startup is weighed, but it corrects the magnitude for whoever
reads DD-1's numbers next to this entry.

**Toolchain consequence**: the selected mode is self-contained, not framework-dependent, so no
`./.github/actions/setup-dotnet` steps are needed in the eight currently-toolchain-free CI jobs — a
self-contained publish bundles the runtime and is equally toolchain-free, per
[tech-docs.md DD-1](./tech-docs.md#dd-1--nativeaot-is-preferred-not-mandatory).

### Cleanup

`local-tmp/publish-spike/` was deleted once the figures above were recorded, per
[Plans & Temporary Files](../../../AGENTS.md#plans--temporary-files) and this phase's own cleanup
acceptance criterion.

## 2026-08-26 — Phase 2: shared-steps mode (decision)

`rhino-cli-fsharp` stays in **shared-steps** mode, matching both existing precedents (Rust
`rhino-cli`, F#/TickSpec `crane-cli`). Three-level mode is not adopted: it would need the
`--unit-dir`, `--integration-dir`, `--e2e-dir`, and `--<level>-report` arguments plus whatever
generates those report files from `dotnet test`, and none of that exists anywhere in this plan
today — adopting it now would leave the target unrunnable. Shared-steps mode's own check (missing
step implementations) is sufficient for every wave this plan schedules; `@covers` markers and
runtime-execution cross-checks are not needed until a future plan explicitly charters three-level
mode with its own argument-wiring steps.

## 2026-08-26 — Phase 2: TickSpec fallback protocol

Per [tech-docs DD-2](./tech-docs.md#dd-2--reuse-the-gherkin-replace-only-the-harness) and the risk
table, this is the protocol every wave from Wave A onward must follow:

- **Trigger**: a step cannot be expressed in TickSpec after one honest attempt.
- **Action**: write a plain `xunit.v3` test asserting the same scenario, keeping the scenario
  itself — its Gherkin text in `specs/apps/rhino/behavior/rhino-cli/gherkin/` — unchanged.
  Weakening or deleting a scenario is never the fallback.
- **Recording obligation**: one `learnings.md` entry naming the scenario and the reason the step
  could not be expressed in TickSpec.
- **Auditability**: every fallback test carries a comment naming its feature file and scenario
  title, and `grep -rc 'TickSpec fallback' apps/rhino-cli/src-fsharp/tests/` must equal the number
  of `learnings.md` fallback entries at every wave gate. At Phase 2, both counts are **0** — no
  wave has run yet, so this is the protocol's baseline, not evidence it was exercised. A mismatch
  after a wave lands means a scenario was silently re-implemented rather than deliberately
  re-expressed, and the wave gate must not pass until the counts agree again.

## 2026-08-26 — Phase 2: widening protocol

Recorded before Wave A opens, per delivery.md's own instruction, so six later integration PRs do
not each re-derive it. Two Phase-2-authored artifacts encode "no namespace flipped yet" as the
literal, nonexistent directory name `specs/apps/rhino/behavior/rhino-cli/gherkin/.fsharp-flipped-none`
(confirmed empirically: `specs behavior-coverage validate --shared-steps <nonexistent-dir> apps/rhino-cli/src-fsharp`
reports "0 specs, 0 scenarios, 0 steps — all covered" and exits 0, the same as pointing at a real
empty directory):

- `apps/rhino-cli/src-fsharp/project.json`'s `specs:behavior:coverage` target's `--shared-steps`
  positional argument.
- `repo-config.yml`'s `coverage.projects` `rhino-cli-fsharp` entry's `specs` glob.

**Each wave's integration PR widens both of these by exactly that wave's spec directories** — Wave
A replaces the placeholder with `specs/apps/rhino/behavior/rhino-cli/gherkin/convention` (and the
`repo-config.yml` glob correspondingly), Wave B additionally adds `repo-config`,
`repo-config-validate`, `env`, `env-contract`, and so on through Wave F. Phase 9c widens to the
full tree (`specs/apps/rhino/behavior/rhino-cli/gherkin/**`) and drops the `rhino-cli` entry in the
same commit that deletes the Rust crate — at that point exactly one entry (`rhino-cli-fsharp`)
covers the whole spec tree, matching the pattern every other ported namespace already established.

**Verified wiring, not merely inert**: temporarily pointing the `specs:behavior:coverage` command at
`specs/apps/rhino/behavior/rhino-cli/gherkin/convention` (Wave A's real directory, one un-ported
namespace) against the still-empty `apps/rhino-cli/src-fsharp` produced `ERROR: Found 44 step(s)
without matching step definitions` and exited 1, proving the target is wired rather than inert. The
widening was reverted immediately after the proof; Phase 2 ships with the placeholder.

## 2026-08-26 — Phase 2: `deps:audit` reporting-vs-gating proof

Per delivery.md's instruction, `dotnet list package --vulnerable --include-transitive` was proven to
be a reporting command before either Nx project shipped it. A scratch F# console project
(`local-tmp/deps-audit-scratch/`, deleted after this proof) referenced `Newtonsoft.Json` 12.0.1
(GHSA-5crp-9r3c-p9vr, "High" severity) and `dotnet list Scratch.fsproj package --vulnerable
--include-transitive` printed the finding as an `NU1903` warning and **exited 0** — confirming the
command gates nothing on its own.

**The fix**: `apps/rhino-cli/scripts/dotnet-deps-audit.sh` wraps the command, re-running it with
`--format json` and using `jq` to detect any non-empty `vulnerabilities` array under either
top-level or transitive packages across every framework/project in the report; a finding prints the
human-readable table to stderr and exits 1. Re-proven against the same scratch project: the wrapper
exited **1** against the vulnerable reference and **0** once the reference was removed.

**Live-target break-and-restore, both repos**: with the scratch proof done, `RhinoCli.Program.fsproj`
was temporarily edited to reference `Newtonsoft.Json` 12.0.1 (confined to the uncommitted working
tree — no `git add`/`git commit` while broken), `npx nx run rhino-cli-fsharp:deps:audit` was required
to exit non-zero (confirmed), the reference was restored, the same target was re-run and required to
exit 0 (confirmed), `git diff --exit-code -- apps/rhino-cli/src-fsharp/` was required to exit 0
(confirmed), and `git rev-parse HEAD` was confirmed unchanged across the whole sequence in both
repos. All exit codes matched the required shape in both `ose-public` and `ose-private`.

## 2026-08-26 — Phase 2: CI files confirmed unaffected

Per delivery.md's instruction, the reasoning for each of the five named workflow files, none of
which needed a Phase 2 edit:

- `rhino-cli-parity-audit.yml` — diffs `parity-manifest.sha256` between the two repos as an opaque
  file; it does not inspect which paths compose it, so adding `apps/rhino-cli/src-fsharp` to the
  manifest's `BOUNDARY_PATHS` needed no change here.
- `validate-env.yml` — invokes `env validate`, a namespace that stays on Rust at Phase 2
  (`FSHARP_NAMESPACES` ships empty); its `rhino-bin.sh` calls fall straight through the unchanged
  Rust tiers.
- `dependency-vulnerability-audit.yml` — invokes rhino namespaces that also stay on Rust at Phase 2,
  for the same reason; it is unrelated to the new `deps:audit` Nx target the F# project defines,
  which is a different mechanism (an Nx target invoked via `nx run`/`nx affected`, not this
  workflow's own scheduled/dispatch-triggered rhino-cli invocations).
- `_reusable-www-test-local-deploy.yml` and `_reusable-app-test-local-deploy-stag.yml` — both invoke
  rhino namespaces that stay on Rust at Phase 2, for the same reason as the two above.

## 2026-08-26 — Phase 2: `detect` job's `has-dotnet-projects` mapping

Confirmed already present and unedited in `ose-public`'s `.github/workflows/pr-quality-gate.yml`:
`lang:fsharp | lang:csharp) echo "has-dotnet-projects=true" >> "$GITHUB_OUTPUT" ;;` — `rhino-cli-fsharp`
carries `tag:lang:fsharp`, so this existing mapping already routes it to the `dotnet` job with no
new line added, exactly as delivery.md's acceptance predicted.

**`ose-private` is different and needed real work, not confirmation.** Per the delta table at the
top of this file, `ose-private` had **no** `has-dotnet-projects` output, **no** `lang:fsharp`
mapping, and **no** `dotnet` CI job at all before Phase 2 — it never carried an F# or C# project.
Phase 2 added all three there: the `has-dotnet-projects` output and its `lang:fsharp | lang:csharp`
case in the `detect` job, and a new `dotnet` job mirroring `ose-public`'s (gated on
`needs.detect.outputs.has-dotnet-projects == 'true'`). This is genuinely new CI surface in
`ose-private`, not a like-for-like mirror of an existing job.

**A gap the delta table implied but did not spell out**: `ose-private`'s `typescript` job excluded
only `tag:lang:rust` (`ose-public`'s equivalent excludes `lang:fsharp`, `lang:csharp`, `lang:rust`,
`lang:dart`). Left as-is, the moment `rhino-cli-fsharp` existed as an affected `lang:fsharp` project,
this job's own `nx affected` would have swept it in and run its targets on a runner installing no
.NET SDK. Fixed by adding `,tag:lang:fsharp` to that job's `--exclude`.

**`ose-private`'s new `dotnet` job needs `setup-rust`, unlike `ose-public`'s.** `rhino-cli-fsharp`'s
`specs:behavior:coverage`/`specs:structure-validation`/`specs:gherkin-cardinality-validation`/
`governance-*`/`env:validation` targets shell out to `cargo run --manifest-path
apps/rhino-cli/Cargo.toml` directly, mirroring `crane-cli`'s own existing `project.json` (the
established precedent for this shape in this repo). `ose-public`'s `dotnet` job runs on GH-hosted
`ubuntu-latest`, which ships a Rust toolchain preinstalled, so it has never needed an explicit
`setup-rust` step for this. `ose-private`'s runners are `[self-hosted, linux, ose-self-hosted]`,
which — per this repo's own `gate` job comment — have **no ambient Rust toolchain**. Its new
`dotnet` job therefore adds `./.github/actions/setup-rust` explicitly; omitting it would have made
every one of those five targets fail with "cargo: command not found" the first time an affected
`lang:fsharp` project's `test:quick`/`test:specs` chain ran there.

**`ose-private` had no `.config/dotnet-tools.json` or `.config/` directory at all** — no F# project
had ever needed one there. Phase 2 created it (copied verbatim from `ose-public`'s, since it is a
generic tool-version manifest with no repo-specific content: `fantomas` 7.0.5, `dotnet-fsharplint`
0.26.10, `fsharp-analyzers` 0.36.0), so `rhino-cli-fsharp`'s `lint` target's `dotnet tool restore`
step has a manifest to restore from. Verified: `dotnet tool restore` in `ose-private` now installs
all three tools successfully.

**`ose-private`'s `format` job gained a new `needs: build-rhino` dependency edge.** Unlike
`ose-public`'s `format` job, `ose-private`'s never depended on `build-rhino` — its `rhino-bin.sh`
calls resolved the Rust binary through tier 3 (build on demand) rather than a prebuilt artifact, and
it carried no `RHINO_CLI_BIN` at all. Adding the F# artifact's `download-artifact`/`chmod
+x`/`RHINO_CLI_FSHARP_BIN` wiring there — required for parity with the `format`/`enumerate`/`gate`
three-job list delivery.md names — needed a real `needs: build-rhino` edge first, since downloading
an artifact from a job that has not necessarily finished (or run) is not reliable without one. This
is a genuine, judgment-call CI-topology change in `ose-private` only: it adds wall-clock
serialization between `build-rhino` and `format` that did not exist before, with no functional risk
while `FSHARP_NAMESPACES` stays empty. `ose-public`'s `format` job already depended on `build-rhino`
before this plan, so no equivalent change was needed there.

## 2026-08-26 — Phase 2: `apps/rhino-cli/scripts/shadow-diff.sh` was not a new file

Both repos already had a tracked `apps/rhino-cli/scripts/shadow-diff.sh` from the prior Go→Rust
rewrite (`plans/done/2026-05-23__rhino-cli-rust-rewrite/` in `ose-public`), comparing a Go binary
(`apps/rhino-cli/main.go`) against the Rust one. That Go source tree no longer exists in either repo
(`apps/rhino-cli/main.go`: no such file), and nothing else in either repository references this
script by path (`grep -rn 'shadow-diff.sh'` outside `plans/` returns nothing) — it was dead,
orphaned tooling from a completed migration, never cleaned up in a prior phase. **The
File-Impact Analysis in `tech-docs.md` marks this file `[N]` (new); it is actually `[E]` (edited) —
a plan-documentation inaccuracy being recorded here rather than silently corrected upstream.** Phase
2 repurposes the same path for the new Rust↔F# differential runner, replacing the Go-era content
entirely, which is the same tool serving the same purpose for the migration now in progress.

## 2026-08-26 — Phase 2: publish RID pinned to `linux-x64` (judgment call)

Neither `ose-public`'s `ubuntu-latest` GH-hosted runners nor `ose-private`'s
`[self-hosted, linux, ose-self-hosted]` runners have their CPU architecture stated anywhere in this
plan or its workflows. `ubuntu-latest` is documented by GitHub as `x64` today, so `-r linux-x64` is
correct there. `ose-private`'s self-hosted runner architecture is `[Unverified]` from this plan's own
sources — `linux-x64` is used for both repos' `build-rhino` publish step as the reasonable default
for this class of infrastructure, but this is a judgment call, not a grounded fact, and should be
confirmed against the actual self-hosted runner hardware before this PR merges. If the self-hosted
runner is `linux-arm64`, the publish step's `-r` flag needs a matching correction there (and only
there — `ose-public` stays `linux-x64` either way).

## 2026-08-26 — Phase 2: `RhinoCli.Program` → `RhinoCli.Cli` reference direction (judgment call)

`tech-docs.md`'s architecture mermaid diagram draws `CLI --> PROG` (i.e., `RhinoCli.Cli` referencing
`RhinoCli.Program`), which would be backwards for a conventional layered CLI: an entry-point `Exe`
project is normally the one referencing the parser layer beneath it, not the reverse, and Argu
parsers have no reason to depend on the process entry point. Phase 2 implements the conventional
direction instead — `RhinoCli.Program` (`Exe`) references `RhinoCli.Cli`, which references
`RhinoCli.Application`, which references both `RhinoCli.Domain` and `RhinoCli.Infrastructure` — on
the judgment that the diagram's arrow direction is an artifact of its left-to-right layout choice
rather than a literal, intended dependency contract. No wave's plan text depends on the literal
arrow direction, so this does not block any later step, but it is recorded here as a deviation from
the tech-docs diagram as drawn.

## 2026-08-26 — Phase 2: `Severity` DU renamed from the Rust source's `Error`/`Warn`

`apps/rhino-cli/src/application/severity.rs`'s two-level scale (`Error`, `Warn`) cannot be ported
case-for-case into `RhinoCli.Domain.Types.Severity`: a case literally named `Error` collides with
`FSharp.Core`'s own `Result.Error`, which the G-Research analyzer's `GRA-UNIONCASE-001` rule
(treated as an error in this project's `lint` target) catches — confirmed by running the analyzer
suite against the initial three-case draft (`Error`/`Warning`/`Info`, the last invented rather than
grounded in the Rust source and corrected here too) before landing on the final two-case
`Blocking`/`Advisory` naming. `RequireQualifiedAccess` alone does not silence the rule; only renaming
the case does. Whichever wave first ports `severity.rs`'s real validators should decide whether
`Blocking`/`Advisory` is the permanent naming or gets revisited then, since Phase 2's choice here was
made for lint compliance on a placeholder type, not as a settled domain-naming decision.

## 2026-08-26 — Phase 2: placeholder modules avoid executable `let` bindings

`RhinoCli.Infrastructure.Placeholder`, `RhinoCli.Application.Placeholder`, and
`RhinoCli.Cli.RootArgs` were each drafted first with an executable top-level `let` binding (a string
constant, an empty list, and an Argu `IArgParserTemplate` implementation respectively) to prove each
project builds and its `ProjectReference` edges resolve. Running `test:coverage` against that draft
measured **0%** line coverage on all three (Domain's pure DU/record file measured 100%, since type
declarations carry no coverable sequence point) and failed the 90%-line threshold outright — before
any wave had shipped a single real function or test. Each was rewritten to a pure type declaration
(a single-case marker DU, a type alias into `RhinoCli.Domain.Types.Finding`, and a bare DU with the
`IArgParserTemplate` implementation removed, respectively), which restored `test:coverage` to 100%
while still proving the project references are live. The threshold-breaking behavior was re-verified
directly: temporarily adding one deliberately-uncovered function to the Infrastructure placeholder
dropped the measured figure to 0% and turned the target red, then the addition was reverted and the
target was re-verified green — confirming the 90% threshold itself gates correctly, per delivery.md's
own acceptance clause for that step.

## 2026-08-28 — Phase 6: a stale `target/gate` binary fakes a shadow-diff parity failure

Wave D's integration shadow-diff (`shadow-diff.sh md governance git`) first reported **9 of 60
invocations differing** — every `md mermaid validate` format, every `md audit` format, and
`md links validate -o json`. Every one of those diffs was a pure **ordering** difference: the
finding multisets were provably identical (`sorted(rust) == sorted(fsharp)` over the parsed JSON),
only the emission order differed. The tempting reading — "the F# port sorts its findings and Rust
does not, so fix the F# comparer" — was wrong in both direction and substance.

The real cause is that `shadow-diff.sh` resolves its Rust side to a **prebuilt**
`apps/rhino-cli/target/gate/rhino-cli`, and nothing in the script rebuilds it. The determinism
fixes this wave depends on — `md_files.sort()` in `commands/md_validate_mermaid.rs` (WalkDir
returns raw readdir order) and the insertion-order preservation of `broken_by_category` in
`application/docs/links.rs` — live in the **Rust source**, so a `target/gate` binary published
before those edits still emits filesystem-walk order. The F# side was correct the whole time;
the Rust side under comparison was simply months old.

`cargo build --profile gate --manifest-path apps/rhino-cli/Cargo.toml` (7.8 s, already-warm
cache) took the run to **60 invocations compared, 0 difference(s)** with no source change at all.

**Protocol for every remaining wave's integration step**: rebuild _both_ binaries immediately
before `shadow-diff.sh` — `cargo build --profile gate` **and** `npx nx run rhino-cli-fsharp:build`.
A stale binary on either side produces a mismatch that reads exactly like a real port defect and
invites a "fix" to correct code. The failure is silent in the worst way: the script's own
`RUST_BIN`/`FSHARP_BIN` resolution succeeds, the binary is executable, and the exit codes even
agree (`rust=1 fsharp=1`) — only the ordering betrays it. CI never hits this because
`build-rhino` publishes both artifacts fresh on every run; it is strictly a local-worktree trap.

## 2026-08-28 — Phase 6: two Wave D defects only `ose-private`'s corpus could expose

Wave D's `ose-public` shadow-diff was green at 60/0. The identical run in `ose-private` — same
commit, byte-identical sources, both binaries freshly built — reported **9 differences**. Neither
defect was reachable from `ose-public` data, so verifying the wave in one repo alone would have
shipped both.

### 1. `effectiveMermaidLabelLen` counted UTF-16 code units, not Unicode scalars

`Md.fs` measured each normalised line with `String.Length`. .NET counts UTF-16 code units, so an
astral character (any emoji) counts **two**, while Rust's `graph.rs::effective_label_len` uses
`line.chars().count()` and counts **one**. The label
`"📝 Log recovery via link-bounce"` — U+1F4DD plus 29 ASCII characters — is 30 scalars but 31 code
units, so the F# binary emitted a `label_too_long` violation against `--max-label-len 30` that Rust
never produced, and the run totals diverged (`110` vs `109`). Fixed with an explicit
`unicodeScalarCount` that advances by two on `Char.IsSurrogatePair` — exactly `chars().count()`.
`ose-public` has no mermaid node label that both contains an astral character and sits on the
30-character boundary, which is why every prior wave's shadow-diff missed it.

### 2. `wordBudgetMarkdown` rendered a seven-column table where Rust renders four

`Formatters.fs` emitted `| Path | Size | Target | Warn | Fail | Severity | Message |` with
`|------|` separators and bare paths. `governance_validate_word_budget.rs` emits
`| Path | Size (words) | Severity | Message |` with `| --- |` separators and a **backticked**
path. This is invisible whenever the finding list is empty — both sides then print the same
`**PASSED**` line and never render a table at all. `ose-public` has no surface over its word
budget, so the table never rendered there; `ose-private`'s
`repo-governance/workflows/plan/plan-execution/README.md` (901 words against a 900-word target) is
the single row that made the drift observable.

### The transferable rule

A formatter branch that only renders when findings exist is **untested by a green shadow-diff on a
clean corpus**. Both defects sat in already-merged Wave D PRs whose own shadow-diffs passed. For
every remaining wave, treat `ose-private`'s run as a first-class gate rather than a mirror-and-
confirm formality, and prefer a unit test that constructs a finding directly over relying on live
repo data to happen to contain one — `WaveDParityRegressionUnitTests.fs` pins both behaviours that
way, so neither can regress in either repo regardless of corpus.

## 2026-08-28 — Phase 6: FSharpLint hangs on a 25-arm cons-of-string-literal `match`

`nx run rhino-cli-fsharp:test:quick` never terminated after the Wave D flip. The stall was
`dotnet fsharplint lint apps/rhino-cli/src-fsharp/RhinoCli.Cli/RhinoCli.Cli.fsproj`, pinned at
100% CPU for **over an hour** on a 2,394-line project, while the other four projects — including
the 11,899-line `RhinoCli.Application` — each linted in 2–4 seconds.

### What it was not

- **Not a compiler problem.** `dotnet build` of the same project completes in 4 seconds with zero
  warnings. Type inference was never the bottleneck.
- **Not visible in single-file mode.** `dotnet fsharplint lint <file>.fs` on every one of
  `RhinoCli.Cli`'s four sources finished in 2–3 seconds with 0 warnings. Only project mode, which
  supplies type-check results, hangs. A per-file probe is therefore useless for reproducing this.
- **Not a stale `obj/`, a lock, or a cracking failure.** The hang reproduces in a clean `rsync`
  copy of `src-fsharp/` with `bin/`, `obj/`, and `dist/` excluded.

### The bisect

Reverting `RhinoCli.Cli` to its `origin/main` state in that scratch copy lints in **6 seconds**.
Restoring Wave D's `Formatters.fs` alone (194 → 814 lines) still lints in 6 seconds. Restoring
Wave D's `Dispatch.fs` alone (877 → 1,538 lines) reproduces the hang. Inside `Dispatch.fs` the
sole structural change of that shape is `route`'s opening `match argvList with`, which Wave D grew
from 13 to **25 arms**, each of the form
`| "governance" :: "readme-index" :: "validate" :: rest -> Some "…", rest`.

### The fix and the measurement

Holding the same command paths as data — a `routeTable: (string list * string) list` plus a
`matchRoute` that strips the first matching prefix — takes the same project from **>60 minutes to
7 seconds**, and the whole `rhino-cli-fsharp:lint` target to 42 seconds. Behaviour is unchanged:
`shadow-diff.sh md governance git` reports 60 invocations compared, 0 differences, in both repos,
and the 761 unit plus 5 integration tests pass in both.

### The transferable rule

FSharpLint's project-mode analysis is super-linear in the arm count of a `match` over
cons-of-string-literal patterns, and the knee sits somewhere between 13 and 25 arms. Waves E and F
add roughly twenty more command paths between them; had `route` kept its original shape, each
subsequent wave would have made the lint gate slower until CI timed out on a change that looks
completely innocent in review. **Any argv-shaped dispatch in this port stays data-driven.** More
generally: when a lint or analysis step in this repo appears to hang, time `dotnet build` on the
same project first — a fast build against a stalled analyser localises the problem to the analyser
immediately, and the per-file probe that seems like the obvious next step will exonerate the guilty
file.

## 2026-08-28 — Phase 6: `dotnet fsharp-analyzers` is a silent no-op locally

`rhino-cli-fsharp:lint` runs two commands: `dotnet fsharplint` and then the G-Research
`dotnet fsharp-analyzers` sweep. On this workstation the second one **prints nothing and exits 0
regardless of the code**, so a green local `nx run rhino-cli-fsharp:lint` says nothing about the
analyzer half of the same target. CI, running the identical command line, reported

```text
RhinoCli.Application/src/Md.fs(2769,38): Error GRA-TYPE-ANNOTATE-001 :
Please annotate your type when using the `string` function.
```

for `sb.Append(Regex.Escape(string c))` inside `globToRegex`, fixed by writing
`string<char> c`. `ANALYZERS_PATH` resolves correctly here
(`~/.nuget/packages/g-research.fsharp.analyzers/0.22.0/analyzers/dotnet/fs`) and the tool is in
`.config/dotnet-tools.json`, so this is not a missing-install — the CLI simply produces no
diagnostics locally.

### The transferable rule

**The local lint gate is strictly weaker than the CI lint gate for F#.** Treat a green local
`lint` as covering FSharpLint only. Because `--treat-as-error` makes the analyzer sweep stop at
its first finding, one CI round-trip surfaces one violation, so batch-check by inspection before
pushing: any new `string x` application needs `string<'t> x`, and the other twelve
`--treat-as-error` rules (`GRA-STRING-00{1..4}`, `GRA-UNIONCASE-001`, `GRA-VIRTUALCALL-001`,
`GRA-JSONOPTS-001`, `GRA-DISPBEFOREASYNC-001`, `GRA-IMMUTABLECOLLECTIONEQUALITY-001`,
`GRA-LOGARGFUNCFULLAPP-001`, `GRA-LOGTEMPLMISSVALS-001`, `GRA-INTERPOLATED-001`) deserve the same
read-through on every wave's new code.

## 2026-08-28 — Phase 6: the coverage gate is a per-module minimum, not a repo total

`rhino-cli-fsharp:test:coverage` runs coverlet with `/p:Threshold=90
/p:ThresholdType=line`. Coverlet's `ThresholdStat` defaults to **`minimum`**, so the bar applies to
**every module independently** — `RhinoCli.Domain`, `RhinoCli.Infrastructure`,
`RhinoCli.Application`, and `RhinoCli.Cli` each need 90% line coverage on their own. Reading the
"Total" row and concluding the gate passes is wrong twice over: a total of exactly 90.00% still
failed here because `RhinoCli.Application` sat at 89.65%.

### What Wave D did to it

Wave D added roughly 1,300 lines to `RhinoCli.Cli` — the new dispatch leaves and their formatters —
and no `RhinoCli.Cli` unit tests, because `shadow-diff.sh` was treated as the coverage story. It
is not one: shadow-diff proves byte-identity for the code paths a live corpus happens to take, and
coverlet counts lines. The result was `RhinoCli.Cli` at 44.73% line coverage and the total at
80.87%, failing CI on a PR whose local `test:quick` was green — `test:quick` does not run
`test:coverage`.

### Where the uncovered lines actually were

Three clusters, all the same shape — code that only runs when something is **wrong** or when a
flag is **passed**, neither of which a clean repository produces:

1. Every formatter's findings-present arm (headers, table shapes, per-row rendering). The Wave D
   seven-column word-budget table shipped through a green shadow-diff for exactly this reason.
2. Every dispatch leaf's body, reachable only by driving `route` against a fixture repository.
   `DispatchUnitTests.fs`'s existing `runCaptured` + `newTempDir` harness makes this cheap.
3. `md mermaid validate`'s **warning** renderers. This repository's committed diagrams stay inside
   every default threshold, so `mermaidWarningDetail` and the JSON `warningNode` builder never ran
   on live data at all.

Closing all three took 78 tests (761 → 839) and moved `RhinoCli.Cli` to 91.08%,
`RhinoCli.Application` to 90.65%, total to 90.82%.

### The transferable rule

**Every wave's flip PR must land Cli-level unit tests with the wave's dispatch and formatter
code**, not after CI rejects it. Waves E and F add far more Cli surface than Wave D did, and the
current margins are thin — 1.08 points on `RhinoCli.Cli`, 0.65 on `RhinoCli.Application`. Run
`npx nx run rhino-cli-fsharp:test:coverage` locally before pushing any wave; `test:quick` will not
tell you. When it fails, read `apps/rhino-cli/src-fsharp/tests/unit/coverage.json` per file rather
than guessing — the fully-uncovered functions in it are the cheapest lines to win, and they name
themselves.

## 2026-08-29 — Phase 9a: spec disposition enumeration and verdict table

Enumerating command: `grep -rlEi 'cargo|clippy|\brust\b' specs/apps/rhino/behavior/rhino-cli/gherkin/`,
starting from `cargo-target-share.feature` per the plan step. Confirming command:
`grep -rl '"lang:rust"' --include=project.json .` returns exactly one hit —
`apps/rhino-cli/project.json` — so no other project in either repo carries `tag:lang:rust`; every
retain verdict below rests on that result, not on an assumption.

**The literal grep is not sufficient on its own.** Three of `gate-binary-resolution.feature`'s four
scenarios contain none of `cargo`/`rust`/`clippy` in their Gherkin text (they say "the ambient
sweeper removed target/", "the prebuilt gate-profile binary in target/", "a path that does not
exist" — never the literal words), yet all four scenarios exist solely to test
`rhino-bin.sh`'s Rust-resolution-tier rebuild mechanics
[Repo-grounded — `apps/rhino-cli/src-fsharp/tests/unit/Steps/GateSteps.fs`, which drives the real
shim and asserts on `cargo build --profile gate`/`target/gate/rhino-cli`]. A second, broader search
(`grep -rniE "target/gate|CARGO_TARGET_DIR|ambient sweeper|gate-profile binary|resolver shim|rhino-bin"`)
was run precisely because the plan's own prescribed grep would have silently missed these three.
Applying only the literal instruction here would have left a whole feature file's worth of
soon-to-be-dead coverage untouched.

### Per-file verdict table

| File                                  | Scenario                                                                                                                                                           | Verdict                                                               | Reason                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `system/cargo-target-share.feature`   | 17 of 18 (all except the one below)                                                                                                                                | **Retain**                                                            | Generic `doctor` crate-discovery/target-sharing/pruning capability, exercised entirely through synthetic temp-directory fixtures [Repo-grounded — `DoctorSteps.fs`, `Directory.CreateDirectory`/`Path.GetTempPath` fixtures, never `apps/rhino-cli`'s real crate]. `discoverCrates` walks `apps/*`/`libs/*` for any `Cargo.toml` with no hardcoded crate list, so the mechanism activates for any future top-level Rust crate; it is not rhino-cli-specific even though rhino-cli was its only real-world subject historically.                                                                                                                                                                                                                                                                                                                                                                           |
| `system/cargo-target-share.feature`   | "Rust test targets ignore inherited Git process state"                                                                                                             | **Rename, not retire**                                                | The Gherkin prose still says "Rust"/"the Rust test or coverage command", but the step definition already reads `apps/rhino-cli/src-fsharp/project.json` and asserts every `dotnet test` invocation is prefixed with `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_COMMON_DIR` [Repo-grounded — `DoctorSteps.fs` lines 109, 405-406, 736-740]. This scenario already tests live F# behavior under stale Rust-era prose. 9a's edit renames the scenario title and its Given/When/Then text to describe the F# git-state-scrub guard; the assertion and its production code are untouched.                                                                                                                                                                                                                                                                                                                         |
| `repo-config/data-driven.feature`     | all 8 scenarios                                                                                                                                                    | **Retain**                                                            | None of the eight Scenario bodies mention Rust/cargo/clippy; only the Feature-level narrative line ("So that the Rust source stays identical") does. Wording fix only — drop the language-specific qualifier, since the data-driven design principle holds identically for F#.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `system/doctor.feature`               | "doctor compares rustc against the toolchain that builds"                                                                                                          | **Retire**                                                            | Backed by a hardcoded path, not generic discovery [Repo-grounded — `Doctor.fs:1476`, `Path.Combine(repoRoot, "apps", "rhino-cli", "rust-toolchain.toml")`]. 9c deletes that exact file and no other `rust-toolchain.toml` exists anywhere in the repo (confirmed by `find`), so this check has zero remaining subject.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `system/doctor.feature`               | "A pinned Rust toolchain without lint components is reported as a warning"; "A pinned Rust toolchain declaring only one lint component names just the missing one" | **Retain**                                                            | Backed by `rustToolchainManifests` [Repo-grounded — `Doctor.fs:1041`], a generic workspace-root-plus-`apps/*`/`libs/*` scan with no hardcoded path — the same shape as `discoverCrates`. The step definitions happen to write their synthetic fixture file under `apps/rhino-cli/`'s directory inside a temp repo skeleton, which is incidental to fixture authoring, not a functional dependency on that project existing for real.                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| `gate/gate-binary-resolution.feature` | all 4 scenarios (whole file)                                                                                                                                       | **Retire**                                                            | All four exist to test `rhino-bin.sh`'s Rust resolution tiers (build-on-missing, rebuild-on-stale, `RHINO_CLI_BIN` override, invalid-override fallback), which 9c's own "simplify `rhino-bin.sh`: `FSHARP_NAMESPACES` and the Rust resolution tiers are both dead once every namespace is F#" step deletes outright, collapsing the shim to one resolution path. None of the four survive that collapse as worded. **Follow-up for 9c, not authored here**: the simplified script may still warrant fresh, F#-only-tier scenarios for "explicit override takes precedence" and "invalid override falls through to discovery" — the resolution-order comment already promises this behavior for `RHINO_CLI_FSHARP_BIN` — but the exact tier semantics and variable name only exist once 9c actually ships the simplification, so authoring that coverage belongs to 9c, not to this retire-only sub-phase. |
| `gate/gate-execution.feature`         | "Rust CI target families run serially"                                                                                                                             | **Retire**                                                            | Given clause is "the real Rust quality gate" — the `rust` job in `pr-quality-gate.yml`, which 9d deletes entirely. No replacement subject.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `gate/gate-execution.feature`         | "The MSRV pre-install covers the toolchain name cargo-hack requests"                                                                                               | **Retire**                                                            | Tests `setup-rust/action.yml`'s `cargo-hack` MSRV pre-install step, whose only real consumer is `compat:min-version` [Repo-grounded — `setup-rust/action.yml` line 13, "used by rhino-cli compat:min-version"] — a target 9c deletes outright — and whose own discovery glob (`apps/*/Cargo.toml libs/*/Cargo.toml`, one level deep) matches zero files repo-wide once `apps/rhino-cli/Cargo.toml` is gone, since the `ayokoding-www` course-example crates nest far deeper than that glob reaches.                                                                                                                                                                                                                                                                                                                                                                                                       |
| `gate/gate-execution.feature`         | "Gate group jobs consume a prebuilt binary"                                                                                                                        | **Retain**                                                            | Negative assertion ("runs no cargo install command", "no Rust toolchain setup") about gate CI jobs downloading a prebuilt artifact rather than compiling. Remains straightforwardly true and worth protecting post-9c.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| `gate/gate-emission.feature`          | "Rhino CLI kind renders a resolver shim invocation"                                                                                                                | **Retain**                                                            | Negative assertion ("contains no cargo run substring") about the generated command shape. Remains valid regardless of what runs inside the shim.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `gate/gate-validation.feature`        | "The gate job's Doctor bootstrap must use the resolver shim"                                                                                                       | **Retain (not a grep hit — checked because it names `rhino-bin.sh`)** | Tests that a generated command points at the shim path, independent of the shim's internal resolution tiers.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `README.md` (gherkin tree index)      | table rows and grand total                                                                                                                                         | **Edit, not a scenario**                                              | `cargo-target-share.feature`'s row stays at 18 (17 retained + 1 renamed, none deleted). `gate-binary-resolution.feature`'s row is removed entirely (file deleted, 4→0). `doctor.feature` and `gate-execution.feature` rows drop by 1 and 2 respectively. Grand total drops by 7: 525 → 518.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |

Net effect: **7 scenarios retire** (1 from `doctor.feature`, 4 from `gate-binary-resolution.feature`
— the whole file — 2 from `gate-execution.feature`), **1 scenario is renamed** (not retired) in
`cargo-target-share.feature`, and one Feature-level narrative line is reworded in
`data-driven.feature`. `apps/rhino-cli/scripts/deny-check.sh`'s discovery glob and `Doctor.fs`'s
hardcoded `apps/rhino-cli/rust-toolchain.toml` rustc-mismatch check both become dead production
code once 9c/9d land — flagged here for 9c/9d to remove, since 9a's own scope is specs-only.

## 2026-08-29 — Phase 9a follow-up: orphaned Rust cucumber step implementations

9a's retire/rename edits above updated the Gherkin `.feature` files and the F# (TickSpec) step
definitions, and verified `npx nx run rhino-cli-fsharp:specs:behavior:coverage` (the F#-side
coverage target) exits 0 with 518 scenarios covered. That verification was incomplete: it never ran
`npx nx run rhino-cli:specs:behavior:coverage` (the Rust-crate-side coverage target, a distinct
target backed by a distinct cucumber-rs harness that binds the exact same `.feature` files). 9b's
first push attempt in both repos failed pre-push with `rhino-cli:test:quick` reporting "Found 22
orphan step implementation(s)" — Rust `#[given]`/`#[when]`/`#[then]` functions in
`apps/rhino-cli/tests/{doctor,gate_specs}.rs` whose literal step text no longer matched anything
after 9a deleted or renamed the corresponding Gherkin steps.

**Root cause**: both the retired-scenario cleanup and the "fix the class not the site" grep-blind-
spot lesson from 9a's enumeration above applied equally to the Rust side, but only the F# side was
actually checked. The Rust crate has its own independent cucumber-rs step-definition inventory,
completely separate from TickSpec's — during this migration's transition period (Rust crate still
present, deleted only in 9c) every Gherkin-level retire/rename touches **two** step-definition
surfaces, not one, and both must be swept.

**Fix**: deleted the 22 orphaned step-impl functions plus their exclusively-used `World` struct
fields and now-dead helper functions (`rhino_bin_shim_path`, `real_prebuilt_rhino_cli`,
`path_without_cargo_directory`, `RESOLVER_SHIM_PROBE_ARGS`, `step_block`, `run_block`,
`rust_report_line`), while preserving helpers still shared with retained scenarios (`repo_root`,
`action_steps`, `run_block_from_step`, `gate_job_block`) — verified by grepping every symbol's full
caller list before deleting it, not just the deleted function's own body. Also separately caught and
fixed a related miss: `cargo-target-share.feature`'s renamed step ("Nx launches the dotnet test
command") only had its F# binding (`DoctorSteps.fs`) updated in 9a; the Rust binding in
`apps/rhino-cli/tests/cargo_target_share.rs` still carried the old step text and needed the same
one-line rebind. Both fixes regenerate the parity manifest (all three `.rs` files are inside the
byte-identity boundary) and are verified via a full local `npx nx run rhino-cli:test:quick` (not
just the F# target) passing clean in both repos before pushing.

**Compounding navigational error, unrelated to the above**: three consecutive `git push` attempts in
ose-public silently pushed to the wrong remote ref (`rhino-fsharp-wave-e-p7-17`, an already-merged,
closed-PR branch left over from an earlier Wave E sub-phase) instead of the actual open-PR branch
(`rhino-fsharp-wave-e-p7-18`, PR #366) — `git push origin <name>` resolves `<name>` against a
same-named **local** branch when the working tree is checked out on a _different_ local branch, so
the stale local branch's old tip kept getting force-published rather than the checked-out HEAD.
Every pre-push hook run still executed against the correct (checked-out) working tree, so all prior
verification was valid; only the destination ref was wrong. Caught by `git ls-remote` showing an
unexpected old SHA after a "completed" push, cross-checked against `gh pr view <number>
--json headRefName` to find the actual tracked branch name. Lesson: after any push, verify the
**branch name being pushed matches `git branch --show-current`**, not just that the push exited 0 —
especially in a repo carrying many old per-sub-phase local branches from the same plan.

## 2026-08-29 — Phase 9c: crate deletion and Nx rewire — decisions and proofs

**Nx-project merge** (item 3): merged `rhino-cli-fsharp` into `rhino-cli`. Rationale: post-retirement
there is one physical F# tree, and CI already invoked both names for the same artifact (`rhino-cli`
via `nx affected` sweeps, `rhino-cli-fsharp` via named build/test steps) — exactly the duplication
Phase 9 exists to remove. `apps/rhino-cli/src-fsharp/project.json` is deleted; its `build`,
`install`, `typecheck`, `lint`, `test:unit`, `test:integration`, `test:coverage`, `deps:audit`
targets now live in `apps/rhino-cli/project.json`. `repo-config.yml`'s two `coverage.projects`
entries (`rhino-cli`, `rhino-cli-fsharp`) are collapsed into one `rhino-cli` entry with the full
`specs/apps/rhino/behavior/rhino-cli/**` glob — the per-wave incremental-widening rationale that
justified two entries no longer applies once F# is the only implementation.

**Source-tree flatten** (item 11): `apps/rhino-cli/src-fsharp/` moved to `apps/rhino-cli/src/` via
`git mv` (86 files, all recognized as renames). `fsharp-source-root: apps/rhino-cli/src/` — the
literal value every downstream reader (9d's formatter-glob step, Phase 10's build/source-size
measurements) must derive from `test -d` against its own tree, never by reading this file from
`ose-private` (it carries no copy of this plan). `tech-docs.md` §Target layout's `TBD` is replaced
with this same path in the same commit as this entry.

**Coverage-scope widening** (item 4): `rhino-cli:specs:behavior:coverage`'s `--shared-steps` argument
reverted to the simple two-argument form (`specs/apps/rhino/behavior/rhino-cli/gherkin
apps/rhino-cli/src`), replacing the itemized per-subdirectory list `rhino-cli-fsharp` carried during
the migration. Actual run: **518 scenarios, all covered** (69 specs, 2112 steps) — delivery.md's
stated acceptance figure of 524 is stale: 9a retired 7 scenarios (525 → 518) after that figure was
written into the plan. 518 is the correct, freshly-measured total, not a discrepancy to chase.

**`deps:audit`** (items 6-7): re-pointed at the existing `apps/rhino-cli/scripts/dotnet-deps-audit.sh`
wrapper (already built in Phase 2, already proven to turn a reporting-only `dotnet list package
--vulnerable` into a real gate) rather than inlining a bare `dotnet list` command — the wrapper _is_
the correct implementation of item 6's intent, not a deviation from it. Re-confirmed the live
break-and-restore proof against the merged `rhino-cli:deps:audit` target name (the prior proof at
Phase 2 ran against `rhino-cli-fsharp:deps:audit`, a name that no longer exists post-merge): recorded
`git rev-parse HEAD` (`754b1ef5`); temporarily added `<PackageReference Include="Newtonsoft.Json"
Version="12.0.1" />` to `RhinoCli.Program.fsproj`, confined to the uncommitted working tree;
`npx nx run rhino-cli:deps:audit` exited **1**; removed the reference; re-run exited **0**;
`git diff --exit-code -- apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj` exited 0; `git
rev-parse HEAD` still `754b1ef5`. All four conditions matched the required shape.

**NuGet license-allowlist and source-pin controls — accepted regression** (item 8): **not restored**.
`deny.toml`'s `[licenses]` (MIT/Apache-2.0/ISC/BSD-2-Clause/BSD-3-Clause/Unicode-3.0 allowlist) and
`[sources]`/`[bans]` (deny unknown registries/git sources) controls have no F#-side equivalent and
none is added here. Investigated first: `dotnet list package --include-transitive --format json`
carries no license field at all (confirmed by running it against `RhinoCli.Program.fsproj` directly —
the JSON schema has only `id`/`requestedVersion`/`resolvedVersion`, nothing else), so a license check
would require parsing each resolved package's `.nuspec` out of the local NuGet cache — a bespoke
scanner with no existing repo precedent (the same five other F# projects item 7 already names ship
no license check either). Building and proving that scanner to this plan's own break-restore
standard is disproportionate net-new scope for a crate-retirement sub-phase, not a like-for-like
port of anything that existed. A repo-committed `nuget.config` pinning `packageSources` alone was
considered and rejected too: no project anywhere in this repo (`ose-be`, `organiclever-be`) carries
one, so adding it only for `rhino-cli` would be a new, inconsistent, unproven pattern that — alone,
without the license check — does not satisfy item 8's "restore" branch anyway (the branch requires
both together). **Decision, dated and attributed**: accepted as a permanent regression by the
executing agent under this plan's standing autonomous-execution authorization, 2026-08-29. Both
dropped controls are named here so a future reader does not mistake silence for oversight. See
`tech-docs.md`'s new DD recording this.

**`compat:min-version` removal + `global.json` fix** (item 9): target deleted (asserted a Rust MSRV
floor that cannot survive the crate). Added `apps/rhino-cli/global.json` (SDK `10.0.204`,
`rollForward: latestMinor`), matching `apps/ose-be/global.json` and `apps/organiclever-be/global.json`
verbatim — placed at `apps/rhino-cli/` (parent of `src/`) rather than repo-root, since `.NET`
resolves `global.json` by walking upward only and this is the narrowest ancestor that actually covers
`apps/rhino-cli/src/`, matching the sibling apps' own convention (their `global.json` sits at their
own app root too, not repo-root). Verification nuance: `dotnet --version` from inside
`apps/rhino-cli/src/` prints `10.0.300` **both with and without** this file present, because the only
installed SDKs are `10.0.107`/`10.0.201`/`10.0.300` and `rollForward: latestMinor` happily accepts
`10.0.300` as satisfying a `10.0.204` floor — the same is true today for `ose-be`, confirmed by the
same check. A version-string match is therefore not a meaningful proof in this environment. Proved
resolution reaches the new file a different way instead: temporarily set the pin to an unsatisfiable
`99.0.0`/`rollForward: disable`, ran `dotnet --version` from `apps/rhino-cli/src/`, and the SDK-not-
found error explicitly printed `global.json file:
.../apps/rhino-cli/global.json` — proving the ancestor-walk reaches this exact file from that
directory. Restored the real pin immediately after; `git diff --exit-code` clean.

**`rhino-bin.sh` simplification** (item 13): `FSHARP_NAMESPACES` and the three-tier Rust resolution
(`RHINO_CLI_BIN`, `<target>/gate/rhino-cli`, `cargo build --profile gate`) both deleted — one
resolution path remains (`RHINO_CLI_FSHARP_BIN` override → `apps/rhino-cli/src/dist/rhino-cli-fsharp`
→ `dotnet run` fallback), same tier order and env-var name the F# side already used during migration,
so no CI-facing rename was needed beyond the `src-fsharp` → `src` path swap. **Scope note**: 9a's
retire-verdict table flagged that the simplified shim "may still warrant fresh, F#-only-tier
scenarios" for the two behaviors `gate-binary-resolution.feature` used to cover before its full
retirement. Considered and declined: that note itself hedges ("may"), it is not one of 9c's 13 named
checklist items, and authoring a new `.feature` file plus TickSpec bindings for a resolver shim is
net-new test-authoring scope beyond "delete/simplify", not a like-for-like port. Not silently
dropped — recorded here as a deliberate scope decision, not an oversight.

**Incidental fixes caused directly by the flatten**, not separately itemized in 9c but required for
correctness: `Parity.fs`'s `boundaryPaths` trimmed from 8 entries (`src`, `src-fsharp`, `tests`,
`Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, the specs dir) to 4 (`src`, `project.json`,
`LICENSE`, the specs dir) — the four removed either no longer exist or are now covered by `src`.
`Dispatch.fs`'s unrecognized-invocation error string changed from `"rhino-cli-fsharp: ..."` to
`"rhino-cli: ..."` (user-facing output; the `-fsharp` qualifier only ever made sense while a parallel
Rust binary existed). Three test files had hardcoded `src-fsharp` literal paths that broke under
`dotnet test` once the move landed (`HarnessSteps.fs`, `DoctorSteps.fs`'s `fsharpProjectJsonPath` —
which additionally needed one more `../` once `project.json` moved up a level to the merged file —
and the two gate/parity step files' `prebuiltFsharpCli` fixture paths); all fixed and the full
`rhino-cli:test:unit` suite re-run clean (1203/1203) after each. `apps/rhino-cli/scripts/shadow-diff.sh`
kept, not deleted — `tech-docs.md`'s file-tree annotates it `[N] Phase 2` with no `[D]` at any phase,
unlike `deny-check.sh`'s explicit `[D] Phase 9c`, a deliberate distinction the plan draws between the
two migration-era scripts; only its now-stale `src-fsharp` default path and `rhino-cli-fsharp:build`
hint were corrected, its Rust-comparison logic is left untouched pending 9e's own grep-sweep verdict
on it (it matches that sweep's enumerating grep, so it gets a verdict there, not invented here).

**Full verification after all of the above**: `npx nx run rhino-cli:typecheck` (0 warnings),
`rhino-cli:lint` (fantomas/fsharplint/fsharp-analyzers all clean, after fantomas auto-formatted one
touched file), `rhino-cli:test:unit` (1203/1203 passed), `rhino-cli:specs:behavior:coverage` (518
scenarios, all covered), `rhino-cli:deps:audit` (clean pre- and post- break/restore proof above).
`.github/workflows/pr-quality-gate.yml` updated for the same `src-fsharp` → `src` and
`rhino-cli-fsharp:build` → `rhino-cli:build` renames; `actionlint` exits 0.

**Addendum — a genuine regression the first `test:quick` run caught**: `ParityManifestSteps.fs`'s
`Given a tracked Rhino CLI parity boundary` step seeds a fully synthetic, self-contained fixture
repo with its own fabricated file list (`apps/rhino-cli/tests/parity.rs` among them) — independent
of `Parity.fs`'s real `boundaryPaths`, but written to mirror its shape at authoring time. Trimming
`boundaryPaths` (above) without updating this fixture's file list left `apps/rhino-cli/tests/parity.rs`
outside the boundary the real compiled binary now enforces, so "The manifest covers tests as well as
source" failed with "test drift unexpectedly passed" — the edited fixture file was silently outside
every boundary entry, not silently inside one. Fixed by moving the fixture's test file into the
`src` boundary (`apps/rhino-cli/src/tests/parity.rs`), consistent across the `Given`/`When`/`Then`
steps. Caught by running the actual `dotnet test` output rather than trusting a backgrounded shell
command's reported exit code — the first background run's exit code read as 0 only because the
command piped through `tail`, masking `dotnet test`'s real non-zero exit (the same class of bug as
[[feedback_pipeline_exit_code_masked_by_tail]]); the real failure was only visible by reading the
captured output text. Re-run without a masking pipe afterward, exit code 0, 1203/1203 passed.

## 2026-08-29 — Phase 9c follow-up: three findings surfaced only once external projects flipped to F

Pushing the 9c commit surfaced three problems the crate-deletion commit itself couldn't have caught
— each because deleting `apps/rhino-cli/Cargo.toml` was the FIRST time something other than
rhino-cli's own Nx targets exercised the F# binary in anger.

**1. Every other project's Nx target still hardcoded `cargo run`.** Grepping the whole repo found
50 files invoking `cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- ...`
directly — never routed through `rhino-bin.sh` — across every other app/lib's `project.json`,
`package.json`'s `generate:bindings`/`doctor`/etc. scripts, and one `.claude/hooks/` self-test.
These were never migrated during Wave A-F because that work only ever touched rhino-cli's own
targets and `rhino-bin.sh`'s dispatch. Fixed 28 real invocation sites (26 `project.json` + root
`package.json` + `guard-pre-commit-env.test.sh`) by substituting
`dotnet run --project apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj --`, preserving
the `../../` relative-path variant e2e projects with a `cwd` use. Deferred (not a mechanical path
swap): `block-env-file-access.test.sh`'s mention is an inert string literal never executed, and
`shadow-diff.sh`'s Rust-vs-F# comparison is now permanently unreachable since there is no Rust
binary left to compare against — both need their own disposition decision in 9d/9e.

**2. A genuine F# parity bug in `specs e2e-coverage validate`, hidden until now.** Once those 28
sites ran the real F# binary, three previously-green e2e projects (`ayokoding-www-fe-e2e`,
`ose-be-e2e`, `organiclever-be-e2e`) started reporting already-baselined scenarios as brand-new
gaps. Root cause: `Dispatch.fs`'s `globFeatureFiles` resolves the default `--project-dir` (`"."`)
via `Path.Combine(".", pattern)`, which — like Rust's own `PathBuf::join` — literally produces a
`./`-prefixed string; but Rust's `glob` crate silently drops that prefix from its match results,
while `Directory.GetFiles` preserves whatever `root` string it's handed verbatim. A `Feature` path
carrying the stray `./` never equality-matched the checked-in baseline's un-prefixed entries. Proven
against the still-on-disk pre-deletion Rust binaries (`apps/rhino-cli/target/{release,gate}/rhino-cli`)
byte-for-byte on the exact same fixture inputs before writing the fix. This CLI-argument-resolution
layer was never covered by the port's own test suite (`SpecsSteps.fs` drives `diffGaps`/
`scanFixmeDir` directly, bypassing `Dispatch.fs` entirely) or by Wave E/F's shadow-diff (which only
ever ran rhino-cli's own spec directory through both binaries) — a coverage gap in the ORIGINAL
Rust test suite too, not something the port introduced. Fixed by stripping a leading `./` in
`globFeatureFiles`; added a new subprocess-based Gherkin scenario + step binding (the other 13
`e2e-coverage.feature` scenarios test the pure `Specs.fs` core only) proven red against the
pre-fix `Dispatch.fs`, green after.

**3. `governance readme-index validate`'s "FAILED: N finding(s)" text is a red herring — faithfully
so.** Chased what looked like a `governance-readme-index` pre-push gate failure (419 pre-existing
"unannotated" findings across `specs/`/`docs/`, already documented in `repo-config.yml` as deferred
debt with `fail-kinds: [missing, orphan, ghost]` explicitly excluding "unannotated") for far longer
than warranted before checking `rhino-bin.sh gate run --surface=pre-push --group=markdown` in
isolation, which showed `governance-readme-index    PASS` the whole time — confirmed identical to
the original Rust (`format_text`/`format_json` compute their "FAILED"/`status` purely from
`findings.is_empty()`, independent of `has_failing_finding`'s `fail_kinds` filtering, which only
gates the real exit code). `gate run` executes every declared gate regardless of individual outcome
and reports each one's PASS/FAIL on its own summary line; a check's own verbose "FAILED" text
mid-stream is not that signal. The actual blocker was a different, later gate
(`parity-manifest`, genuinely stale from the pre-commit prettier pass reformatting `project.json`
after the manifest had already been generated) — recorded as
[[feedback_rhino_gate_text_failed_not_gate_failure]].

Verification: full `rhino-cli:test:unit` (1204/1204, including the new scenario),
`specs:behavior:coverage` (519 scenarios), and all three previously-failing e2e projects'
`specs:e2e:coverage` targets re-run clean. Landed as three follow-up commits on
`rhino-fsharp-wave-e-p7-18` (`97641d50a`, `1832a0aee`, `264e32db9`, `4a3c127b3`), pushed and
confirmed via `git ls-remote`.

## 2026-08-29 — Phase 9d: CI teardown

**Course-example count**: `find . -name '*.rs' -not -path './node_modules/*' -not -path
'./apps/rhino-cli/*' -not -path './**/target/*' | wc -l` → **198**, matching the delta table's
recorded fact. Non-zero, so the restrictions around `setup-rust`/`format-verify-rustfmt` in
`repo-config.yml` bind: both retained unchanged.

**`compat:min-version` cross-check**: the plan text asserts "the `rust` job is the only caller of
`nx affected -t test:coverage`" and "nothing else invokes [`compat:min-version`]" — the second claim
does not hold literally. `grep -rl '"compat:min-version"' --include=project.json .` returns **26**
other files, every one an `echo` no-op placeholder (e.g. `"compat:min-version: no standard
min-version floor for F#"`). Checked both mandatory-target governance docs
(`nx-targets/mandatory-targets-all-projects-six-and-required.md`'s Mandatory-Six and
Required-Where-Applicable tables) — `compat:min-version` appears in neither, so these 26 echoes are
pre-existing, out-of-plan-scope debt, not a currently-enforced convention this plan must honor.
Deleting the `compat-min-version` CI job is still correct: its only-ever-meaningful check
(`cargo hack check --rust-version` on `rhino-cli`) is gone, and every remaining invoker is a no-op
that cannot fail, so no real coverage is lost. Filed as a note here rather than a repo-governance
edit — the docs are already accurate; the 26 stale stubs are a separate, unopened cleanup.

**Per-file `setup-rust` disposition** (the four workflows outside `pr-quality-gate.yml`, each
provisioning Rust only to build `rhino-cli` from source):

| File                                       | Verdict                                                                 |
| ------------------------------------------ | ----------------------------------------------------------------------- |
| `validate-env.yml`                         | Removed; replaced with `setup-dotnet` (runs `rhino-cli:env:validation`) |
| `dependency-vulnerability-audit.yml`       | Removed; `setup-dotnet` already present, no addition needed             |
| `_reusable-www-test-local-deploy.yml`      | Removed; replaced with `setup-dotnet` (`specs-gate` job)                |
| `_reusable-app-test-local-deploy-stag.yml` | Removed; replaced with `setup-dotnet` (`specs-gate` job)                |

**Elixir re-homing**: the `rust` job's `RHINO_REQUIRE_ELIXIR: "1"` env and `erlef/setup-beam@v1` step
moved onto the `dotnet` job verbatim — that job is now the only place `rhino-cli`'s `test:quick`
(and therefore the Elixir formatter-wrapper `.fs` tests) runs, per Wave F's flip to `lang:fsharp`.
`test:coverage` needed no re-homing — the `dotnet` job already ran it for every `lang:fsharp`/
`lang:csharp` project, `rhino-cli` included, since Wave F.

**`format-verify-fantomas` reach**: `repo-config.yml`'s glob (`*.fs`, `affected-file-type` scope) is
extension-only, not path-scoped, so the `src-fsharp` → `src` flatten needed no repo-config change.
Proved live: appended a badly-indented line to a tracked `.fs` file, ran
`gate run --surface=ci --group=formatting-verify`, confirmed `format-verify-fantomas FAIL` and the
group failing, then restored the file and confirmed `git diff --exit-code` clean.

**Workflow-wide sweep**: `rust` job deleted (its `if: needs.detect.outputs.has-rust` guard went with
it); `has-rust` removed from `detect` (6 occurrences: output, two echoes, the `lang:rust` case, the
job's own guard, and the `has-ts`/`has-rust` analogy comment — reworded to `has-ts` alone);
`compat-min-version` job deleted outright (see above); `specs-structure` swapped `setup-rust` for
`setup-dotnet`. Post-edit `pr-quality-gate.yml` carries exactly one `setup-rust` (the `format` job,
retained for the 198 course-example files) and zero `has-rust`/`clippy` occurrences. `actionlint`
exits 0 on every touched workflow file.

## 2026-08-29/30 — Phase 9d follow-up: CI's floating SDK surfaced a real analyzer gap, then a real (but non-reproducing) test failure

**SDK drift**: `apps/rhino-cli/global.json` pins `10.0.204`; the local dev machine has `10.0.300`
installed; `.github/actions/setup-dotnet/action.yml` resolves the floating channel `10.0.x` via
`actions/setup-dotnet@v5`, landing on whatever the latest patch is on the runner that day
(`10.0.400` at the time of this entry). All three differ, and the F# compiler's type inference for
the bare `string` operator is sensitive to this: `G-Research.FSharp.Analyzers` rule
`GRA-TYPE-ANNOTATE-001` ("annotate your type when using the `string` function") fired in CI on
`Formatters.fs`/`Dispatch.fs` call sites that never flagged locally, even pinning the exact same
analyzer version (0.22.0, already pinned repo-wide).

**First fix attempt failed**: annotating the _let-binding_ the `string` result flows into (e.g.
`let whole: int64 = nanos / scale`) does not satisfy this rule — it still flags the generic `string`
call itself, regardless of downstream annotations. Confirmed by a second identical CI failure after
that fix. **Working fix**: eliminate the `string` operator entirely in favor of `.ToString(...)`.
For numeric types, this must be `.ToString(CultureInfo.InvariantCulture)`, not bare `.ToString()` —
F#'s `string` operator formats numerics with invariant culture, and bare `.ToString()` uses the
current culture, which would have been a silent, locale-dependent break in Rust-parity byte-identical
output. A single `char` result may use plain `.ToString()` (culture-insensitive). Same CI sweep also
converted six single-argument `String.StartsWith`/`.EndsWith` calls in `Gate.fs` to the explicit
`StringComparison.Ordinal` overload for `GRA-STRING-001`/`002` — also strictly more correct for
Rust parity, since Rust's string methods are always byte-exact.

**The `gh run rerun --failed` trap**: once the analyzer fix landed, a different test —
`GateExecutionSteps`'s "Path-gated gates still fire when a trigger path is only deleted" — failed on
that same CI run (`isSuccess` true but `was-run.txt` never created, i.e. the gate was silently
skipped because `triggerMatches` saw no changed paths). Rerunning via `gh run rerun --failed`
reproduced the identical failure, which looked like proof of a deterministic bug. It wasn't:
**`gh run rerun --failed` does not rebuild upstream jobs** — `build-rhino`'s artifact from the
original run is reused verbatim by the dependent `dotnet` job, so the "second" failure was the same
compiled binary being exercised twice, not two independent trials. A genuinely fresh run (new
commit, or `gh run rerun` **without** `--failed`, which does rebuild everything) is the only way to
get an independent sample.

**Investigation before realizing this**: the scenario's own logic was read line-by-line
(`changedPaths` → `mergeBasePaths` → `changedPathsFromBase` → `triggerMatches` → the `PathGated`
dispatch branch in `runAtRootWithOnlyAndMessageFile`) and found correct by inspection. Reproduction
was attempted locally (macOS, passed every time, filtered and full-suite) and in a Docker container
built to match the CI runner exactly — Ubuntu 24.04, git 2.55.0 (installed via the `ppa:git-core/ppa`
PPA to get past Ubuntu 24.04's stock 2.43.0), dotnet 10.0.400 — cloning the worktree at the exact
failing commit and running both the filtered test and the full 1204-test suite unfiltered. It passed
cleanly every time. A scoped, single-gate-id diagnostic (`gate.Id = "path-gated-check"`, printing
`changedPathsResult`/`triggerMatches` via the CLI's own `write`, surfaced through the test's
assertion message) was committed, pushed, and — critically — the CI run it produced also passed. A
second **fresh** rerun (no `--failed`, forcing a new `build-rhino` artifact) of the same commit also
passed. Two independent fresh builds, zero reproductions; the earlier "two failures" was one real
failure plus one artifact-reuse replay of it. The diagnostic commit was reverted
(`git revert --no-edit`, verified byte-identical to the pre-diagnostic tree via
`git diff <before> <after>` returning empty) rather than kept, since there was nothing left to
diagnose.

**Conclusion**: treated as CI-runner-level flakiness in the same class as this repo's other
documented CI-only flakes (`feedback_nx_flaky_warm_cache_commit.md`,
`project_ci_rustup_concurrency_race.md`), not a defect in the F# port — no skip/xfail was applied
(the test is unchanged from its original, fully-asserting form), no root-cause fix was needed in
`Gate.fs`, and the only lasting artifacts of this investigation are this entry and the corrected
understanding of `gh run rerun --failed`'s artifact-reuse semantics for future incidents.
