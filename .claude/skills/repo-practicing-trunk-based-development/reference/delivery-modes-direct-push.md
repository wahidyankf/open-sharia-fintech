# Trunk-Based Development — Delivery Modes: Direct Push

## When a Direct-Push Mode Is Appropriate

`worktree-to-origin-main` and `main-to-origin-main` push straight to `main` with no PR. In this repo
that is available in exactly one place: **`ose-private`, and only for a genuinely
infrastructure-as-code plan** (Terraform, Ansible, and equivalent state-changing infra work needing
the primary checkout's real secrets and local state). `main` is branch-protected against direct
pushes, including for admins, in `ose-public` — neither direct-push mode has an
executable path there, regardless of how small or well-understood the change is.

Within that one surviving `ose-private` infrastructure-as-code case, select a direct-push mode for
changes that are also small, well-understood, and safe to integrate immediately:

- **Small bug fixes** where the failure and the fix are both obvious
- **Small, safe refactors** with existing test coverage
- **Documentation** and **configuration** touch-ups
- **Dependency updates** that pass the full gate locally

**Key principle**: the direct-push modes trade review for speed, and this repo's topology only
offers that trade in `ose-private`. Choose them when the change is small enough that the trade is
obviously worth it — and declare the mode explicitly in the plan, since it is a deliberate departure
from the `worktree-to-pr` default rather than the assumed path.
