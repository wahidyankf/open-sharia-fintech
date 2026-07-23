---
title: "Advanced"
date: 2025-12-30T01:23:25+07:00
draft: false
weight: 10000003
description: "Examples 58-80: Production CLI patterns - module organization, Clippy, restriction lints, Markdown/XML parsing, regex caches, validation orchestration, release profiles, and a capstone example"
tags: ["rust", "cli", "tutorial", "by-example", "examples", "code-first", "advanced", "clippy", "serde", "release"]
---

## Advanced Level: Production CLI

Examples 58-80 cover the patterns that distinguish professional Rust CLI codebases from amateur ones. Module organization, type aliases, Clippy configuration, restriction lints, replacing `.unwrap()`, custom Display/FromStr, file format parsing, glob patterns, SHA-2 hashing, OnceLock regex caches, validation orchestration, release profiles, dual crate layout, complex match guards, recursive validation, date handling, common pitfalls, complex test fixtures, and a capstone synthesizing everything.

---

## Example 58: Module Organization

Production CLIs organize code into `src/commands/` for user-facing command handlers and `src/internal/` for logic not part of the public interface. Each subdirectory has a `mod.rs` that declares and re-exports submodules. `pub(crate)` exposes items within the crate without making them part of a public library API.

```
src/
├── main.rs          — entry point, Cli::parse(), dispatch
├── commands/
│   ├── mod.rs       — pub mod check; pub mod report;
│   ├── check.rs     — pub fn run(args: &CheckArgs) -> Result<()>
│   └── report.rs    — pub fn run(args: &ReportArgs) -> Result<()>
└── internal/
    ├── mod.rs       — pub(crate) mod validator; pub(crate) mod formatter;
    ├── validator.rs — pub(crate) struct Validator, pub(crate) fn run(...)
    └── formatter.rs — pub(crate) fn format_text(...), format_json(...)
```

```rust
// src/internal/validator.rs (conceptual example in one file)

// pub(crate): visible anywhere in this crate, not to external users of a library
pub(crate) struct ValidationResult {     // => pub(crate): crate-internal type
    pub(crate) violations: Vec<String>,  // => pub(crate): accessible within crate
    pub(crate) files_checked: u32,
}

impl ValidationResult {
    pub(crate) fn new() -> Self {        // => Constructor: crate-internal
        Self { violations: Vec::new(), files_checked: 0 }
    }

    pub(crate) fn add_violation(&mut self, msg: String) {
        self.violations.push(msg);
    }

    pub(crate) fn is_clean(&self) -> bool {
        self.violations.is_empty()
    }
}

// src/commands/check.rs (conceptual)
// use crate::internal::validator::ValidationResult;  // => crate:: prefix for absolute paths
//
// pub fn run(path: &str) -> anyhow::Result<()> {
//     let mut result = ValidationResult::new();
//     // ... run validators ...
//     if !result.is_clean() { ... }
//     Ok(())
// }

fn main() {
    // Inline demonstration of the module structure concept
    let mut result = ValidationResult::new();
    result.add_violation(String::from("bad-file.rs: uppercase in name"));
    result.files_checked = 10;

    println!("Clean: {}", result.is_clean());        // => Clean: false
    println!("Files: {}", result.files_checked);     // => Files: 10
    println!("Violations: {}", result.violations.len()); // => Violations: 1
}
```

**Key Takeaway**: Organize CLIs with `src/commands/` for subcommand handlers and `src/internal/` for business logic. Use `pub(crate)` to share types within the crate without exposing them in a public library API. Use `crate::` prefix for absolute paths.

**Why It Matters**: The commands/internal split is the standard Rust CLI architecture. It separates the user-facing argument handling (commands) from the core logic (internal), making each independently testable. When you add a new `commands/migrate.rs`, it imports from `internal::` without touching any other command module. This is the structure used by `cargo` itself and is what makes large CLIs maintainable.

---

## Example 59: Type Aliases

`type Result<T> = anyhow::Result<T>` defines a local alias that hides the `anyhow::` prefix. Function signatures become `fn validate(path: &str) -> Result<CheckResult>` instead of `fn validate(path: &str) -> anyhow::Result<CheckResult>`. This is the dominant pattern in production Rust codebases.

```rust
use anyhow::Context;

// Local type alias: hides anyhow:: prefix from all signatures in this module
type Result<T> = anyhow::Result<T>;     // => All function signatures use this
                                         // => Same as anyhow::Result but shorter

// Now every function in this module returns Result<T> = anyhow::Result<T>
fn read_config(path: &str) -> Result<String> {
                                         // => Without alias: anyhow::Result<String>
    std::fs::read_to_string(path)
        .with_context(|| format!("failed to read config file: {}", path))
}

fn validate_config(content: &str) -> Result<u32> {
                                         // => Return type reads cleanly
    if content.is_empty() {
        anyhow::bail!("config is empty");// => Still need anyhow:: prefix for macros
    }
    let line_count = content.lines().count() as u32;
    Ok(line_count)
}

fn run(config_path: &str) -> Result<()> {
    let content = read_config(config_path)?;
                                         // => ? works: Result<String> = anyhow::Result<String>
    let lines = validate_config(&content)?;
    println!("Config: {} lines", lines);
    Ok(())
}

fn main() {
    // Type alias in main: use anyhow::Result directly or shadow with local alias
    match run("Cargo.toml") {
        Ok(())  => println!("Done"),
        Err(e)  => {
            eprintln!("Error: {}", e);
            std::process::exit(1);
        }
    }
}
```

**Key Takeaway**: `type Result<T> = anyhow::Result<T>` at the top of a module makes all function signatures cleaner. The alias is transparent—callers use `anyhow::Result` and your `Result` interchangeably.

**Why It Matters**: Every module in a production Rust CLI that uses `anyhow` declares `type Result<T> = anyhow::Result<T>`. Reading `fn run() -> Result<()>` is immediately understood; reading `fn run() -> anyhow::Result<()>` adds cognitive noise. The `cargo` source code, `ripgrep`, and virtually every serious Rust binary use this pattern. It is the single most common alias in Rust CLI codebases.

---

## Example 60: Clippy Basics

`cargo clippy` runs the Clippy linter, which catches common mistakes and anti-patterns beyond what the compiler checks. Clippy categories include `correctness` (bugs), `style` (readability), `perf` (unnecessary allocations), and `pedantic` (strict style). `#[allow(clippy::lint_name)]` suppresses a specific lint with documentation.

```rust
// Run with: cargo clippy -- -W clippy::pedantic
// Or configure in Cargo.toml (Example 61)

fn main() {
    // Clippy catch: needless use of .clone() on a Copy type
    let x: i32 = 42;
    let _y = x.clone();                  // => Clippy warns: redundant_clone
                                          // => i32 is Copy: just write let _y = x;

    // Clippy catch: using .into_iter() on Vec is redundant (Vec is IntoIterator)
    let v = vec![1u32, 2, 3];
    for item in v.into_iter() {          // => Clippy warns: useless_conversion
        let _ = item;                    // => Just write: for item in v
    }

    // Clippy catch: using range_plus_one
    let nums: Vec<u32> = (0..5+1).collect();  // => Clippy warns: range_plus_one
                                               // => Write: (0..=5)
    println!("{:?}", nums);

    // Clippy suggestion: use .is_empty() instead of .len() == 0
    let items: Vec<u32> = vec![];
    if items.len() == 0 {               // => Clippy warns: len_zero
        println!("empty");              // => Write: if items.is_empty()
    }

    // Documented suppression: sometimes Clippy is wrong for your use case
    #[allow(clippy::cast_possible_truncation)]
    let truncated = 300u32 as u8;       // => Intentional truncation
                                         // => Comment explains WHY it's OK:
                                         // => Values are always 0-255 due to upstream validation

    println!("{}", truncated);
}
```

**Key Takeaway**: `cargo clippy` catches anti-patterns the compiler allows. Use `#[allow(clippy::lint_name)]` to suppress specific lints when intentional, always with a comment explaining why. Configure Clippy in `Cargo.toml` rather than per-file attributes (Example 61).

**Why It Matters**: Clippy catches the subtle inefficiencies and style issues that slow code review: cloning when borrowing suffices, collecting when chaining would do, using `.len() == 0` instead of `.is_empty()`. Running `cargo clippy --all-targets -- -W clippy::pedantic` in CI ensures every pull request meets the codebase's quality bar. Production Rust CLIs like `ripgrep` run Clippy in CI with pedantic warnings enabled.

---

## Example 61: Clippy Configuration in Cargo.toml

Configure Clippy in `Cargo.toml` under `[lints.clippy]` rather than scattering `#![allow(...)]` attributes across files. Set `pedantic` to warn with low priority, then selectively allow specific pedantic lints that do not fit your codebase. This gives project-wide consistency.

```toml
# Cargo.toml — Clippy configuration
[lints.rust]
unsafe_code = "forbid"                  # Treat unsafe code as a compile error everywhere

[lints.clippy]
# Enable pedantic warnings at lower priority (priority = -1)
# Lower priority means explicit lint rules below override this
pedantic = { level = "warn", priority = -1 }

# Allow specific pedantic lints that are noisy for CLI code
# Each has a documented reason
module_name_repetitions = "allow"       # ValidationValidator is fine in small CLIs
missing_errors_doc = "allow"            # We document errors in function body, not rustdoc
missing_panics_doc = "allow"            # Same as above

# Deny specific non-pedantic lints (make them errors)
unwrap_used = "warn"                    # Warn on .unwrap() — prefer ? or .expect()
expect_used = "warn"                    # Warn on .expect() in non-test code

# Allow in test code only (done via #[allow] in test modules)
# Tests commonly use .unwrap() for brevity
```

```rust
// With the above Cargo.toml, clippy runs with pedantic + selected overrides
// Run: cargo clippy --all-targets

fn main() {
    // This would trigger unwrap_used warning (from Cargo.toml config)
    // std::fs::read_to_string("file.txt").unwrap();

    // Better: use expect with context
    // std::fs::read_to_string("file.txt").expect("config file must exist");

    // Or use ? and anyhow
    println!("Clippy config example — see Cargo.toml for the actual configuration");
}
```

**Key Takeaway**: Configure Clippy in `Cargo.toml` under `[lints.clippy]` for project-wide consistency. Set `pedantic` at priority -1, then override individual lints with specific `"allow"` or `"deny"` at priority 0 (default). Avoid per-file `#![allow]` attributes.

**Why It Matters**: Scattered `#[allow(clippy::something)]` across 50 files creates a fragmented, unmaintainable lint configuration where it is impossible to see the overall policy. Centralizing in `Cargo.toml` gives a single source of truth. When a new developer joins, they see the linting policy immediately without reading every source file. Production Rust CLIs enforce this through CI: `cargo clippy --all-targets -- -D warnings` fails the build on any Clippy warning.

---

## Example 62: Restriction Lints

Restriction lints are opt-in strict rules that catch specific patterns you want to forbid in your codebase. `unwrap_used = "deny"` forbids `.unwrap()` entirely. `panic = "deny"` forbids `panic!()`. `unsafe_code = "forbid"` forbids all unsafe blocks. These elevate warnings to errors, ensuring patterns never slip through.

```toml
# Cargo.toml additions for restriction lints
[lints.clippy]
pedantic = { level = "warn", priority = -1 }

# Restriction lints: forbidden in production code
unwrap_used = "warn"                    # Use .expect("reason") or ? instead
indexing_slicing = "warn"               # Use .get(i) instead of [i] for safety
arithmetic_side_effects = "warn"        # Use checked_add, saturating_add instead of +

[lints.rust]
unsafe_code = "forbid"                  # No unsafe anywhere in the codebase
```

```rust
// How to handle each restriction lint in practice:

fn main() {
    // Instead of .unwrap(): use .expect() with a reason, or ?
    let val: Option<u32> = Some(42);

    // Forbidden: .unwrap() gives no context on failure
    // let x = val.unwrap();

    // Better: .expect() with a reason that appears in the panic message
    let x = val.expect("val is always Some — initialized above");
    println!("{}", x);

    // Even better: handle it explicitly when failure is possible
    let y = val.unwrap_or(0);           // => Default value when None
    println!("{}", y);

    // Instead of indexing ([i]): use .get() returning Option
    let items = vec![1u32, 2, 3];

    // Potentially panicking:
    // let first = items[0];

    // Safe: returns None if out of bounds
    if let Some(first) = items.get(0) {
        println!("First: {}", first);
    }

    // Instead of arithmetic that can overflow: use checked or saturating math
    let a: u32 = u32::MAX;

    // Overflows in debug, wraps in release:
    // let b = a + 1;

    // Checked: returns None on overflow
    let b = a.checked_add(1);
    println!("Checked: {:?}", b);        // => Checked: None

    // Saturating: clamps to MAX on overflow
    let c = a.saturating_add(1);
    println!("Saturating: {}", c);       // => Saturating: 4294967295 (MAX)
}
```

**Key Takeaway**: Restriction lints (`unwrap_used`, `indexing_slicing`, `unsafe_code = "forbid"`) enforce code quality rules that the regular compiler and basic Clippy do not catch. Use them in production code to eliminate entire categories of potential panics.

**Why It Matters**: A CLI that panics on unexpected input is a bad CLI. Restriction lints make panics structurally impossible (for `.unwrap()`) or explicitly visible (for `unsafe`). Security-sensitive tools and tools running in CI where a panic kills the entire pipeline benefit most. The `cargo` CLI itself runs with similar restrictions to ensure it cannot panic on malformed input.

---

## Example 63: Replacing unwrap

`.unwrap()` panics when the value is `None` or `Err`. Production code replaces it with: `.expect("context")` (panics with context), `?` (propagates the error), `if let Some(v)` (handles the None case), or `match` (handles both cases). Knowing which replacement to use depends on whether failure is a programming error or a user-visible error.

```rust
use anyhow::{Context, Result};

fn main() -> Result<()> {
    // Pattern 1: .expect() for "this should never be None" (programming error)
    let items = vec![1u32, 2, 3];
    let first = items.first()
        .expect("items is non-empty — populated above");
                                         // => Panics with message if items is empty
                                         // => Appropriate when empty = programming bug
    println!("First: {}", first);

    // Pattern 2: ? for propagating user-visible errors
    let content = std::fs::read_to_string("Cargo.toml")
        .context("failed to read Cargo.toml")?;
                                         // => Returns Err to caller instead of panicking
                                         // => Appropriate for expected failure modes
    println!("Read {} bytes", content.len());

    // Pattern 3: if let for "might be absent, that's OK"
    let maybe_value: Option<u32> = None;
    if let Some(v) = maybe_value {
        println!("Value: {}", v);
    }
    // No else needed: absence is a normal case, not an error

    // Pattern 4: .unwrap_or() for a sensible default
    let count: Option<u32> = None;
    let actual = count.unwrap_or(0);     // => Use 0 when None
    println!("Count: {}", actual);

    // Pattern 5: match for handling both cases explicitly
    let result: Result<u32, &str> = Err("parse failed");
    match result {
        Ok(n)  => println!("Got: {}", n),
        Err(e) => eprintln!("Error: {}", e),
    }

    Ok(())
}

// Decision guide:
// .expect("msg")  — failure = programming error (impossible state in correct code)
// ?               — failure = user error (bad input, missing file, etc.)
// .unwrap_or(d)   — failure = expected, use default
// if let / match  — failure = expected, different code paths
// .ok_or(err)?    — convert Option to Result and propagate
```

**Key Takeaway**: Replace `.unwrap()` with `.expect("reason")` for programming errors, `?` for user-visible errors, `.unwrap_or(default)` for expected absence, and `if let / match` for branching on presence. Never use `.unwrap()` in code that runs on user input.

**Why It Matters**: Every `.unwrap()` is a latent panic. In a tool that processes user-provided paths and content, panics are a quality failure—users see a cryptic "thread main panicked" message instead of a helpful error. The `?` operator with `.context()` produces error messages that tell users what went wrong and why. This is the difference between a tool that professionals recommend and one they warn others to avoid.

---

## Example 64: Custom Display for Enums

Implementing `std::fmt::Display` enables `{}` formatting and `to_string()` on custom types. For output format enums, `Display` returns the string the user typed. `std::str::FromStr` enables parsing from strings—needed for deserializing from config files or clap arguments without `ValueEnum`.

```rust
use std::fmt;
use std::str::FromStr;

#[derive(Debug, Clone, PartialEq)]
enum OutputFormat {
    Text,
    Json,
    Markdown,
}

// Display: how the enum looks when printed with {}
impl fmt::Display for OutputFormat {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            OutputFormat::Text     => write!(f, "text"),
                                      // => write!(f, "...") writes to formatter
            OutputFormat::Json     => write!(f, "json"),
            OutputFormat::Markdown => write!(f, "markdown"),
        }
    }
}

// FromStr: parse from &str (enables .parse::<OutputFormat>() and clap parsing)
impl FromStr for OutputFormat {
    type Err = String;                   // => Error type for parse failure

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        match s.to_lowercase().as_str() {// => Case-insensitive parsing
            "text"     => Ok(OutputFormat::Text),
            "json"     => Ok(OutputFormat::Json),
            "markdown" | "md" => Ok(OutputFormat::Markdown),
                                         // => Accept "md" alias for "markdown"
            other => Err(format!("unknown format: '{}'. Expected: text, json, markdown", other)),
        }
    }
}

fn main() {
    // Display: use in format strings and println!
    let fmt = OutputFormat::Json;
    println!("Format: {}", fmt);         // => Format: json (uses Display)
    println!("Format: {:?}", fmt);       // => Format: Json (uses Debug)

    let s = fmt.to_string();             // => "json" (uses Display)
    println!("String: {}", s);

    // FromStr: parse from a string
    let parsed: Result<OutputFormat, _> = "markdown".parse();
                                         // => .parse::<OutputFormat>() uses FromStr
    println!("{:?}", parsed);            // => Ok(Markdown)

    let alias: Result<OutputFormat, _> = "md".parse();
    println!("{:?}", alias);             // => Ok(Markdown)

    let bad: Result<OutputFormat, _> = "xml".parse();
    println!("{:?}", bad);               // => Err("unknown format: 'xml'...")

    // Round-trip: Display then FromStr
    for format in [OutputFormat::Text, OutputFormat::Json, OutputFormat::Markdown] {
        let s = format.to_string();
        let back: OutputFormat = s.parse().expect("Display produces valid FromStr input");
        assert_eq!(format, back);        // => Round-trip works
    }
    println!("Round-trip: all passed");
}
```

**Key Takeaway**: Implement `Display` for `{}` formatting and `to_string()`. Implement `FromStr` for `.parse()` support. Together they enable round-trip serialization and deserialization of enums from user-provided strings.

**Why It Matters**: An output format enum that implements `Display` and `FromStr` can be serialized to a config file, deserialized back, and printed in help messages—all using the same representation the user typed. This consistency removes the gap between what users type (`--format markdown`) and what appears in error messages and config files (`"markdown"`).

---

## Example 65: Markdown Parsing

`pulldown-cmark` provides an event-based Markdown parser. It streams events (headings, links, text, code blocks) rather than building a full AST. This makes it memory-efficient for large documents. Add `pulldown-cmark = "0.12"` to `Cargo.toml`.

```rust
use pulldown_cmark::{Event, HeadingLevel, Options, Parser, Tag, TagEnd};

fn main() {
    let markdown = r#"
# My CLI Tool

This tool validates file naming conventions.

## Usage

Run with `my-tool check --path src/`.

## Links

See the [documentation](https://example.com/docs) for details.
And the [source code](https://github.com/example/my-tool).
"#;

    // Create a parser with default options
    let parser = Parser::new_ext(markdown, Options::all());
                                         // => Options::all(): enable all Markdown extensions
                                         // => Returns an iterator of Event values

    let mut headings: Vec<String> = Vec::new();
    let mut links: Vec<String> = Vec::new();
    let mut in_heading = false;
    let mut current_heading = String::new();

    for event in parser {
        match event {
            Event::Start(Tag::Heading { level: HeadingLevel::H1 | HeadingLevel::H2, .. }) => {
                in_heading = true;       // => Opening heading tag
                current_heading.clear();
            }
            Event::End(TagEnd::Heading(_)) => {
                if in_heading && !current_heading.is_empty() {
                    headings.push(current_heading.clone());
                }
                in_heading = false;
            }
            Event::Text(text) if in_heading => {
                current_heading.push_str(&text);
                                         // => Accumulate text within headings
            }
            Event::Start(Tag::Link { dest_url, .. }) => {
                links.push(dest_url.to_string());
                                         // => Extract the URL from link tags
            }
            _ => {}                      // => Ignore all other events
        }
    }

    println!("Headings:");
    for h in &headings {
        println!("  {}", h);             // => My CLI Tool
    }                                    // => Usage
                                         // => Links

    println!("Links:");
    for l in &links {
        println!("  {}", l);             // => https://example.com/docs
    }                                    // => https://github.com/example/my-tool
}
```

**Key Takeaway**: `pulldown-cmark` streams Markdown as `Event` values. Match on `Event::Start(Tag::...)`, `Event::Text(...)`, and `Event::End(...)` to extract specific elements like headings, links, and code blocks.

**Why It Matters**: Documentation validators check that Markdown files have correct heading structure, working links, and proper code block language tags. Event-based parsing handles arbitrarily large files without loading them entirely into an AST. Tools like `cargo`'s doc linter and the `ayokoding-cli` link validator use pulldown-cmark to process Markdown efficiently.

---

## Example 66: XML Parsing

`quick-xml` provides event-based XML parsing. It reads XML as a stream of events (start elements, end elements, text, attributes). This handles large XML files like code coverage reports without loading them into memory. Add `quick-xml = "0.37"` to `Cargo.toml`.

```rust
use quick_xml::events::Event;
use quick_xml::Reader;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Simulate a simplified coverage report (like Cobertura format)
    let xml = r#"<?xml version="1.0"?>
<coverage line-rate="0.85" branch-rate="0.75">
    <packages>
        <package name="src.commands">
            <classes>
                <class name="check.rs" line-rate="0.90"/>
                <class name="report.rs" line-rate="0.75"/>
            </classes>
        </package>
    </packages>
</coverage>"#;

    let mut reader = Reader::from_str(xml);
                                         // => Reader: streams XML events from &str
    reader.config_mut().trim_text(true); // => Trim whitespace from text nodes

    let mut buf = Vec::new();            // => Reused buffer for efficiency

    loop {
        match reader.read_event_into(&mut buf) {
            Ok(Event::Start(ref e)) => {  // => Opening tag: <element attr="...">
                match e.name().as_ref() {
                    b"coverage" => {      // => b"...": byte string for comparison
                        for attr in e.attributes().flatten() {
                            if attr.key.as_ref() == b"line-rate" {
                                let rate = std::str::from_utf8(&attr.value)?;
                                println!("Overall line rate: {}", rate);
                            }
                        }
                    }
                    b"class" => {
                        let mut name = String::new();
                        let mut rate = String::new();
                        for attr in e.attributes().flatten() {
                            match attr.key.as_ref() {
                                b"name"      => name = String::from_utf8(attr.value.to_vec())?,
                                b"line-rate" => rate = String::from_utf8(attr.value.to_vec())?,
                                _ => {}
                            }
                        }
                        println!("Class {}: {}%", name,
                            rate.parse::<f64>().unwrap_or(0.0) * 100.0);
                    }
                    _ => {}
                }
            }
            Ok(Event::Eof) => break,     // => End of document: exit loop
            Err(e) => return Err(Box::new(e)),
            _ => {}                      // => Ignore all other events
        }
        buf.clear();                     // => Reuse buffer for next event
    }

    Ok(())
}
```

**Key Takeaway**: `quick-xml` streams XML events without loading the full document. Match on `Event::Start`, extract attributes, and handle `Event::Eof` to terminate. Clear the buffer between events for efficiency.

**Why It Matters**: CI coverage reports (Cobertura, JaCoCo, Clover) are XML. A coverage-checking CLI that reads these reports needs XML parsing. Event-based parsing handles multi-megabyte XML files efficiently. Production tools like `cargo-llvm-cov` and various CI integrations use quick-xml for exactly this reason.

---

## Example 67: Glob Patterns

The `glob` crate provides `glob::glob()` that returns an iterator over matching paths. Patterns use `*` (any filename characters), `**` (any directory depth), and `?` (single character). Add `glob = "0.3"` to `Cargo.toml`.

```rust
use glob::glob;

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Find all Rust files in current directory tree
    for entry in glob("**/*.rs")? {      // => **/*.rs: any depth, any .rs file
                                          // => Returns GlobResult<PathBuf>
        match entry {
            Ok(path) => {
                println!("{}", path.display());
                                          // => Prints each matching path
            }
            Err(e) => eprintln!("Error: {}", e),
                                          // => Permission denied or similar
        }
    }

    // Find top-level TOML files
    let toml_files: Vec<_> = glob("*.toml")?
        .filter_map(|r| r.ok())           // => Skip errors
        .collect();
    println!("TOML files: {:?}", toml_files);

    // Find all Markdown files with depth limit (manual)
    let md_files: Vec<_> = glob("**/*.md")?
        .filter_map(|r| r.ok())
        .filter(|p| {
            p.components().count() <= 4  // => Limit depth to 4 components
        })
        .collect();
    println!("Shallow Markdown files: {}", md_files.len());

    // Glob with alternatives using separate patterns
    let patterns = ["**/*.rs", "**/*.toml", "**/*.md"];
    let all_files: Vec<_> = patterns.iter()
        .flat_map(|pat| glob(pat).ok().into_iter().flatten())
        .filter_map(|r| r.ok())
        .collect();
    println!("Source + config + docs files: {}", all_files.len());

    Ok(())
}
```

**Key Takeaway**: `glob("**/*.rs")?` iterates over matching paths. Use `.filter_map(|r| r.ok())` to skip permission errors. Chain multiple glob patterns with `.flat_map()` to match multiple extensions.

**Why It Matters**: Glob patterns are the standard way to specify file sets in build tools, linters, and formatters. A tool that accepts `--include "**/*.rs"` and `--exclude "target/**"` needs glob evaluation. The glob crate handles the `**` recursive matching that `std::fs::read_dir` does not provide.

---

## Example 68: SHA-2 Hashing

The `sha2` crate computes SHA-256 and SHA-512 hashes. Use SHA-256 for file integrity checks and content-addressed caching. The hex crate (or manual formatting) converts bytes to a hex string. Add `sha2 = "0.10"` to `Cargo.toml`.

```rust
use sha2::{Digest, Sha256};

fn hash_string(s: &str) -> String {
    let mut hasher = Sha256::new();      // => Create new SHA-256 hasher
    hasher.update(s.as_bytes());         // => Feed data to the hasher
                                          // => Can call .update() multiple times
    let result = hasher.finalize();      // => Compute the final hash (consumes hasher)
                                          // => Returns GenericArray<u8, U32>

    // Format as hex string
    result.iter()
          .map(|byte| format!("{:02x}", byte))
                                          // => Each byte as 2-digit hex: 0a, ff, etc.
          .collect::<String>()            // => Join all hex strings
}

fn hash_file_content(content: &[u8]) -> String {
    let mut hasher = Sha256::new();
    hasher.update(content);              // => &[u8] content fed directly
    let result = hasher.finalize();
    result.iter().map(|b| format!("{:02x}", b)).collect()
}

fn main() {
    let text = "my-checker 0.1.0";
    let hash = hash_string(text);
    println!("SHA-256 of '{}': {}", text, hash);
    // Output: SHA-256 of 'my-checker 0.1.0': (64-char hex string)

    // Useful for content integrity: if content changes, hash changes
    let hash2 = hash_string("my-checker 0.1.1"); // => Version bump
    println!("Hashes equal: {}", hash == hash2);
                                          // => Output: Hashes equal: false

    // Hash a file's content
    match std::fs::read("Cargo.toml") {
        Ok(content) => {
            let file_hash = hash_file_content(&content);
            println!("Cargo.toml hash: {}", &file_hash[..16]);
                                          // => First 16 chars of hash (for display)
        }
        Err(e) => eprintln!("Could not read Cargo.toml: {}", e),
    }

    // Incremental hashing: hash multiple pieces without concatenating
    let mut hasher = Sha256::new();
    hasher.update(b"tool-name:");        // => Byte literal prefix
    hasher.update(b"my-checker");        // => Actual name
    hasher.update(b":version:0.1.0");   // => Version
    let combined_hash: String = hasher.finalize().iter()
        .map(|b| format!("{:02x}", b)).collect();
    println!("Combined hash: {}", &combined_hash[..16]);
}
```

**Key Takeaway**: Create `Sha256::new()`, call `.update(data)` for each piece, then `.finalize()` for the hash bytes. Format with `{:02x}` for hex strings. Use incremental hashing to avoid concatenating large inputs.

**Why It Matters**: CLI tools that cache expensive computations use content hashes to detect changes: "if the hash of this config file matches the stored hash, skip recomputation." File integrity checking tools compare hashes to detect corruption or tampering. `cargo` uses hashes extensively in its build cache to determine which artifacts need rebuilding.

---

## Example 69: OnceLock and Regex Cache

Compile all Regex patterns once into a `HashMap<&str, Regex>` stored in a `OnceLock`. Functions look up patterns by name. This avoids recompilation on every call while allowing a flexible, named pattern registry. This is the production pattern for CLIs with many patterns.

```rust
use std::collections::HashMap;
use std::sync::OnceLock;
use regex::Regex;

// Global pattern cache: initialized once, reused forever
static PATTERNS: OnceLock<HashMap<&'static str, Regex>> = OnceLock::new();

fn get_pattern(name: &str) -> Option<&'static Regex> {
    let cache = PATTERNS.get_or_init(|| {
                                          // => Closure runs exactly once on first call
        let mut map = HashMap::new();

        // Register all patterns by name
        map.insert(
            "kebab-case",
            Regex::new(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
                .expect("kebab-case is a valid regex"),
        );
        map.insert(
            "version",
            Regex::new(r"^\d+\.\d+\.\d+$")
                .expect("version is a valid regex"),
        );
        map.insert(
            "commit-msg",
            Regex::new(r"^(feat|fix|docs|chore|refactor|test|ci|style|perf|revert)(\(.+\))?: .{1,72}$")
                .expect("commit-msg is a valid regex"),
        );

        map
    });

    cache.get(name)                       // => Returns Option<&Regex>
}

fn check_name(name: &str) -> bool {
    get_pattern("kebab-case")             // => Lookup: O(1), no recompilation
        .map(|re| re.is_match(name))
        .unwrap_or(false)
}

fn check_version(ver: &str) -> bool {
    get_pattern("version")
        .map(|re| re.is_match(ver))
        .unwrap_or(false)
}

fn main() {
    let names = ["my-tool", "MyTool", "my_tool", "checker-v2"];
    for name in &names {
        println!("{}: {}", name, if check_name(name) { "ok" } else { "bad" });
    }
    // Output:
    // my-tool: ok
    // MyTool: bad
    // my_tool: bad
    // checker-v2: ok

    let versions = ["1.0.0", "0.1.2", "1.0", "1.0.0.0"];
    for ver in &versions {
        println!("{}: {}", ver, if check_version(ver) { "valid" } else { "invalid" });
    }
    // Output:
    // 1.0.0: valid
    // 0.1.2: valid
    // 1.0: invalid
    // 1.0.0.0: invalid
}
```

**Key Takeaway**: Store compiled `Regex` patterns in a `OnceLock<HashMap<&'static str, Regex>>`. Look up patterns by name for O(1) access with zero recompilation. The `OnceLock` ensures thread-safe initialization.

**Why It Matters**: A checker that validates 10,000 files with 5 patterns would recompile those patterns 50,000 times without caching. With `OnceLock`, they compile once on the first file and reuse on all subsequent files. The named registry pattern also enables configuration-driven rule sets: load rule names from config, look up compiled patterns by name, run only enabled rules.

---

## Example 70: Validation Orchestration

Orchestrate multiple validators by collecting all results before reporting. Run every validator regardless of earlier failures ("collect all" strategy), accumulate results in a `Vec`, and summarize at the end. This gives users a complete picture in one run rather than requiring multiple fix-run cycles.

```rust
use std::path::Path;

#[derive(Debug)]
struct Violation {
    check: String,
    path: String,
    message: String,
}

impl Violation {
    fn new(check: &str, path: &str, message: &str) -> Self {
        Self {
            check: check.to_string(),
            path: path.to_string(),
            message: message.to_string(),
        }
    }
}

// Individual validators: each returns Vec<Violation> (can be empty)
fn check_naming(files: &[&str]) -> Vec<Violation> {
    files.iter()
        .filter(|f| f.contains('_') || f.chars().any(|c| c.is_uppercase()))
        .map(|f| Violation::new("naming", f, "must be lowercase-kebab-case"))
        .collect()
}

fn check_extension(files: &[&str]) -> Vec<Violation> {
    files.iter()
        .filter(|f| !f.ends_with(".rs") && !f.ends_with(".toml") && !f.ends_with(".md"))
        .map(|f| Violation::new("extension", f, "unexpected file extension"))
        .collect()
}

// Orchestrator: runs all validators, collects all results
fn run_all_checks(files: &[&str]) -> Vec<Violation> {
    let mut all_violations: Vec<Violation> = Vec::new();

    // Run each check and extend the accumulator
    all_violations.extend(check_naming(files));
                                         // => Always runs, even if naming found issues
    all_violations.extend(check_extension(files));
                                         // => Always runs, even if extension found issues

    // Sort by path for deterministic output
    all_violations.sort_by(|a, b| a.path.cmp(&b.path).then(a.check.cmp(&b.check)));

    all_violations
}

fn main() {
    let files = vec![
        "main.rs",
        "BadName.rs",        // => naming violation
        "utils.go",          // => extension violation
        "my_lib.rs",         // => naming violation
        "Cargo.toml",
    ];

    let violations = run_all_checks(&files);

    if violations.is_empty() {
        println!("All checks passed");
        return;
    }

    println!("Found {} violation(s):", violations.len());
    for v in &violations {
        println!("  [{}] {}: {}", v.check, v.path, v.message);
    }

    // Summary
    println!("\nSummary: {} violations in {} files",
        violations.len(),
        violations.iter().map(|v| &v.path).collect::<std::collections::HashSet<_>>().len());

    std::process::exit(1);
}
```

**Key Takeaway**: Run all validators regardless of earlier failures. Collect violations into a shared `Vec`, sort for deterministic output, then summarize. This gives users all issues in one run.

**Why It Matters**: A tool that stops at the first error forces users into a slow cycle of fix-run-fix-run. Collecting all violations means the user can fix everything in one editing session. This is why `clippy`, `eslint`, and `mypy` all run all checks by default and report everything. The sort for deterministic output ensures that the report is the same on every run, making it diffable in version control.

---

## Example 71: Integration Testing with assert_cmd and predicates

Complex integration test scenarios combine `assert_cmd` command invocations with `predicates` for rich stdout/stderr assertions. Test multiple subcommands in sequence, verify exact output patterns, and test error cases with specific error messages.

```rust
#[cfg(test)]
mod tests {
    use assert_cmd::Command;
    use predicates::prelude::*;

    // Test that the binary exists and responds to --help
    #[test]
    fn test_help_flag() {
        Command::cargo_bin("my-checker").unwrap()
            .arg("--help")
            .assert()
            .success()
            .stdout(predicate::str::contains("Validates file naming"))
                                         // => Help output contains description
            .stdout(predicate::str::contains("check"))
                                         // => Lists the check subcommand
            .stdout(predicate::str::contains("report"));
                                         // => Lists the report subcommand
    }

    #[test]
    fn test_version() {
        Command::cargo_bin("my-checker").unwrap()
            .arg("--version")
            .assert()
            .success()
            .stdout(predicate::str::is_match(r"\d+\.\d+\.\d+").unwrap());
                                         // => stdout matches version number regex
    }

    #[test]
    fn test_check_with_json_output() {
        let dir = tempfile::tempdir().unwrap();
        std::fs::write(dir.path().join("bad_File.rs"), b"// test").unwrap();

        Command::cargo_bin("my-checker").unwrap()
            .arg("check")
            .arg("--path").arg(dir.path())
            .arg("--format").arg("json")
            .assert()
            .failure()
            .stdout(predicate::str::contains("\"rule\""))
                                         // => JSON output contains "rule" key
            .stdout(predicate::str::contains("bad_File.rs"));
                                         // => References the problematic file
    }

    #[test]
    fn test_unknown_subcommand_error() {
        Command::cargo_bin("my-checker").unwrap()
            .arg("nonexistent")
            .assert()
            .failure()
            .stderr(predicate::str::contains("error"));
                                         // => Error message goes to stderr
    }

    #[test]
    fn test_multiple_assertions() {
        Command::cargo_bin("my-checker").unwrap()
            .arg("check")
            .arg("--path").arg(".")
            .assert()
            .code(predicate::in_iter([0, 1]));
                                         // => Exit code is either 0 or 1 (not 2+)
    }
}
```

**Key Takeaway**: Combine `assert_cmd` with `predicates` for rich assertions: `.stdout(predicate::str::contains("..."))`, `.stdout(predicate::str::is_match(regex).unwrap())`, `.code(predicate::in_iter([...]))`. Always test both success and failure paths.

**Why It Matters**: Integration tests verify the complete user experience: correct subcommand dispatch, proper exit codes, helpful error messages, and valid output format. Unit tests cannot catch bugs where the CLI parses arguments correctly but routes them to the wrong handler. Every integration test in the test suite represents a user scenario that must never regress.

---

## Example 72: Testing stderr

CLI tools write errors and diagnostics to stderr. Test stderr output with `.stderr(predicate::str::contains("..."))` in `assert_cmd`. This verifies that errors contain actionable messages and that normal output does not contaminate stderr.

```rust
#[cfg(test)]
mod tests {
    use assert_cmd::Command;
    use predicates::prelude::*;

    #[test]
    fn test_missing_file_error() {
        Command::cargo_bin("my-checker").unwrap()
            .arg("check")
            .arg("--path").arg("/nonexistent/path/that/does/not/exist")
            .assert()
            .failure()                   // => Must fail (path doesn't exist)
            .stderr(predicate::str::contains("not found")
                .or(predicate::str::contains("No such file")));
                                         // => Error message explains what's missing
    }

    #[test]
    fn test_success_has_no_stderr() {
        let dir = tempfile::tempdir().unwrap();
                                         // => Empty directory: no violations

        Command::cargo_bin("my-checker").unwrap()
            .arg("check")
            .arg("--path").arg(dir.path())
            .assert()
            .success()
            .stderr(predicate::str::is_empty());
                                         // => Stderr is empty on success
                                         // => No spurious warnings or debug output
    }

    #[test]
    fn test_verbose_goes_to_stderr() {
        let dir = tempfile::tempdir().unwrap();

        Command::cargo_bin("my-checker").unwrap()
            .arg("--verbose")
            .arg("check")
            .arg("--path").arg(dir.path())
            .assert()
            .success()
            .stderr(predicate::str::contains("verbose"));
                                         // => Verbose messages go to stderr
                                         // => Not mixed into stdout report
    }

    #[test]
    fn test_error_message_context() {
        Command::cargo_bin("my-checker").unwrap()
            .arg("check")
            .arg("--path").arg("/dev/null")
            .assert()
            .code(predicate::ge(1u8))    // => Exit code >= 1 (failure or usage error)
            .stderr(predicate::str::is_match(r"(error|Error|failed)").unwrap());
                                         // => Error message uses "error" or "failed"
    }
}
```

**Key Takeaway**: Test stderr separately from stdout. Verify that error cases produce descriptive stderr messages, that success produces empty stderr, and that verbose output goes to stderr rather than stdout. These tests protect the stdout/stderr contract that shell pipelines depend on.

**Why It Matters**: The stdout/stderr separation is what makes CLI tools composable. A tool that mixes error messages into stdout breaks `my-checker check | jq '.[]'` because the error message is not valid JSON. Tests that verify stderr content protect this contract. Without them, a refactoring could accidentally move a diagnostic from `eprintln!` to `println!` and silently break every downstream pipeline.

---

## Example 73: Release Profile

The `[profile.release]` section in `Cargo.toml` controls optimization for release builds. `opt-level = 3` enables maximum optimization. `lto = "thin"` enables cross-module optimization. `codegen-units = 1` maximizes inlining. `panic = "abort"` removes unwinding code. `strip = "symbols"` reduces binary size.

```toml
# Cargo.toml — release profile
[profile.release]
opt-level = 3          # Maximum optimization: 1=fast compile, 2=default, 3=max speed
lto = "thin"           # Link-time optimization: "thin" (fast+good) or "fat" (slow+best)
codegen-units = 1      # Single compilation unit: allows more inlining across modules
                       # Trade-off: slower compile, faster binary
panic = "abort"        # On panic: abort immediately (no stack unwinding)
                       # Removes unwinding tables: ~10% smaller binary
                       # Do NOT use if you catch panics (std::panic::catch_unwind)
strip = "symbols"      # Strip debug symbols from binary: smaller release binary
                       # Alternative: "debuginfo" (strip only debug info, keep symbols)

# Development profile: fast compilation, debug info
[profile.dev]
opt-level = 0          # No optimization: fastest compilation
debug = true           # Full debug info for debuggers and backtraces

# A balanced profile for CI testing (faster than release, more realistic than dev)
[profile.test]
opt-level = 1          # Basic optimization: faster than dev, compiles quicker than release
```

```rust
// This is not compilable code — it documents Cargo.toml configuration
// Create this in your actual Cargo.toml
fn main() {
    // Build for release: cargo build --release
    // Binary in: target/release/my-checker
    //
    // With the above settings:
    // - Binary runs at near-maximum speed
    // - Binary is as small as possible (stripped symbols)
    // - Panics abort immediately (smaller, faster)
    // - LTO allows inlining across crate boundaries
    println!("Release profile documentation example");
}
```

**Key Takeaway**: Configure `[profile.release]` in `Cargo.toml` for optimized production binaries. `opt-level = 3`, `lto = "thin"`, `codegen-units = 1`, `panic = "abort"`, and `strip = "symbols"` are the standard production settings for CLI tools.

**Why It Matters**: Default Rust release builds are already much faster than Python or Java equivalents, but the above settings close the gap to C and improve further. For a CLI checking 100,000 files, the difference between `opt-level = 2` and `opt-level = 3` with `lto = "thin"` can be 20-30% faster execution. `strip = "symbols"` reduces binary size from ~5MB to ~1MB for a typical CLI, making distribution via `cargo install` faster. Tools like `ripgrep` and `fd` distribute with similar settings.

---

## Example 74: Dual Crate Layout

A dual crate has both a library (`[lib]`) and a binary (`[[bin]]`) in one `Cargo.toml`. The library contains the core logic; the binary is a thin wrapper that calls library functions. Integration tests can import the library directly without spawning a process, enabling fast unit-style testing of CLI business logic.

```toml
# Cargo.toml
[package]
name = "my-checker"
version = "0.1.0"
edition = "2024"

[[bin]]
name = "my-checker"
path = "src/main.rs"   # Binary: parses CLI args, calls library

[lib]
name = "my_checker"    # Library: contains all business logic
path = "src/lib.rs"    # Tests import this directly
```

```rust
// src/lib.rs — library: public API for testing
pub struct CheckConfig {
    pub path: String,
    pub max_errors: u32,
}

pub struct CheckReport {
    pub violations: Vec<String>,
    pub files_checked: u32,
}

pub fn run_check(config: &CheckConfig) -> anyhow::Result<CheckReport> {
                                          // => Library function: testable without spawning process
    let mut report = CheckReport {
        violations: Vec::new(),
        files_checked: 0,
    };

    // Process files (simplified)
    report.files_checked = 1;
    if config.path.contains('_') {
        report.violations.push(format!("{}: underscores not allowed", config.path));
    }

    Ok(report)
}

// src/main.rs — binary: thin CLI wrapper
// use clap::Parser;
// use my_checker::{run_check, CheckConfig};
//
// fn main() -> anyhow::Result<()> {
//     let cli = Cli::parse();
//     let config = CheckConfig { path: cli.path, max_errors: cli.max_errors };
//     let report = run_check(&config)?;
//     // ... print report ...
//     Ok(())
// }

// Tests in src/lib.rs (accessible directly, no process spawn):
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_run_check_clean() {
        let config = CheckConfig { path: String::from("my-tool"), max_errors: 10 };
        let report = run_check(&config).unwrap();
        assert!(report.violations.is_empty());
    }

    #[test]
    fn test_run_check_violation() {
        let config = CheckConfig { path: String::from("my_tool"), max_errors: 10 };
        let report = run_check(&config).unwrap();
        assert_eq!(report.violations.len(), 1);
    }
}

fn main() {
    println!("Dual crate layout demonstration");
}
```

**Key Takeaway**: Dual crate layout (`[[bin]]` + `[lib]`) separates the CLI entry point from business logic. Library tests run without process spawning—much faster than `assert_cmd` integration tests. The binary becomes a thin `Cli::parse()` → `lib::run()` wrapper.

**Why It Matters**: Integration tests with `assert_cmd` take 50-500ms per test because they compile and spawn a new process. Library tests run in microseconds because they call functions directly. For a test suite with 100 checks, this is the difference between a 10-second test run and a 10-minute test run. `cargo` itself uses this pattern: `cargo-lib` contains all logic, `cargo` binary is a thin wrapper.

---

## Example 75: Complex Match Guards

Match guards (`if condition`) add extra constraints to match arms. Combining patterns with guards enables expressing complex conditions that cannot be captured by pattern structure alone. Guards are expressions and can call functions.

```rust
fn main() {
    // Match on a tuple with guards
    let files: Vec<(&str, u32, bool)> = vec![
        ("main.rs", 0, true),
        ("bad_name.rs", 5, false),
        ("lib.rs", 0, false),
        ("UPPER.rs", 3, true),
        ("utils.rs", 1, true),
    ];

    for (name, errors, has_tests) in &files {
        let status = match (name, errors, has_tests) {
            (_, 0, true)  => "PASS: clean with tests",
                                          // => 0 errors AND has tests
            (_, 0, false) => "WARN: clean but no tests",
                                          // => 0 errors BUT no tests
            (n, e, _) if n.chars().any(|c| c.is_uppercase()) && *e > 0 => {
                "FAIL: bad name + errors"  // => Uppercase name AND has errors
                                          // => Guard: checks two conditions
            }
            (_, e, _) if *e > 10 => "CRITICAL: too many errors",
                                          // => More than 10 errors (regardless of name)
            _ => "FAIL: has errors",      // => Any other error case
        };
        println!("{}: {}", name, status);
    }
    // Output:
    // main.rs: PASS: clean with tests
    // bad_name.rs: FAIL: has errors
    // lib.rs: WARN: clean but no tests
    // UPPER.rs: FAIL: bad name + errors
    // utils.rs: FAIL: has errors

    // Match guard with binding
    let thresholds = [0u32, 50, 75, 90, 100];
    for t in &thresholds {
        let grade = match t {
            t if *t == 100 => "Perfect",
            t if *t >= 90  => "Excellent",
            t if *t >= 75  => "Good",
            t if *t >= 50  => "Pass",
            _              => "Fail",    // => t is bound but not used in this arm
        };
        println!("{}: {}", t, grade);
    }
}
```

**Key Takeaway**: Match guards (`if condition`) add Boolean conditions to match arms. The pattern must match first, then the guard is evaluated. Bindings in the pattern are available in the guard expression. Combine patterns and guards for complex dispatch logic.

**Why It Matters**: Validation orchestrators dispatch to different reporting modes based on multiple conditions simultaneously: error count, violation severity, and output format. Match guards express these multi-condition dispatches readably without nested if-else chains. The compiler still enforces exhaustiveness even with guards—if no arm matches (all guards false), the compiler requires a wildcard `_` arm.

---

## Example 76: Recursive Directory Validation

Walk a directory tree, apply validators to each file, accumulate violations, and produce a summary. This is the end-to-end pattern for a file-system checker. Combine `walkdir` for traversal, per-file validators returning `Vec<Violation>`, and a summary that shows which files had the most issues.

```rust
use walkdir::WalkDir;

struct Violation {
    path: String,
    rule: String,
    message: String,
}

fn validate_file(path: &str) -> Vec<Violation> {
    let mut violations = Vec::new();

    // Check 1: filename must be kebab-case
    let filename = std::path::Path::new(path)
        .file_name()
        .and_then(|n| n.to_str())
        .unwrap_or("");

    if filename.contains('_') || filename.chars().any(|c| c.is_uppercase()) {
        violations.push(Violation {
            path: path.to_string(),
            rule: String::from("file-naming"),
            message: String::from("filename must be lowercase-kebab-case"),
        });
    }

    violations
}

fn validate_directory(dir: &str) -> Vec<Violation> {
    WalkDir::new(dir)
        .into_iter()
        .filter_map(|e| e.ok())           // => Skip permission errors
        .filter(|e| e.file_type().is_file())
        .filter(|e| e.path().extension().map(|ext| ext == "rs").unwrap_or(false))
        .flat_map(|entry| {               // => Produce violations for each file
            let path = entry.path().to_string_lossy().to_string();
            validate_file(&path)          // => Returns Vec<Violation>
        })
        .collect()                        // => All violations from all files
}

fn main() {
    let violations = validate_directory(".");

    if violations.is_empty() {
        println!("All files pass validation");
        return;
    }

    // Sort by path for deterministic output
    let mut sorted = violations;
    sorted.sort_by(|a, b| a.path.cmp(&b.path));

    println!("Found {} violation(s):", sorted.len());
    for v in &sorted {
        println!("  [{}] {}: {}", v.rule, v.path, v.message);
    }

    // Files with most violations (top 3)
    let mut by_file: std::collections::HashMap<String, u32> = std::collections::HashMap::new();
    for v in &sorted {
        *by_file.entry(v.path.clone()).or_insert(0) += 1;
    }

    let mut file_counts: Vec<_> = by_file.iter().collect();
    file_counts.sort_by(|a, b| b.1.cmp(a.1));

    println!("\nTop violators:");
    for (file, count) in file_counts.iter().take(3) {
        println!("  {} ({} violations)", file, count);
    }

    std::process::exit(1);
}
```

**Key Takeaway**: Compose `WalkDir` traversal with `.flat_map(|entry| validate_file(&path))` to collect all violations from all files in a single chain. Sort for deterministic output. Summarize by file for actionable reporting.

**Why It Matters**: This is the complete pattern for a file-system checker CLI. Each component is independently testable: `validate_file` takes a string and returns violations (pure function), `validate_directory` composes the traversal and per-file validation. Integration tests can use `tempfile::tempdir()` to create a known directory structure and verify the output exactly.

---

## Example 77: chrono for Dates

`chrono` provides date and time handling. Use `Utc::now()` for timestamps, `NaiveDate` for dates without timezone, `format!` for formatting, and duration arithmetic for checking file ages. Add `chrono = "0.4"` to `Cargo.toml`.

```rust
use chrono::{Duration, NaiveDate, Utc};

fn main() {
    // Current UTC timestamp
    let now = Utc::now();                // => DateTime<Utc>: current time in UTC
    println!("Now: {}", now.format("%Y-%m-%d %H:%M:%S UTC"));
                                          // => Output: 2025-12-30 10:23:45 UTC

    // Parse a date string (e.g., from a file or config)
    let release_date = NaiveDate::parse_from_str("2025-06-15", "%Y-%m-%d")
        .expect("valid date format");     // => NaiveDate: no timezone
    println!("Release date: {}", release_date);
                                          // => Output: Release date: 2025-06-15

    // Date arithmetic: how many days since release?
    let today = now.date_naive();         // => Extract date component from DateTime
    let days_since = today.signed_duration_since(release_date).num_days();
    println!("Days since release: {}", days_since);

    // Check if a file is stale (older than N days)
    let last_updated = NaiveDate::parse_from_str("2024-01-01", "%Y-%m-%d")
        .expect("valid date");
    let age = today.signed_duration_since(last_updated).num_days();

    if age > 365 {
        println!("WARNING: file last updated {} days ago ({} > 365)", age, age);
    }

    // Duration arithmetic
    let deadline = today + Duration::days(30); // => 30 days from today
    println!("Deadline: {}", deadline);

    // Format for filenames (ISO 8601: sortable)
    let filename = format!("{}-report.json", now.format("%Y-%m-%d"));
    println!("Report filename: {}", filename);
                                          // => Output: 2025-12-30-report.json
}
```

**Key Takeaway**: Use `Utc::now()` for current timestamps, `NaiveDate::parse_from_str()` for parsing, `.signed_duration_since()` for date differences, and `.format()` for output. Use `NaiveDate` (no timezone) for dates in configs and logs.

**Why It Matters**: CLI tools that generate reports include timestamps for auditability. Tools that check file staleness compare modification dates to thresholds. Tools that generate sorted filenames use ISO 8601 format (`YYYY-MM-DD`) because it sorts lexicographically. These are standard requirements for any CLI that interacts with a governance or CI workflow.

---

## Example 78: Avoiding Common Rust Pitfalls

Four common patterns that GC-language engineers bring to Rust that should be replaced with idiomatic Rust: unnecessary `.clone()`, collecting when you could chain, `.unwrap()` in production, and `String` everywhere instead of `&str` in function parameters.

**Anti-pattern 1: Unnecessary clone**

```rust
fn main() {
    let name = String::from("my-tool");

    // Anti-pattern: clone before passing to a function that only reads
    // process_name(name.clone());      // => Allocates new heap String unnecessarily

    // Correct: pass a reference (borrow)
    process_name(&name);               // => &name: borrow, no allocation
    println!("{}", name);              // => name still valid after borrow

    // Anti-pattern: clone to keep ownership when you could restructure
    let items = vec!["a", "b", "c"];
    // for item in items.clone() { ... } // => Unnecessary clone of Vec

    // Correct: iterate by reference
    for item in &items {               // => &items: iterate borrowed references
        process_item(item);
    }
    println!("{:?}", items);           // => items still valid
}

fn process_name(name: &str) {         // => Takes &str, not String — borrows, not owns
    println!("Processing: {}", name);
}

fn process_item(item: &&str) {
    println!("Item: {}", item);
}
```

**Anti-pattern 2: Collecting when you could chain**

```rust
fn main() {
    let names = vec!["main.rs", "lib.rs", "bad_name.rs"];

    // Anti-pattern: collect intermediate results into Vec
    // let valid: Vec<_> = names.iter().filter(|n| !n.contains('_')).collect();
    // let count = valid.len();
    // for n in &valid { println!("{}", n); }

    // Correct: chain the pipeline, consume once
    let (valid_names, invalid_count): (Vec<_>, usize) = {
        let all = names.iter().filter(|n| !n.contains('_'));
        let valid: Vec<_> = all.collect();
        let invalid = names.len() - valid.len();
        (valid, invalid)
    };

    for n in &valid_names {
        println!("{}", n);
    }
    println!("{} invalid", invalid_count);
}
```

**Anti-pattern 3: String everywhere**

```rust
// Anti-pattern: function takes String when it only reads
// fn validate(name: String) -> bool { name.contains('-') }
// Caller: validate(file_name.clone())  -- unnecessary clone

// Correct: take &str for read-only string access
fn validate(name: &str) -> bool {    // => &str: works with &String, literals, slices
    name.contains('-')
}

fn main() {
    let file = String::from("my-file.rs");
    println!("{}", validate(&file));   // => No clone needed
    println!("{}", validate("literal")); // => Literal &str works too
}
```

**Key Takeaway**: Borrow instead of clone. Chain iterators instead of collecting intermediates. Use `&str` in function parameters instead of `String`. Match instead of `.unwrap()`. Each is a common GC-language reflex that costs performance or reliability in Rust.

**Why It Matters**: The `.clone()` reflex from languages where copying is cheap causes significant heap allocation pressure in Rust. A file-name validator that clones every file path before validation will allocate gigabytes of strings across a large codebase check. The `&str` parameter reflex from Java (where all strings are already references) maps naturally to Rust—the Deref coercion from `&String` to `&str` makes callers pay nothing.

---

## Example 79: Testing with Complex Fixtures

Build complex directory structures in `tempfile::tempdir()` for integration tests that verify multi-file, multi-rule behavior. Table-driven tests in Rust use a `Vec` of test cases run in a loop—readable, concise, and easy to extend.

```rust
#[cfg(test)]
mod tests {
    use std::fs;

    fn setup_project_dir() -> tempfile::TempDir {
        let dir = tempfile::tempdir().expect("failed to create temp dir");

        // Create a realistic project structure
        fs::create_dir(dir.path().join("src")).expect("create src");
        fs::create_dir(dir.path().join("tests")).expect("create tests");

        // Good files
        fs::write(dir.path().join("src/main.rs"), b"fn main() {}").expect("write");
        fs::write(dir.path().join("src/lib.rs"), b"pub fn run() {}").expect("write");

        // Bad files (naming violations)
        fs::write(dir.path().join("src/BadFile.rs"), b"// bad").expect("write");
        fs::write(dir.path().join("src/another_bad.rs"), b"// bad").expect("write");

        dir                              // => Return dir: must not drop before test ends
    }

    #[test]
    fn test_finds_correct_violations() {
        let dir = setup_project_dir();   // => dir lives for the duration of this test
        let violations = super::validate_directory(dir.path().to_str().unwrap());

        assert_eq!(violations.len(), 2, "expected exactly 2 violations");
        assert!(violations.iter().any(|v| v.path.contains("BadFile")));
        assert!(violations.iter().any(|v| v.path.contains("another_bad")));
    }

    // Table-driven tests: each entry is a (input, expected) pair
    #[test]
    fn test_validate_file_table() {
        struct TestCase {
            filename: &'static str,
            expect_violations: usize,
        }

        let cases = vec![
            TestCase { filename: "good-name.rs",   expect_violations: 0 },
            TestCase { filename: "BadName.rs",      expect_violations: 1 },
            TestCase { filename: "under_score.rs",  expect_violations: 1 },
            TestCase { filename: "main.rs",         expect_violations: 0 },
            TestCase { filename: "ALLCAPS.rs",      expect_violations: 1 },
        ];

        for case in &cases {
            let violations = super::validate_file(case.filename);
            assert_eq!(
                violations.len(), case.expect_violations,
                "filename '{}': expected {} violations, got {}",
                case.filename, case.expect_violations, violations.len()
            );
        }
    }

    // Bring in functions from the outer module for testing
    use super::super::{validate_directory, validate_file};
}

// Required: bring in functions tested above
fn validate_file(path: &str) -> Vec<super::Violation> { super::validate_file(path) }
fn validate_directory(dir: &str) -> Vec<super::Violation> { super::validate_directory(dir) }

use super::*;
```

**Key Takeaway**: Build complex test fixtures with `setup_project_dir()` that creates realistic directory structures. Use table-driven tests (`Vec` of test cases with input/expected pairs) to cover many scenarios concisely. The `tempdir` value must live until the test ends—do not immediately drop it.

**Why It Matters**: Complex directory structures cannot be tested with unit tests on individual functions. A fixture that matches the real project structure catches bugs in how validators interact with directory traversal, file filtering, and accumulation. Table-driven tests make it trivial to add new cases: add one struct literal to the `vec!`, and the test covers the new scenario automatically.

---

## Example 80: Putting It All Together

A mini "file naming validator" CLI that synthesizes all concepts from the tutorial. It reads a directory tree with `walkdir`, filters by extension, checks naming convention with a compiled regex from `LazyLock`, reports violations in text/JSON/markdown format based on `--format`, returns exit code 0 on clean and 1 on violations, and has a `check` subcommand with `--path` and `--format` arguments.

```rust
// Cargo.toml dependencies:
// clap = { version = "4.6.1", features = ["derive"] }
// anyhow = "1.0"
// walkdir = "2.5"
// regex = "1.11"
// serde = { version = "1.0", features = ["derive"] }
// serde_json = "1.0"

use std::sync::LazyLock;
use anyhow::{Context, Result};
use clap::{Parser, Subcommand, ValueEnum};
use regex::Regex;
use serde::Serialize;
use walkdir::WalkDir;

// Type alias: cleaner signatures throughout
type AResult<T> = anyhow::Result<T>;

// Compiled regex: initialized once on first check
static KEBAB_RE: LazyLock<Regex> = LazyLock::new(|| {
    Regex::new(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*(\.[a-z0-9]+)?$")
        .expect("KEBAB_RE is a valid regex")
});

// --- CLI definition ---

#[derive(Parser)]
#[command(name = "name-check", version = "0.1.0", about = "Validates file naming conventions")]
struct Cli {
    #[arg(long, global = true, help = "Enable verbose diagnostic output")]
    verbose: bool,

    #[command(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    #[command(about = "Check files in a directory")]
    Check {
        #[arg(long, default_value = ".")]
        path: String,
        #[arg(long, value_enum, default_value = "text")]
        format: OutputFormat,
    },
}

#[derive(Debug, Clone, ValueEnum)]
enum OutputFormat { Text, Json, Markdown }

// --- Domain types ---

#[derive(Debug, Serialize)]
struct Violation {
    path: String,
    rule: String,
    message: String,
}

// --- Core logic ---

fn is_valid_name(name: &str) -> bool {
    KEBAB_RE.is_match(name)              // => Reuses compiled regex (no recompilation)
}

fn check_file(path_str: &str) -> Vec<Violation> {
    let path = std::path::Path::new(path_str);
    let name = path.file_name()
        .and_then(|n| n.to_str())
        .unwrap_or("");                  // => Unknown name: treated as empty (no check)

    if name.is_empty() || is_valid_name(name) {
        return Vec::new();               // => No violations for valid names
    }

    vec![Violation {
        path: path_str.to_string(),
        rule: String::from("file-naming"),
        message: format!("'{}' must be lowercase-kebab-case with optional extension", name),
    }]
}

fn run_check(dir: &str, format: &OutputFormat, verbose: bool) -> AResult<u32> {
    let mut all_violations: Vec<Violation> = Vec::new();

    let walker = WalkDir::new(dir)
        .min_depth(1)
        .into_iter()
        .filter_map(|e| e.ok())
        .filter(|e| e.file_type().is_file());

    for entry in walker {
        let path = entry.path().to_string_lossy().to_string();

        if verbose {
            eprintln!("[verbose] checking: {}", path);
        }

        let violations = check_file(&path);
        all_violations.extend(violations);
    }

    // Sort for deterministic output
    all_violations.sort_by(|a, b| a.path.cmp(&b.path));

    let count = all_violations.len() as u32;

    // Output in requested format
    match format {
        OutputFormat::Text => {
            for v in &all_violations {
                println!("[{}] {}: {}", v.rule, v.path, v.message);
            }
            if count == 0 { println!("All files pass naming check"); }
        }
        OutputFormat::Json => {
            let json = serde_json::to_string_pretty(&all_violations)
                .context("failed to serialize JSON output")?;
            println!("{}", json);
        }
        OutputFormat::Markdown => {
            println!("| File | Rule | Message |");
            println!("|------|------|---------|");
            for v in &all_violations {
                println!("| {} | {} | {} |", v.path, v.rule, v.message);
            }
        }
    }

    Ok(count)
}

fn main() -> Result<()> {
    let cli = Cli::parse();

    match cli.command {
        Commands::Check { path, format } => {
            let violation_count = run_check(&path, &format, cli.verbose)
                .with_context(|| format!("failed to check directory: {}", path))?;

            if violation_count > 0 {
                eprintln!("\n{} violation(s) found", violation_count);
                std::process::exit(1);
            }

            eprintln!("Done: all files pass");
        }
    }

    Ok(())
}

// Tests demonstrate the dual-crate benefit: library functions testable directly
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_valid_names() {
        assert!(is_valid_name("my-tool.rs"));
        assert!(is_valid_name("utils.rs"));
        assert!(is_valid_name("main.rs"));
        assert!(is_valid_name("config-parser.toml"));
    }

    #[test]
    fn test_invalid_names() {
        assert!(!is_valid_name("MyTool.rs"));
        assert!(!is_valid_name("bad_name.rs"));
        assert!(!is_valid_name("UPPER.rs"));
    }

    #[test]
    fn test_check_file_violations() {
        let v = check_file("src/BadFile.rs");
        assert_eq!(v.len(), 1);
        assert_eq!(v[0].rule, "file-naming");
    }

    #[test]
    fn test_check_file_clean() {
        let v = check_file("src/good-file.rs");
        assert!(v.is_empty());
    }
}
```

**Key Takeaway**: A production CLI combines all concepts: `LazyLock` for compiled regex, `anyhow` for errors with context, clap derive for argument parsing, `walkdir` for traversal, `serde` for JSON output, `BTreeMap`-style sorting for deterministic output, proper exit codes, and in-module tests for fast feedback. Each component is independently understandable.

**Why It Matters**: This capstone shows that production Rust CLI code is not magical—it is the composition of the same 20-30 patterns you have practiced in examples 1-79. Real tools like `rhino-cli`, `ayokoding-cli`, and `ripgrep` use exactly these patterns at larger scale. The discipline of small, pure functions (`is_valid_name`, `check_file`) composed by an orchestrator (`run_check`) called by a thin CLI entry point (`main`) makes the code readable, testable, and maintainable as requirements evolve. Congratulations on completing the tutorial—you can now read any production Rust CLI codebase.

---
