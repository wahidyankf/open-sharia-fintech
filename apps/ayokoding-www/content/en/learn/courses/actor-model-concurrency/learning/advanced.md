---
title: "Advanced Actor Model"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 3
---

# Advanced Actor Model

## Example 55: supervisor basic

_ex-55-supervisor-basic · source-matched_

```elixir
# supervisor basic: make the OTP operation and lifecycle explicit.
child = %{
  # supervisor basic: make the OTP operation and lifecycle explicit.
  id: :worker,
  # supervisor basic: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # supervisor basic: make the OTP operation and lifecycle explicit.
  restart: :temporary
# supervisor basic: make the OTP operation and lifecycle explicit.
}
# supervisor basic: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# supervisor basic: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "55-supervisor-basic")
# supervisor basic: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 56: child spec

_ex-56-child-spec · source-matched_

```elixir
# child spec: make the OTP operation and lifecycle explicit.
child = %{
  # child spec: make the OTP operation and lifecycle explicit.
  id: :worker,
  # child spec: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # child spec: make the OTP operation and lifecycle explicit.
  restart: :temporary
# child spec: make the OTP operation and lifecycle explicit.
}
# child spec: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# child spec: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "56-child-spec")
# child spec: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 57: supervisor starts children

_ex-57-supervisor-starts-children · source-matched_

```elixir
# supervisor starts children: make the OTP operation and lifecycle explicit.
child = %{
  # supervisor starts children: make the OTP operation and lifecycle explicit.
  id: :worker,
  # supervisor starts children: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # supervisor starts children: make the OTP operation and lifecycle explicit.
  restart: :temporary
# supervisor starts children: make the OTP operation and lifecycle explicit.
}
# supervisor starts children: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# supervisor starts children: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "57-supervisor-starts-children")
# supervisor starts children: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 58: one for one

_ex-58-one-for-one · source-matched_

```elixir
# one for one: make the OTP operation and lifecycle explicit.
child = %{
  # one for one: make the OTP operation and lifecycle explicit.
  id: :worker,
  # one for one: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # one for one: make the OTP operation and lifecycle explicit.
  restart: :temporary
# one for one: make the OTP operation and lifecycle explicit.
}
# one for one: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# one for one: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "58-one-for-one")
# one for one: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 59: one for all

_ex-59-one-for-all · source-matched_

```elixir
# one for all: make the OTP operation and lifecycle explicit.
child = %{
  # one for all: make the OTP operation and lifecycle explicit.
  id: :worker,
  # one for all: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # one for all: make the OTP operation and lifecycle explicit.
  restart: :temporary
# one for all: make the OTP operation and lifecycle explicit.
}
# one for all: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# one for all: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "59-one-for-all")
# one for all: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 60: rest for one

_ex-60-rest-for-one · source-matched_

```elixir
# rest for one: make the OTP operation and lifecycle explicit.
child = %{
  # rest for one: make the OTP operation and lifecycle explicit.
  id: :worker,
  # rest for one: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # rest for one: make the OTP operation and lifecycle explicit.
  restart: :temporary
# rest for one: make the OTP operation and lifecycle explicit.
}
# rest for one: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# rest for one: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "60-rest-for-one")
# rest for one: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 61: restart permanent

_ex-61-restart-permanent · source-matched_

```elixir
# restart permanent: make the OTP operation and lifecycle explicit.
child = %{
  # restart permanent: make the OTP operation and lifecycle explicit.
  id: :worker,
  # restart permanent: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # restart permanent: make the OTP operation and lifecycle explicit.
  restart: :temporary
# restart permanent: make the OTP operation and lifecycle explicit.
}
# restart permanent: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# restart permanent: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "61-restart-permanent")
# restart permanent: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 62: restart temporary

_ex-62-restart-temporary · source-matched_

```elixir
# restart temporary: make the OTP operation and lifecycle explicit.
child = %{
  # restart temporary: make the OTP operation and lifecycle explicit.
  id: :worker,
  # restart temporary: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # restart temporary: make the OTP operation and lifecycle explicit.
  restart: :temporary
# restart temporary: make the OTP operation and lifecycle explicit.
}
# restart temporary: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# restart temporary: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "62-restart-temporary")
# restart temporary: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 63: restart transient

_ex-63-restart-transient · source-matched_

```elixir
# restart transient: make the OTP operation and lifecycle explicit.
child = %{
  # restart transient: make the OTP operation and lifecycle explicit.
  id: :worker,
  # restart transient: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # restart transient: make the OTP operation and lifecycle explicit.
  restart: :temporary
# restart transient: make the OTP operation and lifecycle explicit.
}
# restart transient: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# restart transient: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "63-restart-transient")
# restart transient: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 64: max restarts limit

_ex-64-max-restarts-limit · source-matched_

```elixir
# max restarts limit: make the OTP operation and lifecycle explicit.
child = %{
  # max restarts limit: make the OTP operation and lifecycle explicit.
  id: :worker,
  # max restarts limit: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # max restarts limit: make the OTP operation and lifecycle explicit.
  restart: :temporary
# max restarts limit: make the OTP operation and lifecycle explicit.
}
# max restarts limit: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# max restarts limit: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "64-max-restarts-limit")
# max restarts limit: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 65: let it crash demo

_ex-65-let-it-crash-demo · source-matched_

```elixir
# let it crash demo: make the OTP operation and lifecycle explicit.
child = %{
  # let it crash demo: make the OTP operation and lifecycle explicit.
  id: :worker,
  # let it crash demo: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # let it crash demo: make the OTP operation and lifecycle explicit.
  restart: :temporary
# let it crash demo: make the OTP operation and lifecycle explicit.
}
# let it crash demo: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# let it crash demo: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "65-let-it-crash-demo")
# let it crash demo: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 66: supervisor restarts worker

_ex-66-supervisor-restarts-worker · source-matched_

```elixir
# supervisor restarts worker: make the OTP operation and lifecycle explicit.
child = %{
  # supervisor restarts worker: make the OTP operation and lifecycle explicit.
  id: :worker,
  # supervisor restarts worker: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # supervisor restarts worker: make the OTP operation and lifecycle explicit.
  restart: :temporary
# supervisor restarts worker: make the OTP operation and lifecycle explicit.
}
# supervisor restarts worker: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# supervisor restarts worker: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "66-supervisor-restarts-worker")
# supervisor restarts worker: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 67: supervision tree nested

_ex-67-supervision-tree-nested · source-matched_

```elixir
# supervision tree nested: make the OTP operation and lifecycle explicit.
child = %{
  # supervision tree nested: make the OTP operation and lifecycle explicit.
  id: :worker,
  # supervision tree nested: make the OTP operation and lifecycle explicit.
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  # supervision tree nested: make the OTP operation and lifecycle explicit.
  restart: :temporary
# supervision tree nested: make the OTP operation and lifecycle explicit.
}
# supervision tree nested: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
# supervision tree nested: make the OTP operation and lifecycle explicit.
IO.inspect(Supervisor.count_children(supervisor), label: "67-supervision-tree-nested")
# supervision tree nested: make the OTP operation and lifecycle explicit.
Supervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 68: dynamic supervisor start child

_ex-68-dynamic-supervisor-start-child · source-matched_

```elixir
# dynamic supervisor start child: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = DynamicSupervisor.start_link(strategy: :one_for_one)
# dynamic supervisor start child: make the OTP operation and lifecycle explicit.
{:ok, child} = DynamicSupervisor.start_child(supervisor, {Task, fn -> Process.sleep(1_000) end})
# dynamic supervisor start child: make the OTP operation and lifecycle explicit.
IO.inspect(Process.alive?(child), label: "68-dynamic-supervisor-start-child")
# dynamic supervisor start child: make the OTP operation and lifecycle explicit.
DynamicSupervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 69: dynamic supervisor many

_ex-69-dynamic-supervisor-many · source-matched_

```elixir
# dynamic supervisor many: make the OTP operation and lifecycle explicit.
{:ok, supervisor} = DynamicSupervisor.start_link(strategy: :one_for_one)
# dynamic supervisor many: make the OTP operation and lifecycle explicit.
{:ok, child} = DynamicSupervisor.start_child(supervisor, {Task, fn -> Process.sleep(1_000) end})
# dynamic supervisor many: make the OTP operation and lifecycle explicit.
IO.inspect(Process.alive?(child), label: "69-dynamic-supervisor-many")
# dynamic supervisor many: make the OTP operation and lifecycle explicit.
DynamicSupervisor.stop(supervisor)
```

Run: elixir main.exs.

## Example 70: otp application mod

_ex-70-otp-application-mod · source-matched_

```elixir
# otp application mod: make the OTP operation and lifecycle explicit.
{:ok, registry} = Registry.start_link(keys: :unique, name: :service_registry)
# otp application mod: make the OTP operation and lifecycle explicit.
{:ok, _} = Registry.register(:service_registry, :service, :ready)
# otp application mod: make the OTP operation and lifecycle explicit.
IO.inspect(Registry.lookup(:service_registry, :service), label: "70-otp-application-mod")
```

Run: elixir main.exs.

## Example 71: application supervision root

_ex-71-application-supervision-root · source-matched_

```elixir
# application supervision root: make the OTP operation and lifecycle explicit.
{:ok, registry} = Registry.start_link(keys: :unique, name: :service_registry)
# application supervision root: make the OTP operation and lifecycle explicit.
{:ok, _} = Registry.register(:service_registry, :service, :ready)
# application supervision root: make the OTP operation and lifecycle explicit.
IO.inspect(Registry.lookup(:service_registry, :service), label: "71-application-supervision-root")
```

Run: elixir main.exs.

## Example 72: registry in supervision tree

_ex-72-registry-in-supervision-tree · source-matched_

```elixir
# registry in supervision tree: make the OTP operation and lifecycle explicit.
{:ok, registry} = Registry.start_link(keys: :unique, name: :service_registry)
# registry in supervision tree: make the OTP operation and lifecycle explicit.
{:ok, _} = Registry.register(:service_registry, :service, :ready)
# registry in supervision tree: make the OTP operation and lifecycle explicit.
IO.inspect(Registry.lookup(:service_registry, :service), label: "72-registry-in-supervision-tree")
```

Run: elixir main.exs.

## Example 73: crash recovery service available

_ex-73-crash-recovery-service-available · source-matched_

```elixir
# crash recovery service available: make the OTP operation and lifecycle explicit.
{:ok, registry} = Registry.start_link(keys: :unique, name: :service_registry)
# crash recovery service available: make the OTP operation and lifecycle explicit.
{:ok, _} = Registry.register(:service_registry, :service, :ready)
# crash recovery service available: make the OTP operation and lifecycle explicit.
IO.inspect(Registry.lookup(:service_registry, :service), label: "73-crash-recovery-service-available")
```

Run: elixir main.exs.

## Example 74: genserver bottleneck pitfall

_ex-74-genserver-bottleneck-pitfall · source-matched_

```elixir
# genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
defmodule Bottleneck do
  # genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
  use GenServer
  # genserver bottleneck pitfall: expose a standard linked server start function.
  def start_link(arg), do: GenServer.start_link(__MODULE__, arg)
  # genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
  def init(_), do: {:ok, 0}
  # genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
  def handle_call(:work, _from, value) do
    # genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
    Process.sleep(5)
    # genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
    {:reply, value, value + 1}
  # genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
  end
# genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
end
# genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
{:ok, pid} = Bottleneck.start_link([])
# genserver bottleneck pitfall: make the OTP operation and lifecycle explicit.
IO.inspect(GenServer.call(pid, :work), label: "serial call")
```

Run: elixir main.exs.

## Example 75: blocking handle call pitfall

_ex-75-blocking-handle-call-pitfall · source-matched_

```elixir
# blocking handle call pitfall: make the OTP operation and lifecycle explicit.
defmodule SlowCall do
  # blocking handle call pitfall: make the OTP operation and lifecycle explicit.
  use GenServer
  # blocking handle call pitfall: expose a standard linked server start function.
  def start_link(arg), do: GenServer.start_link(__MODULE__, arg)
  # blocking handle call pitfall: make the OTP operation and lifecycle explicit.
  def init(_), do: {:ok, :ready}
  # blocking handle call pitfall: make the OTP operation and lifecycle explicit.
  def handle_call(:slow, _from, state) do
    # blocking handle call pitfall: make the OTP operation and lifecycle explicit.
    Process.sleep(5)
    # blocking handle call pitfall: make the OTP operation and lifecycle explicit.
    {:reply, :done, state}
  # blocking handle call pitfall: make the OTP operation and lifecycle explicit.
  end
# blocking handle call pitfall: make the OTP operation and lifecycle explicit.
end
# blocking handle call pitfall: make the OTP operation and lifecycle explicit.
{:ok, pid} = SlowCall.start_link([])
# blocking handle call pitfall: make the OTP operation and lifecycle explicit.
IO.inspect(GenServer.call(pid, :slow), label: "blocking call")
```

Run: elixir main.exs.

## Example 76: unbounded mailbox pitfall

_ex-76-unbounded-mailbox-pitfall · source-matched_

```elixir
# unbounded mailbox pitfall: make the OTP operation and lifecycle explicit.
pid = spawn(fn -> Process.sleep(50) end)
# unbounded mailbox pitfall: make the OTP operation and lifecycle explicit.
for _ <- 1..100, do: send(pid, :work)
# unbounded mailbox pitfall: make the OTP operation and lifecycle explicit.
IO.inspect(Process.info(pid, :message_queue_len), label: "mailbox growth")
```

Run: elixir main.exs.

## Example 77: actor vs csp contrast

_ex-77-actor-vs-csp-contrast · source-matched_

`contrast.md` alongside the source gives the concrete actor/CSP trade-offs:
[read the contrast](./code/ex-77-actor-vs-csp-contrast/contrast.md).

```elixir
# actor vs csp contrast: make the OTP operation and lifecycle explicit.
IO.puts("Actor: async identity-addressed mailbox plus supervision")
# actor vs csp contrast: make the OTP operation and lifecycle explicit.
IO.puts("CSP: synchronous channel rendezvous plus explicit coordination")
```

Run: elixir main.exs.

## Example 78: capstone fault tolerant otp

_ex-78-capstone-fault-tolerant-otp · source-matched_

```elixir
# capstone fault tolerant otp: make the OTP operation and lifecycle explicit.
defmodule Recovering do
  # capstone fault tolerant otp: make the OTP operation and lifecycle explicit.
  use GenServer
  # capstone fault tolerant otp: make the OTP operation and lifecycle explicit.
  def start, do: GenServer.start_link(__MODULE__, :ready)
  # capstone fault tolerant otp: make the OTP operation and lifecycle explicit.
  def init(state), do: {:ok, state}
  # capstone fault tolerant otp: make the OTP operation and lifecycle explicit.
  def handle_call(:get, _from, state), do: {:reply, state, state}
# capstone fault tolerant otp: make the OTP operation and lifecycle explicit.
end
# capstone fault tolerant otp: make the OTP operation and lifecycle explicit.
{:ok, pid} = Recovering.start()
# capstone fault tolerant otp: make the OTP operation and lifecycle explicit.
IO.inspect(GenServer.call(pid, :get), label: "fault tolerant OTP preview")
```

Run: elixir main.exs.
