#!/usr/bin/env bash
# Example 30: Attach a Domain and TLS on the PaaS. (co-10, co-11, co-16)
#
# The PaaS does what Caddy did by hand in Examples 13-14: point a domain at it
# and obtain automatic TLS. The difference: it is two CLI commands, not a
# Caddyfile edit -- the PaaS absorbs the proxy + ACME chore. Run on the box.

set -euo pipefail  # => fail fast; a half-attached domain serves the wrong cert

APP_NAME="myapp"  # => the deployed app
DOMAIN="paas.example.com"  # => a DIFFERENT domain from the self-hosted one, to keep them distinct

# --- 1. Point a DNS record at the box first (co-11, as in Example 13) ---------
echo "[step 1] create an A record: ${DOMAIN}. -> <box-ip> at your DNS provider (as in Example 13)"  # => prerequisite for ACME

# --- 2. Tell the PaaS which domains to answer for -----------------------------
dokku domains:add "${APP_NAME}" "${DOMAIN}"  # => the PaaS proxy now routes this domain to the app

# --- 3. Enable automatic TLS (Let's Encrypt via the PaaS) ---------------------
# 'letsencrypt:set' configures ACME; the email is used for expiry notices.
dokku letsencrypt:set "${APP_NAME}" email "ops@example.com"  # => co-10: the ACME account contact
dokku letsencrypt:enable "${APP_NAME}"  # => obtain + install the cert; auto-renew is enabled too

# --- 4. Verify HTTPS with a real CA-issued cert -------------------------------
echo "[verify] (after DNS propagates):"  # => co-10 proof
echo "  curl -sI https://${DOMAIN}/         # => expect HTTP/2 200"  # => the app over TLS
echo "  curl -sI https://${DOMAIN}/ | grep -i strict-transport  # => PaaS adds HSTS by default"