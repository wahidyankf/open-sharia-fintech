---
title: "Intermediate Examples"
date: 2026-07-30T00:00:00+07:00
draft: false
weight: 20
---

Examples 17-32 operate and automate the substrate the Beginner tier built: a health-check endpoint, a
timer-based uptime check, a reproducible `setup.sh` (and its idempotent version), secret rotation,
proxy security headers, a least-privilege firewall audit, log rotation, then the PaaS arc --
installing a git-push platform, deploying via `git push`, comparing buildpack and Dockerfile builds,
PaaS env config and TLS, a rollback, and a zero-downtime restart. Every artifact is a real shell
script, `systemd` unit/timer, Caddyfile, logrotate rule, Procfile, or Dockerfile -- minimal
application code.

---

### Example 17: A Health-Check Endpoint Through the Proxy

_ex-17 &middot; exercises co-14_

A health endpoint (`/health`) is the floor of observability: a 200 means the app is up and answering.
This script curls it THROUGH the proxy (the full public path), so the check exercises proxy + app
together.

**`learning/code/ex-17-health-check-endpoint/check.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
DOMAIN="myapp.example.com"; HEALTH_PATH="/health"
curl -fsS "http://127.0.0.1:8000${HEALTH_PATH}" >/dev/null  # => isolate the app from the proxy first
STATUS="$(curl -s -o /dev/null -w '%{http_code}' "https://${DOMAIN}${HEALTH_PATH}")"  # => full public path
echo "[health] ${DOMAIN}${HEALTH_PATH} -> HTTP ${STATUS}"
if [ "${STATUS}" = "200" ]; then echo "[verify] PASS: healthy (200)"; else echo "[verify] FAIL: unhealthy (${STATUS})"; exit 1; fi
```

**Run**: `bash check.sh`

**Expected**:

```text
[health] myapp.example.com/health -> HTTP 200
[verify] PASS: healthy (200)
```

**Key takeaway**: a health check hit THROUGH the proxy tests the whole path (TLS + proxy + app); a
loopback-only check tests just the app and would miss a broken proxy.

**Why it matters**: this endpoint is what Example 18's timer probes every minute and what Example 67
alerts on. A health endpoint nobody hits is decoration; one that an automated check actually curls is
the floor of observability.

---

### Example 18: A Basic Uptime Check on a Timer

_ex-18 &middot; exercises co-14_

A health endpoint only helps if SOMETHING hits it regularly. This is a `systemd` TIMER + SERVICE
pair that curls `/health` every minute and logs failures to the journal -- the lightest possible
uptime monitor.

**`learning/code/ex-18-basic-uptime-check/myapp-health.service`** (and companion `.timer`):

```ini
# myapp-health.service
[Unit]
Description=MyApp uptime check  # => co-14: a one-shot probe, not a long-running daemon
[Service]
Type=oneshot  # => runs once per activation, exits, then the timer re-arms it
ExecStart=/usr/bin/curl -fsS --max-time 5 https://myapp.example.com/health  # => -f fails on non-2xx -> journald logs it

# myapp-health.timer
[Unit]
Description=Run the MyApp uptime check every minute
[Timer]
OnBootSec=30s  # => first probe 30s after boot (give the stack time to come up)
OnUnitActiveSec=1min  # => then re-probe 1min after each completed run -> ~once a minute forever
Persistent=true  # => if the box was off, run a "missed" probe on next boot
[Install]
WantedBy=timers.target
```

**Run**: `install both files && systemctl daemon-reload && systemctl enable --now myapp-health.timer`

**Expected**:

```text
$ systemctl list-timers myapp-health.timer
NEXT ... UNIT                ACTIVATES
...  myapp-health.timer      myapp-health.service
$ # after stopping myapp to force an outage:
$ journalctl -u myapp-health.service -n 2
... curl: (22) The requested URL returned error: 502
```

**Key takeaway**: a `systemd` timer is the reboot-safe, journaled replacement for a cron line -- a
failure lands in `journalctl`, not a lost mailbox, and a missed tick during downtime is recovered on
next boot.

**Why it matters**: "is it working" is unanswerable without something probing it. The timer closes
the gap between "it crashed" and "someone told us it crashed," which is the whole reason a health
endpoint exists.

---

### Example 19: A Reproducible setup.sh

_ex-19 &middot; exercises co-21_

Capture the WHOLE box setup from Examples 1-16 as one script, so a clean machine converges to the
same baseline unattended. This is co-21's core move: "the box's setup is captured as scripts so it
can be rebuilt, not remembered."

**`learning/code/ex-19-reproducible-setup-script/setup.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
DOMAIN="myapp.example.com"; APP_DIR="/opt/myapp"; PYTHON_VERSION="3.12"
echo "=== [1/5] system packages + runtime ==="
apt-get update && apt-get install -y curl ca-certificates ufw python${PYTHON_VERSION} python${PYTHON_VERSION}-venv
echo "=== [2/5] deploy user + firewall ==="
id -u deploy >/dev/null 2>&1 || useradd -m -s /bin/bash deploy
ufw --force reset >/dev/null; ufw default deny incoming; ufw default allow outgoing
ufw allow 22/tcp; ufw allow 80/tcp; ufw allow 443/tcp; ufw --force enable
echo "=== [3/5] app + venv ==="
install -d -o deploy -g deploy -m 755 "${APP_DIR}"
sudo -u deploy "python${PYTHON_VERSION}" -m venv "${APP_DIR}/venv"
cp ./app.py "${APP_DIR}/app.py" && chown deploy:deploy "${APP_DIR}/app.py"
echo "=== [4/5] systemd unit + enable ==="
cp ./myapp.service /etc/systemd/system/myapp.service
systemctl daemon-reload && systemctl enable --now myapp
echo "=== [5/5] reverse proxy + TLS ==="
apt-get install -y caddy; cp ./Caddyfile /etc/caddy/Caddyfile; systemctl reload caddy
echo "=== DONE ==="
curl -fsS "https://${DOMAIN}/health" && echo " [verify] 200 OK"
```

**Run**: `bash setup.sh` (as root, on a fresh box)

**Expected** (tail):

```text
=== [5/5] reverse proxy + TLS ===
=== DONE ===
ok [verify] 200 OK
```

**Key takeaway**: one script reproduces the entire baseline -- runtime, user, firewall, service,
proxy, TLS -- so the box is rebuildable from a committed file rather than tribal knowledge.

**Why it matters**: this is what makes Example 42's disaster rebuild possible at all. A box whose
setup is "I remember roughly what I did" is a box you cannot recover; a box whose setup is a script
is a box you can lose and rebuild identically.

---

### Example 20: Make the setup.sh Idempotent

_ex-20 &middot; exercises co-21_

Example 19 works on a fresh box, but a second run redoes everything. Idempotence means "running it N
times has the same effect as running it once" -- so you can safely re-run to converge drift. Every
step here checks "is this already done?" before acting.

**`learning/code/ex-20-idempotent-provisioning/setup.sh`** (guarded extract):

```bash
#!/usr/bin/env bash
set -euo pipefail
DOMAIN="myapp.example.com"; APP_DIR="/opt/myapp"; PYTHON_VERSION="3.12"
ensure_user()      { id -u deploy >/dev/null 2>&1 || useradd -m -s /bin/bash deploy; }
ensure_packages()  { dpkg -l ufw caddy "python${PYTHON_VERSION}" 2>/dev/null | grep -q '^ii' || \
                     { apt-get update && apt-get install -y ufw caddy "python${PYTHON_VERSION}" "python${PYTHON_VERSION}-venv"; }; }
ensure_firewall()  { ufw status | grep -q 'Status: active' || { ufw --force reset >/dev/null; \
                     ufw default deny incoming; ufw default allow outgoing; ufw allow 22/tcp; ufw allow 80/tcp; ufw allow 443/tcp; ufw --force enable; }; }
ensure_venv()      { [ -x "${APP_DIR}/venv/bin/python" ] || sudo -u deploy "python${PYTHON_VERSION}" -m venv "${APP_DIR}/venv"; }
ensure_app()       { install -d -o deploy -g deploy -m 755 "${APP_DIR}"; cmp -s ./app.py "${APP_DIR}/app.py" || \
                     { cp ./app.py "${APP_DIR}/app.py"; chown deploy:deploy "${APP_DIR}/app.py"; }; }
ensure_unit()      { cmp -s ./myapp.service /etc/systemd/system/myapp.service || cp ./myapp.service /etc/systemd/system/myapp.service; \
                     systemctl daemon-reload; systemctl is-enabled --quiet myapp || systemctl enable myapp; systemctl reload-or-restart myapp; }
ensure_caddy()     { cmp -s ./Caddyfile /etc/caddy/Caddyfile || cp ./Caddyfile /etc/caddy/Caddyfile; systemctl reload caddy; }
ensure_user; ensure_packages; ensure_firewall; ensure_venv; ensure_app; ensure_unit; ensure_caddy
echo "[verify] run a SECOND time; 'is-active myapp' and 'curl /health' are unchanged"
```

**Run**: `bash setup.sh` (twice in a row)

**Expected**: the second run produces no observable change -- `systemctl is-active myapp` stays
`active`, `/health` stays `200`.

**Key takeaway**: each `ensure_*` function is a no-op if its postcondition already holds, so the
script is safe to re-run forever to converge drift -- the property that separates a one-shot
installer from a maintainable provisioning script.

**Why it matters**: drift happens (a firewall rule gets added, a file edited by hand). An idempotent
script lets you re-apply the known-good state without fear of breaking a partially-changed box -- the
light, script-level preview of what Terraform/Ansible (out of scope here) automate at fleet scale.

---

### Example 21: Rotate a Secret and Reload

_ex-21 &middot; exercises co-13, co-08_

Secrets are not immortal. This script generates a NEW signing secret on the box, writes it to the
locked-down file atomically, and gracefully reloads the service so the app picks up the new value --
without downtime.

**`learning/code/ex-21-rotate-a-secret/rotate.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
SECRET_PATH="/opt/myapp/secrets.env"; UNIT="myapp"
NEW_SECRET="$(openssl rand -hex 32)"  # => generated on the box; the repo never sees it
echo "[rotate] generated a new signing secret"
TMP="$(mktemp)"; printf 'APP_SIGNING_SECRET=%s\n' "${NEW_SECRET}" > "${TMP}"
chmod 600 "${TMP}" && chown deploy:deploy "${TMP}"  # => same ownership/perms as Example 16
mv -f "${TMP}" "${SECRET_PATH}"  # => atomic rename: readers see old OR new, never half
systemctl reload "${UNIT}" 2>/dev/null || systemctl restart "${UNIT}"  # => co-08: pick up the new env
echo "[verify] journalctl -u ${UNIT} -n 3 --no-pager   # => a fresh 'Reloaded' line after the swap"
```

**Run**: `bash rotate.sh`

**Expected**:

```text
[rotate] generated a new signing secret
[verify] journalctl -u myapp -n 3 --no-pager   # => a fresh 'Reloaded' line after the swap
```

**Key takeaway**: writing to a temp file then `mv` makes the swap atomic -- the service reads either
the OLD secret or the NEW one, never a half-written file, which is why rotation can happen live
without corruption.

**Why it matters**: a secret that cannot be rotated is a secret that, once leaked, stays leaked. The
discipline of rotate-then-reload-on-the-fly is what makes "we had to rotate all our keys" a Tuesday
afternoon instead of an all-hands incident. Example 63 automates this on a schedule.

---

### Example 22: Security Headers at the Proxy

_ex-22 &middot; exercises co-09, co-04_

The reverse proxy is a single chokepoint to add defensive HTTP headers the app never has to know
about: HSTS, a frame-buster, MIME-sniffing protection. Defense in depth at the transport edge.

**`learning/code/ex-22-proxy-security-headers/Caddyfile`**

```caddy
myapp.example.com {
  reverse_proxy 127.0.0.1:8000
  header {  # => co-09/co-04: security headers ADDED at the proxy, not the app
    Strict-Transport-Security "max-age=31536000; includeSubDomains"  # => insist on HTTPS for 1y (full HSTS in Ex 54)
    X-Content-Type-Options "nosniff"  # => stop browsers MIME-sniffing JSON as HTML
    X-Frame-Options "DENY"  # => stop this site being framed (clickjacking)
    Referrer-Policy "no-referrer"  # => do not leak the URL to linked third parties
    Permissions-Policy "geolocation=(), camera=()"  # => this app needs no device permissions
    -Server  # => strip Caddy's version banner (no free recon for attackers)
  }
}
```

**Run**: `install Caddyfile /etc/caddy/ && systemctl reload caddy`, then
`curl -sI https://myapp.example.com/ | grep -iE 'strict-transport|x-content-type|x-frame'`

**Expected**:

```text
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

**Key takeaway**: security headers belong at the proxy because the proxy sees EVERY response -- add
them once and every backend behind the proxy inherits them, instead of each app re-implementing the
same header set.

**Why it matters**: these headers independently block different attack classes (downgrade,
clickjacking, MIME confusion). Adding them at the chokepoint is defense in depth that survives an app
restart and applies uniformly to every service behind the proxy.

---

### Example 23: Firewall Least-Privilege Audit

_ex-23 &middot; exercises co-05, co-04_

Example 4 opened {22, 80, 443}, but services bind ports over time and "what's listening" drifts from
"what's allowed." This audit reconciles the two and tightens `ufw` so the allowed set is EXACTLY the
required set.

**`learning/code/ex-23-firewall-least-privilege/audit.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
echo "[listening] sockets bound on this box:"
ss -tulnp | grep LISTEN || true  # => the ground truth a firewall must match
echo "[ufw] currently allowed:"
ufw status  # => co-05: every line here is a deliberately-open door
REQUIRED="22 80 443"  # => the only ports this stack needs
echo "[audit] any allowed port NOT in {${REQUIRED}} is drift to remove:"
echo "         e.g. 'ufw delete allow 8080/tcp' for a port nothing should use"
ALLOWED="$(ufw status | awk '/ALLOW/ {print $1}' | grep -oE '^[0-9]+' | sort -u | tr '\n' ' ')"
echo "[verify] allowed = '${ALLOWED}' (expected: '${REQUIRED} ')"
```

**Run**: `bash audit.sh`

**Expected**:

```text
[verify] allowed = '22 80 443 ' (expected: '22 80 443 ')
```

**Key takeaway**: "least privilege" is a periodic reconciliation -- what's listening should equal
what's allowed should equal what's required, and any gap in either direction is drift to fix.

**Why it matters**: a service that silently bound a new port now has a public door you never opened.
The audit is the habit that catches that door before an attacker does, turning "the firewall is
configured" from a one-time setup into an ongoing discipline.

---

### Example 24: Log Rotation for the Service

_ex-24 &middot; exercises co-14_

A service that logs forever will eventually fill the disk -- and a full disk is an outage that looks
like every other outage. `logrotate` keeps logs bounded: rotate weekly, keep N weeks, compress the
old ones.

**`learning/code/ex-24-logrotate/myapp.logrotate`**

```text
/var/log/caddy/*.log {  # => co-14: every file Caddy writes under its log dir
  weekly  # => rotate once a week
  rotate 8  # => keep 8 old weeks (~2 months of history), then delete
  compress  # => gzip the rotated files (saves disk)
  delaycompress  # => compress one rotation LATE, so the just-rotated file is readable for a day
  missingok  # => no error if the log file does not exist yet
  notifempty  # => do not rotate a zero-byte file
  postrotate  # => after rotating, tell Caddy to reopen its log file
    systemctl reload caddy >/dev/null 2>&1 || true  # => reload, not restart, so no dropped requests
  endscript
}
# Also cap the journal: /etc/systemd/journald.conf -> SystemMaxUse=500M
```

**Run**: `install myapp.logrotate /etc/logrotate.d/myapp`, then `logrotate -dv /etc/logrotate.d/myapp`
(dry-run) or `logrotate -fv ...` (force).

**Expected** (forced rotation):

```text
rotating pattern: /var/log/caddy/*.log
renaming /var/log/caddy/access.log to /var/log/caddy/access.log.1
```

**Key takeaway**: log rotation turns "logs grow forever" into "logs are bounded and compressed,"
which is what keeps a long-running box's disk from filling silently under you.

**Why it matters**: a full disk takes down every service on the box -- logging, the database, the app
itself -- and presents as a dozen confusing failures whose single root cause is "no space." Rotation
prevents that entire class of outage with one config file.

---

### Example 25: Install a Git-Push PaaS

_ex-25 &middot; exercises co-16_

A PaaS builds and deploys your app from a `git push` -- the contrast case that shows what the manual
substrate was automating. This installs a self-hosted git-push PaaS (Dokku) on the same box, so you
can feel the trade-off without a second provider.

**`learning/code/ex-25-install-paas/install-paas.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
wget -qO- https://dokku.com/install.sh | DOKKU_TAG=v0.34.9 bash  # => pinned tag; re-verify CVE-clean
dokku version  # => co-16 proof: the platform CLI responds
systemctl is-active dokku  # => the supervisor managing deploys is running
dokku apps:create myapp  # => a named slot a 'git push' will fill (Example 26)
echo "[verify] PaaS up; app 'myapp' created"
echo "[next]  Example 26 deploys the app with a single 'git push dokku main:master'"
```

**Run**: `bash install-paas.sh`

**Expected**:

```text
0.34.9
active
-----> Creating myapp... done
[verify] PaaS up; app 'myapp' created
```

**Key takeaway**: the PaaS is a build+release+supervise+proxy machine that turns "deploy my app"
into "push to a git remote" -- absorbing, in one install, every primitive Examples 1-24 built by hand.

**Why it matters**: feeling the PaaS absorb the build, the release, the supervision, and the TLS in
one push is what makes the co-20 trade-off concrete. You can finally name what you pay a managed
platform for, and what you give up when you self-host.

---

### Example 26: Deploy via git push

_ex-26 &middot; exercises co-16_

The whole point of a PaaS: ONE command (`git push`) builds and releases the app. This is the contrast
to Examples 7-10's hand-managed `systemd` unit.

**`learning/code/ex-26-paas-git-push-deploy/deploy.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
BOX_IP="$(cat .box-ip)"; APP_NAME="myapp"
git remote add dokku "dokku@${BOX_IP}:${APP_NAME}" 2>/dev/null || git remote set-url dokku "dokku@${BOX_IP}:${APP_NAME}"
git push dokku main:master  # => co-16: the push triggers build -> release -> deploy automatically
echo "[verify] curl the deploy URL Dokku printed"
echo "         or: ssh dokku@${BOX_IP} ps:status ${APP_NAME}   # => shows 'running'"
```

**Run**: `bash deploy.sh`

**Expected** (tail):

```text
-----> Deploying myapp...
-----> App myapp deployed
        http://192.0.2.10:31234
[verify] curl the deploy URL Dokku printed
```

**Key takeaway**: the difference between this and Example 8 is the entire co-16 thesis -- the same
"get my app serving" outcome, achieved by a single `git push` instead of a manual unit file, venv,
and proxy edit.

**Why it matters**: this is the abstraction the PaaS sells. Every step Examples 1-24 taught (runtime,
unit, proxy, TLS) still happens -- the PaaS just automates them, hiding the box while keeping it
yours.

---

### Example 27: Buildpack Deploy Without a Dockerfile

_ex-27 &middot; exercises co-17_

A Procfile declares your process types and start commands. A buildpack reads it, DETECTS your
language, and supplies the runtime -- zero image authoring. This is the "convenience" half of co-17's
trade-off.

**`learning/code/ex-27-buildpack-deploy/Procfile`**

```text
web: gunicorn app:app --bind 0.0.0.0:${PORT:-5000}
# web          => a PROCESS TYPE named 'web' (the PaaS routes HTTP to this type)
# gunicorn ... => the start command the buildpack-installed gunicorn runs
# ${PORT:-5000} => the PaaS injects $PORT at runtime; default 5000 if unset
# 0.0.0.0      => bind ALL interfaces INSIDE the container; the PaaS proxy maps it out

# (optional) a second process type for a background worker:
# worker: python worker.py
```

**Run**: commit the Procfile + `requirements.txt`, then `git push dokku main:master`

**Expected**:

```text
-----> Python app detected
-----> Installing requirements.txt dependencies using pip
-----> Discovering process types
       Procfile declares types -> web
-----> Releasing myapp...
```

**Key takeaway**: a buildpack means you never write a Dockerfile -- the PaaS infers the runtime from
your files (`requirements.txt` -> Python) and builds the image for you.

**Why it matters**: this is the convenience side of co-17. Example 28 then deploys the SAME app via a
Dockerfile so you can feel the control trade-off -- buildpack = zero image work but constrained to
what it detects; Dockerfile = full control but you own every layer.

---

### Example 28: Dockerfile Deploy on the PaaS

_ex-28 &middot; exercises co-17_

The "control" half of co-17: instead of a buildpack detecting your language, YOU specify the exact
image, layer by layer. The PaaS detects this Dockerfile and builds from IT, ignoring the Procfile.
Deploy with the same `git push` -- only the build recipe changes.

**`learning/code/ex-28-docker-deploy/Dockerfile`**

```dockerfile
# syntax=docker/dockerfile:1
FROM docker.io/library/python:3.12-slim  # => specific tag (not 'latest'); slim base
RUN apt-get update \
    && apt-get install -y --no-install-recommends curl ca-certificates \
    && rm -rf /var/lib/apt/lists/*  # => clean the apt cache so it is not baked into the image
WORKDIR /app
COPY requirements.txt ./  # => manifest alone, so dependency install caches independently of code
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./  # => changes every push -> invalidates only this thin layer
RUN useradd --create-home appuser  # => a dedicated unprivileged user (co-04 inside the container)
USER appuser  # => all subsequent commands + the CMD run as appuser, not root
ENV PORT=5000  # => default; the PaaS overrides it at runtime
EXPOSE 5000  # => DOCUMENTS the port (the PaaS maps it; this does not publish it)
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]  # => exec form (JSON array)
```

**Run**: commit the Dockerfile, then `git push dokku main:master`

**Expected**:

```text
-----> Dockerfile app detected
-----> Building image ...
-----> Releasing myapp...
$ curl http://<box>/<app-url>/health   # => parity with Example 27's buildpack build
```

**Key takeaway**: the Dockerfile and the Procfile (Example 27) both deploy the SAME app -- the
difference is who owns the runtime recipe (you vs. the buildpack), and that is the entire co-17
choice.

**Why it matters**: knowing which you reached for is knowing where your build's reproducibility comes
from. A buildpack is convenient but opaque; a Dockerfile is verbose but fully explicit and portable
to any container runtime, not just this PaaS.

---

### Example 29: PaaS Env Config and Secrets

_ex-29 &middot; exercises co-12, co-16_

On a PaaS, config and secrets are set via the PaaS CLI (stored in the PaaS, injected into the
container at runtime) -- NOT in the repo. This is co-12/co-13 applied to the PaaS altitude.

**`learning/code/ex-29-paas-env-config/configure.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
APP_NAME="myapp"
dokku config:set "${APP_NAME}" APP_LOG_LEVEL=info APP_FEATURE_NEW_CACHE=false  # => co-12: tunables
SIGNING_SECRET="$(openssl rand -hex 32)"  # => generated in this shell; the repo never sees it
dokku config:set "${APP_NAME}" "APP_SIGNING_SECRET=${SIGNING_SECRET}"  # => co-13: secret in the PaaS
dokku ps:restart "${APP_NAME}"  # => rebuild the env into the running process
echo "[verify] ssh dokku@<box> config:show ${APP_NAME}   # => APP_* keys are present"
```

**Run**: `bash configure.sh`

**Expected**:

```text
-----> Setting config vars and restarting myapp
[verify] ssh dokku@<box> config:show myapp   # => APP_* keys are present
```

**Key takeaway**: the "config in env, never in code" rule (co-12) holds at every altitude -- on bare
metal it is an env file (Example 15); on a PaaS it is `config:set`; either way the repo stays clean.

**Why it matters**: a secret committed to a PaaS-deployed repo is just as leaked as any other. The
PaaS's `config:set` is the out-of-band channel that keeps the secret on the platform, injected at
runtime, never in git -- the same hard rule, different mechanism.

---

### Example 30: Attach a Domain and TLS on the PaaS

_ex-30 &middot; exercises co-10, co-11, co-16_

The PaaS does what Caddy did by hand in Examples 13-14: point a domain at it and obtain automatic
TLS. The difference: it is two CLI commands, not a Caddyfile edit -- the PaaS absorbs the proxy +
ACME chore.

**`learning/code/ex-30-paas-tls-domain/attach-domain.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
APP_NAME="myapp"; DOMAIN="paas.example.com"
echo "[step 1] create an A record: ${DOMAIN}. -> <box-ip> at your DNS provider (as in Example 13)"
dokku domains:add "${APP_NAME}" "${DOMAIN}"  # => the PaaS proxy now routes this domain to the app
dokku letsencrypt:set "${APP_NAME}" email "ops@example.com"  # => co-10: the ACME account contact
dokku letsencrypt:enable "${APP_NAME}"  # => obtain + install the cert; auto-renew enabled too
echo "[verify] curl -sI https://${DOMAIN}/         # => expect HTTP/2 200"
```

**Run**: `bash attach-domain.sh`

**Expected**:

```text
-----> Domains updated: myapp
-----> Let's Encrypt is now enabled for myapp
[verify] curl -sI https://paas.example.com/   # => expect HTTP/2 200
```

**Key takeaway**: the PaaS collapses Examples 11-14 (install proxy, edit Caddyfile, DNS, ACME) into
two `dokku` commands -- the exact chore it sells you not having to do.

**Why it matters**: this is the managed-platform value proposition made tangible. The same HTTPS
result, with the box's ACME and renewal work absorbed by the platform -- which is precisely the
effort you trade away when you self-host.

---

### Example 31: Roll Back a Deploy

_ex-31 &middot; exercises co-16, co-18_

A bad deploy happens. A PaaS keeps a history of releases, so "go back to the last known-good one" is
ONE command -- the operational payoff of co-16's build history.

**`learning/code/ex-31-rollback-a-deploy/rollback.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
APP_NAME="myapp"
echo "[history] recent releases of ${APP_NAME}:"
dokku releases:list "${APP_NAME}"  # => numbered list, newest last (v1 .. v5)
ROLLBACK_TO="${1:-vN}"  # => pass the target version as $1
echo "[rollback] target: ${ROLLBACK_TO}"
dokku tags:deploy "${APP_NAME}" "${ROLLBACK_TO}" 2>/dev/null || dokku ps:rollback "${APP_NAME}"
echo "[verify] curl -s https://${APP_NAME}.<domain>/version   # => the previous version string"
```

**Run**: `bash rollback.sh v4`

**Expected**:

```text
[history] recent releases of myapp:
v1  2026-07-30 09:00:00 +0000
v2  2026-07-30 10:00:00 +0000
...
[verify] curl -s https://myapp.<domain>/version   # => the previous version string
```

**Key takeaway**: a release history turns "a bad deploy" from a scramble into a one-command revert --
the version you just shipped is never load-bearing if the previous one is one command away.

**Why it matters**: on the self-hosted side (Examples 7-10), a bad deploy means re-running setup.sh
and hoping; on the PaaS, every push is an immutable release you can return to instantly. This is a
concrete piece of operational value the managed platform provides.

---

### Example 32: A Zero-Downtime Restart

_ex-32 &middot; exercises co-18_

A naive "stop then start" deploy drops every in-flight request at the moment of the stop. This script
does a health-checked restart that drops no requests: hammer the endpoint with `curl` in a loop,
restart the app, and prove the loop keeps getting 200s throughout.

**`learning/code/ex-32-zero-downtime-restart/traffic-loop.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
DOMAIN="myapp.example.com"
echo "[traffic] curling https://${DOMAIN}/health in a loop; failures are PRINTED"
while true; do  # => hammer until Ctrl-C
  CODE="$(curl -s -o /dev/null -w '%{http_code}' --max-time 3 "https://${DOMAIN}/health" || echo "ERR")"
  if [ "${CODE}" != "200" ]; then echo "[drop!] $(date +%T) got ${CODE}"; fi  # => a dropped request prints here
  sleep 0.2  # => 5 requests/sec -- enough to catch a gap during the restart
done
# In a second terminal: systemctl restart myapp
# [verify] this loop prints NO "[drop!]" lines during the restart window.
```

**Run**: `bash traffic-loop.sh` in terminal 1; `systemctl restart myapp` in terminal 2

**Expected**: terminal 1 prints NO `[drop!]` lines across the restart.

**Key takeaway**: zero-downtime is an OBSERVABLE property -- you prove it by hammering the endpoint
during the cutover and watching for gaps, not by assuming it.

**Why it matters**: a restart that drops even a few requests breaks clients mid-operation. Example 73
pushes this further with a blue-green swap that keeps the OLD instance answering until the NEW one is
proven healthy; the discipline is the same -- verify, don't assume.

---

← Previous: [Beginner Examples](./beginner.md) · Next: [Advanced Examples](./advanced.md) →
