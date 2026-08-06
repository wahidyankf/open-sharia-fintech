# Example 46: Capstone Preview of a Fully Self-Hosted Service

_Traces to: `co-01`–`co-21`; the full four-step build lives in
[`./capstone/overview.md`](../../capstone/overview.md)._

This is the one-paragraph "what the capstone proves" the Advanced tier closes on: every primitive
from `co-01`–`co-21`, assembled into one runnable service on one box.

## What the capstone builds

A small service, fully self-hosted on ONE box:

- provisioned, SSH-hardened, and firewalled (`co-02`–`co-05`)
- run under `systemd` with restart-on-crash and a boot hook (`co-06`–`co-08`, `co-15`)
- behind a reverse proxy with automatic TLS on a real domain (`co-09`, `co-10`, `co-11`)
- configured via env, with secrets kept out-of-band only (`co-12`, `co-13`)
- with a health check, a tested backup, and a restore (`co-14`, `co-19`)
- captured as reproducible scripts (`co-21`)
- then deployed once more via a git-push PaaS for contrast (`co-16`, `co-20`)

## Acceptance bar

A reader reproduces the service from scripts on a CLEAN box, reaches it at an HTTPS domain, confirms
restart-on-failure plus reboot resilience plus a working restore, and separately deploys the app via
`git push` -- with no committed secrets anywhere.

**Verify**: see `./capstone/overview.md` for the four steps and the per-step checks.
