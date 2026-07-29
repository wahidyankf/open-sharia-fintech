#!/usr/bin/env bash
# Example 3: Create a Non-Root Sudo User. (co-04)
#
# Running everything as root is the other half of "compromise waiting to
# happen": a process that runs as root IS the whole box. The safe baseline is
# a dedicated, unprivileged user with sudo for the few actions that need it.
# Run this OVER the key session established in Example 2.

set -euo pipefail  # => fail fast; this script edits accounts, so safety matters

DEPLOY_USER="deploy"  # => a single-purpose account named for what it does

# --- 1. Create the user with a home directory ---------------------------------
# -m creates /home/${DEPLOY_USER}; -s sets its login shell to bash.
useradd -m -s /bin/bash "${DEPLOY_USER}"  # => co-04: an unprivileged account, no root powers by default

# --- 2. Grant narrow sudo (the ONE privilege escalation path) -----------------
# Adding to the 'sudo' group lets it run privileged commands via sudo + password.
# (For tighter control, replace this with a single NOPASSWD line in sudoers.d.)
usermod -aG sudo "${DEPLOY_USER}"  # => -aG appends to the group without leaving others

# --- 3. Let YOUR key log in AS this user (not just root) ----------------------
# Reuse the public key from Example 2 so the same laptop reaches the new user.
PUBKEY="$(cat "${HOME}/.ssh/myapp_box_ed25519.pub")"  # => the public half of the Example 2 key
install -d -m 700 -o "${DEPLOY_USER}" -g "${DEPLOY_USER}" "/home/${DEPLOY_USER}/.ssh"  # => .ssh must be 0700
echo "${PUBKEY}" > "/home/${DEPLOY_USER}/.ssh/authorized_keys"  # => same key, now accepted for deploy@
chmod 600 "/home/${DEPLOY_USER}/.ssh/authorized_keys"  # => authorized_keys must be 0600 or sshd ignores it
chown "${DEPLOY_USER}:${DEPLOY_USER}" "/home/${DEPLOY_USER}/.ssh/authorized_keys"  # => owned by the new user

BOX_IP="$(cat .box-ip)"  # => Example 1's recorded IP
echo "[verify] SSH in as the non-root user and confirm sudo works:"
echo "         ssh -i ~/.ssh/myapp_box_ed25519 ${DEPLOY_USER}@${BOX_IP} 'sudo -n true || echo sudo-needs-password'"  # => co-04