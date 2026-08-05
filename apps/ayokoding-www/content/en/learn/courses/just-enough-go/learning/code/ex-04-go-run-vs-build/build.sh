#!/usr/bin/env sh
set -eu
go run main.go
go build -o hello main.go
test -x ./hello
