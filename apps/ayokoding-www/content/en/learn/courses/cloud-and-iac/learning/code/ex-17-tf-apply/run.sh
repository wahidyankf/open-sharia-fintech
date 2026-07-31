#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/../ex-13-resource"
terraform init
terraform apply
aws --endpoint-url=http://localhost:4566 s3 ls
