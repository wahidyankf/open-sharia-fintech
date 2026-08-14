# Business Requirements Document — BeaverNest CLI Chat

## Business Goal

Make the already-authenticated CLI agents available through BeaverNest's browser workspace so a
trusted sandbox user can hold a normal conversation without working in terminal UIs. The product
preserves each CLI as the execution/authentication surface, so it does not create a new vendor-key
distribution or subscription-management problem.

## Affected Roles

| Role                 | Outcome                                                                                                     |
| -------------------- | ----------------------------------------------------------------------------------------------------------- |
| Sandbox-network user | Starts or resumes a browser chat, selects an agent per turn, and receives streamed output.                  |
| Sandbox operator     | Installs/authenticates the CLIs and is responsible for the external full-authority sandbox.                 |
| Maintainer           | Has one provider-neutral backend boundary, deterministic persistence, and automated contract/browser proof. |

## Success Signals

- A ready combined runtime supports a complete text-only chat turn without a terminal UI.
- Switching provider does not discard visible prior context: the selected provider receives bounded replay.
- A missing/auth-failed/exited CLI produces a safe error and leaves the transcript usable.
- Thread deletion removes its transcript and saved provider-session references from local SQLite.
- No browser bundle, API response, log, or persisted message contains a CLI credential.

## Business Non-Goals

BeaverNest does not supply identity, private conversations, policy enforcement, remote isolation,
or provider fallback. The user explicitly accepts a shared workspace and auto-approved full authority
inside a secure external sandbox; these are product constraints, not security claims made by the app.

## Risks and Accepted Trade-offs

| Risk                                                        | Treatment                                                                                                                |
| ----------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Full authority can modify the sandbox workspace.            | Show a persistent plain-language notice; rely on the external sandbox as directed, not on browser approvals.             |
| All trusted-network users can read all threads.             | State shared-workspace semantics in UI/API/docs; do not imply privacy without identity.                                  |
| CLI output changes over time.                               | Best-effort adapter parsing is an accepted risk; tests use captured current JSON fixtures and errors remain visible.     |
| Replaying a mixed-provider transcript costs tokens/context. | Bound replay by explicit message/character budgets and record a visible truncation notice in the new provider's context. |
| Long turns hold resources.                                  | Permit one active run per thread, provide cancellation, and retain partial output.                                       |
