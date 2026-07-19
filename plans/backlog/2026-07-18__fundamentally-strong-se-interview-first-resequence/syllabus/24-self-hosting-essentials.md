# 24 · Self-Hosting Essentials (By Example, — ops/config, minimal app code)

**Mapping row** (frozen [tech-docs §Canonical Mapping Table](../tech-docs.md#canonical-mapping-table)):
N=24 · Phase 2 · Multi-Platform Productivity (cloud / backend-at-scale sub-phase, head) · By Example ·
— (ops/config, minimal app code) · folder weight 340 / learn 124 / drill 224. **NEW (Addition 3)** — a
light self-hosting on-ramp; strictly below the heavier containers (N=26) and cloud-IaC (N=27) topics.

**Scope note**: the **light** on-ramp to running your own software — provision one box/VM, run a
service on it, put a reverse proxy with TLS in front, and deploy via a PaaS-style git-push. It is a
_first altitude_: "get a real service of mine on the internet, reproducibly." It is **deliberately NOT**
the full-depth bare-metal / hypervisor topic — that is [N=98 `bare-metal-virtualization`](./README.md)
(Proxmox), which stays in Phase 3 (design decision DN-13, mirroring the two-altitude split). This
module uses minimal app code (a small service from earlier phases) and focuses on ops/config.

## Why this exists · the big idea

- **The problem before the solution**: a working engineer who has only ever pushed to a managed platform
  is helpless the moment they must run their own box — they cannot reason about a Linux service, a
  reverse proxy, TLS, a firewall, or "why is it not reachable." Self-hosting one service demystifies the
  whole deployment substrate.
- **Keep-this-if-you-forget-everything**: a deployment is just _a process running on a machine, reachable
  through a proxy, over TLS, restarted when it dies, reproducible from config_ — everything fancier is an
  automation of those same primitives.
- **Big ideas touched**: `abstraction-and-its-cost` (PaaS hides the box; self-hosting shows you what it
  was hiding and what you pay to peel it back), `taming-state` (a service's lifecycle, config, and data
  must be managed deliberately, not assumed).

## Prerequisites

- **Prior topics**: [N=19 Backend Essentials](./README.md) (a service to host) and
  [N=5 Just Enough Bash](./README.md) (the shell, `ssh`, scripts). A small service from
  [N=20](./20-async-python-and-fastapi-services.md) or N=19 is the thing being hosted.
- **Tools & environment**: a macOS/Linux terminal; `ssh`; a single cheap Linux VM/box (any provider, or
  a local VM); `systemd`; a reverse proxy (e.g. Caddy or Nginx) with automatic TLS; a firewall (`ufw`);
  a git-push PaaS (e.g. a self-hosted or managed buildpack platform) — all pinned/CVE-clean at authoring.
- **Assumed knowledge**: running a service locally and hitting it with `curl`; basic Linux file/permission
  concepts; using `git`.

## Accuracy notes

> Pre-authoring `web-researcher` sweep pending (DD-28 convention).

- 2026-07-18 — `ssh`, `systemd` unit files, reverse proxies, TLS via ACME/Let's Encrypt, and firewall
  basics are **stable, evergreen** operational concepts.
- 2026-07-18 — `[Needs Verification]`: exact current CVE-clean versions and command surfaces of the
  chosen reverse proxy (Caddy/Nginx) and PaaS (e.g. Dokku/Coolify or a managed buildpack platform) — pin
  and re-verify at authoring; keep the module portable across a couple of proxy/PaaS choices.
- 2026-07-18 — `[Needs Verification]`: any provider-specific VM provisioning UI/CLI — keep the steps
  provider-agnostic where possible.

## Concepts

1. **co-01 · what-self-hosting-is** — running your own software on a machine you control, versus handing
   it to a fully managed platform.
2. **co-02 · provision-a-box** — creating a Linux VM/instance and getting SSH access is the first,
   reproducible step.
3. **co-03 · ssh-access-and-keys** — key-based SSH (not passwords) is the secure default for reaching a
   remote box.
4. **co-04 · basic-server-hardening** — a non-root user, key-only SSH, and a firewall are the minimum
   safe baseline.
5. **co-05 · firewall-basics** — `ufw`/nftables allow only the ports a service needs and deny the rest.
6. **co-06 · run-a-service** — starting your application process on the box so it serves requests.
7. **co-07 · systemd-service-units** — a `systemd` unit runs a service, restarts it on failure, and
   starts it on boot.
8. **co-08 · process-lifecycle** — start/stop/status/enable and reading logs (`journalctl`) manage a
   running service.
9. **co-09 · reverse-proxy** — a reverse proxy terminates public traffic and forwards to the app on a
   local port.
10. **co-10 · tls-and-https** — automatic TLS (ACME/Let's Encrypt) gives the service HTTPS with a real
    certificate.
11. **co-11 · dns-and-domains** — an A/AAAA record points a domain at the box so the service is reachable
    by name.
12. **co-12 · environment-config** — service config and secrets live in the environment/config files on
    the box, never in the repo.
13. **co-13 · secrets-on-a-server** — secrets are set out-of-band (env files with locked permissions),
    not committed — the hard iron rule applies to servers too.
14. **co-14 · logs-and-basic-monitoring** — reading logs and a simple health check tell you whether the
    service is alive and why it failed.
15. **co-15 · restart-and-resilience** — a service must come back after a crash or a reboot without
    manual intervention.
16. **co-16 · paas-git-push-deploy** — a PaaS builds and deploys your app from a `git push`, hiding the
    box while keeping it yours.
17. **co-17 · buildpacks-vs-dockerfile** — a PaaS builds from a buildpack or a Dockerfile; each is a
    reproducible recipe for the runtime.
18. **co-18 · zero-downtime-basics** — a health-checked rolling restart avoids dropping requests on
    deploy (light version).
19. **co-19 · backups-basics** — a service with data needs a simple, tested backup of that data.
20. **co-20 · self-hosting-vs-managed-tradeoff** — self-hosting buys control and cost savings at the
    price of the operational responsibility a managed platform absorbs.
21. **co-21 · reproducible-server-config** — the box's setup is captured as scripts/config so it can be
    rebuilt, not remembered.
22. **co-22 · when-to-stay-managed** — recognising when a managed platform is the right call (small team,
    no ops appetite) versus self-hosting.

## Tensions & trade-offs — when NOT to reach for this

- **Control vs responsibility**: self-hosting gives you the whole box and the whole bill for keeping it
  patched, backed up, and alive at 3am. That trade is worth it for learning and for cost/control, and
  often not worth it for a small team shipping a product — know which situation you are in.
- **This altitude vs the deep one**: this module deliberately stops at "one box, one service, a proxy, a
  PaaS." Clustering, hypervisors, and fleet management ([N=98](./README.md), [N=99](./README.md)) are a
  different, later altitude — reaching for them here is premature.
- **When NOT to self-host**: a stateful, high-availability, compliance-bound system is not a good first
  self-host — start with a stateless service where a mistake is cheap.

## Lineage — why it beat the alternative

- The industry swung from self-managed servers to fully managed PaaS/serverless for good reasons (less
  ops toil), but an engineer who _only_ knows the managed abstraction cannot debug it when it leaks — and
  it always leaks. Self-hosting one service re-exposes the primitives (a process, a proxy, TLS, a
  firewall, a restart policy) that every managed platform is automating, so the reader can reason about
  deployment anywhere. This is the light on-ramp; [N=26 Containers &
  Orchestration](./README.md), [N=27 Cloud & IaC](./README.md), [N=98
  Bare-Metal Virtualization](./README.md), and [N=99 Self-Managed Kubernetes &
  GitOps](./README.md) build the heavier altitudes on top of it.

## Worked examples

Colocated under `self-hosting-essentials/learning/code/` (scripts, unit files, proxy configs; minimal
app code reused from an earlier topic). Each is followable on a single cheap VM (or a local VM).
Contiguous `ex-01..ex-46`. Every example cites the `co-NN` it exercises.

> **Volume-target floor**: this syllabus lists **46** of the required **≥75** (the 75–85 By-Example/
> Primer band, floor not cap — see
> [prd.md §Volume-target bands](../prd.md#volume-target-bands-inherited-from-sibling-dd-34-floor-not-cap-dd-8)).
> The maker adds **≥29** more `ex-NN` entries at authoring time, continuing the numbering and pattern
> taxonomy below, before this topic passes its by-example quality gate.

### Beginner (ex 01–16)

1. **ex-01 · provision-a-vm** — create a Linux VM and record its IP — verify you can reach it. (co-02)
2. **ex-02 · ssh-key-login** — generate a key and log in key-only — verify password login is disabled.
   (co-03)
3. **ex-03 · create-nonroot-user** — add a sudo non-root user — verify SSH as that user works. (co-04)
4. **ex-04 · enable-firewall** — `ufw` allow SSH + HTTP/HTTPS, deny the rest — verify closed ports are
   unreachable. (co-05)
5. **ex-05 · install-runtime** — install the app's runtime (pinned) on the box — verify the version.
   (co-06)
6. **ex-06 · run-service-foreground** — run the app in the foreground and hit it locally — verify a
   response over `curl localhost`. (co-06)
7. **ex-07 · systemd-unit** — write a `systemd` unit for the service — verify `systemctl start` runs it.
   (co-07)
8. **ex-08 · enable-on-boot** — `systemctl enable` the service — verify it starts after a reboot. (co-07,
   co-15)
9. **ex-09 · service-status-logs** — read status + `journalctl` logs — verify you can see start/stop
   events. (co-08, co-14)
10. **ex-10 · restart-on-crash** — kill the process and confirm `systemd` restarts it — verify recovery.
    (co-15)
11. **ex-11 · install-reverse-proxy** — install Caddy/Nginx — verify it serves a test page. (co-09)
12. **ex-12 · proxy-to-app** — proxy public port 80/443 to the app's local port — verify the app is
    reachable through the proxy. (co-09)
13. **ex-13 · dns-a-record** — point a domain at the box — verify the domain resolves to the IP. (co-11)
14. **ex-14 · automatic-tls** — enable ACME TLS on the proxy — verify HTTPS with a valid certificate.
    (co-10)
15. **ex-15 · env-config** — configure the app via an env file with locked permissions — verify the app
    reads it. (co-12)
16. **ex-16 · secrets-not-in-repo** — confirm no secret is in the repo; set it on the box out-of-band —
    verify the repo is clean. (co-13)

### Intermediate (ex 17–32)

1. **ex-17 · health-check-endpoint** — expose + curl a health endpoint through the proxy — verify a 200.
   (co-14)
2. **ex-18 · basic-uptime-check** — a cron/systemd-timer curl that logs failures — verify it fires on a
   forced outage. (co-14)
3. **ex-19 · reproducible-setup-script** — a `setup.sh` capturing the whole box setup — verify a rebuild
   from scratch reproduces the service. (co-21)
4. **ex-20 · idempotent-provisioning** — make the setup script re-runnable safely — verify a second run
   changes nothing. (co-21)
5. **ex-21 · rotate-a-secret** — change a secret on the box + restart — verify the app picks up the new
   value. (co-13, co-08)
6. **ex-22 · proxy-security-headers** — add security headers at the proxy — verify with `curl -I`.
   (co-09, co-04)
7. **ex-23 · firewall-least-privilege** — audit + tighten open ports to only the required — verify the
   minimal set. (co-05, co-04)
8. **ex-24 · logrotate** — configure log rotation for the service — verify old logs are rotated. (co-14)
9. **ex-25 · install-paas** — install a git-push PaaS (or use a managed one) — verify the platform is
   up. (co-16)
10. **ex-26 · paas-git-push-deploy** — deploy the app via `git push` — verify a push builds + releases
    it. (co-16, co-17)
11. **ex-27 · buildpack-deploy** — deploy via a buildpack (no Dockerfile) — verify a reproducible build.
    (co-17)
12. **ex-28 · dockerfile-deploy** — deploy the same app via a Dockerfile on the PaaS — verify parity with
    the buildpack build. (co-17)
13. **ex-29 · paas-env-config** — set config/secrets via the PaaS, not the repo — verify the app reads
    them. (co-12, co-16)
14. **ex-30 · paas-tls-domain** — attach a domain + TLS on the PaaS — verify HTTPS. (co-10, co-11, co-16)
15. **ex-31 · rollback-a-deploy** — roll back to the previous release on the PaaS — verify the old
    version serves. (co-16, co-18)
16. **ex-32 · zero-downtime-restart** — a health-checked restart that drops no request — verify with a
    concurrent curl loop during deploy. (co-18)

### Advanced (ex 33–46)

1. **ex-33 · data-backed-service** — host a service with a small database + persistent volume — verify
   data survives a restart. (co-06, co-19)
2. **ex-34 · backup-the-data** — a scripted, tested backup of the service's data — verify a restore
   reproduces it. (co-19)
3. **ex-35 · restore-drill** — wipe + restore from backup — verify the service comes back with its data.
   (co-19, co-15)
4. **ex-36 · reboot-resilience** — reboot the box and confirm the whole stack returns — verify the
   service + proxy + TLS all recover. (co-15, co-07, co-09)
5. **ex-37 · multi-service-on-one-box** — host two services behind one proxy on distinct paths/domains —
   verify both are reachable. (co-09, co-11)
6. **ex-38 · resource-limits** — set `systemd` resource limits on a service — verify the cap is
   enforced. (co-07, co-08)
7. **ex-39 · basic-metrics** — expose + scrape a simple metrics endpoint — verify metrics update.
   (co-14)
8. **ex-40 · deploy-pipeline-from-git** — a full git-push → build → health-check → release flow on the
   PaaS — verify an end-to-end deploy. (co-16, co-18)
9. **ex-41 · self-hosted-vs-managed-writeup** — deploy the same app self-hosted and on a managed PaaS,
   comparing effort + control — verify a documented trade-off. (co-20, co-22)
10. **ex-42 · disaster-rebuild** — rebuild the entire box from the setup script + backup after a total
    loss — verify full recovery. (co-21, co-19)
11. **ex-43 · firewall-and-fail2ban** — add brute-force protection to SSH — verify repeated failures are
    blocked. (co-04, co-05)
12. **ex-44 · staging-vs-prod-on-paas** — run a staging + prod app on the PaaS with promotion — verify a
    promote flow. (co-16, co-18)
13. **ex-45 · cost-and-scope-note** — document when to stay managed vs self-host for this workload —
    verify a concrete recommendation. (co-20, co-22)
14. **ex-46 · capstone-self-hosted-service** — a domain-named, TLS-terminated, `systemd`-managed,
    firewalled, backed-up self-hosted service reproducible from scripts — verify a clean-machine rebuild
    reaches a healthy HTTPS endpoint. (co-01–co-21)

## Capstone spec — intra-topic (subject → light-to-full runnable)

- **Goal**: take a small service and fully self-host it on one box — SSH-hardened, firewalled,
  `systemd`-managed with restart-on-failure, behind a reverse proxy with automatic TLS on a real domain,
  configured via env (no committed secrets), with a tested backup — and capture the whole setup as
  reproducible scripts; then deploy the same app once more via a git-push PaaS for contrast.
- **Concepts exercised**: [ ] provision + SSH keys + hardening + firewall (co-02–co-05) [ ] `systemd`
  service + lifecycle + restart (co-07, co-08, co-15) [ ] reverse proxy + TLS + DNS (co-09–co-11)
  [ ] env config + server secrets (co-12, co-13) [ ] logs + health check (co-14) [ ] backup + restore
  (co-19) [ ] reproducible setup (co-21) [ ] PaaS git-push deploy contrast (co-16, co-20).
- **Ordered steps**:
  1. `self-hosting-essentials/learning/capstone/scripts/` — provision + harden + firewall a box; a
     reproducible `setup.sh`. Verify a rebuild from the script reaches the same baseline.
  2. Install + `systemd`-manage the service; put a TLS reverse proxy on a real domain in front. Verify a
     public HTTPS endpoint returns 200 and the service restarts after a kill and a reboot.
  3. Configure via env (no committed secrets); add a tested backup + restore of the service's data.
     Verify a restore reproduces the data.
  4. Deploy the same app to a git-push PaaS and write a self-hosted-vs-managed trade-off note. Verify the
     PaaS deploy serves and the note names a concrete recommendation.
- **Acceptance criteria**: a reader reproduces the self-hosted service from scripts on a clean box,
  reaches it at an HTTPS domain, confirms restart-on-failure + reboot resilience + a working restore,
  and separately deploys the app via `git push` to a PaaS — with no committed secrets anywhere.
- **Done bar**: runnable end-to-end (clean-box reproduction) + web-verified.

## Read more

- **The Linux Command Line** — William Shotts (free). The foundation for operating a Linux box from the
  shell.
- **systemd documentation** (`man systemd.service`, `man systemctl`) — the authoritative reference for
  service units and lifecycle.
- **Let's Encrypt / ACME documentation** — the authoritative reference for automatic TLS.

---

← Previous: N=23 `advanced-frontend` ([index](./README.md)) · Next: N=25 `backend-at-scale`
([index](./README.md)) →
