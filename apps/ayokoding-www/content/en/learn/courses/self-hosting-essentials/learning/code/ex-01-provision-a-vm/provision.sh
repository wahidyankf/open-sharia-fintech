#!/usr/bin/env bash
# Example 1: Provision a Linux VM and Record Its IP. (co-02)
#
# Provisioning is the first reproducible step of any self-host: create a Linux
# VM, wait for it to answer, and RECORD its public IP so every later step (SSH,
# DNS, TLS) can refer to one stable value rather than a dashboard you forget.
# Provider-agnostic: the shape ("create a VM, read back its IP") is universal;
# swap the one provisioner command for your own provider's CLI.

set -euo pipefail  # => fail fast: -e exit on error, -u error on unset var, -o pipefail

# --- 1. Create the VM (provider-agnostic shape) --------------------------------
# Replace the line below with YOUR provider's create command, e.g.:
#   gcloud compute instances create myapp-box --image-family=ubuntu-2404-lts ...
#   aws ec2 run-instances --image-id ami-... ...
#   multipass launch --name myapp-box 24.04        # a free LOCAL VM, no cloud
# Here we just NAME the box so the script is runnable and self-documenting.
BOX_NAME="myapp-box"  # => co-02: a stable name for the instance across all later steps
echo "[provision] creating Linux VM: ${BOX_NAME}"  # => the one line a real provider echoes back

# --- 2. Record the public IP ---------------------------------------------------
# A freshly created VM hands back a public IP; capture it ONCE into a variable
# so SSH, DNS (Example 13), and TLS (Example 14) all reference the same value.
BOX_IP="192.0.2.10"  # => co-02: placeholder TEST-NET-3 IP; a real run writes the real IP here
echo "${BOX_IP}" > .box-ip  # => co-02: persist it to disk so later scripts read, not re-derive

# --- 3. Verify reachability before moving on -----------------------------------
# co-02's acceptance check: can we even talk to the box? A failed ping here
# means SSH (Example 2) will fail too -- fail at the cheapest step, not later.
echo "[verify] probing ${BOX_IP}:22 (SSH) ..."  # => the port we open in Example 4's firewall
nc -z -w 5 "${BOX_IP}" 22 && echo "[verify] SSH port reachable" || echo "[verify] port not open yet (may be booting)"