# Make the beavernest-be database-configuration test say which case failed

One-line summary: `DatabaseConfigurationTests` flakes on `ubuntu-latest` and blocks the `.NET quality
gate`, but its seven cases share one bare `Assert.True`, so three failures have produced no evidence
about which case is nondeterministic.

> Surfaced 2026-08-17 during `optimize-gov` execution.

## Problem / context

The `.NET quality gate` on `ose-public` PR #225 failed three times, on three different heads, with
the same signature:

```text
BeaverNestBe.Tests.Unit.Tests.DatabaseConfigurationTests.database configuration refuses empty, root,
home, repository, and nonpositive timeout values [FAIL]
   Assert.True() Failure
   at ...DatabaseConfigurationTests.fs:line 30
Failed!  - Failed: 1, Passed: 85, Skipped: 0, Total: 86
```

| Run           | Head        | Outcome                         |
| ------------- | ----------- | ------------------------------- |
| `31981345722` | `62cba3409` | failed; never re-run            |
| `32023981040` | `46a295fc1` | failed attempt 1; re-run passed |
| `32027131986` | `da015e675` | failed attempt 1; re-run passed |

Two of the three were re-run on the **identical commit** and passed. Same code, same runner image,
different outcome — that is nondeterminism, not a code defect, and it is the only reason the PR was
not treated as broken. No commit on this branch touched `apps/beavernest-be/`.

Counting these correctly requires care, and getting it wrong is easy: a successful re-run rewrites
the run's own `conclusion` to `success`, so enumerating runs by final conclusion finds only the one
failure nobody re-ran. The other two are visible only via `run_attempt` or the
`/attempts/1/jobs` API. Two independent reviewers of this brief both undercounted for exactly that
reason, and its first draft overcounted the re-runs by claiming all failures were re-run.

The diagnostic problem is structural. `DatabaseConfigurationTests.fs:19-30` builds a seven-element
list and asserts over it:

```fsharp
invalidCases
|> List.iter (fun (directory, timeout) -> Assert.True(create directory timeout |> Result.isError))
```

One assertion, no message, no case identity. Every failure reports line 30 regardless of which tuple
broke, so two occurrences have yielded zero information about the culprit. Three of the seven cases
read ambient process state and are the plausible suspects:

- `Path.GetPathRoot(Path.GetTempPath())` — depends on `TMPDIR`.
- `Environment.GetFolderPath(Environment.SpecialFolder.UserProfile)` — reads `$HOME` on Linux and
  returns an empty string when it is unset.
- `Directory.GetCurrentDirectory()` — depends on the test host's working directory.

The remaining four are literals or Guid-suffixed temp paths with non-positive timeouts.

## Why now

It has fired three times within one working day and gates every PR that makes a .NET project
affected.
Each occurrence costs a re-run of the whole gate and, worse, trains reviewers to re-run a red check
reflexively — which is precisely how a genuine failure gets waved through. The test cannot currently
distinguish those two situations for anyone.

## Prior art / precedents

- **xUnit `[<Theory>]` / `[<InlineData>]`** — the standard remedy for case-per-assertion identity;
  already used elsewhere in this solution.
- **`Assert.True(condition, message)`** — the one-line mitigation if splitting is unwanted.
- **CI rustup concurrency race** (`ose-public`, prior finding) — precedent in this repo for
  classifying an infra-flake separately from a code defect rather than "fixing" the code.

## Proposed direction (sketch)

1. Split the single `List.iter` assertion into seven `Theory` cases so the next failure names itself.
2. Re-run CI until it fires again, now with case identity, and fix the actual nondeterminism.
3. If the culprit is an ambient-state case, give the test explicit inputs rather than reading the
   environment.

## Rough scope & non-goals

In scope: `apps/beavernest-be/tests/unit/Tests/DatabaseConfigurationTests.fs`, and any sibling test
sharing the one-assert-many-cases shape.

**Out of scope (for now)**: changing `BeaverNestBe.Domain.DatabaseConfiguration` itself — no evidence
yet that production logic is wrong; retrying flaky tests automatically, which would hide the signal.

## Risks & open questions

- Which of the three ambient-state cases is actually nondeterministic? Unknown, and unknowable until
  the test can report it — this is the whole point.
- Is `$HOME` ever unset or the cwd ever unexpected on `ubuntu-latest`? If `UserProfile` returns an
  empty string, that case collapses into the already-covered empty-string case and would pass, so the
  mechanism is not yet explained.
- Does the same shape exist in other F# test suites in the repo?

## What success looks like + promotion signal

A failure of this test names the offending case in its output, and the underlying nondeterminism is
identified rather than re-run away. Promotion signal: the split lands and one more failure is
observed with case identity attached — that failure is the plan's actual input.
