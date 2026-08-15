---
title: "Beginner Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 10
---

Examples 1–26 establish Cargo, immutable-by-default values, typed functions, ordinary data models,
and owned collections. Run each with `cargo run --bin ex-NN` from `learning/code/`.

### Example 1: Create a Cargo Project

_ex-01 · exercises co-01_

Cargo creates the manifest and source layout that make a Rust program reproducible. The annotated
source reports the two artifacts rather than relying on a pre-existing project.

```rust
// `cargo new hello` creates Cargo.toml and src/main.rs.
// This output states the layout the command provides.
fn main() {
    println!("Cargo.toml + src/main.rs");
}
```

**Run**: `cargo run --bin ex-01`.

**Key takeaway**: Cargo owns the standard project shape.

**Why it matters**: A shared project shape lets tools locate code, dependencies, tests, and build
outputs predictably. That predictability is the foundation for every later example.

### Example 2: Run a Binary

_ex-02 · exercises co-02_

`cargo run` compiles the selected binary and executes it. The example keeps the observable action
to a single output line.

```rust
// main is the executable entry point.
// println makes the run observable.
fn main() {
    println!("hello, Rust");
}
```

**Run**: `cargo run --bin ex-02`.

**Key takeaway**: `cargo run` closes the edit–compile–execute loop.

**Why it matters**: Frequent small runs turn compiler feedback into a normal part of programming,
not a late integration surprise.

### Example 3: Build Without Running

_ex-03 · exercises co-03_

`cargo build` produces a binary in `target/` without running it. The source identifies that
separation so compiling and executing remain distinct choices.

```rust
// cargo build --bin ex-03 compiles this program.
// The program runs only when explicitly invoked.
fn main() {
    println!("built, then run deliberately");
}
```

**Run**: `cargo build --bin ex-03`.

**Key takeaway**: Building verifies compilation without causing program effects.

**Why it matters**: Later systems programs may inspect files, sockets, or processes. Separating
build from execution makes that boundary deliberate from the start.

### Example 4: Bind an Immutable Value

_ex-04 · exercises co-06_

Bindings are immutable unless declared with `mut`. This first value needs no mutation, so its name
communicates that stable intent.

```rust
// This binding cannot be reassigned.
// Printing verifies the stored value.
fn main() {
    let name = "Rust";
    println!("{name}");
}
```

**Run**: `cargo run --bin ex-04`.

**Key takeaway**: Immutability is Rust’s default, not an extra annotation.

**Why it matters**: Stable values reduce the number of states a reader must consider. Add mutation
only at the narrow point where changing state is genuinely needed.

### Example 5: Opt Into Mutation

_ex-05 · exercises co-06_

`mut` documents a binding whose value will change. The reassignment is visible and limited to this
small scope.

```rust
// mut permits reassignment of this binding.
// The final print shows the changed value.
fn main() {
    let mut retries = 0;
    retries += 1;
    println!("{retries}");
}
```

**Run**: `cargo run --bin ex-05`.

**Key takeaway**: Mutation is explicit at the binding site.

**Why it matters**: Explicit mutation helps reviewers find state changes quickly, a valuable habit
when state later crosses IO or resource-management boundaries.

### Example 6: Observe an Immutable-Binding Error

_ex-06 · exercises co-06_

The runnable form documents the compiler rule without shipping a deliberately failing binary. The
comment names the rejected reassignment and the program shows the valid repair.

```rust
// `let count = 1; count = 2;` is rejected.
// `mut` makes the intended reassignment legal.
fn main() {
    let mut count = 1;
    count = 2;
    println!("{count}");
}
```

**Run**: `cargo run --bin ex-06`.

**Key takeaway**: Make intended mutation explicit instead of fighting the compiler.

**Why it matters**: Rust’s errors describe an invariant. Reading the error as a design question
usually leads to a clearer ownership or mutation boundary.

### Example 7: Use Integer Arithmetic

_ex-07 · exercises co-07_

An integer’s type is inferred from the arithmetic here. A suffix can make a fixed-width choice
explicit when an API requires it.

```rust
// i32 is the usual inferred integer type.
// The expression evaluates before it is printed.
fn main() {
    let total: i32 = 20 + 22;
    println!("{total}");
}
```

**Run**: `cargo run --bin ex-07`.

**Key takeaway**: Types can be inferred or written where precision helps.

**Why it matters**: Numeric types carry range and API contracts. Let inference remove noise, then
write a type when it protects a boundary or explains a decision.

### Example 8: Use Floating-Point Arithmetic

_ex-08 · exercises co-07_

`f64` is Rust’s default floating-point type. This example makes the type explicit to distinguish it
from exact integer arithmetic.

```rust
// f64 represents a floating-point value.
// Formatting makes the result easy to inspect.
fn main() {
    let average: f64 = 7.0 / 2.0;
    println!("{average:.1}");
}
```

**Run**: `cargo run --bin ex-08`.

**Key takeaway**: Numeric type choice is part of the program’s contract.

**Why it matters**: Systems programs often convert sizes, counts, and measurements. Knowing when a
value is integer or floating point prevents accidental assumptions at those boundaries.

### Example 9: Use Bool and Char

_ex-09 · exercises co-07_

`bool` stores a truth value and `char` stores one Unicode scalar value. They are different types
with distinct meanings even when both print compactly.

```rust
// bool expresses a true-or-false condition.
// char holds one Unicode scalar value.
fn main() {
    let ready = true;
    let marker = 'y';
    println!("{ready} {marker}");
}
```

**Run**: `cargo run --bin ex-09`.

**Key takeaway**: Small scalar types express specific intent.

**Why it matters**: Choosing the smallest honest representation clarifies whether code is making a
decision, carrying text, or storing a numeric quantity.

### Example 10: Define a Typed Function

_ex-10 · exercises co-07_

Function parameters and returns are typed in the signature. The body stays focused on one
calculation, and `main` supplies an observable caller.

```rust
// The signature states both input and output types.
// main verifies the function at a call site.
fn double(value: i32) -> i32 { value * 2 }
fn main() { println!("{}", double(21)); }
```

**Run**: `cargo run --bin ex-10`.

**Key takeaway**: A Rust function declares the contract before its body.

**Why it matters**: Explicit signatures let the compiler and a reader check how data flows before
learning implementation detail, especially useful when a function can fail later.

### Example 11: Define a Struct

_ex-11 · co-14_ — A `Service` groups a named field. **Takeaway**: structs model related owned data.

### Example 12: Add a Struct Method

_ex-12 · co-14_ — An `impl` method borrows `self`. **Takeaway**: behavior stays beside its data type.

### Example 13: Define an Enum

_ex-13 · co-15_ — `State` selects one named alternative. **Takeaway**: enums model distinct states.

### Example 14: Carry Data in an Enum

_ex-14 · co-15_ — `Connected(u16)` carries a port. **Takeaway**: variants can contain typed payloads.

### Example 15: Match an Enum Exhaustively

_ex-15 · co-16_ — Every `State` gets a match arm. **Takeaway**: exhaustive matching protects state handling.

### Example 16: Add a Match Guard

_ex-16 · co-16_ — A guard refines a pattern. **Takeaway**: guards keep conditional classification local.

### Example 17: Bind a Match Payload

_ex-17 · co-16_ — An arm names `Bytes` data. **Takeaway**: patterns both test and extract values.

### Example 18: Use If Let

_ex-18 · co-17, co-18_ — `if let` focuses on `Some`. **Takeaway**: use it when only one pattern matters.

### Example 19: Use While Let

_ex-19 · co-17_ — `while let` drains a vector. **Takeaway**: repetition ends cleanly at `None`.

### Example 20: Model Some and None

_ex-20 · co-18_ — `Option` represents presence and absence. **Takeaway**: missing data is explicit.

### Example 21: Grow a Vec

_ex-21 · co-24_ — `Vec` owns a growable sequence. **Takeaway**: push is visible mutation.

### Example 22: Grow a String

_ex-22 · co-24_ — `String` owns mutable text. **Takeaway**: borrow text when appending it.

### Example 23: Iterate a Vec

_ex-23 · co-24_ — The loop borrows each item. **Takeaway**: reading a collection need not consume it.

### Example 24: Destructure a Tuple

_ex-24 · co-07_ — Tuple patterns name positional values. **Takeaway**: compact values can still be clear.

### Example 25: Borrow a Slice

_ex-25 · co-24_ — A slice views part of an array. **Takeaway**: a slice borrows rather than copies.

### Example 26: Shadow a Binding

_ex-26 · co-06_ — A second `port` has a more useful type. **Takeaway**: shadowing keeps conversion local.

These examples use the same `cargo run --bin ex-NN` command from `learning/code/`. They establish
the data surface whose ownership rules start in Example 27.
