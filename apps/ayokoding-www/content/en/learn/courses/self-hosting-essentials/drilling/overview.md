---
title: "Overview"
date: 2026-07-30T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Self-Hosting Essentials course: five fixed drills
that force active recall instead of passive re-reading. Work through them in order -- short-answer
recall first, then scenario judgment, then hands-on repetition against small ops/config fixtures,
then a checklist to confirm real automaticity, and finally why/why-not prompts that test whether you
can explain the reasoning -- including this topic's cross-cutting big ideas,
`abstraction-and-its-cost` and `taming-state` -- not just recite the commands. Every answer is hidden
in a `<details>` block; try each item yourself before opening it.

## Recall Q&A

Twenty-two short-answer questions, one per concept (`co-01` through `co-22`). Answer from memory,
then check.

**Q1 (co-01 -- what-self-hosting-is).** A working engineer has only ever pushed to a fully managed
platform. What does running their own box for the first time teach them that the managed platform was
hiding?

<details>
<summary>Answer</summary>

It re-exposes the primitives every managed platform automates: a process running on a machine, a
reverse proxy, TLS, a firewall, a restart policy, and reproducible config. The managed platform is an
abstraction over exactly those things, and self-hosting one service shows what that abstraction costs
to peel back (and why it sometimes leaks). Example 41 stands the same app up both ways to make the
trade-off concrete.

</details>

**Q2 (co-02 -- provision-a-box).** Why does provisioning end by RECORDING the box's IP, rather than
leaving it in the provider's dashboard?

<details>
<summary>Answer</summary>

Because every later step -- SSH, the DNS A record (Example 13), the ACME TLS order (Example 14), the
PaaS deploy (Example 26) -- needs that one stable value. Recording it (Example 1's `.box-ip`) is what
makes the setup reproducible: a box whose address lives only in a browser tab cannot be rebuilt from
memory, which is why Example 42's disaster rebuild depends on the IP (and the setup) being captured.

</details>

**Q3 (co-03 -- ssh-access-and-keys).** Why is key-based SSH the default, and what does disabling
password login (Example 2) specifically close off?

<details>
<summary>Answer</summary>

A key pair is unguessable and scoped to one machine; a password is brute-forceable and reuseable
across boxes. Disabling password login closes the single most common remote-compromise vector -- the
bots that hammer port 22 trying passwords (Example 43's `fail2ban` then deals with the residual log
noise from those still-trying bots, which can now never succeed).

</details>

**Q4 (co-04 -- basic-server-hardening).** Name the three layers of the minimum safe baseline, and why
"defense in depth" matters even if one layer feels sufficient.

<details>
<summary>Answer</summary>

A non-root user (Example 3), key-only SSH (Example 2), and a firewall (Example 4) -- plus, later,
proxy security headers (Example 22) and `fail2ban` (Example 43). Defense in depth matters because each
layer blocks a different attack class, so a failure in one (a forgotten open port, a leaked key) does
not hand the attacker the whole box; the other layers still stand.

</details>

**Q5 (co-05 -- firewall-basics).** What is the default-deny stance, and why does it turn "open port"
into an auditable decision rather than an accident?

<details>
<summary>Answer</summary>

Default-deny (`ufw default deny incoming`, Example 4) blocks every port except the few explicitly
allowed (22/80/443). Because nothing is reachable unless you said so, an "open port" becomes a
deliberate, listed rule -- which Example 23 then audits down to the true minimum, catching any service
that silently bound a new port.

</details>

**Q6 (co-06 -- run-a-service).** Why run the app in the foreground FIRST (Example 6) before wiring up
`systemd`?

<details>
<summary>Answer</summary>

To separate "does the app even work" from "does the supervision work." If the public endpoint later
fails, you already know the app answers `curl` locally, so you can narrow the bug to the layer you
just added (the unit, the proxy, or TLS) instead of guessing across all of them at once.

</details>

**Q7 (co-07 -- systemd-service-units).** What does a `systemd` unit file replace that a manually typed
command cannot provide?

<details>
<summary>Answer</summary>

Reproducible configuration: the unit declares the start command, the user, the restart policy, and the
boot hook, turning "a process I launched by hand" into "a service the OS owns." That is what makes
restart-on-crash (Example 10), boot-resilience (Example 36), resource limits (Example 38), and the
watchdog (Example 68) expressible at all -- none of which a one-off shell command gives you.

</details>

**Q8 (co-08 -- process-lifecycle).** What are the two commands first reached for when "is it up and
why did it fail," and what does `journalctl -u` give you that an app's own log file does not?

<details>
<summary>Answer</summary>

`systemctl status` and `journalctl -u` (Example 9). The journal is the single, unified log stream
`systemd` captures for EVERY unit's stdout+stderr, so it is one place to look for every service --
rather than each app inventing its own log location, which you then have to hunt for per service.

</details>

**Q9 (co-09 -- reverse-proxy).** Why put a reverse proxy in front of the app instead of binding the
app directly to port 443?

<details>
<summary>Answer</summary>

The proxy centralizes TLS, virtual hosting (multiple services on one `:443`, Example 37), security
headers (Example 22), rate limiting (Example 56), and graceful drain (Example 74) at one chokepoint.
Binding the app to 443 means re-implementing all of that inside the app; the proxy keeps the app
simple and lets one box serve many services behind one public face.

</details>

**Q10 (co-10 -- tls-and-https).** What does ACME automation replace, and why is "real TLS on a
personal box" practical now rather than a weekend chore?

<details>
<summary>Answer</summary>

It replaces manual `openssl` cert generation and the renewal-cron that followed -- Caddy obtains,
serves, and renews a Let's Encrypt cert automatically on first request (Example 14). That automation
is the difference: a 90-day cert that renews itself needs zero ongoing effort, so HTTPS becomes a
one-line config change instead of a recurring manual task.

</details>

**Q11 (co-11 -- dns-and-domains).** Why is a DNS record a precondition for BOTH human-usable URLs and
for TLS itself?

<details>
<summary>Answer</summary>

The A record maps the name to the box's IP (Example 13), which is what makes the URL human-usable --
and ACME's HTTP-01 challenge proves domain CONTROL by serving a token from that name, so without the
DNS record no certificate can be issued. DNS is the prerequisite for both the name and the cert.

</details>

**Q12 (co-12 -- environment-config).** What does "separating config from code" buy you, in one
sentence?

<details>
<summary>Answer</summary>

It lets the IDENTICAL artifact run in staging and prod -- the difference between two environments
becomes a set of environment variables (Example 15's `app.env`), not a second copy of the application,
so you deploy the same image everywhere and vary only its config (Example 29 does this on a PaaS,
Example 61 templates it).

</details>

**Q13 (co-13 -- secrets-on-a-server).** Why is a committed secret permanent, and what is the
server-side discipline that prevents it?

<details>
<summary>Answer</summary>

Git history is forever -- even a deleted-and-force-pushed commit may already be cloned or cached, so
"it was only one commit" is no defense. The discipline (Example 16) is to keep every secret in a
mode-0600 file the repo never sees (`/opt/myapp/secrets.env`), and to add a scan gate (Example 64's
pre-commit hook) that blocks the slip at the keyboard before it lands.

</details>

**Q14 (co-14 -- logs-and-basic-monitoring).** What gap does a health check + a timer (Examples 17-18)
close, and what does it NOT close?

<details>
<summary>Answer</summary>

It closes the gap between "it crashed" and "someone told us it crashed" -- a probe hits `/health`
every minute and logs a failure. It does NOT close the "is it degrading before it fails" gap, which is
what metrics (Example 39) and alerting on a threshold (Example 67) add. Logs + a health check are the
floor; metrics are the next step up.

</details>

**Q15 (co-15 -- restart-and-resilience).** What two failure modes does "the service must come back on
its own" cover, and which mechanism catches each?

<details>
<summary>Answer</summary>

A CRASH (the process exits) is caught by `Restart=always` (Example 10); a HANG (the process is alive
but stuck) is caught by the `systemd` watchdog (Example 68), which force-restarts a service that stops
pinging within `WatchdogSec`. A reboot is the third case, handled by `enable` + `WantedBy` (Example 8,
drilled in Example 36). All three make "alive" the default state without a human.

</details>

**Q16 (co-16 -- paas-git-push-deploy).** What does a `git push` to a PaaS absorb that Examples 1-14
did by hand?

<details>
<summary>Answer</summary>

The build (it compiles your image from a buildpack or Dockerfile, Examples 27-28), the release (it
runs the new image under its own supervisor), the proxy + TLS (it attaches a domain and obtains a
cert, Example 30), and the rollback history (Example 31). One push does the work of setup + unit +
Caddyfile + ACME -- the exact trade-off Example 41 names.

</details>

**Q17 (co-17 -- buildpacks-vs-dockerfile).** What is the trade-off between a buildpack and a
Dockerfile, and what does each make reproducible?

<details>
<summary>Answer</summary>

A buildpack (Example 27) detects your language and supplies the runtime -- zero image authoring, but
constrained to what it detects. A Dockerfile (Example 28) is fully explicit and portable to any
container runtime, but you own every layer. Both are reproducible build recipes; the difference is
convenience (buildpack) versus control and portability (Dockerfile).

</details>

**Q18 (co-18 -- zero-downtime-basics).** Why does a naive "stop then start" deploy drop requests, and
what two mechanisms (Examples 32 and 74) prevent it?

<details>
<summary>Answer</summary>

A naive stop kills the process (and its in-flight requests) the instant the new one is not yet
serving. Graceful shutdown (Example 50/74) drains in-flight work before the process exits, and a
blue-green swap (Example 73) keeps the OLD instance answering until the NEW one is proven healthy --
so no request ever hits a stopped backend.

</details>

**Q19 (co-19 -- backups-basics).** Why is an untested backup "a wish, not a safeguard," and what two
habits convert it into evidence?

<details>
<summary>Answer</summary>

Because a backup that has never been restored might be torn, truncated, or empty, and you only find
out under duress. The two habits: integrity-check the backup AT BACKUP TIME (Example 34) and run a
PERIODIC restore drill (Example 35, automated in Example 77) -- so a corrupt backup is caught when the
stakes are zero, not during the first real data loss.

</details>

**Q20 (co-20 -- self-hosting-vs-managed-tradeoff).** Name the two sides of the trade-off concretely,
and why it is a trade-off rather than a strict upgrade.

<details>
<summary>Answer</summary>

Self-hosting buys control and cost savings at the price of operational responsibility (patching,
backups, 3am uptime); a managed platform absorbs that responsibility at the price of control and a
higher per-app spend. It is a trade-off because no side is strictly better -- the right answer depends
on whether you value the control/cost (self-host) or the absorbed ops burden (managed) for THIS
workload, as Example 41 and Example 45 spell out.

</details>

**Q21 (co-21 -- reproducible-server-config).** What does capturing the box's setup as scripts
(Example 19/20) change about a box you might lose?

<details>
<summary>Answer</summary>

It turns "the box works" into "the box works AGAIN, on fresh hardware, without me." A box whose setup
is tribal knowledge is unrecoverable in any practical sense; a box whose setup is a script (or a
`cloud-init` user-data, Example 78) is rebuildable -- which is the entire premise of Example 42's
disaster-rebuild drill and the capstone's acceptance bar.

</details>

**Q22 (co-22 -- when-to-stay-managed).** Name two workload characteristics that should push you toward
a managed platform despite knowing how to self-host.

<details>
<summary>Answer</summary>

A stateful, high-availability, or compliance-bound workload is a poor first self-host -- a managed
platform absorbs the backups/failover (stateful+HA) or already carries the compliance cert
(compliance) you would otherwise own at 3am (Example 45). The discipline is to name the deciding force
(state, HA, compliance, team ops-appetite) rather than default to self-hosting everything.

</details>

## Applied problems

Twelve scenarios. Each describes a symptom without naming the construct -- decide which mechanism
solves it, then check.

**AP1.** You SSH into the box after a deploy and the service is `inactive (dead)` with no recent
journal entries -- it crashed hours ago and nothing brought it back.

<details>
<summary>Answer</summary>

The unit is missing `Restart=always` (co-15; Example 10, kata 1). Without it, the default `Restart=no`
applies and a crash stays dead until a human restarts it. Add `Restart=always` (with a
`StartLimitBurst` cap) so the box heals itself.

</details>

**AP2.** You ran a firewall script and your SSH session died mid-command; you can no longer reach the
box at all.

<details>
<summary>Answer</summary>

The script enabled the firewall BEFORE allowing port 22 (co-04/co-05; kata 2). The default-deny
policy went live with SSH still closed, dropping your session. The fix is order: `ufw allow 22/tcp`
FIRST, then `ufw --force enable`. Recovery requires console/access from the provider, since SSH is now
locked out.

</details>

**AP3.** The service is healthy on `curl http://127.0.0.1:8000/health`, but
`curl https://myapp.example.com/health` returns `502 Bad Gateway`.

<details>
<summary>Answer</summary>

The proxy and the app disagree on the port (co-09; Example 12, kata 3). The proxy is forwarding to a
local port the app is NOT bound on (e.g. 8001 instead of 8000). Fix the `reverse_proxy` upstream to
match the app's actual bind port.

</details>

**AP4.** A teammate accidentally committed `APP_SIGNING_SECRET=...` to the repo and pushed.

<details>
<summary>Answer</summary>

This is a co-13 hard-iron violation, and it is permanent (history). The secret must be ROTATED (not
just deleted), the repo cleaned, and a pre-commit hook (Example 64) added to block the next slip.
Going forward, secrets live only in a mode-0600, gitignored file (Example 16), never in the repo.

</details>

**AP5.** The box rebooted for a kernel patch and the service did not come back, even though
`systemctl start` works fine by hand.

<details>
<summary>Answer</summary>

The unit is not `enable`d (co-15; Example 8). `start` runs it now; only `enable` (the `WantedBy`
symlink) makes it start on BOOT. Run `systemctl enable myapp` (and `systemctl enable caddy` -- the
proxy must also survive the reboot, or the app is unreachable, Example 36).

</details>

**AP6.** `curl https://myapp.example.com/` works, but `curl http://myapp.example.com/` also serves
content (unencrypted) instead of redirecting.

<details>
<summary>Answer</summary>

The HTTP-to-HTTPS redirect is missing (co-10; Example 53). Without it, a typo'd `http://` URL serves
content unencrypted, enabling a silent downgrade. Add the redirect block (and HSTS, Example 54, to
make browsers stop trying HTTP at all).

</details>

**AP7.** You ran the same `setup.sh` a second time to converge drift and it reset the firewall and
re-created the user, briefly disrupting the service.

<details>
<summary>Answer</summary>

The script is not idempotent (co-21; Example 19 vs Example 20). A second run should be a no-op where
its postconditions already hold. Wrap each step in an `ensure_*` guard (Example 20) so re-running
changes nothing observable.

</details>

**AP8.** The service's logs are filling `/var/log`, and a near-full disk caused confusing failures
across every service on the box.

<details>
<summary>Answer</summary>

Missing log rotation (co-14; Example 24). A `logrotate` rule (rotate, keep N, compress) bounds the
logs, and a `SystemMaxUse` cap bounds the journal. A full disk presents as a dozen unrelated failures
whose single root cause is "no space."

</details>

**AP9.** You deployed a bad release via `git push` and now every request 500s; you need the previous
version back immediately.

<details>
<summary>Answer</summary>

A PaaS rollback (co-16/co-18; Example 31). The PaaS keeps a release history, so one command restores
the last known-good image. (On the self-hosted side, the equivalent is a blue-green flip back to
BLUE, Example 73.)

</details>

**AP10.** You have a daily backup job, but you have never restored from one, and you are not sure the
backups even work.

<details>
<summary>Answer</summary>

An untested backup is a wish (co-19; Examples 34-35, kata-less but central). Add an integrity check at
backup time and run a periodic restore drill (automated in Example 77) -- so a corrupt backup is
caught now, not during the first real data loss.

</details>

**AP11.** The service is "active (running)" but not answering requests; `systemctl status` looks fine
even though `curl` hangs.

<details>
<summary>Answer</summary>

The process is hung, not crashed (co-15; Example 68). `Restart=always` only catches an EXIT; a hung
process stays "active" forever while serving nothing. Add a `systemd` watchdog (`WatchdogSec`) so the
service must ping periodically or be force-restarted.

</details>

**AP12.** You are choosing whether to self-host or use a managed platform for a small team's
must-not-lose Postgres-backed SaaS, and a teammate argues "self-host, we know how now."

<details>
<summary>Answer</summary>

This is the wrong workload to self-host (co-22; Example 45). A stateful, must-not-lose, HA-adjacent
database is a poor first self-host -- a managed Postgres absorbs the backups and failover you would
otherwise own at 3am. Name the deciding force (stateful + HA), not the team's newfound skill.

</details>

## Code katas

Four hands-on repetition drills against small ops/config fixtures -- a `systemd` unit, a firewall
script, a Caddyfile, and an env file. Each is a before/after pair colocated under `drilling/code/`.
Every "before" fixture is real and misapplies a concept this course teaches -- read it, diagnose the
bug from the described symptom, fix it from memory, then compare against the "after" fixture and the
model solution.

### Kata 1 -- a systemd unit that does not restart on crash

**Task.** The service should come back after a crash (co-15). The "before" unit has NO `Restart=`
directive, so the default (`no`) applies and a crash stays dead until a human intervenes.

**Before** (`drilling/code/kata-01-systemd-unit-no-restart/before/kata.service`):

```ini
[Service]
Type=simple
User=deploy
ExecStart=/opt/myapp/venv/bin/python /opt/myapp/app.py
# THE BUG: no Restart= directive -> default 'no' -> a crash is permanent.
[Install]
WantedBy=multi-user.target
```

**Symptom**: after `kill -9 $(systemctl show -p MainPID --value myapp)`, `systemctl is-active myapp`
stays `inactive` forever.

<details>
<summary>Model solution</summary>

```ini
[Service]
Restart=always
RestartSec=3
StartLimitIntervalSec=60
StartLimitBurst=5
```

**Root cause**: the unit relies on `systemd`'s default `Restart=no` (co-15; Example 10, kata 1). Adding
`Restart=always` makes a crash self-healing; `StartLimitBurst` caps it so a hopeless crash loop trips
into `failed` instead of burning the box. The "after" fixture adds exactly these lines.

</details>

### Kata 2 -- a firewall that locks you out

**Task.** Enable the firewall safely (co-04/co-05). The "before" script enables the default-deny
policy BEFORE allowing SSH, so the enabling command drops your own session.

**Before** (`drilling/code/kata-02-firewall-locks-out-ssh/before/kata.sh`):

```bash
ufw default deny incoming
ufw default allow outgoing
ufw --force enable      # BUG: SSH not yet allowed -> session dropped here
ufw allow 22/tcp        # too late
```

**Symptom**: your SSH session dies the instant `ufw --force enable` runs, and you cannot get back in.

<details>
<summary>Model solution</summary>

```bash
ufw allow 22/tcp        # allow SSH FIRST
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable      # NOW enabling is safe
```

**Root cause**: order is load-bearing. The default-deny policy is LIVE the moment `enable` runs, so
SSH must already be allowed or your session is one of the things denied. Recovery requires
console/access from the provider, which is why the bug is so costly (co-04).

</details>

### Kata 3 -- a proxy pointing at the wrong port

**Task.** Proxy public traffic to the app (co-09). The app binds `127.0.0.1:8000`; the "before"
Caddyfile forwards to `127.0.0.1:8001`.

**Before** (`drilling/code/kata-03-proxy-misses-local-port/before/kata.Caddyfile`):

```caddy
myapp.example.com {
  reverse_proxy 127.0.0.1:8001   # BUG: the app is on 8000, not 8001
}
```

**Symptom**: `curl https://myapp.example.com/health` returns `502 Bad Gateway`, even though both the
proxy and the app are healthy in isolation.

<details>
<summary>Model solution</summary>

```caddy
myapp.example.com {
  reverse_proxy 127.0.0.1:8000   # match the app's actual bind port
}
```

**Root cause**: the proxy and the app disagree on where to meet (co-09; Example 12). A `502` with both
sides healthy is almost always a port/path mismatch between `reverse_proxy` and the app's bind
address. Verifying the app directly (`curl 127.0.0.1:8000/health`) isolates it from the proxy first.

</details>

### Kata 4 -- a secret committed to the repo

**Task.** Keep secrets out of the repo (co-13). The "before" env file holds a REAL signing secret,
baked into a repo-tracked file.

**Before** (`drilling/code/kata-04-secret-committed-to-repo/before/kata.env`):

```bash
APP_HOST=127.0.0.1
APP_PORT=8000
APP_SIGNING_SECRET=5f3e9a8c2b...   # BUG: a real secret, in git
```

**Symptom**: a repo scan (Example 16) or a pre-commit hook (Example 64) flags the file; even after
deletion, the secret is in history.

<details>
<summary>Model solution</summary>

```bash
APP_HOST=127.0.0.1
APP_PORT=8000
# No secret here. The real APP_SIGNING_SECRET lives ONLY in:
#   /opt/myapp/secrets.env   (mode 0600, gitignored), read via EnvironmentFile=-
```

**Root cause**: this violates the hard-iron rule (co-13; Example 16). The fix is two-sided: move the
secret to a mode-0600, gitignored file set out of band, AND rotate the leaked value (deleting it from
one commit does not undo history). A pre-commit hook (Example 64) blocks the next slip at the
keyboard.

</details>

## Self-check checklist

Confirm each item without checking the manual first. If you hesitate, that concept needs another
pass.

- [ ] I can explain what a managed platform was hiding that self-hosting re-exposes. (co-01)
- [ ] I can provision a box and record its IP so the setup is reproducible. (co-02)
- [ ] I can set up key-only SSH and disable password login. (co-03)
- [ ] I can name the minimum safe baseline (non-root user, key-only SSH, firewall) and why it is
      defense in depth. (co-04)
- [ ] I can configure a default-deny firewall with exactly the ports this stack needs. (co-05)
- [ ] I can run a service in the foreground and curl it before wiring up supervision. (co-06)
- [ ] I can write a `systemd` unit that restarts on crash and starts on boot. (co-07)
- [ ] I can read service status and logs with `systemctl`/`journalctl`. (co-08)
- [ ] I can configure a reverse proxy to forward public traffic to a local app port. (co-09)
- [ ] I can enable automatic TLS on a real domain and verify the cert. (co-10)
- [ ] I can point a DNS A record at a box and verify propagation. (co-11)
- [ ] I can configure an app via an env file separate from the code. (co-12)
- [ ] I can keep a secret out of the repo and scan for slips. (co-13)
- [ ] I can add a health endpoint and a timer that probes it. (co-14)
- [ ] I can make a service restart on crash, on hang, and on reboot. (co-15)
- [ ] I can deploy an app via `git push` to a PaaS. (co-16)
- [ ] I can contrast a buildpack deploy against a Dockerfile deploy. (co-17)
- [ ] I can do a zero-downtime restart and verify it drops no requests. (co-18)
- [ ] I can take a tested backup and prove a restore reproduces the data. (co-19)
- [ ] I can name the self-host vs managed trade-off's two sides concretely. (co-20)
- [ ] I can capture a box's setup as a re-runnable, idempotent script. (co-21)
- [ ] I can name two workload characteristics that should push me to managed. (co-22)

## Elaborative-interrogation prompts

Explain the WHY behind each -- if you can only state the rule but not the reason, the concept has not
landed yet.

**E1.** Why does key-only SSH (co-03) close a vector that a firewall (co-05) does not? (A firewall
controls which PORTS are reachable; what does key-only auth control that a port rule cannot?)

**E2.** Why is "restart on crash" (co-15) NOT enough on its own -- what failure mode does it miss that
a watchdog (Example 68) catches? (Hint: what is the difference between a process that EXITS and one
that is alive but stuck?)

**E3.** Why does separating config from code (co-12) matter MORE as you add environments (staging,
prod), not less? (What would be true of your deploys if config were baked into the code?)

**E4.** Why is a committed secret (co-13) treated as permanently leaked even after you delete the
commit? (What does "git history is forever" mean operationally, and why is rotation the only remedy?)

**E5.** Why does a reverse proxy (co-09) let ONE box serve MANY services, and what would be true of
your infrastructure without it? (Name two things the proxy centralizes that each app would otherwise
re-implement.)

**E6.** This topic's two cross-cutting big ideas are `abstraction-and-its-cost` and `taming-state`.
Name one place in this course where each shows up concretely. (For abstraction: what does the PaaS
hide, and what do you pay to peel it back? For taming-state: which example deliberately manages a
service's lifecycle/config/data instead of assuming it?)

---

← Previous: [Capstone](../learning/capstone/overview.md)
