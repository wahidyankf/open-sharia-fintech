#!/usr/bin/env bash
# kata-02 (before): a firewall setup that LOCKS YOU OUT (enables before allowing SSH).
set -euo pipefail

ufw default deny incoming   # => default-deny is correct (co-05)
ufw default allow outgoing  # => box can still reach out
# THE BUG: 'ufw --force enable' runs BEFORE the 'ufw allow 22/tcp' line below.
# The moment enable fires, the default-deny policy is LIVE and port 22 is closed,
# so your current SSH session dies and you can never get back in.
ufw --force enable          # => BUG: SSH not yet allowed -> session dropped here
ufw allow 22/tcp            # => too late -- you are already locked out
ufw allow 80/tcp
ufw allow 443/tcp
