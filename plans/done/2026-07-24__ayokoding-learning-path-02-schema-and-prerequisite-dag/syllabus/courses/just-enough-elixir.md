# Just Enough Elixir (Primer, Elixir)

**Course ID**: `just-enough-elixir` · **Format**: Primer · **Language**: Elixir.

**Short summary**: Elixir syntax, pattern matching, functional idioms

**Scope note**: **just enough Elixir** to be productive in
[`67-actor-model-concurrency`](./actor-model-concurrency.md). Immutable data, pattern matching, the pipe
operator, functions/modules, recursion, and a `spawn`/`send`/`receive` _preview_ only (process depth
belongs to topic 67).

## Why this exists · the big idea

- **The problem before the solution**: the actor model in topic 67 assumes immutable data and lightweight
  processes, which map poorly onto imperative habits — this primer rewires you to think in immutable
  transforms and message passing before the depth arrives.
- **Keep-this-if-you-forget-everything**: with no mutable state, a program is just data flowing through
  pure transforms (`|>`) — nothing to alias, nothing to lock.
- **Big ideas touched**: `taming-state` — immutability removes shared mutable state entirely, so the
  concurrency that follows is safe by construction rather than by careful locking.

## Prerequisites

- **Prior topics**: [topic 23 Functional Programming](./functional-programming.md) (immutability,
  pure functions, recursion over loops) and [topic 4 Just Enough Python](./just-enough-python.md) (a
  contrasting first language).
- **Tools & environment**: a macOS/Linux terminal; **Elixir** + `mix` + `iex`, pinned to a current stable
  release (note the Erlang/Elixir license posture, DD-15); Neovim/VSCode (DD-17).
- **Assumed knowledge**: immutability + recursion (topic 23); running a REPL + a CLI build tool
  (topics 04/05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep the version unpinned in shipped text. Current stable is **Elixir v1.20**
  (1.20.2 with OTP 29 released 2026-06-23; requires OTP 27+). `spawn`/`send`/`receive` preview syntax and
  `mix`/`iex` usage are unchanged. Re-pull the exact version at authoring time.
- 2026-07-12 — verified: **both Erlang/OTP (since OTP 18.0) and Elixir are Apache License 2.0** — permissive
  open source, not source-available (DD-21 clean). (github.com/erlang/otp/blob/master/LICENSE.txt)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official elixir-lang.org / elixir.hexdocs.pm page the pre-authoring
> `web-researcher` sweep fetched and read. `[Needs Verification]` marks phrasing not found verbatim at
> source (behaviour still verified) or currency risk.

- **Version** — elixir-lang.org/install.html + github.com/elixir-lang/elixir/releases: current stable
  **Elixir v1.20.2** (2026-06-23); "Elixir v1.20 requires Erlang 27.0 or later" (compatible with OTP
  27/28/29). Fast release cadence — re-pull at authoring time. `[Verified]`
- **Immutability** — hexdocs `lists-and-tuples.html`: "You can freely pass the data around with the
  guarantee no one will mutate it in memory — only transform it"; `recursion.html`: "data structures in
  Elixir are immutable. For this reason, functional languages rely on recursion." Rebinding (`x = 1` then
  `x = 2`) re-points the name; the underlying value is never mutated. (Cite these pages, NOT
  `basic-types.html`, which does not state immutability.) `[Verified]`
- **Basic types** — hexdocs `basic-types.html`: integers, floats ("a dot followed by at least one digit"),
  booleans (`true`/`false`), atoms ("a constant whose value is its own name"), strings ("delimited by
  double quotes ... encoded in UTF-8 ... represented internally by ... binaries"); `is_integer/1`,
  `is_float/1`, `is_atom/1`, `is_binary/1`, etc. Tuples "store elements contiguously" (fast index/size,
  costly update); lists are cheap to prepend, costly to append. `[Verified]`
- **Pattern matching** — hexdocs `pattern-matching.html`: "the `=` operator ... is actually called the
  match operator"; `{a, b, c} = {:hello, "world", 42}`; `[a, b, c] = [1, 2, 3]`; head/tail `[head | tail]`
  and `[0 | list]` prepend; wildcard `_` ("Trying to read from it gives a compile error"); pin `^` matches
  "against a variable's existing value rather than rebinding". The literal phrase "not assignment" is a
  standard paraphrase of the demonstrated behaviour, not a verbatim doc quote: `[Needs Verification]` on
  wording, `[Verified]` on mechanics.
- **Pipe operator** — hexdocs `enumerable-and-streams.html`: `|>` "takes the output from the expression on
  its left side and passes it as the first argument to the function call on its right side"; example
  `1..100_000 |> Enum.map(&(&1 * 3)) |> Enum.filter(odd?) |> Enum.sum()`. (Doc filename is singular
  `enumerable-and-streams.html`.) `[Verified]`
- **Modules & functions** — hexdocs `modules-and-functions.html`: `defmodule` macro; `def/2` (public) vs
  `defp/2` (private); "Functions in Elixir are identified by both their name and their arity"; default args
  via `\\`; `anonymous-functions.html`: `fn ... end`, called with a dot `add.(1, 2)`. `[Verified]`
- **Guards** — hexdocs `patterns-and-guards.html`: `when` clauses; allowed guard exprs (comparison ops,
  strictly-boolean `and`/`or`/`not`, arithmetic, type-check `is_*`, `abs/1`/`hd/1`/`map_size/1`, `in`,
  `Bitwise`, custom `defguard`); "errors in guards do not leak but simply make the guard fail". `[Verified]`
- **Recursion** — hexdocs `recursion.html`: "Elixir does not provide loop constructs. Instead we leverage
  recursion and high-level functions for working with collections"; accumulator pattern; "Recursion and
  tail call optimization ... commonly used to create loops"; and idiomatically `Enum.reduce`/`Enum.map`
  replace hand-rolled recursion. `[Verified]`
- **Processes preview** — hexdocs `processes.html`: `spawn/1` ("takes a function which it will execute in
  another process"), `self/0` ("retrieve the PID of the current process"), `send/2` ("does not block ...
  puts the message in the recipient's mailbox"), `receive/1` ("goes through the current process mailbox
  searching for a message that matches any of the given patterns ... waits until a matching message
  arrives"); "Processes are isolated ... communicate via message passing" and are "extremely lightweight".
  GenServer/Supervisor/OTP are explicitly OUT of scope for this primer (they live in
  [`67-actor-model-concurrency`](./actor-model-concurrency.md)). `[Verified]`
- **`mix`/`iex`/`.ex` vs `.exs`** — hexdocs `introduction.html`: three executables `iex`, `elixir`,
  `elixirc`; run a script with `elixir file.exs`. `modules-and-functions.html` (Scripting section):
  "`.ex` files are meant to be compiled" while "`.exs` files are used for scripting". `mix new kv`
  scaffolds `mix.exs` + `lib/` + `test/`. `[Verified]`
- **Enum + String combined pipeline** — the doc's own pipe example chains only `Enum`; a combined
  `String.split |> Enum.map` pipeline is idiomatic and mechanically valid but is ORIGINAL curriculum code
  to author and test, not a doc quote: `[Needs Verification]` as a citation (write-and-run instead).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · iex-repl** — `iex` is the interactive shell; the fastest loop for exploring values, functions,
  and pattern matches before writing a file.
- **co-02 · mix-project** — `mix new` scaffolds a project (`mix.exs`, `lib/`, `test/`); `mix run` /
  `mix test` drive it — the standard build tool.
- **co-03 · ex-vs-exs** — `.ex` files are compiled, `.exs` are scripts run directly (`elixir foo.exs`);
  the language treats them identically, the difference is intent.
- **co-04 · immutability** — data is never mutated in place; you transform it into new values, and a
  variable name can be rebound without ever changing the underlying data.
- **co-05 · basic-types** — integers, floats, booleans, atoms, strings (UTF-8 binaries), lists, tuples,
  and keyword lists; `is_*` predicates classify them.
- **co-06 · atoms** — an atom is a constant whose value is its own name (`:ok`, `:error`); the building
  block of tagged tuples and status flags.
- **co-07 · match-operator** — `=` is the MATCH operator, not assignment: it asserts both sides match,
  binding variables on the left; a mismatch raises `MatchError`.
- **co-08 · pattern-matching-destructure** — matching destructures tuples and lists in one step
  (`{a, b} = {1, 2}`, `[a, b, c] = [1, 2, 3]`), the core control-flow tool.
- **co-09 · list-head-tail** — `[head | tail]` matches or builds a list from its first element and the
  rest; the recursion-friendly shape of a list.
- **co-10 · pin-operator** — `^x` matches against a variable's EXISTING value instead of rebinding it,
  turning a pattern into an equality check.
- **co-11 · wildcard-underscore** — `_` (or `_name`) matches anything and discards it; reading from `_`
  is a compile error.
- **co-12 · pipe-operator** — `|>` passes the value on its left as the FIRST argument of the call on its
  right, so nested calls read as a top-to-bottom data pipeline.
- **co-13 · modules-def-defp** — `defmodule` groups functions; `def` defines a public function, `defp` a
  private one callable only within the module.
- **co-14 · anonymous-functions** — `fn args -> body end` builds a first-class function, called with a dot
  (`add.(1, 2)`); the `&` capture operator is the shorthand.
- **co-15 · arity** — a function is identified by name AND arity (`sum/2`); different arities are different
  functions even with the same name.
- **co-16 · default-args** — `\\` gives a parameter a default value, collapsing several arities into one
  definition.
- **co-17 · guards** — `when` clauses add conditions to a clause using a restricted set of guard-safe
  expressions; an error in a guard just makes it fail rather than raising.
- **co-18 · multiple-clauses** — a function can have several clauses distinguished by pattern + guard;
  Elixir tries them top-to-bottom and runs the first that matches — dispatch without `if`.
- **co-19 · recursion** — with no loops, iteration is recursion: a base clause plus a step clause carrying
  an accumulator replaces every `for`/`while`.
- **co-20 · tail-call** — a tail-recursive call (the recursive call is the last expression) runs in
  constant stack space, the idiom for long loops.
- **co-21 · enum-higher-order** — `Enum.map`/`filter`/`reduce` and friends express most iteration
  declaratively, replacing hand-rolled recursion for collections.
- **co-22 · string-processing** — `String.*` functions (split, upcase, trim) pipe naturally with `Enum`
  to transform text.
- **co-23 · process-spawn-preview** — `spawn/1` starts a function in a new, isolated, lightweight process
  and returns its PID (depth in [`67-actor-model-concurrency`](./actor-model-concurrency.md)).
- **co-24 · send-receive-preview** — `send/2` drops a message in a process's mailbox (non-blocking) and
  `receive do ... end` pattern-matches the next matching message; the core of message passing.
- **co-25 · self-and-mailbox** — `self/0` is the current process's PID; each process has a FIFO mailbox
  that `receive` drains by pattern — the reply address for a round-trip.
- **co-26 · process-isolation** — processes share nothing and communicate only by messages, so a crash in
  one cannot corrupt another's state — the safety property the actor model builds on.

## Worked examples

Colocated under `just-enough-elixir/learning/code/`; each runnable via `iex`/`mix` (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · iex-start-eval** — start `iex`, evaluate `1 + 2` and a string — verify the results. (co-01)
- **ex-02 · iex-helpers** — use `h Enum.map` / `i "abc"` in `iex` — verify docs/type info print. (co-01)
- **ex-03 · mix-new-project** — `mix new greeter` — verify `mix.exs` + `lib/greeter.ex` appear. (co-02)
- **ex-04 · mix-run-script** — `mix run -e 'IO.puts("hi")'` — verify it prints. (co-02)
- **ex-05 · ex-vs-exs** — run the same code as compiled `.ex` and script `.exs` — verify both work, note
  the intent difference. (co-03)
- **ex-06 · immutable-rebind** — bind `x = 1` then `x = 2` in `iex` — verify rebinding works and the old
  value is untouched. (co-04)
- **ex-07 · immutable-list-transform** — `List.insert_at/3` returns a NEW list — verify the original is
  unchanged. (co-04)
- **ex-08 · integer-float** — evaluate integer vs float arithmetic and `div`/`rem` — verify the types. (co-05)
- **ex-09 · boolean-and-atom** — `true`, `:ok`, `is_boolean/1`, `is_atom/1` — verify a boolean is an
  atom. (co-06)
- **ex-10 · string-binary** — a UTF-8 string, `String.length/1` vs `byte_size/1` — verify a multi-byte
  char differs. (co-05)
- **ex-11 · list-literal** — build a list, `hd/1` / `tl/1` — verify head and tail. (co-05)
- **ex-12 · tuple-literal** — a tuple, `elem/2`, `tuple_size/1` — verify indexed access. (co-05)
- **ex-13 · is-type-checks** — `is_integer`/`is_list`/`is_tuple`/`is_binary` on samples — verify each. (co-05)
- **ex-14 · atom-as-tag** — a `{:ok, value}` / `{:error, reason}` tagged tuple — verify pattern-matching
  the tag. (co-06)
- **ex-15 · match-operator-basic** — `x = 1` then `1 = x` — verify the second succeeds (match, not
  assignment). (co-07)
- **ex-16 · match-mismatch-error** — `2 = x` when `x` is 1 — verify a `MatchError`. (co-07)
- **ex-17 · destructure-tuple** — `{a, b, c} = {:ok, "v", 42}` — verify the bindings. (co-08)
- **ex-18 · destructure-list** — `[a, b, c] = [1, 2, 3]` — verify the bindings. (co-08)
- **ex-19 · head-tail-match** — `[head | tail] = [1, 2, 3]` — verify head=1, tail=[2,3]. (co-09)
- **ex-20 · prepend-list** — `[0 | list]` — verify it prepends. (co-09)
- **ex-21 · pin-operator** — `^x = 2` when `x` is 1 — verify it raises (matches existing value). (co-10)
- **ex-22 · wildcard-underscore** — `{_, b} = {1, 2}` — verify `b` binds and `_` discards. (co-11)
- **ex-23 · pipe-single** — `"hello" |> String.upcase()` — verify the output. (co-12)
- **ex-24 · pipe-chain** — `[1,2,3] |> Enum.map(&(&1*2)) |> Enum.sum()` — verify the result. (co-12)
- **ex-25 · pipe-first-arg** — show `|>` inserts the left value as the FIRST argument — verify vs the
  explicit call. (co-12)
- **ex-26 · pipe-vs-nested** — rewrite a nested call as a pipeline — verify identical result, better
  readability. (co-12)

### Intermediate

- **ex-27 · defmodule-def** — a module with a public `def` — verify calling it from `iex`. (co-13)
- **ex-28 · private-defp** — a `defp` helper — verify it is NOT callable from outside the module. (co-13)
- **ex-29 · call-cross-module** — one module calling another's public function — verify it resolves. (co-13)
- **ex-30 · anonymous-fn** — `add = fn a, b -> a + b end` — verify `add.(1, 2)`. (co-14)
- **ex-31 · anonymous-fn-dot-call** — contrast `add.(…)` with a named `add(…)` — verify the dot is
  required for the variable form. (co-14)
- **ex-32 · capture-operator** — `&(&1 * 2)` and `&String.upcase/1` — verify they equal the `fn` form. (co-14)
- **ex-33 · arity-notation** — reference `sum/2` — verify `sum/2` and `sum/3` are distinct functions. (co-15)
- **ex-34 · same-name-diff-arity** — define `greet/1` and `greet/2` — verify both dispatch by arity. (co-15)
- **ex-35 · default-args** — `def greet(name, greeting \\ "Hi")` — verify both call forms work. (co-16)
- **ex-36 · guard-when** — `def abs_(n) when n < 0` — verify the negative branch. (co-17)
- **ex-37 · guard-allowed-exprs** — a guard using `is_integer/1` + comparison — verify it filters. (co-17)
- **ex-38 · guard-fail-skips** — a guard that errors — verify it just fails the clause (no raise). (co-17)
- **ex-39 · function-clauses-pattern** — multiple clauses matching `{:ok, v}` vs `{:error, r}` — verify
  each routes correctly. (co-18)
- **ex-40 · clause-order-matters** — a general clause before a specific one — verify the specific never
  fires, then reorder. (co-18)
- **ex-41 · recursion-sum-list** — a recursive `sum_list/1` — verify it totals a list. (co-19)
- **ex-42 · recursion-accumulator** — `sum_list/2` with an accumulator — verify the same result. (co-19)
- **ex-43 · recursion-map-manual** — hand-roll a `map/2` with recursion — verify vs `Enum.map`. (co-19)
- **ex-44 · recursion-base-case** — a factorial with an explicit base clause — verify `0! = 1`. (co-19)
- **ex-45 · tail-call-recursion** — a tail-recursive `length/1` on a large list — verify no stack blowup. (co-20)
- **ex-46 · tail-vs-body-recursion** — contrast body- and tail-recursive sums — verify identical output. (co-20)
- **ex-47 · enum-map** — `Enum.map(list, fn x -> x*x end)` — verify the squared list. (co-21)
- **ex-48 · enum-filter** — `Enum.filter(list, &(&1 > 0))` — verify it drops non-positives. (co-21)
- **ex-49 · enum-reduce** — `Enum.reduce(list, 0, &+/2)` — verify the sum. (co-21)
- **ex-50 · enum-vs-recursion** — solve one task with `Enum` and with recursion — verify same result,
  note when each fits. (co-21)
- **ex-51 · string-split** — `String.split("a,b,c", ",")` — verify the parts. (co-22)
- **ex-52 · string-upcase-trim** — `"  hi  " |> String.trim() |> String.upcase()` — verify `"HI"`. (co-22)
- **ex-53 · pipe-enum-string** — `"a b c" |> String.split() |> Enum.map(&String.upcase/1)` — verify the
  transformed list. (co-22)
- **ex-54 · keyword-list-opts** — pass `[color: :red]` as trailing options — verify keyword access. (co-05)

### Advanced

- **ex-55 · spawn-basic** — `spawn(fn -> IO.puts("hi") end)` — verify the process runs. (co-23)
- **ex-56 · spawn-returns-pid** — capture the PID and `Process.alive?/1` — verify it returns a PID. (co-23)
- **ex-57 · self-pid** — `self()` in `iex` — verify it returns the current PID. (co-25)
- **ex-58 · send-message** — `send(pid, {:hello, self()})` — verify the message is delivered. (co-24)
- **ex-59 · receive-block** — a `receive do {:hello, _} -> ... end` — verify it matches. (co-24)
- **ex-60 · send-receive-roundtrip** — spawn a process that replies to the sender — verify the round-trip. (co-24)
- **ex-61 · receive-pattern-match** — a `receive` with multiple patterns — verify each message routes. (co-24)
- **ex-62 · mailbox-fifo** — send two messages, receive both — verify FIFO order. (co-25)
- **ex-63 · process-isolation** — crash a spawned process — verify the parent is unaffected. (co-26)
- **ex-64 · process-lightweight** — spawn 10_000 processes — verify they start cheaply. (co-26)
- **ex-65 · ping-pong-processes** — two processes exchanging messages — verify the ping/pong sequence. (co-23, co-24)
- **ex-66 · spawn-closure-capture** — a spawned closure capturing a local value — verify it sees the
  captured value. (co-23)
- **ex-67 · receive-timeout** — `receive do ... after 100 -> ... end` — verify the timeout branch fires. (co-24)
- **ex-68 · stateful-loop-process** — a recursive `receive` loop holding state — verify state updates
  across messages. (co-23, co-19)
- **ex-69 · pattern-match-messages** — match `{:add, n}` / `{:get, from}` messages — verify the handler
  dispatch. (co-24, co-08)
- **ex-70 · pipe-transform-pipeline** — a multi-stage `|>` over `Enum` — verify the final value. (co-12, co-21)
- **ex-71 · immutable-transform-chain** — transform a struct/map through pipes — verify the original is
  unchanged. (co-04, co-12)
- **ex-72 · fold-with-pattern** — a recursive fold using head/tail pattern matching — verify the
  aggregate. (co-19, co-08)
- **ex-73 · map-reduce-pipeline** — `list |> Enum.map(...) |> Enum.reduce(...)` — verify the reduction. (co-21, co-12)
- **ex-74 · string-word-count** — split text, count words with `Enum.reduce` — verify the counts. (co-22, co-21)
- **ex-75 · spawn-worker-compute** — spawn a worker that computes and sends back a result — verify the
  reply. (co-23, co-24)
- **ex-76 · process-vs-shared-state** — show two processes cannot share a variable, only messages — verify
  isolation. (co-26, co-04)
- **ex-77 · mix-module-end-to-end** — a `mix` module with a public API + a test — verify `mix test`
  passes. (co-02, co-13)
- **ex-78 · capstone-preview-roundtrip** — a module: `|>` pipeline + recursion + a `spawn`/`send`/`receive`
  hand-off — verify the message round-trips and the pipeline result is correct. (co-23, co-24, co-19)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small `mix` program that exercises the primer's surface — immutable data, pattern
  matching, the pipe operator, a module with recursion, and a single `spawn`/`send`/`receive` message
  hand-off — proving readiness for actor-model concurrency.
- **Concepts exercised**: [ ] a `mix` project (co-02) [ ] pattern matching (co-08, co-09) [ ] the pipe
  operator (co-12) [ ] recursion — no mutable loop (co-19) [ ] a `spawn`/`send`/`receive` hand-off (co-23,
  co-24, co-25).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a module transforming data through a `|>` pipeline with pattern
     matching. Verify the pipeline produces the expected value.
  2. Add a recursive function (e.g. a fold/aggregate) with no mutable loop. Verify it returns the correct
     result on a known input.
  3. Add a `spawn`ed process with `send`/`receive`. Verify the message round-trips and the program exits
     cleanly.
- **Acceptance criteria**: the pipeline + pattern matching work; the recursion is correct; the process
  hand-off round-trips.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Programming Elixir ≥ 1.6** — Dave Thomas (2018, Pragmatic Bookshelf). The most widely recommended Elixir primer, by a Pragmatic Programmer co-founder.
- **Elixir in Action**, 3rd ed. — Saša Jurić (2024, Manning). The canonical intermediate/advanced Elixir and OTP text.

**Papers & articles**

- **Getting Started** — Elixir core team, official guide (elixir-lang.org). The authoritative free primer maintained by the language's creators. <https://elixir-lang.org/getting-started/introduction.html>
- **Elixir documentation — Introduction** — official (hexdocs.pm). The canonical language and standard-library reference. <https://hexdocs.pm/elixir/introduction.html>
- **Erlang/Elixir Syntax: A Crash Course** — official (elixir-lang.org). Bridges Elixir syntax to the underlying Erlang/BEAM concepts. <https://elixir-lang.org/crash-course.html>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Concurrency, JVM & languages — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Concurrency & language breadth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 3 · Concurrency & language breadth.

> _Content originated in the now-closed FS-SE plan (topic 66); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
