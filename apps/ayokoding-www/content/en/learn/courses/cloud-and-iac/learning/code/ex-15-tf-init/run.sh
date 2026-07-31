#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/../ex-12-provider"
terraform init
terraform providers
