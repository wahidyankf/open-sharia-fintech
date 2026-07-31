#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/../ex-13-resource"
terraform validate
terraform import aws_s3_bucket.logs cloud-iac-learning-logs
terraform plan
