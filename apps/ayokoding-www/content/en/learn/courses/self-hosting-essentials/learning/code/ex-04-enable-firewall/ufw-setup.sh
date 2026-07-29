#!/usr/bin/env bash
# Example 4: Enable the Firewall with ufw. (co-05)
#
# ufw (Uncomplicated Firewall) is a default-DENY front end to netfilter: you
# explicitly open only the ports a service needs (SSH, HTTP, HTTPS) and every
# other port stays unreachable from the internet. Run on the box.

set -euo pipefail  # => fail fast; a firewall script is the worst place to ignore errors

# --- 1. Set the default policy: deny incoming, allow outgoing -----------------
# co-05's core stance: nothing reaches the box unless you said so.
ufw default deny incoming  # => block every port we did not explicitly open below
ufw default allow outgoing  # => the box itself can still reach out (package updates, DNS, ACME)

# --- 2. Open ONLY the ports this course's stack needs -------------------------
ufw allow 22/tcp comment 'ssh'  # => co-05: SSH (so we do not lock ourselves out -- open this FIRST)
ufw allow 80/tcp comment 'http'  # => co-09/co-10: HTTP, for the ACME challenge and the ->HTTPS redirect
ufw allow 443/tcp comment 'https'  # => co-09/co-10: HTTPS, where the reverse proxy terminates TLS

# --- 3. Turn the firewall ON --------------------------------------------------
# '-f' skips the "this may disrupt existing ssh connections" prompt (we opened 22).
ufw --force enable  # => policies are now LIVE; closed ports become unreachable

# --- 4. Verify: the open set is exactly {22, 80, 443} -------------------------
ufw status numbered  # => co-05's acceptance check: list every rule with a number
echo "[verify] a port NOT in {22,80,443} should now be unreachable, e.g.:"
echo "         nc -z <box-ip> 8080   # => expect 'connection refused' or timeout"  # => closed port blocked