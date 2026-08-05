---
title: "Beginner Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish parsing, conventional flags, help, versioning, output channels, defaults,
environment configuration, subcommands, and the first binary release decision.

### Example 1: Go Hello CLI

_ex-01 · exercises co-01, co-25_

Go Hello CLI isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-01-go-hello-cli/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import "fmt"

func main() { fmt.Println("hello from ship; run ship --help to discover commands") }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 2: Rust Hello CLI

_ex-02 · exercises co-01, co-26_

Rust Hello CLI isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-02-rust-hello-cli/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { println!("hello from ship; run ship --help to discover commands"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 3: Parse a Boolean Flag

_ex-03 · exercises co-03_

Parse a Boolean Flag isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-03-bool-flag/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    verbose := flag.Bool("verbose", false, "show detail")
    flag.Parse()
    fmt.Printf("verbose=%t\n", *verbose)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 4: Parse a String Flag

_ex-04 · exercises co-03_

Parse a String Flag isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-04-string-flag/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() {
    let args: Vec<String> = std::env::args().collect();
    let name = if args.len() == 3 && args[1] == "--name" { &args[2] } else { "world" };
    println!("hello, {name}");
}
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 5: Parse an Integer Flag

_ex-05 · exercises co-03_

Parse an Integer Flag isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-05-int-flag/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    retries := flag.Int("retries", 3, "retry count")
    flag.Parse()
    fmt.Printf("retries=%d\n", *retries)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 6: Read a Positional Argument

_ex-06 · exercises co-01_

Read a Positional Argument isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-06-positional-arg/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { match std::env::args().nth(1) { Some(file) => println!("checking {file}"), None => { eprintln!("usage: check FILE"); std::process::exit(2) } } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 7: Support Short and Long Flags

_ex-07 · exercises co-01, co-30_

Support Short and Long Flags isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-07-short-long-flag/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    var verbose bool
    flag.BoolVar(&verbose, "verbose", false, "show detail")
    flag.BoolVar(&verbose, "v", false, "show detail")
    flag.Parse()
    fmt.Printf("verbose=%t\n", verbose)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 8: Preserve Arguments After Double Dash

_ex-08 · exercises co-04_

Preserve Arguments After Double Dash isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-08-double-dash/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let args: Vec<String> = std::env::args().skip(1).collect(); let i = args.iter().position(|a| a == "--"); println!("child args: {}", i.map(|n| args[n + 1..].join(" ")).unwrap_or_default()) }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 9: Generate Go Help

_ex-09 · exercises co-05, co-25_

Generate Go Help isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-09-go-help/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    flag.Usage = func() { fmt.Fprintln(flag.CommandLine.Output(), "usage: ship [--dry-run] RELEASE") }
    dry := flag.Bool("dry-run", false, "print without publishing")
    flag.Parse()
    if flag.NArg() == 0 {
        flag.Usage()
        return
    }
    fmt.Printf("publish %s (dry-run=%t)\n", flag.Arg(0), *dry)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 10: Generate Rust Help

_ex-10 · exercises co-05, co-26_

Generate Rust Help isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-10-rust-help/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { if std::env::args().any(|a| a == "--help" || a == "-h") { println!("usage: ship [--dry-run] RELEASE\n\nPublish a release safely.") } else { println!("run ship --help") } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 11: Report a Version

_ex-11 · exercises co-06_

Report a Version isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-11-version-flag/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "flag"
    "fmt"
)

func main() {
    version := flag.Bool("version", false, "print version")
    flag.Parse()
    if *version {
        fmt.Println("ship 1.2.0")
        return
    }
    fmt.Println("run ship --version")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 12: Exit Zero on Success

_ex-12 · exercises co-11_

Exit Zero on Success isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-12-exit-zero/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { println!("checked: ok"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 13: Exit Non-Zero on Failure

_ex-13 · exercises co-11_

Exit Non-Zero on Failure isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-13-exit-nonzero/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() { fmt.Fprintln(os.Stderr, "error: remote is unavailable"); os.Exit(1) }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 14: Send Data to Standard Output

_ex-14 · exercises co-12_

Send Data to Standard Output isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-14-stdout-data/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { println!("v1.2.0"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 15: Send Diagnostics to Standard Error

_ex-15 · exercises co-13_

Send Diagnostics to Standard Error isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-15-stderr-error/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() { fmt.Fprintln(os.Stderr, "warning: cache is stale") }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 16: Make an Error Actionable

_ex-16 · exercises co-14_

Make an Error Actionable isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-16-error-message/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { eprintln!("error: token file is missing; run `ship login` to create one"); std::process::exit(1) }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 17: Reject an Unknown Flag

_ex-17 · exercises co-14, co-11_

Reject an Unknown Flag isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-17-unknown-flag/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "flag"
    "fmt"
    "os"
)

func main() {
    flag.Usage = func() { fmt.Fprintln(os.Stderr, "usage: ship [--dry-run]") }
    flag.Parse()
    fmt.Println("arguments accepted")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 18: Use a Sensible Default

_ex-18 · exercises co-10_

Use a Sensible Default isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-18-default-value/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let format = std::env::args().nth(1).unwrap_or_else(|| "text".into()); println!("format={format}") }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 19: Read a Namespaced Environment Variable

_ex-19 · exercises co-08_

Read a Namespaced Environment Variable isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-19-env-read/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    token := os.Getenv("SHIP_TOKEN")
    if token == "" {
        fmt.Fprintln(os.Stderr, "SHIP_TOKEN is required")
        os.Exit(2)
    }
    fmt.Printf("token supplied (%d bytes)\n", len(token))
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 20: Dispatch a Go Subcommand

_ex-20 · exercises co-02, co-25_

Dispatch a Go Subcommand isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-20-go-subcommand/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    if len(os.Args) < 2 {
        fmt.Fprintln(os.Stderr, "usage: ship <check|publish>")
        os.Exit(2)
    }
    switch os.Args[1] {
    case "check":
        fmt.Println("ok")
    case "publish":
        fmt.Println("published")
    default:
        fmt.Fprintln(os.Stderr, "unknown command; run --help")
        os.Exit(2)
    }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 21: Dispatch a Rust Subcommand

_ex-21 · exercises co-02, co-26_

Dispatch a Rust Subcommand isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-21-rust-subcommand/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let command = std::env::args().nth(1).unwrap_or_default(); match command.as_str() { "check" => println!("ok"), "publish" => println!("published"), _ => { eprintln!("usage: ship <check|publish>"); std::process::exit(2) } } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 22: Show Subcommand Help

_ex-22 · exercises co-02, co-05_

Show Subcommand Help isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-22-subcommand-help/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    if len(os.Args) != 3 || os.Args[2] != "--help" {
        fmt.Fprintln(os.Stderr, "usage: ship COMMAND --help")
        os.Exit(2)
    }
    switch os.Args[1] {
    case "check":
        fmt.Println("usage: ship check FILE")
    case "publish":
        fmt.Println("usage: ship publish RELEASE")
    default:
        fmt.Fprintln(os.Stderr, "unknown command")
        os.Exit(2)
    }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 23: Require a Flag

_ex-23 · exercises co-03, co-14_

Require a Flag isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-23-required-flag/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let args: Vec<String> = std::env::args().collect(); match args.windows(2).find(|p| p[0] == "--release").map(|p| p[1].as_str()) { Some(value) => println!("publishing {value}"), None => { eprintln!("--release is required"); std::process::exit(2) } } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 24: Count Repeated Flags

_ex-24 · exercises co-03_

Count Repeated Flags isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-24-repeated-flag/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "flag"
    "fmt"
)

type count int

func (c *count) String() string   { return fmt.Sprint(*c) }
func (c *count) Set(string) error { *c++; return nil }
func main() {
    var verbose count
    flag.Var(&verbose, "v", "increase verbosity (repeatable)")
    flag.Parse()
    fmt.Printf("verbosity=%d\n", verbose)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 25: Accept a POSIX Flag Cluster

_ex-25 · exercises co-30_

Accept a POSIX Flag Cluster isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-25-posix-cluster/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let mut flags = Vec::new(); for arg in std::env::args().skip(1) { if arg.starts_with('-') && !arg.starts_with("--") { flags.extend(arg[1..].chars()); } }; println!("flags={}", flags.into_iter().collect::<String>()); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 26: Build a Go Binary

_ex-26 · exercises co-22, co-25_

Build a Go Binary isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-26-go-build-binary/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import "fmt"

func main() { fmt.Println("build with: go build -o ship main.go") }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.
