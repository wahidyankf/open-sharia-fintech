#!/usr/bin/env sh
set -eu
docker run --rm --name cloud-iac-localstack -p 4566:4566 localstack/localstack:4.10
