# Business Requirements — Declare the `vite` Every Vitest Config Already Imports

## Problem

Eleven packages across two repositories run their tests through a `vite*.config.*` file. None of them
declared the `vite` that config imports. Every one of them worked anyway, because npm auto-installs
`vitest`'s peer and hoists it to the root `node_modules`.

That arrangement is not a decision anyone made or reviewed. It is an emergent property of npm's
hoisting, and it holds only while every package shares one dependency store.

## What It Already Cost

One instance of this class stopped a two-repository plan at its merge boundary — though not in the way
the shape of the problem suggests.

`ts-ui:test:unit` had never run in CI on a branch where `ts-ui` was affected. Pinning `oxlint` made it
affected for the first time. The test then failed with `Cannot find module 'vite'` — in a package the
branch did not touch, naming a dependency the branch did not change, on a gate that had been green
minutes earlier.

The cost was the diagnosis. Four hypotheses were investigated and falsified before the real cause
surfaced: a cache flake, a platform-specific lockfile gap, a missing declaration, and only then the
runner's `node_modules` persistence. The third of those was wrong in an instructive way — the
declaration was added, pushed, and CI failed identically, because **declaring a package does not stop
npm hoisting it to the root**.

The undeclared manifest did not cause the outage. It did make the outage unreadable: with nothing in
`libs/ts-ui/package.json` mentioning `vite`, there was no way to tell whether the dependency was
missing or merely unreachable, and that ambiguity cost a full CI cycle to resolve.

## Why Fix It Rather Than Leave It

**Not because it is about to break.** The specific mechanism that broke `ts-ui` is fixed, and it never
existed in `ose-public` at all — that repository has no persisted-symlink cache, which is why nine
undeclared packages sat green through the entire incident. Overstating the risk here would be the
same error as the third hypothesis.

**Because the manifests are wrong, and wrong manifests cost diagnosis time.** Ten `package.json` files
claim not to need something their own config imports on every run. Anyone reading them — a person, a
tool, or a future dependency audit — is misled.

**Because declaring costs nothing.** The versions are already resolved and already installed. WS-V1
changes what the manifests say, not what gets installed, and the plan requires proving exactly that.

**Because WS-V2 is the durable part.** A gate that fails on a config importing an undeclared module
would have named `libs/ts-ui` long before a runner-cache change turned a silent gap into a red one —
and would have removed the third hypothesis from the list entirely.

## Cost of Skipping

Skipping WS-V1 leaves ten manifests that misdescribe their own packages. Low severity, permanent.

Skipping WS-V2 is the real loss: nothing checks, so every new package with a `vitest` config repeats
the pattern, and the next ambiguous failure costs the same diagnosis time this one did.

## Success Criteria

- Every package that imports `vite` in a config declares it, pinned to what its own repository already
  resolves.
- Declaring changes no installed version in either repository — provable from the lockfile diff.
- A package whose config imports an undeclared module fails CI, with a message naming the package and
  the module.
- Both repositories carry the same gate, so neither drifts into the state the other just left.
