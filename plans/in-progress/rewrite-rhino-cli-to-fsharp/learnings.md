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
