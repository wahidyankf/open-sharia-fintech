#!/usr/bin/env sh
set -eu
go build -o hello main.go
./hello
