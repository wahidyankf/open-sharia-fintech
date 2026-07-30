#!/usr/bin/env bash
# Example 25: Install a Git-Push PaaS. (co-16)
#
# A PaaS builds and deploys your app from a `git push` -- the contrast case
# that shows what the manual substrate (Examples 1-24) was automating. This
# installs a self-hosted git-push PaaS (Dokku is the canonical one) ON the same
# box, so you can feel the trade-off (co-20) without a second provider. Run as
# root on the box. (A managed PaaS -- Fly, Railway, Render -- skips this step
# entirely; the deploy shape in Example 26 is identical either way.)

set -euo pipefail  # => fail fast on a failed download or a failed service start

# --- 1. Install Dokku from its signed install script --------------------------
# Dokku is a single-host PaaS: each `git push` builds a container and runs it
# under its own process supervisor, with a proxy + TLS layer in front.
wget -qO- https://dokku.com/install.sh | DOKKU_TAG=v0.34.9 bash  # => pinned tag; re-verify CVE-clean before real use
# ^ the install script adds the dokku apt repo, installs dokku, and enables its service.

# --- 2. Confirm the PaaS is up and answering ----------------------------------
dokku version  # => co-16 proof: the platform is installed and its CLI responds
systemctl is-active dokku  # => the supervisor managing deploys is running

# --- 3. Create the app the next example will deploy into ----------------------
dokku apps:create myapp  # => a named slot a `git push` will fill (Example 26)

echo "[verify] PaaS up; app 'myapp' created"  # => co-16
echo "[next]  Example 26 deploys the app with a single 'git push dokku main:master'"  # => the co-16 payoff