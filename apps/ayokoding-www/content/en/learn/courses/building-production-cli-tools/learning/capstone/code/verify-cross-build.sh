#!/usr/bin/env bash
set -euo pipefail
mkdir -p dist
GOOS=linux GOARCH=amd64 go build -o dist/ship-linux-amd64 main.go
GOOS=darwin GOARCH=arm64 go build -o dist/ship-darwin-arm64 main.go
test -s dist/ship-linux-amd64
test -s dist/ship-darwin-arm64
rm -rf dist
