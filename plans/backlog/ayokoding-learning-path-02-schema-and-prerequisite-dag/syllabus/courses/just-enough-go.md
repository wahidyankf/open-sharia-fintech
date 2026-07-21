# Just Enough Go (Primer, Go)

**Course ID**: `just-enough-go` · **Format**: Primer · **Language**: Go.

**Short summary**: Go syntax, tooling, goroutines, idioms

**Scope note**: **just enough Go** to be productive in the next topic
([`65-csp-style-concurrency`](./csp-style-concurrency.md)), no more. The toolchain, syntax, structs,
interfaces, the error-value convention, and a goroutine/channel _preview_ only (concurrency depth belongs
to topic 65). This opens Pass 4.

## Why this exists · the big idea

- **The problem before the solution**: Pass 4 is about concurrency, and studying CSP needs a language whose
  runtime makes goroutines and channels first-class — this primer gets you productive in Go without
  detouring into mastery you don't yet need.
- **Keep-this-if-you-forget-everything**: Go trades expressive power for a small, explicit surface — errors
  are values you check (`if err != nil`), not exceptions you catch, and that plainness is the feature.
- **Big ideas touched**: `abstraction-and-its-cost` — Go deliberately hides little (explicit error values,
  no inheritance, few keywords), so what does leak stays minimal and legible.

## Prerequisites

- **Prior topics**: general programming fluency from Pass 1/2 — especially
  [topic 4 Just Enough Python](./just-enough-python.md) (a first language to contrast) and
  [topic 5 Just Enough Bash](./just-enough-bash.md) (driving a toolchain).
- **Tools & environment**: a macOS/Linux terminal; the **Go toolchain** (`go`), pinned to a current stable
  release; Neovim/VSCode with Go LSP (DD-17).
- **Assumed knowledge**: variables/functions/types in some language (topic 04); running CLI tools + a build
  loop (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep the Go version unpinned in shipped text (file already says "current stable").
  Current stable is **Go 1.26.5** (2026-07-07); Go 1.26 (2026-02-10) enabled the Green Tea GC by default.
  `go run`/`build`/`test`/`mod` subcommands and the `if err != nil` error-value convention are unchanged.
  Re-pull the exact version at authoring time. (go.dev/doc/devel/release)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official go.dev / pkg.go.dev page the pre-authoring `web-researcher` sweep
> fetched and read. Unverifiable-at-source items are flagged `[Needs Verification]`.

- **Version & release cadence** — go.dev/dl/ and go.dev/doc/devel/release: current stable **Go 1.26.5**
  (patch, 2026-07-07) on the Go 1.26 line (2026-02-10). `[Verified]`
- **Design philosophy** — Effective Go (go.dev/doc/effective_go): "Go is an open-source programming language
  that focuses on simplicity, reliability, and efficiency." `[Verified]`
- **`package main` / `func main`** — go.dev/doc/code: "The first statement in a Go source file must be
  `package name`. Executable commands must always use `package main`." Package-name convention (Effective
  Go): "packages are given lower case, single-word names ... no need for underscores or mixedCaps."
  `[Verified]`
- **Zero values, `:=`, `iota`** — the Go Language Specification (go.dev/ref/spec): variables without an
  initialiser are "initialized to their zero value"; `iota` "represents successive untyped integer
  constants ... starting at zero." `[Verified]`
- **Basic types & conversions** — spec: `byte` is an alias for `uint8`, `rune` for `int32`; conversions are
  explicit (`Type(expr)`), no implicit numeric coercion. `[Verified]`
- **Functions** — spec + Effective Go: multiple return values, named result params + naked `return`,
  variadic `...T` and slice unpacking `f(s...)`; canonical `func (file *File) Write(b []byte) (n int, err
error)`. `[Verified]`
- **Control flow & `defer`** — spec: `for` is the ONLY loop construct ("Go has no other loop constructs");
  deferred calls run "immediately before the surrounding function returns, in the reverse order in which
  they were deferred" (LIFO). `[Verified]`
- **Slices/maps/builtins** — spec + pkg.go.dev/builtin: exact signatures `make`, `append`, `len`, `cap`,
  `copy`, `close`, `panic`, `recover`; uninitialised slice/map value is `nil`; array length is part of its
  type. `[Verified]`
- **Structs, methods, receivers** — spec + Effective Go: "value methods can be invoked on pointers and
  values, but pointer methods can only be invoked on pointers." `[Verified]`
- **Pointers** — spec: `PointerType = "*" BaseType`; **"Go does not support pointer arithmetic"**;
  dereferencing a nil pointer panics. `[Verified]`
- **Interfaces / `any`** — spec: satisfaction is implicit/structural (no `implements` keyword); "the
  predeclared type `any` is an alias for the empty interface." `[Verified]`
- **Errors** — pkg.go.dev/errors: `errors.New`, `errors.Is`, `errors.As`, `errors.Unwrap`, `errors.Join`;
  wrapping idiom `fmt.Errorf("... %w ...", err)`. `[Verified]`
- **Generics** — go.dev/doc/tutorial/generics: type params in `[...]` before the arg list, union constraints
  with `|`, `comparable` predeclared constraint for `==`/`!=`/map keys. (Introduced Go 1.18 — the "1.18"
  attribution is well-established but was not re-confirmed against a primary changelog this pass:
  `[Needs Verification]` on the version number only.) `[Verified]` on syntax.
- **`encoding/json`** — pkg.go.dev/encoding/json: `Marshal`/`Unmarshal`; struct-tag `json:"name,omitempty"`
  and `json:"-"` semantics. `[Verified]`
- **`go` tool** — pkg.go.dev/cmd/go: exact usage of `go run`, `go build`, `go test`, `go mod init/tidy`.
  `[Verified]`
- **`testing`** — pkg.go.dev/testing: `func TestXxx(*testing.T)`, files end in `_test.go`, `t.Run` subtests
  "enable ... table-driven ... tests." `[Verified]`
- **Modules** — go.dev/ref/mod: `go.mod` line-oriented directives; go.sum checksums; semantic import
  versioning — "Starting with major version 2, module paths must have a major version suffix like `/v2`."
  `[Verified]`
- **Concurrency preview** — Effective Go: "Prefix a function or method call with the `go` keyword to run the
  call in a new goroutine." Channel semantics + `sync.WaitGroup`/`Mutex` and `context` signatures from
  pkg.go.dev. **Version-drift note**: `sync.WaitGroup.Go(f func())` was added in **Go 1.25** and pkg.go.dev
  now says "Callers should prefer WaitGroup.Go"; this primer teaches the classic, more explicit
  `wg.Add(1); go func(){ defer wg.Done(); ... }()` pattern (still fully valid) and mentions `wg.Go` as the
  newer idiom. `[Verified]` (the "Go 1.25" attribution rests on the method existing in current pkg.go.dev
  plus corroborating posts; `[Needs Verification]` on the exact introducing version against a primary
  changelog). Concurrency DEPTH (select fairness, the memory model, pipelines, worker pools, the race
  detector) is deferred to [`65-csp-style-concurrency`](./csp-style-concurrency.md).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · go-toolchain** — `go run`, `go build`, `go test`, `go mod` are the whole daily loop; the tool
  compiles, runs, tests, and manages dependencies with no external build system.
- **co-02 · package-and-main** — every file starts `package name`; an executable is `package main` with a
  `func main()`; imports are explicit and unused imports are a compile error.
- **co-03 · modules** — `go.mod` declares the module path + dependency versions and `go.sum` pins
  checksums; major version ≥ 2 carries a `/vN` path suffix (semantic import versioning).
- **co-04 · variables-zero-values** — `var x T` / `x := v`; an uninitialised variable takes its type's
  zero value (0, "", false, nil), so there is no "uninitialised garbage".
- **co-05 · constants-iota** — `const` blocks with `iota` generate successive untyped integer constants,
  the idiomatic way to build enum-like sequences.
- **co-06 · basic-types** — `int`/`float64`/`string`/`bool`, `byte` (=uint8) and `rune` (=int32);
  conversions are always explicit (`int64(x)`) — Go never coerces numeric types implicitly.
- **co-07 · functions-multiret** — functions return multiple values (the `(result, error)` shape),
  support named results + naked `return`, and variadic `...T` params.
- **co-08 · control-flow** — `if` (with an optional init statement), `switch` (no fallthrough by
  default), and `for` as the ONLY loop keyword (C-style, while-style, infinite, and range forms).
- **co-09 · defer** — `defer` schedules a call to run at function return in LIFO order; the canonical
  cleanup idiom (`defer f.Close()`) that runs regardless of which return path is taken.
- **co-10 · arrays-slices** — an array's length is part of its type; a slice is a growable view built
  with `make`/`append`, with `len` and `cap` distinct; the zero slice is `nil`.
- **co-11 · maps** — `map[K]V` built with `make`; the comma-ok form `v, ok := m[k]` distinguishes
  "absent" from "zero value"; the zero map is `nil` and reads (not writes) are safe on it.
- **co-12 · pointers** — `&x` takes an address, `*p` dereferences; there is NO pointer arithmetic, and a
  nil-pointer dereference panics.
- **co-13 · structs** — `struct{...}` groups typed fields; struct literals, and embedded (anonymous)
  fields give composition without inheritance.
- **co-14 · methods-receivers** — methods attach to a named type via a receiver; a pointer receiver can
  mutate and is required to; a value receiver copies — the choice is a real semantic decision.
- **co-15 · interfaces** — interface satisfaction is implicit and structural (no `implements` keyword);
  `any` is the empty interface; type assertions and type switches recover the concrete type.
- **co-16 · error-values** — `error` is an ordinary interface; the convention is to return it as the last
  value and check `if err != nil` — errors are values you handle, not exceptions you catch.
- **co-17 · error-wrapping** — `fmt.Errorf("...: %w", err)` wraps an error while preserving the chain;
  `errors.Is`/`errors.As` inspect that chain without fragile string matching.
- **co-18 · struct-tags-json** — `encoding/json` marshals/unmarshals structs; back-tick struct tags
  (`json:"name,omitempty"`) control field names and omission.
- **co-19 · generics** — type parameters in `[...]` with union/`comparable` constraints let one function
  or type work over many concrete types with compile-time checking.
- **co-20 · goroutines-preview** — the `go` keyword starts a function as a concurrent goroutine in the
  same address space; lightweight, multiplexed onto OS threads (depth in topic 65).
- **co-21 · channels-preview** — `chan T` carries typed values between goroutines; unbuffered channels
  synchronise sender and receiver, `close` + range drains, `v, ok := <-c` detects close (depth in 65).
- **co-22 · select-preview** — `select` waits on multiple channel operations, picking a ready case (with
  an optional `default` for non-blocking) — the multiplexer for concurrent Go (depth in topic 65).
- **co-23 · sync-preview** — `sync.WaitGroup` waits for a set of goroutines to finish and `sync.Mutex`
  guards shared state, for the cases where channels are the wrong tool (depth in topic 65).
- **co-24 · testing** — `func TestXxx(t *testing.T)` in a `_test.go` file, run by `go test`; the
  table-driven + `t.Run` subtest pattern is idiomatic Go testing.
- **co-25 · gofmt-idiom** — `gofmt`/`go fmt` imposes one canonical layout so formatting is never
  debated; Effective Go fixes naming (short names, exported = Capitalised) and structure.
- **co-26 · context-basics** — `context.Context` carries cancellation + deadlines across call
  boundaries (`WithCancel`/`WithTimeout`, `ctx.Done()`, `ctx.Err()`) — the standard cancellation preview.

## Worked examples

Colocated under `just-enough-go/learning/code/`; each runnable via the Go toolchain (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · hello-world-run** — a `package main` + `func main()` printing a line — verify `go run .`
  prints it. (co-02, co-01)
- **ex-02 · go-mod-init** — `go mod init example/hello` — verify a `go.mod` with the module path appears. (co-03, co-01)
- **ex-03 · go-build-binary** — `go build -o hello` — verify the binary exists and runs standalone. (co-01)
- **ex-04 · go-run-vs-build** — contrast `go run .` (compile+run, no artefact) with `go build` — verify
  only `build` leaves a binary. (co-01)
- **ex-05 · package-and-import** — split code into a second package and import it — verify an unused
  import is a compile error. (co-02)
- **ex-06 · var-declaration** — declare vars with `var name type = value` — verify the printed values. (co-04)
- **ex-07 · short-var-decl** — use `:=` inside a function — verify it infers the type. (co-04)
- **ex-08 · zero-values** — declare `int`/`string`/`bool`/pointer without init — verify they print
  `0`/``/`false`/`<nil>`. (co-04)
- **ex-09 · const-block** — a `const` block of named constants — verify they are immutable (assignment
  fails to compile). (co-05)
- **ex-10 · iota-enum** — build an enum with `iota` — verify successive values 0,1,2. (co-05)
- **ex-11 · int-float-types** — mix `int` and `float64` arithmetic — verify a direct mix fails and
  conversion fixes it. (co-06)
- **ex-12 · string-rune-byte** — index a string as bytes and range it as runes — verify a multi-byte
  character spans multiple bytes but one rune. (co-06)
- **ex-13 · type-conversion** — convert `int` → `int64` → `float64` explicitly — verify no implicit
  coercion is allowed. (co-06)
- **ex-14 · bool-and-comparison** — evaluate comparison + boolean operators — verify short-circuit
  behaviour of `&&`/`||`. (co-06)
- **ex-15 · func-basic** — a function with typed params + one return — verify the returned value. (co-07)
- **ex-16 · func-multiple-return** — return `(int, error)` — verify both values are received. (co-07)
- **ex-17 · named-return-values** — use named results + a naked `return` — verify it returns the current
  named values. (co-07)
- **ex-18 · variadic-func** — a `sum(nums ...int)` — verify both `sum(1,2,3)` and `sum(s...)` work. (co-07)
- **ex-19 · if-with-init** — `if v, err := f(); err != nil { ... }` — verify `v` is scoped to the if. (co-08)
- **ex-20 · for-c-style** — a classic `for i := 0; i < n; i++` — verify the loop count. (co-08)
- **ex-21 · for-while-style** — `for cond { }` as a while loop — verify it exits when cond is false. (co-08)
- **ex-22 · for-range** — range over a slice and a map — verify index/value (slice) and key/value (map). (co-08)
- **ex-23 · switch-statement** — a `switch` on a value with cases — verify no implicit fallthrough. (co-08)
- **ex-24 · switch-no-condition** — a conditionless `switch { case x > 0: }` as an if-else chain — verify
  the matching branch runs. (co-08)
- **ex-25 · defer-basic** — `defer` a cleanup call — verify it runs at function return. (co-09)
- **ex-26 · defer-lifo-order** — three `defer`s — verify they run in reverse (LIFO) order. (co-09)

### Intermediate

- **ex-27 · array-vs-slice** — a fixed `[3]int` array vs a `[]int` slice — verify the array length is part
  of its type. (co-10)
- **ex-28 · slice-append** — grow a slice with `append` — verify new elements and returned slice. (co-10)
- **ex-29 · slice-len-cap** — inspect `len` vs `cap` as a slice grows — verify cap jumps on reallocation. (co-10)
- **ex-30 · make-slice-capacity** — `make([]int, 0, 10)` — verify len 0, cap 10. (co-10)
- **ex-31 · slice-shares-backing** — a re-slice sharing the backing array — verify a write through one
  view is visible in the other. (co-10)
- **ex-32 · map-basic** — build and read a `map[string]int` — verify inserted values. (co-11)
- **ex-33 · map-comma-ok** — `v, ok := m[k]` — verify `ok` distinguishes absent from zero. (co-11)
- **ex-34 · map-delete-iterate** — `delete` a key then range the map — verify the key is gone. (co-11)
- **ex-35 · pointer-basics** — take `&x`, read `*p` — verify the pointer sees the same value. (co-12)
- **ex-36 · pointer-modify** — pass a pointer to a function that mutates — verify the caller's value
  changes. (co-12)
- **ex-37 · nil-pointer-panic** — dereference a nil pointer under `recover` — verify it panics. (co-12)
- **ex-38 · struct-definition** — define a struct with typed fields — verify field access. (co-13)
- **ex-39 · struct-literal** — build with a keyed literal `T{A: 1}` — verify unset fields take zero
  values. (co-13)
- **ex-40 · embedded-struct** — embed one struct in another — verify promoted field access. (co-13)
- **ex-41 · method-value-receiver** — a value-receiver method — verify it does NOT mutate the original. (co-14)
- **ex-42 · method-pointer-receiver** — a pointer-receiver method — verify it mutates the original. (co-14)
- **ex-43 · receiver-choice** — call both on a value and a pointer — verify a pointer method needs an
  addressable value. (co-14)
- **ex-44 · interface-implicit** — a type satisfies an interface with no `implements` keyword — verify it
  is accepted where the interface is required. (co-15)
- **ex-45 · interface-two-impls** — two types satisfying one interface — verify a slice of the interface
  holds both. (co-15)
- **ex-46 · empty-interface-any** — store mixed types in `[]any` — verify each element round-trips. (co-15)
- **ex-47 · type-assertion** — `v, ok := x.(T)` — verify a wrong assertion sets ok false, not panic. (co-15)
- **ex-48 · type-switch** — a `switch v := x.(type)` — verify each concrete branch. (co-15)
- **ex-49 · error-value-check** — a function returning `error`, checked with `if err != nil` — verify the
  error path. (co-16)
- **ex-50 · errors-new** — build an error with `errors.New` — verify the message. (co-16)
- **ex-51 · custom-error-type** — a struct implementing `error` via an `Error()` method — verify it
  satisfies the interface. (co-16)
- **ex-52 · error-wrap-w** — wrap with `fmt.Errorf("...: %w", err)` — verify `errors.Unwrap` returns the
  inner error. (co-17)
- **ex-53 · errors-is-as** — `errors.Is` a sentinel and `errors.As` a typed error — verify both match
  through the wrap. (co-17)
- **ex-54 · struct-tags-json** — annotate fields with `json:"..."` tags — verify the marshalled key
  names. (co-18)

### Advanced

- **ex-55 · json-marshal-unmarshal** — `json.Marshal` then `json.Unmarshal` a struct — verify a
  round-trip is equal. (co-18)
- **ex-56 · json-omitempty** — a field with `omitempty` — verify it disappears when zero. (co-18)
- **ex-57 · generic-function** — a generic `Map[T, U any]` — verify it works on `int` and `string`
  slices. (co-19)
- **ex-58 · generic-constraint** — a union constraint `int | float64` — verify a `string` arg fails to
  compile. (co-19)
- **ex-59 · comparable-constraint** — a generic `Contains[T comparable]` — verify it uses `==`. (co-19)
- **ex-60 · goroutine-preview** — start a function with `go` and wait — verify it ran concurrently. (co-20)
- **ex-61 · goroutine-anonymous** — `go func(){ ... }()` — verify the closure runs in a goroutine. (co-20)
- **ex-62 · unbuffered-channel** — send/receive on an unbuffered `chan int` — verify sender blocks until
  received. (co-21)
- **ex-63 · buffered-channel** — a `make(chan int, 2)` — verify two sends do not block. (co-21)
- **ex-64 · channel-handoff** — hand a value goroutine→main over a channel — verify the value crosses. (co-21)
- **ex-65 · channel-close-range** — close a channel and `for v := range c` — verify the loop ends on
  close. (co-21)
- **ex-66 · channel-comma-ok** — `v, ok := <-c` on a closed channel — verify ok is false. (co-21)
- **ex-67 · select-basic** — a `select` over two ready channels — verify one case runs. (co-22)
- **ex-68 · select-default-nonblock** — a `select` with `default` on an empty channel — verify default
  runs (non-blocking). (co-22)
- **ex-69 · select-timeout** — `select` with a `time.After` case — verify the timeout fires. (co-22)
- **ex-70 · waitgroup** — coordinate N goroutines with `sync.WaitGroup` (classic `Add`/`Done`/`Wait`;
  mention `wg.Go` as the Go 1.25 idiom) — verify all finish before `Wait` returns. (co-23)
- **ex-71 · mutex** — guard a shared counter with `sync.Mutex` — verify no lost updates (clean under
  `go test -race`). (co-23)
- **ex-72 · test-basic** — a `func TestXxx(t *testing.T)` in `_test.go` — verify `go test` passes. (co-24)
- **ex-73 · table-driven-test** — a slice of cases looped in one test — verify each case asserts. (co-24)
- **ex-74 · subtests-run** — `t.Run(name, ...)` subtests — verify each named subtest reports separately. (co-24)
- **ex-75 · gofmt-format** — run `gofmt` on a misformatted file — verify it rewrites to canonical layout. (co-25)
- **ex-76 · effective-go-naming** — exported vs unexported identifiers (Capitalised = exported) — verify
  an unexported name is not visible from another package. (co-25)
- **ex-77 · context-cancel** — `context.WithCancel`; cancel and check `ctx.Done()` — verify `ctx.Err()`
  returns `context.Canceled`. (co-26)
- **ex-78 · context-timeout** — `context.WithTimeout`; let it elapse — verify `ctx.Err()` returns
  `context.DeadlineExceeded`. (co-26)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small idiomatic Go CLI that exercises the primer's surface — structs + interfaces,
  the error-value convention, packages/modules, and a single goroutine/channel hand-off — with a `go test`,
  proving readiness for CSP-style concurrency.
- **Concepts exercised**: [ ] modules + package layout (co-03, co-02) [ ] structs + methods + an interface
  (co-13, co-14, co-15) [ ] error-value handling (co-16, co-17) [ ] a goroutine + channel hand-off (co-20,
  co-21) [ ] a `go test` (co-24).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a CLI with a struct + an interface + explicit error handling. Verify
     `go build` + `go run` work and errors surface via the error value.
  2. Add a single goroutine + channel hand-off. Verify the value crosses the channel and the program exits
     cleanly.
  3. `main_test.go` — a `go test`. Verify the test passes.
- **Acceptance criteria**: the CLI builds and runs; errors are handled via the error value; the
  goroutine/channel hand-off works; `go test` passes.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **The Go Programming Language** — Alan A. A. Donovan, Brian W. Kernighan (2015). The definitive, most widely recommended book on Go, co-authored by a legendary computer scientist.
- **Learning Go** — Jon Bodner (2nd ed., 2024). Widely recommended modern, idiomatic guide to Go covering generics and current tooling.

**Papers & articles**

- **Effective Go** — The Go Team (ongoing). The official guide to writing idiomatic Go, maintained directly by the language's creators. <https://go.dev/doc/effective_go>
- **The Go Memory Model** — The Go Team (ongoing). Official specification of Go's concurrency and memory-ordering guarantees, essential for correct concurrent code. <https://go.dev/ref/mem>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Concurrency, JVM & languages — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Concurrency & language breadth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 3 · Concurrency & language breadth.

> _Content originated in the now-closed FS-SE plan (topic 64); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
