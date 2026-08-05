---
title: "Intermediate Examples"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–54 make configuration resolution, TTY behavior, machine output, completion, core
boundaries, signal handling, and CLI testing observable.

### Example 27: Load a Config File

_ex-27 · exercises co-09_

Load a Config File isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-27-config-file-load/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
    "strings"
)

func main() {
    data, err := os.ReadFile("ship.conf")
    if err != nil {
        fmt.Println("region=local")
        return
    }
    fmt.Println(strings.TrimSpace(string(data)))
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 28: Prefer a Flag over Environment

_ex-28 · exercises co-07, co-08_

Prefer a Flag over Environment isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-28-flag-over-env/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let args: Vec<String> = std::env::args().collect(); let region = args.windows(2).find(|p| p[0] == "--region").map(|p| p[1].clone()).or_else(|| std::env::var("SHIP_REGION").ok()).unwrap_or_else(|| "local".into()); println!("region={region}") }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 29: Prefer Environment over Config

_ex-29 · exercises co-07, co-09_

Prefer Environment over Config isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-29-env-over-config/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
    "strings"
)

func main() {
    region := strings.TrimSpace(string(must(os.ReadFile("ship.conf"))))
    if env := os.Getenv("SHIP_REGION"); env != "" {
        region = env
    }
    fmt.Println(region)
}
func must(b []byte, err error) []byte {
    if err != nil {
        return []byte("local")
    }
    return b
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 30: Prefer Config over a Default

_ex-30 · exercises co-07, co-10_

Prefer Config over a Default isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-30-config-over-default/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let region = std::fs::read_to_string("ship.conf").ok().map(|s| s.trim().to_owned()).filter(|s| !s.is_empty()).unwrap_or_else(|| "local".into()); println!("region={region}") }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 31: Resolve Full Precedence

_ex-31 · exercises co-07_

Resolve Full Precedence isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-31-full-precedence/main.go`; run it, vary its input, and observe the contract before combining it with another
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
    chosen := strings.TrimSpace(string(readConfig()))
    if env := os.Getenv("SHIP_REGION"); env != "" {
        chosen = env
    }
    if *region != "" {
        chosen = *region
    }
    if chosen == "" {
        chosen = "local"
    }
    fmt.Println(chosen)
}
func readConfig() []byte { b, _ := os.ReadFile("ship.conf"); return b }
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 32: Build a Nested Subcommand Tree

_ex-32 · exercises co-02_

Build a Nested Subcommand Tree isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-32-subcommand-tree/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let a: Vec<String> = std::env::args().skip(1).collect(); match a.as_slice() { [group, command] if group == "config" && command == "get" => println!("read config"), [group, command] if group == "config" && command == "set" => println!("write config"), _ => eprintln!("usage: ship config <get|set>") } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 33: Scope Flags to a Subcommand

_ex-33 · exercises co-02, co-03_

Scope Flags to a Subcommand isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-33-subcommand-flags/main.go`; run it, vary its input, and observe the contract before combining it with another
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
    if len(os.Args) < 2 || os.Args[1] != "publish" {
        fmt.Fprintln(os.Stderr, "usage: ship publish --dry-run")
        os.Exit(2)
    }
    fs := flag.NewFlagSet("publish", flag.ExitOnError)
    dry := fs.Bool("dry-run", false, "do not publish")
    fs.Parse(os.Args[2:])
    fmt.Printf("dry-run=%t\n", *dry)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 34: Carry a Global Flag

_ex-34 · exercises co-02, co-03_

Carry a Global Flag isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-34-persistent-flags/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let a: Vec<String> = std::env::args().collect(); let verbose = a.iter().any(|x| x == "--verbose"); let command = a.last().map(String::as_str).unwrap_or("help"); if verbose { eprintln!("debug: dispatching {command}") }; println!("{command}") }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 35: Detect a Terminal

_ex-35 · exercises co-15_

Detect a Terminal isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-35-tty-detect/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    info, err := os.Stdout.Stat()
    if err != nil {
        panic(err)
    }
    fmt.Printf("interactive=%t\n", info.Mode()&os.ModeCharDevice != 0)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 36: Color Only Interactive Output

_ex-36 · exercises co-16, co-15_

Color Only Interactive Output isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-36-color-on-tty/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
use std::io::IsTerminal;
fn main() { if std::io::stdout().is_terminal() { println!("\x1b[32mready\x1b[0m") } else { println!("ready") } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 37: Override Color Policy

_ex-37 · exercises co-16_

Override Color Policy isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-37-color-force-flag/main.go`; run it, vary its input, and observe the contract before combining it with another
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
    color := flag.String("color", "auto", "auto, always, or never")
    flag.Parse()
    tty, _ := os.Stdout.Stat()
    if *color != "auto" && *color != "always" && *color != "never" {
        fmt.Fprintln(os.Stderr, "--color must be auto, always, or never")
        os.Exit(2)
    }
    if *color == "always" || (*color == "auto" && tty.Mode()&os.ModeCharDevice != 0) {
        fmt.Println("\033[32mready\033[0m")
    } else {
        fmt.Println("ready")
    }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 38: Hide Progress in a Pipe

_ex-38 · exercises co-17, co-15_

Hide Progress in a Pipe isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-38-progress-on-tty/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
use std::io::{self, IsTerminal, Write};
fn main() { if io::stderr().is_terminal() { eprint!("\rUploading 100%"); io::stderr().flush().unwrap(); } println!("uploaded") }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 39: Emit Machine JSON

_ex-39 · exercises co-21_

Emit Machine JSON isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-39-machine-json/main.go`; run it, vary its input, and observe the contract before combining it with another
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
    json.NewEncoder(os.Stdout).Encode(map[string]string{"status": "ok", "example": "39"})
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 40: Keep Piped Output Clean

_ex-40 · exercises co-21, co-16_

Keep Piped Output Clean isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-40-pipe-clean-output/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { eprintln!("info: checking release"); println!("{{\"status\":\"ok\"}}"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 41: Suppress Non-Errors

_ex-41 · exercises co-19_

Suppress Non-Errors isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-41-quiet-mode/main.go`; run it, vary its input, and observe the contract before combining it with another
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
    quiet := flag.Bool("quiet", false, "suppress success text")
    flag.Parse()
    if !*quiet {
        fmt.Println("release checked")
    }
    fmt.Fprintln(os.Stderr, "debug: check complete")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 42: Send Verbose Detail to Stderr

_ex-42 · exercises co-19, co-13_

Send Verbose Detail to Stderr isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-42-verbose-mode/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { let verbose = std::env::args().any(|a| a == "--verbose"); if verbose { eprintln!("debug: reading release manifest") }; println!("ready") }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 43: Prompt Only on a Terminal

_ex-43 · exercises co-18, co-15_

Prompt Only on a Terminal isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-43-prompt-on-tty/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "bufio"
    "fmt"
    "os"
)

func main() {
    info, _ := os.Stdin.Stat()
    if info.Mode()&os.ModeCharDevice == 0 {
        fmt.Println("refusing interactive prompt on piped input")
        return
    }
    fmt.Print("Publish? [y/N] ")
    answer, _ := bufio.NewReader(os.Stdin).ReadString('\n')
    fmt.Printf("answer=%q\n", answer)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 44: Generate Go Completion

_ex-44 · exercises co-20, co-25_

Generate Go Completion isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-44-go-completion/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    if len(os.Args) == 3 && os.Args[1] == "completion" && os.Args[2] == "bash" {
        fmt.Println("complete -W 'check publish version' ship")
        return
    }
    fmt.Fprintln(os.Stderr, "usage: ship completion bash")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 45: Generate Rust Completion

_ex-45 · exercises co-20, co-26_

Generate Rust Completion isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-45-rust-completion/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { match std::env::args().nth(1).as_deref() { Some("bash") => println!("complete -W 'check publish' ship"), Some("zsh") => println!("compadd check publish"), _ => eprintln!("usage: ship completion <bash|zsh>") } }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 46: Map Failure Classes to Codes

_ex-46 · exercises co-11_

Map Failure Classes to Codes isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-46-exit-code-map/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func main() {
    switch os.Args[len(os.Args)-1] {
    case "ok":
        fmt.Println("ok")
    case "invalid":
        fmt.Fprintln(os.Stderr, "invalid input")
        os.Exit(2)
    default:
        fmt.Fprintln(os.Stderr, "operation failed")
        os.Exit(1)
    }
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 47: Separate Data While Piped

_ex-47 · exercises co-12, co-13_

Separate Data While Piped isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-47-stderr-vs-stdout-pipe/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn main() { eprintln!("info: fetching release"); println!("v1.2.0"); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 48: Extract a Core Function

_ex-48 · exercises co-27_

Extract a Core Function isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-48-core-function/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import "fmt"

// render is the policy-free core a unit test can call without a terminal.
func render(name string) string { return "hello " + name }

func main() {
    // => Argument parsing and process concerns stay outside the core.
    fmt.Println(render("ship"))
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 49: Let the CLI Call the Core

_ex-49 · exercises co-27, co-02_

Let the CLI Call the Core isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-49-cli-calls-core/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn normalize(name: &str) -> String { name.trim().to_ascii_lowercase() }
fn main() { let raw = std::env::args().nth(1).unwrap_or_else(|| " Ship ".into()); println!("{}", normalize(&raw)); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 50: Handle SIGINT Cleanly

_ex-50 · exercises co-28_

Handle SIGINT Cleanly isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-50-sigint-handling/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
    "os/signal"
    "syscall"
)

func main() {
    stop := make(chan os.Signal, 1)
    signal.Notify(stop, os.Interrupt, syscall.SIGTERM)
    fmt.Println("working; press Ctrl-C")
    <-stop
    fmt.Fprintln(os.Stderr, "cleaning up")
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 51: Test Go CLI Output

_ex-51 · exercises co-29, co-25_

Test Go CLI Output isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-51-go-test-cli/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import (
    "fmt"
    "os"
)

func run(args []string) (string, int) {
    if len(args) != 1 {
        return "usage: ship RELEASE", 2
    }
    return "published " + args[0], 0
}

func main() {
    output, code := run(os.Args[1:])
    if len(os.Args) == 1 {
        output, code = run([]string{"v1"})
    }
    if output != "published v1" || code != 0 {
        panic("CLI contract changed")
    }
    fmt.Println(output)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 52: Test Rust CLI Output

_ex-52 · exercises co-29, co-26_

Test Rust CLI Output isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-52-rust-test-cli/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn render(name: &str) -> String { format!("ok: {name}") }
fn main() { assert_eq!(render("ship"), "ok: ship"); println!("{}", render("ship")); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 53: Compare Golden Output

_ex-53 · exercises co-29_

Compare Golden Output isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-53-golden-output-test/main.go`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```go
package main

import "fmt"

func render(name string) string { return "release=" + name + "\nstatus=ready\n" }

func main() {
    const golden = "release=v1\nstatus=ready\n"
    got := render("v1")
    if got != golden {
        panic("golden output changed")
    }
    fmt.Print(got)
}
```

**Run**: `go run main.go` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.

### Example 54: Snapshot Help Text

_ex-54 · exercises co-29, co-05_

Snapshot Help Text isolates one CLI contract in a small source file. The block is rendered verbatim from
`learning/code/ex-54-help-snapshot-test/main.rs`; run it, vary its input, and observe the contract before combining it with another
command concern.

**Source**

```rust
fn help() -> &'static str { "usage: ship [--json] RELEASE\n" }
fn main() { assert_eq!(help(), "usage: ship [--json] RELEASE\n"); print!("{}", help()); }
```

**Run**: `rustc main.rs && ./main` from this example directory.

**Expected observation**: the example makes its parsing, stream, exit-status, interaction, or
release decision visible to both a terminal reader and a calling script.

**Key takeaway**: production CLI behavior is explicit, conventional, and testable.
