# Capstone Step 4: deploy the same app via a git-push PaaS + write the trade-off note. (co-16, co-20, co-22)

The capstone's closing contrast: deploy the IDENTICAL app once more via a git-push
PaaS (the managed altitude) and write a concrete self-hosted-vs-managed
recommendation that names the deciding force. The point is to FEEL what the PaaS
absorbs (build, release, supervision, TLS) versus what Steps 1-3 built by hand.

## The PaaS deploy (the one-command contrast to Steps 1-3)

```bash
# On the box: create the app slot, then deploy from the laptop with a single push.
dokku apps:create myapp-paas                 # => a second slot, distinct from the self-hosted one
git remote add paas "dokku@$(cat .box-ip):myapp-paas"
git push paas main:master                    # => co-16: build -> release -> deploy, automatically
dokku domains:add myapp-paas paas.example.com
dokku letsencrypt:enable myapp-paas          # => co-10: the PaaS obtains the cert, not you
curl -sI https://paas.example.com/health     # => expect: HTTP/2 200 -- the SAME app, PaaS-deployed
```

## The trade-off note (the co-20/co-22 deliverable)

| Dimension  | Self-hosted (Steps 1-3)            | PaaS (this step)                     |
| ---------- | ---------------------------------- | ------------------------------------ |
| Setup      | ~5 scripts (setup, unit, proxy...) | `git push` + 2 CLI commands          |
| TLS        | Caddy + ACME, configured by hand   | `letsencrypt:enable`, one command    |
| Resilience | systemd Restart= + boot hook       | PaaS supervisor, built in            |
| Control    | Full -- the whole box is yours     | Constrained -- the runtime is theirs |
| Visibility | Full substrate (journalctl, ss)    | Only the app's logs + the leaks      |

**Recommendation (name a force, not a preference):**

- For a solo developer LEARNING the substrate (the capstone's own situation),
  SELF-HOST wins -- the point is to see the primitives Steps 1-3 expose. The PaaS
  deploy exists here to make that value tangible by contrast.
- For a small TEAM shipping a product with no ops appetite, the SAME workload
  should use the PaaS -- the 3am-on-call and patching cost Steps 1-3 leave you
  owning is the deciding force, and it dominates the per-app cost.

## Acceptance criteria (this step)

- [x] the PaaS deploy serves `https://paas.example.com/health` -> `HTTP/2 200`
      (the SAME app, deployed differently).
- [x] this note names a concrete deciding FORCE for each side (learning vs.
      ops-burden), not "it depends."

**Done bar (whole capstone):** a reader reproduces the self-hosted service from
scripts on a CLEAN box (Steps 1-3), reaches it at an HTTPS domain, confirms
restart-on-failure + reboot resilience + a working restore, and SEPARATELY
deploys the app via `git push` (Step 4) -- with NO committed secrets anywhere
(Step 3's secrets live only in `/opt/myapp/secrets.env`, mode 0600, gitignored).
