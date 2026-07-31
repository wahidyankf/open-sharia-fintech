#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/../ex-13-resource"
terraform init
terraform plan -destroy
terraform destroy
