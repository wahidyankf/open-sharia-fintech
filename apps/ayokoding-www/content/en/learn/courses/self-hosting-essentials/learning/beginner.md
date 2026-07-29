---
title: "Beginner Examples"
date: 2026-07-30T00:00:00+07:00
draft: false
weight: 10
---

Examples 1-16 build the deployment substrate one primitive at a time: provision a Linux VM, log in
over SSH with a key, add a non-root user and a firewall, install the runtime, run the service in the
foreground, hand it to `systemd`, enable it on boot, read its logs, make it restart on crash, install
a reverse proxy, expose the app through it on a real domain with automatic TLS, and configure it via
env while keeping secrets out of the repo. Every artifact is a real shell script, `systemd` unit,
Caddyfile, or env file -- minimal application code -- followable on a single cheap VM or a local VM.

---

### Example 1: Provision a Linux VM and Record Its IP

_ex-01 &middot; exercises co-02_

Provisioning is the first reproducible step of any self-host: create a Linux VM, wait for it to
answer, and RECORD its public IP so every later step (SSH, DNS, TLS) refers to one stable value
rather than a dashboard you forget.

**`learning/code/ex-01-provision-a-vm/provision.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail  # => fail fast: -e exit on error, -u error on unset var, -o pipefail
BOX_NAME="myapp-box"  # => co-02: a stable name for the instance across all later steps
echo "[provision] creating Linux VM: ${BOX_NAME}"
BOX_IP="192.0.2.10"  # => co-02: placeholder TEST-NET-3 IP; a real run writes the real IP here
echo "${BOX_IP}" > .box-ip  # => persist it so later scripts read, not re-derive
echo "[verify] probing ${BOX_IP}:22 (SSH) ..."
nc -z -w 5 "${BOX_IP}" 22 && echo "[verify] SSH port reachable" || echo "[verify] port not open yet (may be booting)"
```

**Run**: `bash provision.sh`

**Expected**:

```text
[provision] creating Linux VM: myapp-box
[verify] probing 192.0.2.10:22 (SSH) ...
[verify] SSH port reachable
```

**Key takeaway**: provisioning ends by persisting the box's IP to disk (`.box-ip`), so SSH, DNS,
and TLS each read one value instead of re-deriving it -- the first move of reproducibility.

**Why it matters**: recording the IP at provisioning time is what lets Example 42's disaster rebuild
succeed later. A box whose address lives only in a browser tab is a box you cannot rebuild from
memory; a box whose address (and setup) are captured in files is a box you can lose and recover.

---

### Example 2: SSH Key-Only Login

_ex-02 &middot; exercises co-03_

Key-based SSH replaces a brute-forceable password with an unguessable key pair: the private key stays
on your laptop, the public key goes on the box. Once the key works, password login is disabled --
closing the single most common remote-compromise vector.

**`learning/code/ex-02-ssh-key-login/ssh-setup.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
KEY_PATH="${HOME}/.ssh/myapp_box_ed25519"  # => ed25519: short, fast, modern; prefer over RSA
ssh-keygen -t ed25519 -f "${KEY_PATH}" -N "" -C "myapp-box $(date +%F)"  # => creates key + .pub
BOX_IP="$(cat .box-ip)"
ssh-copy-id -i "${KEY_PATH}.pub" "root@${BOX_IP}"  # => installs the PUBLIC key on the box
ssh -i "${KEY_PATH}" -o BatchMode=yes "root@${BOX_IP}" 'echo key-login-ok'  # => BatchMode refuses passwords
ssh -i "${KEY_PATH}" "root@${BOX_IP}" 'sed -i \
  -e "s/^#\?PasswordAuthentication.*/PasswordAuthentication no/" \
  -e "s/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/" \
  /etc/ssh/sshd_config && systemctl reload ssh'  # => password login now refused
echo "[verify] password login should now FAIL: ssh root@${BOX_IP}  # => Permission denied (publickey)"
```

**Run**: `bash ssh-setup.sh`

**Expected**:

```text
key-login-ok
[verify] password login should now FAIL: ssh root@192.0.2.10  # => Permission denied (publickey)
```

**Key takeaway**: the same key that proves who you are also lets you flip `PasswordAuthentication
no` -- once the key works, passwords are dead on this box, and the SSH brute-force bots hammering
port 22 (Example 43's `fail2ban`) can never succeed.

**Why it matters**: passwords are reuseable across boxes and guessable by any bot; a key pair is
neither. Disabling password login is the cheapest, highest-leverage hardening step on any box -- and
it is reversible only by someone who already has console access, which is the right asymmetry.

---

### Example 3: Create a Non-Root Sudo User

_ex-03 &middot; exercises co-04_

Running everything as root is the other half of "compromise waiting to happen": a process that runs
as root IS the whole box. The safe baseline is a dedicated, unprivileged user with `sudo` for the few
actions that genuinely need it.

**`learning/code/ex-03-create-nonroot-user/add-user.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
DEPLOY_USER="deploy"  # => a single-purpose account named for what it does
useradd -m -s /bin/bash "${DEPLOY_USER}"  # => co-04: unprivileged, no root powers by default
usermod -aG sudo "${DEPLOY_USER}"  # => grant narrow sudo (-aG appends without leaving others)
PUBKEY="$(cat "${HOME}/.ssh/myapp_box_ed25519.pub")"
install -d -m 700 -o "${DEPLOY_USER}" -g "${DEPLOY_USER}" "/home/${DEPLOY_USER}/.ssh"  # => .ssh must be 0700
echo "${PUBKEY}" > "/home/${DEPLOY_USER}/.ssh/authorized_keys"  # => same key now accepted for deploy@
chmod 600 "/home/${DEPLOY_USER}/.ssh/authorized_keys"  # => must be 0600 or sshd ignores it
chown "${DEPLOY_USER}:${DEPLOY_USER}" "/home/${DEPLOY_USER}/.ssh/authorized_keys"
BOX_IP="$(cat .box-ip)"
echo "[verify] ssh -i ~/.ssh/myapp_box_ed25519 ${DEPLOY_USER}@${BOX_IP} 'sudo -n true || echo sudo-needs-password'"
```

**Run**: `bash add-user.sh`

**Expected**:

```text
[verify] ssh -i ~/.ssh/myapp_box_ed25519 deploy@192.0.2.10 'sudo -n true || echo sudo-needs-password'
```

**Key takeaway**: a service running as `deploy` can do only what `deploy` can do; `sudo` is the one
narrow gate to root, used only for the few setup steps that need it.

**Why it matters**: this is defense in depth. If the app is ever exploited, the attacker gets
`deploy`'s privileges -- not root's. The blast radius is the service, not the whole box, which is the
difference between "restart the service" and "rebuild the box from scratch."

---

### Example 4: Enable the Firewall with ufw

_ex-04 &middot; exercises co-05_

`ufw` (Uncomplicated Firewall) is a default-DENY front end to netfilter: you explicitly open only the
ports a service needs and every other port stays unreachable from the internet -- the single most
effective way to shrink a box's attack surface.

**`learning/code/ex-04-enable-firewall/ufw-setup.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
ufw default deny incoming   # => co-05: block every port we did not explicitly open
ufw default allow outgoing  # => the box itself can still reach out (updates, DNS, ACME)
ufw allow 22/tcp comment 'ssh'    # => open SSH FIRST so we do not lock ourselves out
ufw allow 80/tcp comment 'http'   # => co-09/co-10: HTTP, for the ACME challenge and the ->HTTPS redirect
ufw allow 443/tcp comment 'https' # => co-09/co-10: HTTPS, where the reverse proxy terminates TLS
ufw --force enable          # => policies are now LIVE; closed ports become unreachable
ufw status numbered         # => co-05 acceptance: the open set is exactly {22, 80, 443}
echo "[verify] nc -z <box-ip> 8080   # => connection refused/timeout (closed port blocked)"
```

**Run**: `bash ufw-setup.sh`

**Expected**:

```text
Status: active
     To                         Action      From
[ 1] 22/tcp                     ALLOW IN    Anywhere                   # ssh
[ 2] 80/tcp                     ALLOW IN    Anywhere                   # http
[ 3] 443/tcp                    ALLOW IN    Anywhere                   # https
[verify] nc -z <box-ip> 8080   # => connection refused/timeout (closed port blocked)
```

**Key takeaway**: the firewall is default-deny, so "open port" is a deliberate, auditable decision;
a service bound to a port you forgot about is unreachable, not silently exposed.

**Why it matters**: a box without a firewall exposes every listening socket to the whole internet.
The default-deny stance means the only reachable ports are the three you named -- and Example 23 will
later audit even that set down to the true minimum.

---

### Example 5: Install the App Runtime

_ex-05 &middot; exercises co-06_

Before a service can run, the box needs the language runtime it depends on. This pins one version so
a rebuild reproduces the same interpreter rather than grabbing "whatever's latest."

**`learning/code/ex-05-install-runtime/install-runtime.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
apt-get update && apt-get install -y curl ca-certificates  # => curl + certs needed by ACME later
PYTHON_VERSION="3.12"  # => pinned at authoring; re-verify CVE-clean before real use
apt-get install -y "python${PYTHON_VERSION}" "python${PYTHON_VERSION}-venv"  # => exact major.minor
APP_DIR="/opt/myapp"
install -d -o deploy -g deploy -m 755 "${APP_DIR}"  # => owned by the deploy user from Example 3
sudo -u deploy "python${PYTHON_VERSION}" -m venv "${APP_DIR}/venv"  # => isolated interpreter
"${APP_DIR}/venv/bin/python" --version  # => co-06 acceptance: prints the exact version
echo "[verify] expect: Python ${PYTHON_VERSION}.x"
```

**Run**: `bash install-runtime.sh`

**Expected**:

```text
Python 3.12.x
[verify] expect: Python 3.12.x
```

**Key takeaway**: a pinned runtime version + an isolated venv means the app's interpreter is both
reproducible (a rebuild prints the same `--version`) and isolated (no clash with system Python).

**Why it matters**: pinning the version is a `taming-state` move -- it turns "the box works" into
"the box works again on fresh hardware." An unpinned "latest" interpreter is a box that drifts under
you the next time you rebuild it.

---

### Example 6: Run the Service in the Foreground

_ex-06 &middot; exercises co-06_

Before wiring up `systemd`, run the app by hand in the foreground and hit it with `curl`. This
cleanly separates "does the app even work" from "does the supervision work" -- the single best
debugging move when a deploy won't respond.

**`learning/code/ex-06-run-service-foreground/run-foreground.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
APP_DIR="/opt/myapp"; PORT="8000"  # => an unprivileged local port; the proxy fronts 80/443 later
cat > "${APP_DIR}/app.py" <<'PY'  # => a minimal stdlib HTTP service (reused from backend-essentials)
import http.server
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        body = b"ok" if self.path == "/health" else b"hello"  # /health is the probe path
        self.send_response(200); self.send_header("Content-Type","text/plain"); self.end_headers()
        self.wfile.write(body)
    def log_message(self, *a): pass
http.server.HTTPServer(("127.0.0.1", 8000), H).serve_forever()  # bind LOOPBACK only
PY
echo "[run] starting on 127.0.0.1:${PORT} (Ctrl-C to stop) ..."
"${APP_DIR}/venv/bin/python" "${APP_DIR}/app.py"  # => blocks here serving; curl from another shell
echo "[verify] in another terminal: curl http://127.0.0.1:${PORT}/health"
```

**Run**: `bash run-foreground.sh` (then, in a second terminal) `curl http://127.0.0.1:8000/health`

**Expected** (second terminal):

```text
ok
```

**Key takeaway**: the app binds `127.0.0.1` (loopback only), not `0.0.0.0` -- it is reachable
locally but not directly from the internet; the reverse proxy (Example 12) is the public face.

**Why it matters**: confirming the app answers `curl` BEFORE adding `systemd`, a proxy, and TLS means
that when the public endpoint later fails, you already know the app itself works and can narrow the
bug to the layer you just added.

---

### Example 7: Write a systemd Unit for the Service

_ex-07 &middot; exercises co-07_

A `systemd` unit turns "a process I launched by hand" into "a managed service the OS owns." systemd
starts it, restarts it on failure, and starts it on boot -- the difference between a process and a
service.

**`learning/code/ex-07-systemd-unit/myapp.service`**

```ini
[Unit]
Description=MyApp self-hosted service  # => human label shown in systemctl status
After=network-online.target  # => do not start until networking is up
Wants=network-online.target

[Service]
Type=simple  # => foreground process; systemd tracks it directly
User=deploy  # => run as the unprivileged user from Example 3, NOT root (co-04)
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/venv/bin/python /opt/myapp/app.py  # => EXACT command, absolute paths
Restart=on-failure  # => restart only on non-zero exit (Example 10 widens this)
RestartSec=3  # => 3s between a crash and the restart

[Install]
WantedBy=multi-user.target  # => the boot hook 'systemctl enable' plugs into (Example 8)
```

**Run**: `install myapp.service /etc/systemd/system/ && systemctl daemon-reload && systemctl start myapp`

**Expected**:

```text
● myapp.service - MyApp self-hosted service
     Active: active (running)
```

**Key takeaway**: the unit is a small declarative file that replaces "I typed this command once" with
"the OS owns this service" -- the `taming-state` move that makes restart-on-crash and boot-resilience
expressible at all.

**Why it matters**: a unit file is configuration, reproducible from the repo; a manual launch command
is folklore, gone the moment the shell closes. Every later resilience example (10, 36, 68) builds on
this unit existing.

---

### Example 8: Enable the Service on Boot

_ex-08 &middot; exercises co-07, co-15_

`start` runs the service now; `enable` makes it start on the next boot too. Together they give the
resilience property: a reboot is no longer an outage.

**`learning/code/ex-08-enable-on-boot/enable-on-boot.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
UNIT="myapp"
systemctl daemon-reload  # => REQUIRED after any edit under /etc/systemd/system/
systemctl start "${UNIT}"  # => launches ExecStart; Type=simple stays foreground
systemctl status "${UNIT}" --no-pager  # => co-07 proof: "active (running)"
systemctl enable "${UNIT}"  # => creates the WantedBy=multi-user.target symlink (co-15 boot hook)
echo "[verify] is-enabled: $(systemctl is-enabled ${UNIT})"  # => expect: enabled
echo "[next]  reboot the box (Example 36) and confirm the service returns on its own"
```

**Run**: `bash enable-on-boot.sh`

**Expected**:

```text
● myapp.service - MyApp self-hosted service
     Active: active (running)
[verify] is-enabled: enabled
```

**Key takeaway**: `enable` is the single line that turns a crash/reboot from a 3am phone call into a
non-event -- the OS brings the service back without you.

**Why it matters**: this is co-15's core property in its simplest form. A service that does not
survive a reboot is a service that goes down every patch, every power blip, every provider restart;
`enable` is the one-word fix.

---

### Example 9: Read Service Status and Logs

_ex-09 &middot; exercises co-08, co-14_

`systemctl status` and `journalctl -u` are the first two commands reached for when "is it up and why
did it fail." Knowing them cold turns an outage into a five-minute diagnosis.

**`learning/code/ex-09-service-status-logs/inspect.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
UNIT="myapp"
systemctl is-active "${UNIT}"  # => prints 'active' / 'inactive' / 'failed' (machine-parseable)
systemctl status "${UNIT}" --no-pager --full  # => human view: state, PID, recent log lines
journalctl -u "${UNIT}" --no-pager -n 20  # => the last 20 lines for this service
journalctl -u "${UNIT}" --no-pager --since "10 min ago"  # => co-14: only recent entries
systemctl restart "${UNIT}"  # => stop + start; produces a clean pair of journal lines
journalctl -u "${UNIT}" --no-pager -n 10  # => the stop/start lines should now be visible
echo "[verify] the log should show 'Stopped' then 'Started' for ${UNIT}"
```

**Run**: `bash inspect.sh`

**Expected**:

```text
active
● myapp.service ... Active: active (running)
[verify] the log should show 'Stopped' then 'Started' for myapp
```

**Key takeaway**: systemd captures the service's stdout+stderr into the journal, so `journalctl -u`
is where "why did it fail" always lives -- one command, one place, every service.

**Why it matters**: a deployed service with no reachable logs is a black box. The journal is the
single, unified log stream `systemd` gives every unit for free, and it is the substrate every later
observability example (17, 18, 24, 39, 65-67) reads from.

---

### Example 10: Restart on Crash

_ex-10 &middot; exercises co-15_

Drop-in replacement for Example 7's unit, widening `Restart` from `on-failure` to `always`. If the
process dies for any reason, systemd brings it back -- the property that turns a crash from an
incident into a non-event.

**`learning/code/ex-10-restart-on-crash/myapp.service`**

```ini
[Unit]
Description=MyApp self-hosted service (restart-on-crash)
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=deploy
WorkingDirectory=/opt/myapp
ExecStart=/opt/myapp/venv/bin/python /opt/myapp/app.py

Restart=always  # => restart on ANY exit (crash, OOM, even a clean exit) -- widest possible
RestartSec=3  # => 3s pause between death and revival (avoids a hot crash loop)
StartLimitIntervalSec=60  # => over a 60s window ...
StartLimitBurst=5  # => ... allow at most 5 restarts before giving up (stops an infinite loop)

[Install]
WantedBy=multi-user.target
```

**Run**: overwrite the unit, `systemctl daemon-reload && systemctl restart myapp`, then `kill -9
$(systemctl show -p MainPID --value myapp)` and watch it revive.

**Expected**:

```text
# after killing the process and waiting ~3s:
$ systemctl is-active myapp
active
$ journalctl -u myapp -n 3
... Stopped MyApp self-hosted service ...
... Started MyApp self-hosted service ...
```

**Key takeaway**: `Restart=always` makes "alive" the DEFAULT state -- a crash is recovered
automatically, up to the `StartLimitBurst` cap that prevents an infinite crash loop from burning the
box.

**Why it matters**: without a restart policy, a single segfault at 4am takes the service down until a
human notices. With `Restart=always`, that same segfault is a brief blip the box heals itself, which
is the whole point of co-15.

---

### Example 11: Install a Reverse Proxy

_ex-11 &middot; exercises co-09_

The reverse proxy terminates public traffic on 80/443 and forwards to the app on its local port.
Caddy is chosen first because its config is tiny and it does automatic TLS (Example 14) by default.

**`learning/code/ex-11-install-reverse-proxy/install-caddy.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
apt-get install -y debian-keyring debian-archive-keyring apt-transport-https curl
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' > /etc/apt/sources.list.d/caddy-stable.list
apt-get update && apt-get install -y caddy  # => version from the repo; re-verify before real use
systemctl enable --now caddy  # => start now AND on boot (the proxy must survive reboots too)
sleep 2
curl -sI http://127.0.0.1:80 | head -n 1  # => co-09 proof: a status line from Caddy itself
echo "[verify] expect: HTTP/1.1 200 (or 301) -- Caddy is answering on :80"
echo "[next]  Example 12 points it at the app; Example 14 adds real TLS"
```

**Run**: `bash install-caddy.sh`

**Expected**:

```text
HTTP/1.1 200 OK
[verify] expect: HTTP/1.1 200 (or 301) -- Caddy is answering on :80
```

**Key takeaway**: the proxy is its own service (`systemctl enable --now caddy`) -- it must survive
reboots just like the app, or the app behind it becomes unreachable on the next boot.

**Why it matters**: binding the app directly to 443 means re-implementing TLS, virtual hosting, and
graceful shutdown inside the app. A proxy centralizes all of that at one chokepoint and keeps the app
simple -- the architecture every later proxy example (12, 22, 37, 51-60) assumes.

---

### Example 12: Proxy Public Traffic to the App

_ex-12 &middot; exercises co-09_

Two lines of Caddyfile: listen on `:80` and `reverse_proxy` every request to the app's local port.
The app is now reachable through the proxy on the public HTTP port rather than directly on 8000.

**`learning/code/ex-12-proxy-to-app/Caddyfile`**

```caddy
:80 {  # => co-09: the proxy's public listen address (port 80, all interfaces)
  reverse_proxy 127.0.0.1:8000 {  # => forward to the app's loopback port from Example 6
    header_up X-Forwarded-Proto {scheme}  # => tell the app whether upstream was http/https
    header_up X-Forwarded-Host {host}  # => preserve the original Host the caller asked for
  }
  log {  # => co-09/co-14: every proxied request becomes a structured log line
    output file /var/log/caddy/access.log
    format console  # => human-readable; switch to 'json' in Example 65
  }
}
```

**Run**: `install Caddyfile /etc/caddy/ && systemctl reload caddy`, then `curl http://127.0.0.1/health`

**Expected**:

```text
ok
```

**Key takeaway**: the response body is the APP's ("ok"/"hello"), not Caddy's welcome page -- proof the
proxy is forwarding rather than serving its own content.

**Why it matters**: this is the moment the app stops being "a process on a box" and starts being "a
service reachable on a public port." The proxy is the public face; the app stays bound to loopback,
isolated from direct internet exposure.

---

### Example 13: Point a DNS A Record at the Box

_ex-13 &middot; exercises co-11_

An A record maps a name (`myapp.example.com`) to the box's IPv4 address, so the service is reachable
by name and ACME (Example 14) can prove domain control. The record is created at your DNS provider;
this script VERIFIES it resolves correctly once it exists.

**`learning/code/ex-13-dns-a-record/dns-verify.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
DOMAIN="myapp.example.com"  # => the name you will request a certificate for (Example 14)
EXPECTED_IP="$(cat .box-ip)"  # => the IP Example 1 recorded -- what the record SHOULD return
echo "[step 1] At your DNS provider, create an A record:"
echo "         ${DOMAIN}.  IN  A  ${EXPECTED_IP}"
RESOLVED="$(dig +short "${DOMAIN}" A | tr -d '[:space:]')"  # => the addresses the world now sees
echo "[step 2] resolved: ${RESOLVED:-<nothing-yet>}"  # => empty until propagation completes
if [ "${RESOLVED}" = "${EXPECTED_IP}" ]; then
  echo "[verify] PASS: ${DOMAIN} -> ${EXPECTED_IP}"  # => safe to proceed to Example 14 (TLS)
else
  echo "[verify] WAIT: not yet propagated (expected ${EXPECTED_IP}); retry in a minute"
fi
```

**Run**: `bash dns-verify.sh`

**Expected** (after propagation):

```text
[step 1] At your DNS provider, create an A record:
         myapp.example.com.  IN  A  192.0.2.10
[step 2] resolved: 192.0.2.10
[verify] PASS: myapp.example.com -> 192.0.2.10
```

**Key takeaway**: DNS is the mapping that turns "an IP" into "a name a certificate can be issued for"
-- it is the precondition for both TLS and human-usable URLs, and you verify it by polling until
`dig` returns the expected IP.

**Why it matters**: without a DNS record, Example 14's ACME challenge cannot prove you control the
domain, so no certificate is issued. DNS is the often-forgotten prerequisite that makes "real TLS on
a personal box" actually work.

---

### Example 14: Automatic TLS with ACME

_ex-14 &middot; exercises co-10_

Replace Example 12's `:80` block with a real domain. Caddy then automatically obtains a Let's
Encrypt certificate via ACME on first request, serves it on `:443`, redirects `:80` to `:443`, and
renews it before expiry -- all with zero `openssl` and zero cron.

**`learning/code/ex-14-automatic-tls/Caddyfile`**

```caddy
myapp.example.com {  # => co-10/co-11: a real domain -- Caddy issues a cert for THIS name
  reverse_proxy 127.0.0.1:8000  # => same forward as Example 12, now over TLS
}
# Caddy auto-manages, on first HTTPS request:
#  1. runs an ACME HTTP-01 challenge against Let's Encrypt
#  2. obtains + stores the cert
#  3. serves HTTPS on :443 AND redirects :80 -> :443
#  4. renews the cert before its 90-day expiry (~30 days out)
```

**Run**: `install Caddyfile /etc/caddy/ && systemctl reload caddy`, then
`curl https://myapp.example.com/health`

**Expected**:

```text
HTTP/2 200
# openssl s_client ... | openssl x509 -noout -issuer
issuer=O=Let's Encrypt, CN=E5
```

**Key takeaway**: one line -- a real domain instead of `:80` -- is all Caddy needs to obtain, serve,
and renew a real CA-issued certificate automatically. No `openssl`, no cron, no manual renewal chore.

**Why it matters**: HTTPS is table stakes for any public service, and ACME is the automation that
makes "real TLS on a personal box" practical rather than a weekend of certificate suffering. This is
the moment the self-hosted service becomes indistinguishable from a managed one to a caller.

---

### Example 15: Configure the App via an Env File

_ex-15 &middot; exercises co-12_

Non-secret configuration lives in the environment, not the repo. This file holds the app's tunables;
the `systemd` unit (Example 62) reads it. Permissions are locked to the deploy user so only the
service can read it.

**`learning/code/ex-15-env-config/app.env`**

```bash
# --- App tunables (non-secret; safe to read) ---
APP_HOST=127.0.0.1  # => co-12: bind loopback; the proxy (Example 12) is the public face
APP_PORT=8000  # => co-12: the local port the proxy forwards to
APP_LOG_LEVEL=info  # => co-12/co-14: controls verbosity in the journal
APP_FEATURE_NEW_CACHE=false  # => co-12: a feature flag, toggled per-environment

# --- The one rule this file ENFORCES: no secrets here ---
# A DATABASE_URL with a password, an API key, a signing secret -- NONE belong here.
# This file lives next to the repo; a secret here is one git-add away from public.
# Put secrets in Example 16's separate, mode-0600, gitignored file instead.
```

**Run**: `install -o deploy -g deploy -m 600 app.env /opt/myapp/app.env`, then
`sudo -u deploy bash -c 'set -a; . /opt/myapp/app.env; env | grep ^APP_'`

**Expected**:

```text
APP_HOST=127.0.0.1
APP_PORT=8000
APP_LOG_LEVEL=info
APP_FEATURE_NEW_CACHE=false
```

**Key takeaway**: separating config from code is what lets the identical image run in staging and
prod -- the difference between two environments becomes a set of env variables, not a second copy of
the application.

**Why it matters**: a value hardcoded in the repo is baked in; a value in the environment is
swappable at deploy time without a rebuild. Example 29 does the same thing on a PaaS, and Example 61
templates this file -- all built on this same config-not-code principle.

---

### Example 16: Keep Secrets Out of the Repo

_ex-16 &middot; exercises co-13_

The hard-iron rule: no system secret is ever committed to a git-tracked file -- history is permanent.
This script sets a secret on the box out of band (a mode-0600 file the repo never sees), then PROVES
the repo contains no secret material.

**`learning/code/ex-16-secrets-not-in-repo/verify-no-secrets.sh`**

```bash
#!/usr/bin/env bash
set -euo pipefail
SECRET_PATH="/opt/myapp/secrets.env"  # => lives ON THE BOX, outside the repo entirely
FRESH_SECRET="$(openssl rand -hex 32)"  # => 256 bits, generated on the box
install -o deploy -g deploy -m 600 /dev/stdin "${SECRET_PATH}" <<<"APP_SIGNING_SECRET=${FRESH_SECRET}"
chmod 600 "${SECRET_PATH}"

grep -qE 'secrets\.env|\.env$' .gitignore || echo "[warn] add 'secrets.env' and '.env' to .gitignore"
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  if git grep -nIE '(sk-live-|ghp_|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC )?PRIVATE KEY)' -- ':!*.md' >/dev/null 2>&1; then
    echo "[verify] FAIL: a secret-looking string is tracked in the repo"; exit 1
  fi
fi
echo "[verify] PASS: no secret material tracked; secret lives only at ${SECRET_PATH}"
```

**Run**: `bash verify-no-secrets.sh`

**Expected**:

```text
[verify] PASS: no secret material tracked; secret lives only at /opt/myapp/secrets.env
```

**Key takeaway**: a committed secret is permanent (git history is forever) and a single accidental
push away from public; the server-side discipline is a mode-0600 file the repo never sees, plus a
scan gate that catches slips before they land.

**Why it matters**: this is the single most expensive mistake to recover from -- once a secret is in
git, rotating it is the only remedy, and "it was only one commit" is no defense. Example 64 adds a
pre-commit hook that blocks the slip at commit time, the last line of defense.

---

← Previous: [Learning Overview](./overview.md) · Next: [Intermediate Examples](./intermediate.md) →
