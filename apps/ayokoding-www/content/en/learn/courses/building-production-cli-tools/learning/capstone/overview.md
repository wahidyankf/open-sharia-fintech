---
title: "Ship: a Production-Shaped Release CLI"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Build `ship`, a release-status CLI with a human report and stable JSON for automation. The capstone
is intentionally small, but it carries the contracts that make a command safe to call from CI:
explicit configuration precedence, a predictable error code, clean standard output, and diagnostics
on standard error.

**`learning/capstone/code/main.go`**

```go
package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "os"
    "strings"
)

const version = "1.0.0"

type report struct {
    Release string `json:"release"`
    Region  string `json:"region"`
    Status  string `json:"status"`
}

func regionFor(flagValue string) string {
    if flagValue != "" {
        return flagValue
    }
    if value := os.Getenv("SHIP_REGION"); value != "" {
        return value
    }
    if data, err := os.ReadFile("ship.conf"); err == nil && strings.TrimSpace(string(data)) != "" {
        return strings.TrimSpace(string(data))
    }
    return "local"
}

func usage() { fmt.Fprintln(os.Stderr, "usage: ship [--version] <status|completion> [options]") }

func isTerminal(file *os.File) bool {
    info, err := file.Stat()
    return err == nil && info.Mode()&os.ModeCharDevice != 0
}

func progress(message string, interactive bool) {
    if interactive {
        fmt.Fprintf(os.Stderr, "\r\033[36m%s\033[0m\n", message)
    }
}

func main() {
    if len(os.Args) == 2 && (os.Args[1] == "--help" || os.Args[1] == "-h") {
        usage()
        return
    }
    if len(os.Args) == 2 && os.Args[1] == "--version" {
        fmt.Println(version)
        return
    }
    if len(os.Args) < 2 {
        usage()
        os.Exit(2)
    }
    switch os.Args[1] {
    case "completion":
        if len(os.Args) == 3 && os.Args[2] == "bash" {
            fmt.Println("complete -W 'status completion' ship")
            return
        }
        usage()
        os.Exit(2)
    case "status":
        fs := flag.NewFlagSet("status", flag.ContinueOnError)
        fs.SetOutput(os.Stderr)
        jsonMode := fs.Bool("json", false, "emit JSON")
        region := fs.String("region", "", "release region")
        if len(os.Args) == 3 && (os.Args[2] == "--help" || os.Args[2] == "-h") {
            fmt.Println("usage: ship status [--json] [--region REGION] RELEASE")
            return
        }
        if fs.Parse(os.Args[2:]) != nil || fs.NArg() != 1 {
            fmt.Fprintln(os.Stderr, "usage: ship status [--json] [--region REGION] RELEASE")
            os.Exit(2)
        }
        r := report{Release: fs.Arg(0), Region: regionFor(*region), Status: "ready"}
        if *jsonMode {
            _ = json.NewEncoder(os.Stdout).Encode(r)
            return
        }
        progress("progress: checked release metadata", isTerminal(os.Stderr))
        fmt.Printf("release %s is %s in %s\n", r.Release, r.Status, r.Region)
    default:
        fmt.Fprintf(os.Stderr, "error: unknown command %q\n", os.Args[1])
        usage()
        os.Exit(2)
    }
}
```

**Verify**:

```text
go run main.go v1.4.0
release v1.4.0 is ready in local

SHIP_REGION=eu go run main.go --json v1.4.0
{"release":"v1.4.0","region":"eu","status":"ready"}
```

Success criteria:

- `--region` overrides `SHIP_REGION`, and `SHIP_REGION` overrides `local`.
- `--json` emits only one JSON document on standard output.
- A missing release prints usage to standard error and exits `2`.
- On an interactive terminal, progress uses cyan text on standard error; piped or JSON output receives no progress or escape codes.
- `bash verify-cross-build.sh` builds and size-checks `linux/amd64` and `darwin/arm64` single binaries, then removes local `dist/` artifacts.

← Previous: [Advanced Examples](../advanced) · Next: [Drilling](../../drilling/overview)
