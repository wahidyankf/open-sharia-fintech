#!/usr/bin/env bash
# Example 2: SSH Key-Only Login. (co-03)
#
# Key-based SSH replaces a brute-forceable password with an unguessable key
# pair: the PRIVATE key stays on your laptop; the PUBLIC key goes on the box.
# Once the key works, password login is DISABLED -- closing the single most
# common remote-compromise vector (co-03).

set -euo pipefail  # => fail fast on the first error or unset variable

# --- 1. Generate the key pair (run on YOUR laptop, NOT the box) ----------------
KEY_PATH="${HOME}/.ssh/myapp_box_ed25519"  # => ed25519: short, fast, modern; prefer over RSA
# ssh-keygen creates TWO files: ${KEY_PATH} (private) and ${KEY_PATH}.pub (public)
ssh-keygen -t ed25519 -f "${KEY_PATH}" -N "" -C "myapp-box $(date +%F)"  # => -N "" = no passphrase here (set one in real use)

# --- 2. Copy the PUBLIC key to the box ----------------------------------------
# ssh-copy-id appends your public key to ~/.ssh/authorized_keys on the box.
BOX_IP="$(cat .box-ip)"  # => the IP Example 1 recorded, so this step needs no new input
ssh-copy-id -i "${KEY_PATH}.pub" "root@${BOX_IP}"  # => -i names the PUBLIC key to install

# --- 3. Prove the key works WITHOUT a password --------------------------------
# A successful key login exits 0 with no password prompt; this is co-03's proof.
ssh -i "${KEY_PATH}" -o BatchMode=yes "root@${BOX_IP}" 'echo key-login-ok'  # => BatchMode refuses any interactive password

# --- 4. Disable password login (run ON the box, over the key session) ---------
# /etc/ssh/sshd_config is the gatekeeper; flipping two directives closes it.
ssh -i "${KEY_PATH}" "root@${BOX_IP}" 'sed -i \
  -e "s/^#\?PasswordAuthentication.*/PasswordAuthentication no/" \  # => passwords refused
  -e "s/^#\?PubkeyAuthentication.*/PubkeyAuthentication yes/" \     # => keys accepted
  /etc/ssh/sshd_config && systemctl reload ssh'  # => reload applies the new policy with no restart

echo "[verify] password login should now FAIL -- attempt it and confirm the refusal:"
echo "         ssh root@${BOX_IP}   # => expect: Permission denied (publickey)"  # => co-03's acceptance check