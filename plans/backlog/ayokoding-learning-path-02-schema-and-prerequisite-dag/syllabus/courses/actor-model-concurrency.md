# Actor-Model Concurrency (By Example, Elixir)

**Course ID**: `actor-model-concurrency` · **Format**: By Example · **Language**: Elixir.

**Short summary**: Actors, supervision trees, fault-tolerant concurrency

**Scope note**: the actor concurrency model on the BEAM — processes, message passing, mailboxes,
`GenServer` for stateful processes, supervision trees + "let it crash", OTP applications — and the explicit
contrast with CSP ([`65-csp-style-concurrency`](./csp-style-concurrency.md)). License-aware (DD-15).

## Why this exists · the big idea

- **The problem before the solution**: one unhandled error can corrupt shared state and take down a whole
  system — the actor model isolates state inside shared-nothing processes and supervises them so a failure
  is contained, not catastrophic.
- **Keep-this-if-you-forget-everything**: "let it crash" — don't defensively guard every process; isolate
  state per actor and let a supervisor restart a failed one back to a known-good state.
- **Big ideas touched**: `taming-state` — each actor owns its state privately, reachable only by message,
  so there is nothing to share and nothing to corrupt; `determinism-vs-emergence` — system reliability
  emerges from supervision trees and restart strategies, not from any single process being perfect.

## Prerequisites

- **Prior topics**: [topic 66 Just Enough Elixir](./just-enough-elixir.md) (the language + a process
  preview), [topic 65 CSP-Style Concurrency](./csp-style-concurrency.md) (the model to contrast), and
  [topic 24 Concurrency & Parallelism](./concurrency-and-parallelism.md).
- **Tools & environment**: a macOS/Linux terminal; **Elixir/OTP** + `mix` + `iex`, pinned to a current
  stable release; Neovim/VSCode (DD-17).
- **Assumed knowledge**: Elixir syntax + a `spawn`/`send`/`receive` preview (topic 66); channels/CSP for the
  contrast (topic 65).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: `GenServer`/supervisor APIs and OTP application structure have no breaking changes;
  current with Elixir 1.20 / OTP 27-29.
- 2026-07-12 — verified: **Akka is on BSL 1.1** (source-available; production use needs a Lightbend
  commercial license). **Apache Pekko** — the ASF community fork of Akka 2.6.x — is **Apache-2.0** and is
  the current JVM open-source option (DD-21 clean). Nuance: BSL's rolling 3-year Change Date converts each
  _specific_ Akka release to Apache-2.0 eventually, but all current/new Akka releases stay BSL going
  forward, so "Akka moved to BSL" is the correct steady-state framing. (akka.io/bsl-license-faq / github.com/apache/pekko)

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official elixir.hexdocs.pm / erlang.org page the pre-authoring
> `web-researcher` sweep fetched and read (hexdocs `hexdocs.pm/elixir/*` 301-redirects to
> `elixir.hexdocs.pm/*`). `[Needs Verification]` marks items corroborated only by secondary consensus.

- **Version** — elixir-lang.org/install.html + GitHub releases: **Elixir v1.20.2** (2026-06-23), requires
  OTP 27+ (compatible OTP 27/28/29). `[Verified]`
- **Processes** — hexdocs `processes.html`: `spawn/1` "takes a function which it will execute in another
  process"; `self/0` retrieves the current PID; `send/2` "does not block ... puts the message in the
  recipient's mailbox"; `receive/1` "goes through the current process mailbox searching for a message that
  matches any of the given patterns ... waits until a matching message arrives"; "Processes are isolated ...
  communicate via message passing" and are "extremely lightweight". `[Verified]`
- **Links vs monitors** — hexdocs `Process.html`: `spawn_link` establishes a bidirectional link (a crash
  propagates an exit signal); `Process.monitor/1` delivers a one-way `{:DOWN, ref, :process, object,
reason}` message. "Links are bidirectional" is verbatim; the "monitors are unidirectional" wording is
  inferred from the one-way `:DOWN` semantics: `[Needs Verification]` on wording, `[Verified]` on behaviour.
- **GenServer** — hexdocs `GenServer.html` (verbatim callback return shapes): `init/1` →
  `{:ok, state} | {:ok, state, timeout | :hibernate | {:continue, arg}} | :ignore | {:stop, reason}`;
  `handle_call/3` → `{:reply, reply, new_state} | {:noreply, new_state} | {:stop, reason, reply,
new_state} | ...`; `handle_cast/2` / `handle_info/2` → `{:noreply, new_state} | {:stop, reason,
new_state} | ...`. `GenServer.call/3` default timeout **5000 ms**; `cast/2` returns `:ok`. `genservers.html`:
  "Calls are synchronous and the server must send a response back ... the client is waiting" (a "useful
  back-pressure mechanism"); casts "should be used sparingly". Name collision → `{:error,
{:already_started, pid}}`. `[Verified]`
- **Supervisors** — hexdocs `Supervisor.html` (verbatim strategies): `:one_for_one` "if a child process
  terminates, only that process is restarted"; `:one_for_all` "all other child processes are terminated
  and then all ... are restarted"; `:rest_for_one` "the terminated child process and the rest of the
  children started after it, are terminated and restarted". Restart types: `:permanent` "always
  restarted", `:temporary` "never restarted", `:transient` "restarted only if it terminates abnormally".
  Defaults: `:max_restarts` = **3**, `:max_seconds` = **5**; worker `:shutdown` default 5_000. `[Verified]`
- **DynamicSupervisor** — hexdocs `DynamicSupervisor.html`: "starts with no children ... started on demand
  via `start_child/2`"; "The only supported value is `:one_for_one`". `[Verified]`
- **"Let it crash"** — hexdocs `try-catch-and-rescue.html` (the page carrying the phrase, NOT the
  supervision guide), verbatim: "the idea behind let it crash is that, in case something unexpected
  happens, it is best to let the exception happen, without rescuing it ... an unhandled exception in a
  process will never crash or corrupt the state of another process." `supervisor-and-application.html`:
  "Supervisors are processes that monitor workers. A supervisor can restart a worker if something goes
  wrong." (Joe Armstrong's 2003 thesis is the origin but its PDF was not fetched: `[Needs Verification]`
  for any verbatim thesis quote.) `[Verified]`
- **Agent & Task** — hexdocs `Agent.html`: "Agents are a simple abstraction around state"; `get/3`,
  `update/3`, `get_and_update/3` (third arg is `timeout()`). `Task.html`: "Tasks are processes meant to
  execute one particular action"; `Task.async/1` + `Task.await/2` (default timeout **5000 ms**);
  `Task.Supervisor` for dynamically supervised tasks (`[Needs Verification]` on its exact description
  wording). `[Verified]`
- **Registry** — hexdocs `Registry.html`: "A local, decentralized and scalable key-value process storage";
  `:via` tuple `{:via, Registry, {MyApp.Registry, "name"}}`; `:unique` keys → "a key points to 0 or 1
  process" (duplicate register → `{:error, {:already_registered, pid}}`), `:duplicate` keys → any number.
  `[Verified]`
- **OTP Application** — hexdocs `Application.html`: `start/2` "should start the top-level process ... the
  top supervisor of the application's supervision tree" and "return `{:ok, pid}`"; wired via a `:mod` key
  in `mix.exs` `application/0` (`mod: {MyApp, []}`) on a module that `use Application`. `[Verified]`
- **Pitfalls** — hexdocs `process-anti-patterns.html`: the "Code organization by process" anti-pattern —
  using a process for organisation (not runtime concurrency/isolation) "creates bottlenecks when call
  volume increases" (the GenServer-bottleneck pitfall). Blocking `handle_call` (from `genservers.html`:
  "the client is waiting" → don't block too long) and unbounded-mailbox growth are logically implied and
  community-standard but not fetched as named-anti-pattern doc text: `[Needs Verification]`.
- **Actor vs CSP** — grounded on two verified primaries: Go (go.dev/tour/concurrency/2) "sends and
  receives block until the other side is ready" (CSP synchronous rendezvous) vs Elixir `processes.html`
  "the sender does not block on `send/2`" (actor async mailbox). Sharper academic framing (Hewitt actor
  formalism, Hoare CSP) is cited for provenance only: `[Needs Verification]` on any verbatim paraphrase.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · actor-model** — concurrency as shared-nothing processes that own their state privately and
  communicate only by asynchronous messages; a crash in one cannot corrupt another.
- **co-02 · spawn-link** — `spawn/1` starts an isolated process and returns a PID; `spawn_link/1` also
  links it so failures propagate — the raw primitive under every OTP abstraction.
- **co-03 · send-receive** — `send/2` drops a message in a mailbox (non-blocking); `receive do ... end`
  pattern-matches the next matching message, blocking until one arrives.
- **co-04 · links** — a link is bidirectional: a linked process's crash sends an exit signal that (by
  default) takes the other down too, unless it traps exits.
- **co-05 · monitors** — `Process.monitor/1` is a one-way watch: the monitor receives a `{:DOWN, ...}`
  message when the target dies, without being affected itself.
- **co-06 · process-state-loop** — a process holds state by tail-recursing a `receive` loop, threading the
  updated state into the next iteration — the pattern `GenServer` automates.
- **co-07 · genserver-behaviour** — `use GenServer` gives a standard stateful-server behaviour with
  callbacks, hiding the hand-rolled receive loop behind a battle-tested framework.
- **co-08 · genserver-start-link** — `start_link/3` starts and links the server; `init/1` returns
  `{:ok, state}` to set the initial state.
- **co-09 · handle-call** — `handle_call/3` serves synchronous requests, returning `{:reply, reply,
state}`; the client blocks until it replies — a natural back-pressure mechanism.
- **co-10 · handle-cast** — `handle_cast/2` serves asynchronous, fire-and-forget requests, returning
  `{:noreply, state}` with no reply to the caller.
- **co-11 · handle-info** — `handle_info/2` receives non-OTP messages (raw `send`, timeouts, monitor
  `:DOWN`s) the server isn't `call`/`cast`-ed for.
- **co-12 · genserver-client-api** — public functions wrapping `GenServer.call`/`cast` give callers a clean
  API and hide that a process is involved at all.
- **co-13 · supervisor** — a `Supervisor` starts and watches child processes from their child specs,
  restarting them per a strategy — the unit of fault tolerance.
- **co-14 · restart-strategies** — `:one_for_one` (restart only the failed child), `:one_for_all` (restart
  all), `:rest_for_one` (restart the failed one and those started after it).
- **co-15 · restart-types** — `:permanent` (always restart), `:temporary` (never), `:transient` (restart
  only on abnormal exit) tune when a child comes back.
- **co-16 · restart-limits** — `max_restarts` / `max_seconds` (default 3 in 5s) cap restart storms; exceed
  them and the supervisor itself gives up and terminates.
- **co-17 · let-it-crash** — don't defensively rescue every error; let an unexpected fault crash the
  process and let its supervisor restart it to a known-good state.
- **co-18 · supervision-tree** — supervisors of supervisors form a tree; the shape localises failure and
  makes fault tolerance a design property, not per-process perfection.
- **co-19 · dynamic-supervisor** — `DynamicSupervisor` starts with no children and adds them on demand via
  `start_child/2` — for pools of like workers created at runtime.
- **co-20 · agent** — `Agent` is a thin process wrapper around a single piece of state
  (`get`/`update`/`get_and_update`), simpler than a full `GenServer` when there's no request logic.
- **co-21 · task** — `Task.async/1` + `Task.await/2` run work in a linked process and collect its result;
  `Task.Supervisor` supervises dynamically spawned tasks.
- **co-22 · registry** — `Registry` is a local key-value process store; the `{:via, Registry, {...}}`
  tuple lets a process be started and addressed by a name instead of a PID.
- **co-23 · otp-application** — an `Application` (`use Application`, `start/2` returning the top supervisor,
  wired by `:mod` in `mix.exs`) packages a supervision tree as a startable unit.
- **co-24 · process-registration** — a process can be registered under an atom name (`Process.register/2`
  or a GenServer `:name`) so others reach it without holding its PID.
- **co-25 · genserver-pitfalls** — a single GenServer becomes a bottleneck as call volume rises; blocking
  inside `handle_call` stalls every client; an unread mailbox grows unbounded.
- **co-26 · actor-vs-csp** — the actor model (identity-addressed processes, async mailboxes, supervision)
  contrasts with CSP ([`65-csp-style-concurrency`](./csp-style-concurrency.md): anonymous processes,
  synchronous channel rendezvous, explicit coordination).

## Worked examples

Colocated under `actor-model-concurrency/learning/code/`; each runnable via `mix`/`iex` (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · spawn-process** — `spawn(fn -> ... end)` — verify the function runs in another process. (co-01)
- **ex-02 · spawn-pid** — capture the PID, `Process.alive?/1` — verify it returns a live PID. (co-02)
- **ex-03 · spawn-link** — `spawn_link` a process that crashes — verify the crash propagates to the
  parent. (co-02)
- **ex-04 · send-message** — `send(pid, {:msg, self()})` — verify delivery to the mailbox. (co-03)
- **ex-05 · receive-match** — `receive do {:msg, _} -> ... end` — verify it matches. (co-03)
- **ex-06 · send-receive-roundtrip** — a process that replies to the sender — verify the round-trip. (co-03)
- **ex-07 · receive-multiple-patterns** — a `receive` with several clauses — verify each message routes. (co-03)
- **ex-08 · receive-timeout** — `receive do ... after 100 -> ... end` — verify the timeout branch. (co-03)
- **ex-09 · mailbox-fifo** — send two messages, receive both — verify FIFO order. (co-03)
- **ex-10 · link-crash-propagates** — a linked crash with no trap — verify both processes die. (co-04)
- **ex-11 · spawn-link-exit-signal** — observe the `{:EXIT, ...}` propagation — verify the signal. (co-04)
- **ex-12 · trap-exit** — `Process.flag(:trap_exit, true)` — verify the parent survives and gets `:EXIT`. (co-04)
- **ex-13 · monitor-down-message** — `Process.monitor` a dying process — verify a `{:DOWN, ...}` arrives. (co-05)
- **ex-14 · monitor-vs-link** — contrast a monitor (one-way) with a link (two-way) — verify the monitor
  process is unaffected. (co-05)
- **ex-15 · demonitor** — `Process.demonitor` before the target dies — verify no `:DOWN` arrives. (co-05)
- **ex-16 · stateful-loop-basic** — a recursive `receive` loop holding a value — verify state persists
  across messages. (co-06)
- **ex-17 · stateful-loop-counter** — a counter process incremented by messages — verify the running
  total. (co-06)
- **ex-18 · stateful-loop-get-set** — `{:get, from}` / `{:set, v}` messages — verify reads and writes. (co-06)
- **ex-19 · process-isolation** — crash a spawned process — verify the parent's state is intact. (co-01)
- **ex-20 · lightweight-many** — spawn 100_000 processes — verify they start cheaply. (co-01)
- **ex-21 · self-reply-address** — pass `self()` in a message so the worker can reply — verify the reply. (co-03)
- **ex-22 · stateful-loop-immutable** — show the loop's state is a new value each iteration — verify no
  mutation. (co-06)
- **ex-23 · spawn-monitor** — `spawn_monitor` in one call — verify it returns `{pid, ref}` and a `:DOWN`. (co-05)
- **ex-24 · named-register** — `Process.register(pid, :worker)` — verify `:worker` resolves to the PID. (co-24)
- **ex-25 · whereis-lookup** — `Process.whereis(:worker)` — verify it returns the registered PID. (co-24)
- **ex-26 · send-to-named** — `send(:worker, msg)` by name — verify delivery. (co-24)

### Intermediate

- **ex-27 · genserver-minimal** — a `use GenServer` with `init/1` + one `handle_call` — verify it starts
  and replies. (co-07)
- **ex-28 · genserver-state-map** — hold a map as state — verify updates round-trip. (co-07)
- **ex-29 · genserver-start-link** — `GenServer.start_link(Mod, arg)` — verify `{:ok, pid}`. (co-08)
- **ex-30 · genserver-init** — `init/1` returning `{:ok, state}` — verify the initial state. (co-08)
- **ex-31 · handle-call-sync** — a synchronous `GenServer.call` — verify the client waits for the reply. (co-09)
- **ex-32 · handle-call-reply** — `{:reply, value, new_state}` — verify both the reply and the state
  change. (co-09)
- **ex-33 · handle-call-backpressure** — a slow `handle_call` — verify concurrent callers queue (back
  pressure). (co-09)
- **ex-34 · handle-cast-async** — a `GenServer.cast` — verify it returns `:ok` immediately. (co-10)
- **ex-35 · handle-cast-noreply** — `{:noreply, new_state}` — verify the state changes with no reply. (co-10)
- **ex-36 · handle-info-message** — a raw `send` to the GenServer — verify `handle_info/2` receives it. (co-11)
- **ex-37 · handle-info-timeout** — a `{:ok, state, timeout}` returning a `:timeout` — verify it fires. (co-11)
- **ex-38 · client-api-wrapper** — public `get/1` + `put/2` wrapping call/cast — verify callers never see
  a PID. (co-12)
- **ex-39 · genserver-stop** — `GenServer.stop/1` — verify the process terminates. (co-08)
- **ex-40 · genserver-continue** — `{:continue, arg}` from `init` — verify `handle_continue/2` runs post-
  init. (co-08)
- **ex-41 · agent-simple-state** — `Agent.start_link(fn -> 0 end)` — verify it holds state. (co-20)
- **ex-42 · agent-get-update** — `Agent.get`/`Agent.update` — verify read and write. (co-20)
- **ex-43 · agent-vs-genserver** — the same counter as an Agent and a GenServer — verify equivalence, note
  when each fits. (co-20)
- **ex-44 · task-async-await** — `Task.async(fn -> ... end) |> Task.await()` — verify the result. (co-21)
- **ex-45 · task-multiple-parallel** — many `Task.async` awaited together — verify parallel results. (co-21)
- **ex-46 · task-supervisor** — a `Task.Supervisor.async_nolink` — verify a supervised task runs. (co-21)
- **ex-47 · registry-start** — `Registry.start_link(keys: :unique, name: R)` — verify it starts. (co-22)
- **ex-48 · registry-via-tuple** — start a GenServer with `name: {:via, Registry, {R, "w"}}` — verify it
  is addressable by that name. (co-22)
- **ex-49 · registry-unique-keys** — register a duplicate unique key — verify `{:error,
{:already_registered, pid}}`. (co-22)
- **ex-50 · registry-duplicate-keys** — a `:duplicate` registry with many entries under one key — verify
  a lookup returns all. (co-22)
- **ex-51 · genserver-registered-name** — `GenServer.start_link(Mod, arg, name: :srv)` — verify calls by
  name. (co-24)
- **ex-52 · genserver-timeout-call** — `GenServer.call(pid, msg, 100)` on a slow server — verify it times
  out. (co-09)
- **ex-53 · genserver-multi-clause-handle** — several `handle_call` clauses by message pattern — verify
  dispatch. (co-08)
- **ex-54 · genserver-call-cast-choice** — the same op as a call and a cast — verify reply vs no-reply and
  note the trade-off. (co-09, co-10)

### Advanced

- **ex-55 · supervisor-basic** — a `Supervisor` with one child — verify it starts the child. (co-13)
- **ex-56 · child-spec** — an explicit child spec (`id`, `start`) — verify the supervisor uses it. (co-13)
- **ex-57 · supervisor-starts-children** — a supervisor with several children — verify all start. (co-13)
- **ex-58 · one-for-one** — `:one_for_one`; crash one child — verify only it restarts. (co-14)
- **ex-59 · one-for-all** — `:one_for_all`; crash one child — verify all restart. (co-14)
- **ex-60 · rest-for-one** — `:rest_for_one`; crash a middle child — verify it and later ones restart. (co-14)
- **ex-61 · restart-permanent** — a `:permanent` child exiting normally — verify it still restarts. (co-15)
- **ex-62 · restart-temporary** — a `:temporary` child crashing — verify it does NOT restart. (co-15)
- **ex-63 · restart-transient** — a `:transient` child: normal exit vs crash — verify it restarts only on
  crash. (co-15)
- **ex-64 · max-restarts-limit** — exceed `max_restarts` in `max_seconds` — verify the supervisor itself
  terminates. (co-16)
- **ex-65 · let-it-crash-demo** — a worker that crashes on bad input instead of rescuing — verify it
  crashes cleanly. (co-17)
- **ex-66 · supervisor-restarts-worker** — put the crashing worker under a supervisor — verify it comes
  back with fresh state. (co-17, co-13)
- **ex-67 · supervision-tree-nested** — a supervisor supervising a supervisor — verify the tree starts. (co-18)
- **ex-68 · dynamic-supervisor-start-child** — `DynamicSupervisor.start_child/2` — verify a child is added
  at runtime. (co-19)
- **ex-69 · dynamic-supervisor-many** — start N workers dynamically — verify each is supervised. (co-19)
- **ex-70 · otp-application-mod** — an `Application` with `:mod` in `mix.exs` — verify `mix run` starts the
  tree. (co-23)
- **ex-71 · application-supervision-root** — `start/2` returning the top supervisor — verify the whole tree
  boots. (co-23)
- **ex-72 · registry-in-supervision-tree** — a Registry supervised in the app tree — verify named workers
  resolve after start. (co-22, co-18)
- **ex-73 · crash-recovery-service-available** — crash a supervised worker mid-use — verify the service
  stays available after restart. (co-17, co-13)
- **ex-74 · genserver-bottleneck-pitfall** — route all work through one GenServer — verify it serialises
  and bottlenecks under load. (co-25)
- **ex-75 · blocking-handle-call-pitfall** — a long-running op inside `handle_call` — verify it stalls
  other callers; fix by replying async. (co-25)
- **ex-76 · unbounded-mailbox-pitfall** — flood a slow process with messages — verify the mailbox grows
  unbounded. (co-25)
- **ex-77 · actor-vs-csp-contrast** — a `contrast.md` comparing actor async mailboxes + supervision with
  Go's synchronous channels — verify it names a concrete trade-off each way. (co-26)
- **ex-78 · capstone-fault-tolerant-otp** — a GenServer + supervision tree + registry that survives an
  induced crash — verify the service recovers with no loss. (co-07, co-13, co-17, co-22)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a small fault-tolerant OTP system — a `GenServer` holding state, a supervision tree that
  restarts a crashing worker under a chosen strategy ("let it crash"), and a registry — that demonstrably
  recovers from an induced crash without losing the supervised service, plus a written CSP-vs-actor
  contrast.
- **Concepts exercised**: [ ] `spawn`/`send`/`receive` (co-02, co-03) [ ] a stateful `GenServer` (co-07,
  co-09, co-10) [ ] a supervision tree + restart strategy (co-13, co-14, co-18) [ ] crash recovery
  ("let it crash") (co-17) [ ] a registry (co-22) [ ] a CSP-vs-actor contrast note (co-26).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a `GenServer` managing state with a clean client API. Verify state
     updates + reads round-trip through messages.
  2. Put it under a supervisor with a restart strategy + a registry. Verify the supervisor starts the tree
     and the process is discoverable by name.
  3. Induce a crash. Verify the supervisor restarts the worker and the service stays available.
  4. `contrast.md` — actor vs CSP (shared-nothing messaging vs channels; supervision vs explicit
     coordination). Verify the contrast names a concrete trade-off each way.
- **Acceptance criteria**: the `GenServer` manages state correctly; the supervision tree restarts a crashed
  worker with no loss of service; the registry resolves the process; the CSP contrast is concrete.
- **Done bar**: runnable end-to-end (survives an induced crash) + web-verified.

## Read more

**Books**

- **Programming Erlang: Software for a Concurrent World**, 2nd ed. — Joe Armstrong (2013, Pragmatic Bookshelf). The canonical Erlang/actor-model text by one of Erlang's creators.
- **Designing for Scalability with Erlang/OTP** — Francesco Cesarini & Steve Vinoski (2016, O'Reilly). The standard reference on building fault-tolerant, supervision-tree-based systems in production.

**Papers & articles**

- **A Universal Modular ACTOR Formalism for Artificial Intelligence** — Carl Hewitt, Peter Bishop, Richard Steiger, _Proc. 3rd IJCAI_ (1973). The founding paper that introduced the actor model. <http://ijcai.org/Proceedings/73/Papers/027B.pdf>
- **Making Reliable Distributed Systems in the Presence of Software Errors** — Joe Armstrong, PhD thesis, Royal Institute of Technology (2003). Defines OTP's "let it crash" philosophy and supervision trees; officially hosted by erlang.org. <https://erlang.org/download/armstrong_thesis_2003.pdf>
- **OTP Design Principles** — Erlang/OTP official System Documentation. The authoritative reference for workers, supervisors, and supervision trees. <https://www.erlang.org/doc/system/design_principles.html>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Concurrency, JVM & languages — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Concurrency & language breadth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 3 · Concurrency & language breadth.

> _Content originated in the now-closed FS-SE plan (topic 67); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
