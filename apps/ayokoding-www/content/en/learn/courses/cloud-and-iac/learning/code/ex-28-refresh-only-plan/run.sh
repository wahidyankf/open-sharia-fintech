#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/../ex-13-resource"
terraform plan -refresh-only
terraform apply -refresh-only
