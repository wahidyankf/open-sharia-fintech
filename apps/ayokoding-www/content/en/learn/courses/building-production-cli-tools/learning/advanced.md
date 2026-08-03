---
title: "Advanced Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

Examples 55–78 finish the release story: cross-target builds, packaging, installation, script
integration, and a complete production CLI preview.

### Example 55: Cross-Compile Go

_ex-55 · exercises co-23, co-22_

Cross-Compile Go isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-55-cross-compile-go/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import "fmt"

func main() { fmt.Println("GOOS=linux GOARCH=arm64 go build -o dist/ship-linux-arm64 main.go") }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 56: Cross-Compile Rust

_ex-56 · exercises co-23, co-26_

Cross-Compile Rust isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-56-cross-compile-rust/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { println!("rustup target add x86_64-unknown-linux-musl\ncargo build --release --target x86_64-unknown-linux-musl"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 57: Prefer a Single Static Binary

_ex-57 · exercises co-22_

Prefer a Single Static Binary isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-57-static-binary/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import "fmt"

func main() { fmt.Println("CGO_ENABLED=0 go build -trimpath -o ship main.go") }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 58: Build Two Platform Artifacts

_ex-58 · exercises co-23_

Build Two Platform Artifacts isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-58-two-platform-build/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { println!("cargo build --release --target x86_64-unknown-linux-musl\ncargo build --release --target aarch64-apple-darwin"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 59: Install on PATH

_ex-59 · exercises co-24_

Install on PATH isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-59-install-path/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() { fmt.Printf("install destination: %s/.local/bin\n", os.Getenv("HOME")) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 60: Package a Release Archive

_ex-60 · exercises co-24, co-20_

Package a Release Archive isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-60-package-release/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { println!("tar -C dist -czf ship_1.2.0_linux_amd64.tar.gz ship"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 61: Resolve Precedence in a Subcommand

_ex-61 · exercises co-07, co-02_

Resolve Precedence in a Subcommand isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-61-config-precedence-full/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "flag"
    "fmt"
    "os"
    "strings"
)

func main() {
    region := flag.String("region", "", "region")
    flag.Parse()
    value := strings.TrimSpace(string(read()))
    if env := os.Getenv("SHIP_REGION"); env != "" {
        value = env
    }
    if *region != "" {
        value = *region
    }
    if value == "" {
        value = "local"
    }
    fmt.Println(value)
}
func read() []byte { b, _ := os.ReadFile("ship.conf"); return b }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 62: Combine TTY Color and Progress

_ex-62 · exercises co-16, co-17, co-15_

Combine TTY Color and Progress isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-62-tty-color-progress/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
use std::io::IsTerminal;
fn main() { let tty = std::io::stderr().is_terminal(); if tty { eprint!("\r\x1b[36muploading\x1b[0m") }; println!("{{\"status\":\"done\"}}"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 63: Offer JSON and Human Modes

_ex-63 · exercises co-21, co-12_

Offer JSON and Human Modes isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-63-json-and-human/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "encoding/json"
    "os"
)

func main() {
    // => JSON is written only to stdout so jq and other callers can parse it.
    // => A stable key is a public script contract.
    json.NewEncoder(os.Stdout).Encode(map[string]string{"status": "ok", "example": "63"})
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 64: Name the Fix in an Error

_ex-64 · exercises co-14, co-13_

Name the Fix in an Error isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-64-actionable-errors/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let path = ".ship/token"; if std::fs::metadata(path).is_err() { eprintln!("error: {path} is missing; run `ship login`"); std::process::exit(1) } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 65: Consume an Exit Code

_ex-65 · exercises co-11_

Consume an Exit Code isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-65-exit-code-discipline/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    if len(os.Args) != 2 {
        fmt.Fprintln(os.Stderr, "usage: consumer <0|1|2>")
        os.Exit(2)
    }
    switch os.Args[1] {
    case "0":
        fmt.Println("continue pipeline")
    case "1":
        fmt.Println("retry operation")
    case "2":
        fmt.Println("fix command usage")
    default:
        os.Exit(2)
    }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 66: Generate Bash and Zsh Completion

_ex-66 · exercises co-20_

Generate Bash and Zsh Completion isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-66-completion-both-shells/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { match std::env::args().nth(1).as_deref() { Some("bash") => println!("complete -W 'check publish' ship"), Some("zsh") => println!("compadd check publish"), _ => eprintln!("usage: ship completion <bash|zsh>") } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 67: Clean Up after SIGINT

_ex-67 · exercises co-28_

Clean Up after SIGINT isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-67-signal-cleanup/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
    "os/signal"
)

func main() {
    done := make(chan os.Signal, 1)
    signal.Notify(done, os.Interrupt)
    fmt.Println("temporary file created")
    <-done
    fmt.Println("temporary file removed")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 68: Resolve Verbose and Quiet

_ex-68 · exercises co-19_

Resolve Verbose and Quiet isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-68-verbose-quiet-combo/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let a: Vec<String> = std::env::args().collect(); let quiet = a.contains(&"--quiet".into()); let verbose = a.contains(&"--verbose".into()); if verbose && !quiet { eprintln!("debug: resolving configuration") }; if !quiet { println!("done") } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 69: Accept POSIX and GNU Forms

_ex-69 · exercises co-30, co-01_

Accept POSIX and GNU Forms isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-69-posix-gnu-parity/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    for _, a := range os.Args[1:] {
        if a == "-v" || a == "--verbose" {
            fmt.Println("verbose=true")
            return
        }
    }
    fmt.Println("verbose=false")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 70: Match Go and Rust Behavior

_ex-70 · exercises co-25, co-26_

Match Go and Rust Behavior isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-70-go-vs-rust-same-cli/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

**`learning/code/ex-70-go-vs-rust-same-cli/main.go`**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    region := "local"
    if len(os.Args) > 1 {
        region = os.Args[1]
    }
    fmt.Printf("{\"region\":\"%s\",\"status\":\"ready\"}\n", region)
}
```

**Rust source**

```rust
fn main() { let region = std::env::args().nth(1).unwrap_or_else(|| "local".into()); println!("{{\"region\":\"{region}\",\"status\":\"ready\"}}"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 71: Test Core and CLI Separately

_ex-71 · exercises co-27, co-29_

Test Core and CLI Separately isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-71-core-cli-test-split/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import "fmt"

func normalize(region string) string {
    if region == "" {
        return "local"
    }
    return region
}

func main() {
    if normalize("") != "local" {
        panic("core test failed")
    }
    fmt.Println("status " + normalize("eu"))
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 72: Require a Namespaced Prefix

_ex-72 · exercises co-08, co-07_

Require a Namespaced Prefix isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-72-env-prefix/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let endpoint = std::env::var("SHIP_ENDPOINT").unwrap_or_else(|_| "https://api.example.test".into()); println!("endpoint={endpoint}") }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 73: Pipe JSON into jq

_ex-73 · exercises co-21, co-12_

Pipe JSON into jq isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-73-machine-pipe-integration/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "encoding/json"
    "os"
)

func main() {
    // => JSON is written only to stdout so jq and other callers can parse it.
    // => A stable key is a public script contract.
    json.NewEncoder(os.Stdout).Encode(map[string]string{"status": "ok", "example": "73"})
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 74: Install Shell Completion

_ex-74 · exercises co-20, co-24_

Install Shell Completion isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-74-completion-install/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { println!("ship completion zsh > ~/.zfunc/_ship\nfpath=(~/.zfunc $fpath)"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 75: Pair Stderr with a Failure Code

_ex-75 · exercises co-13, co-11_

Pair Stderr with a Failure Code isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-75-error-to-stderr-code/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() { fmt.Fprintln(os.Stderr, "error: release not found"); os.Exit(1) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 76: Combine Subcommands and Precedence

_ex-76 · exercises co-02, co-07, co-05_

Combine Subcommands and Precedence isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-76-subcommand-plus-precedence/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let a: Vec<String> = std::env::args().collect(); if a.get(1).map(String::as_str) != Some("status") || a.iter().any(|x| x == "--help") { println!("usage: ship status [--region REGION]"); return }; let flag_region = a.windows(2).find(|p| p[0] == "--region").map(|p| p[1].clone()); let config = std::fs::read_to_string("ship.conf").ok().map(|s| s.trim().to_owned()).filter(|s| !s.is_empty()); let region = flag_region.or_else(|| std::env::var("SHIP_REGION").ok()).or(config).unwrap_or_else(|| "local".into()); println!("status region={region}") }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 77: Integrate TTY-Aware Output

_ex-77 · exercises co-15, co-16, co-17, co-21_

Integrate TTY-Aware Output isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-77-integration-tty-slice/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "os"
)

func main() {
    machine := flag.Bool("json", false, "machine output")
    flag.Parse()
    if *machine {
        _ = json.NewEncoder(os.Stdout).Encode(map[string]string{"status": "ready"})
        return
    }
    fmt.Println("release ready")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 78: Preview the Production CLI Capstone

_ex-78 · exercises co-02, co-07, co-11, co-13, co-15, co-16, co-06, co-20, co-23_

Preview the Production CLI Capstone isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-78-capstone-production-cli/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "encoding/json"
    "flag"
    "fmt"
    "os"
)

type report struct {
    Release string `json:"release"`
    Region  string `json:"region"`
    Status  string `json:"status"`
}

func main() {
    jsonOutput := flag.Bool("json", false, "emit JSON")
    region := flag.String("region", "", "release region")
    flag.Parse()
    chosenRegion := *region
    if chosenRegion == "" {
        chosenRegion = os.Getenv("SHIP_REGION")
    }
    if chosenRegion == "" {
        chosenRegion = "local"
    }
    if flag.NArg() != 1 {
        fmt.Fprintln(os.Stderr, "usage: ship [--json] [--region REGION] RELEASE")
        os.Exit(2)
    }
    r := report{Release: flag.Arg(0), Region: chosenRegion, Status: "ready"}
    if *jsonOutput {
        _ = json.NewEncoder(os.Stdout).Encode(r)
        return
    }
    fmt.Printf("release %s is %s in %s\n", r.Release, r.Status, r.Region)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.
