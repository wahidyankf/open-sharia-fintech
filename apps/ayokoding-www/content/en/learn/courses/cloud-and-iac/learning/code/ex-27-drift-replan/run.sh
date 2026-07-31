#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/../ex-13-resource"
terraform plan
terraform show -no-color | grep -F 'ManagedBy'
