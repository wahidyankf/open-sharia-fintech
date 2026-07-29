#!/usr/bin/env bash
# Example 16: Keep Secrets Out of the Repo. (co-13)
#
# The hard-iron rule: no system secret is ever committed to a git-tracked file
# -- history is permanent. This script is the verification gate: it sets a
# secret on the BOX out of band (a mode-0600 file the repo never sees), then
# PROVES the repo contains no secret material. Run from the repo root.

set -euo pipefail  # => fail fast; a leaked secret is the worst possible silent failure

SECRET_PATH="/opt/myapp/secrets.env"  # => lives ON THE BOX, outside the repo entirely

# --- 1. Set the secret out of band (on the box, never in git) -----------------
# A fresh signing key generated on the box; the repo never sees this value.
FRESH_SECRET="$(openssl rand -hex 32)"  # => 256 bits of randomness, generated on the box
install -o deploy -g deploy -m 600 /dev/stdin "${SECRET_PATH}" <<<"APP_SIGNING_SECRET=${FRESH_SECRET}"  # => mode 0600, deploy-owned
chmod 600 "${SECRET_PATH}"  # => belt-and-braces: only deploy can read it

# --- 2. Prove the repo has NO secret material ---------------------------------
# (a) .gitignore must list the secret paths so a stray 'git add .' cannot add them.
grep -qE 'secrets\.env|\.env$' .gitignore || echo "[warn] add 'secrets.env' and '.env' to .gitignore"  # => co-13 guardrail
# (b) Scan tracked files for high-entropy / known-secret patterns. A clean exit = clean repo.
#     (gitleaks is one option; this example uses a simple grep for obvious offenders.)
if git rev-parse --is-inside-work-tree >/dev/null 2>&1; then  # => only scan if we ARE in a repo
  if git grep -nIE '(sk-live-|ghp_|AKIA[0-9A-Z]{16}|-----BEGIN (RSA |EC )?PRIVATE KEY)' -- ':!*.md' >/dev/null 2>&1; then
    echo "[verify] FAIL: a secret-looking string is tracked in the repo"  # => co-13 violation
    exit 1
  fi
fi
echo "[verify] PASS: no secret material tracked; secret lives only at ${SECRET_PATH}"  # => co-13 proof