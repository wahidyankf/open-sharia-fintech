---
title: "Beginner Actor Model"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

# Beginner Actor Model

Run each example with elixir main.exs.

## Example 01: Spawn Process

_ex-01-spawn-process · source-matched_

This script is rendered from learning/code/ex-01-spawn-process/main.exs.

```elixir
# spawn process: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# spawn process: this step exposes process identity, mailbox flow, or failure isolation.
spawn(fn -> send(parent, :ran) end)
# spawn process: this step exposes process identity, mailbox flow, or failure isolation.
receive do :ran -> IO.puts("separate process ran") end
```

Run: elixir main.exs.

## Example 02: Spawn Pid

_ex-02-spawn-pid · source-matched_

This script is rendered from learning/code/ex-02-spawn-pid/main.exs.

```elixir
# spawn pid: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do :stop -> :ok end end)
# spawn pid: this step exposes process identity, mailbox flow, or failure isolation.
IO.inspect({is_pid(pid), Process.alive?(pid)})
# spawn pid: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, :stop)
```

Run: elixir main.exs.

## Example 03: Spawn Link

_ex-03-spawn-link · source-matched_

This script is rendered from learning/code/ex-03-spawn-link/main.exs.

```elixir
# spawn link: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# spawn link: this step exposes process identity, mailbox flow, or failure isolation.
spawn(fn ->
  # spawn link: this step exposes process identity, mailbox flow, or failure isolation.
  Process.flag(:trap_exit, true)
  # spawn link: this step exposes process identity, mailbox flow, or failure isolation.
  spawn_link(fn -> exit(:boom) end)
  # spawn link: this step exposes process identity, mailbox flow, or failure isolation.
  receive do {:EXIT, _pid, :boom} -> send(parent, :linked_crash_observed) end
# spawn link: this step exposes process identity, mailbox flow, or failure isolation.
end)
# spawn link: this step exposes process identity, mailbox flow, or failure isolation.
receive do :linked_crash_observed -> IO.puts("spawn_link propagated crash") end
```

Run: elixir main.exs.

## Example 04: Send Message

_ex-04-send-message · source-matched_

This script is rendered from learning/code/ex-04-send-message/main.exs.

```elixir
# send message: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# send message: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do message -> send(parent, {:delivered, message}) end end)
# send message: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:msg, self()})
# send message: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:delivered, message} -> IO.inspect(message) end
```

Run: elixir main.exs.

## Example 05: Receive Match

_ex-05-receive-match · source-matched_

This script is rendered from learning/code/ex-05-receive-match/main.exs.

```elixir
# receive match: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), {:msg, "Ada"})
# receive match: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:msg, name} -> IO.puts("matched #{name}") end
```

Run: elixir main.exs.

## Example 06: Send Receive Roundtrip

_ex-06-send-receive-roundtrip · source-matched_

This script is rendered from learning/code/ex-06-send-receive-roundtrip/main.exs.

```elixir
# send receive roundtrip: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# send receive roundtrip: this step exposes process identity, mailbox flow, or failure isolation.
worker = spawn(fn -> receive do {:ping, from} -> send(from, {:pong, parent}) end end)
# send receive roundtrip: this step exposes process identity, mailbox flow, or failure isolation.
send(worker, {:ping, self()})
# send receive roundtrip: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:pong, from} -> IO.inspect(from, label: "round trip") end
```

Run: elixir main.exs.

## Example 07: Receive Multiple Patterns

_ex-07-receive-multiple-patterns · source-matched_

This script is rendered from learning/code/ex-07-receive-multiple-patterns/main.exs.

```elixir
# receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), {:add, 2})
# receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), :stop)
# receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
for _ <- 1..2 do
  # receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
  receive do
    # receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
    {:add, value} -> IO.puts("add #{value}")
    # receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
    :stop -> IO.puts("stop")
  # receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
  end
# receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
end
```

Run: elixir main.exs.

## Example 08: Receive Timeout

_ex-08-receive-timeout · source-matched_

This script is rendered from learning/code/ex-08-receive-timeout/main.exs.

```elixir
# receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
receive do
  # receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
  :message -> IO.puts("received")
# receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
after
  # receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
  10 -> IO.puts("timeout")
# receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
end
```

Run: elixir main.exs.

## Example 09: Mailbox Fifo

_ex-09-mailbox-fifo · source-matched_

This script is rendered from learning/code/ex-09-mailbox-fifo/main.exs.

```elixir
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), :first)
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), :second)
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
first = receive do message -> message end
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
second = receive do message -> message end
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
IO.inspect({first, second})
```

Run: elixir main.exs.

## Example 10: Link Crash Propagates

_ex-10-link-crash-propagates · source-matched_

This script is rendered from learning/code/ex-10-link-crash-propagates/main.exs.

```elixir
# link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
victim = spawn(fn ->
  # link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
  child = spawn_link(fn -> exit(:boom) end)
  # link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
  Process.monitor(child)
  # link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
  receive do {:DOWN, _ref, :process, _pid, :boom} -> :ok end
# link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
end)
# link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(victim)
# link crash propagates: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^victim, :boom} -> IO.puts("linked parent died too") end
```

Run: elixir main.exs.

## Example 11: Spawn Link Exit Signal

_ex-11-spawn-link-exit-signal · source-matched_

This script is rendered from learning/code/ex-11-spawn-link-exit-signal/main.exs.

```elixir
# spawn link exit signal: this step exposes process identity, mailbox flow, or failure isolation.
Process.flag(:trap_exit, true)
# spawn link exit signal: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn_link(fn -> exit(:boom) end)
# spawn link exit signal: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:EXIT, ^pid, :boom} -> IO.puts("received EXIT signal") end
```

Run: elixir main.exs.

## Example 12: Trap Exit

_ex-12-trap-exit · source-matched_

This script is rendered from learning/code/ex-12-trap-exit/main.exs.

```elixir
# trap exit: this step exposes process identity, mailbox flow, or failure isolation.
Process.flag(:trap_exit, true)
# trap exit: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn_link(fn -> exit(:boom) end)
# trap exit: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:EXIT, ^pid, :boom} -> IO.puts("survived trapped exit") end
```

Run: elixir main.exs.

## Example 13: Monitor Down Message

_ex-13-monitor-down-message · source-matched_

This script is rendered from learning/code/ex-13-monitor-down-message/main.exs.

```elixir
# monitor down message: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> exit(:finished) end)
# monitor down message: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(pid)
# monitor down message: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, :finished} -> IO.puts("DOWN arrived") end
```

Run: elixir main.exs.

## Example 14: Monitor Vs Link

_ex-14-monitor-vs-link · source-matched_

This script is rendered from learning/code/ex-14-monitor-vs-link/main.exs.

```elixir
# monitor vs link: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> exit(:boom) end)
# monitor vs link: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(pid)
# monitor vs link: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, :boom} -> IO.puts("monitor survived target crash") end
```

Run: elixir main.exs.

## Example 15: Demonitor

_ex-15-demonitor · source-matched_

This script is rendered from learning/code/ex-15-demonitor/main.exs.

```elixir
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do :stop -> exit(:done) end end)
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(pid)
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
true = Process.demonitor(ref, [:flush])
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, :stop)
# demonitor: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, _} -> raise "unexpected DOWN" after 10 -> IO.puts("no DOWN after demonitor") end
```

Run: elixir main.exs.

## Example 16: Stateful Loop Basic

_ex-16-stateful-loop-basic · source-matched_

This script is rendered from learning/code/ex-16-stateful-loop-basic/main.exs.

```elixir
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
defmodule ValueLoop do
  # stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
  def loop(value) do
    # stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
    receive do {:get, from} -> send(from, {:value, value}); loop(value) end
  # stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
  end
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
end
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> ValueLoop.loop("saved") end)
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:get, self()})
# stateful loop basic: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:value, value} -> IO.inspect(value) end
```

Run: elixir main.exs.

## Example 17: Stateful Loop Counter

_ex-17-stateful-loop-counter · source-matched_

This script is rendered from learning/code/ex-17-stateful-loop-counter/main.exs.

```elixir
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
defmodule CounterLoop do
  # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
  def loop(total) do
    # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
    receive do
      # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
      {:add, value} -> loop(total + value)
      # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
      {:get, from} -> send(from, {:total, total}); loop(total)
    # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
    end
  # stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
  end
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
end
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> CounterLoop.loop(0) end)
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:add, 3})
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:get, self()})
# stateful loop counter: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:total, total} -> IO.inspect(total) end
```

Run: elixir main.exs.

## Example 18: Stateful Loop Get Set

_ex-18-stateful-loop-get-set · source-matched_

This script is rendered from learning/code/ex-18-stateful-loop-get-set/main.exs.

```elixir
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
defmodule StoreLoop do
  # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
  def loop(value) do
    # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
    receive do
      # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
      {:set, next} -> loop(next)
      # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
      {:get, from} -> send(from, {:value, value}); loop(value)
    # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
    end
  # stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
  end
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
end
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> StoreLoop.loop(:old) end)
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:set, :new})
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:get, self()})
# stateful loop get set: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:value, value} -> IO.inspect(value) end
```

Run: elixir main.exs.

## Example 19: Process Isolation

_ex-19-process-isolation · source-matched_

This script is rendered from learning/code/ex-19-process-isolation/main.exs.

```elixir
# process isolation: this step exposes process identity, mailbox flow, or failure isolation.
parent_state = :intact
# process isolation: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> exit(:boom) end)
# process isolation: this step exposes process identity, mailbox flow, or failure isolation.
ref = Process.monitor(pid)
# process isolation: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, :boom} -> IO.inspect(parent_state) end
```

Run: elixir main.exs.

## Example 20: Lightweight Many

_ex-20-lightweight-many · source-matched_

This script is rendered from learning/code/ex-20-lightweight-many/main.exs.

```elixir
# lightweight many: this step exposes process identity, mailbox flow, or failure isolation.
pids = for _ <- 1..100_000, do: spawn(fn -> :ok end)
# lightweight many: this step exposes process identity, mailbox flow, or failure isolation.
IO.puts("spawned #{length(pids)} processes")
```

Run: elixir main.exs.

## Example 21: Self Reply Address

_ex-21-self-reply-address · source-matched_

This script is rendered from learning/code/ex-21-self-reply-address/main.exs.

```elixir
# self reply address: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# self reply address: this step exposes process identity, mailbox flow, or failure isolation.
worker = spawn(fn -> receive do {:work, from} -> send(from, {:result, parent}) end end)
# self reply address: this step exposes process identity, mailbox flow, or failure isolation.
send(worker, {:work, self()})
# self reply address: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:result, from} -> IO.inspect(from, label: "reply address worked") end
```

Run: elixir main.exs.

## Example 22: Stateful Loop Immutable

_ex-22-stateful-loop-immutable · source-matched_

This script is rendered from learning/code/ex-22-stateful-loop-immutable/main.exs.

```elixir
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
defmodule ImmutableLoop do
  # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
  def loop(value) do
    # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
    receive do
      # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
      {:next, from} -> next = value + 1; send(from, {value, next}); loop(next)
    # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
    end
  # stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
  end
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
end
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> ImmutableLoop.loop(0) end)
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, {:next, self()})
# stateful loop immutable: this step exposes process identity, mailbox flow, or failure isolation.
receive do values -> IO.inspect(values) end
```

Run: elixir main.exs.

## Example 23: Spawn Monitor

_ex-23-spawn-monitor · source-matched_

This script is rendered from learning/code/ex-23-spawn-monitor/main.exs.

```elixir
# spawn monitor: this step exposes process identity, mailbox flow, or failure isolation.
{pid, ref} = spawn_monitor(fn -> exit(:done) end)
# spawn monitor: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:DOWN, ^ref, :process, ^pid, :done} -> IO.puts("pid and ref produced DOWN") end
```

Run: elixir main.exs.

## Example 24: Named Register

_ex-24-named-register · source-matched_

This script is rendered from learning/code/ex-24-named-register/main.exs.

```elixir
# named register: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do :stop -> :ok end end)
# named register: this step exposes process identity, mailbox flow, or failure isolation.
true = Process.register(pid, :actor_worker)
# named register: this step exposes process identity, mailbox flow, or failure isolation.
IO.inspect(Process.whereis(:actor_worker) == pid)
# named register: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, :stop)
```

Run: elixir main.exs.

## Example 25: Whereis Lookup

_ex-25-whereis-lookup · source-matched_

This script is rendered from learning/code/ex-25-whereis-lookup/main.exs.

```elixir
# whereis lookup: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do :stop -> :ok end end)
# whereis lookup: this step exposes process identity, mailbox flow, or failure isolation.
true = Process.register(pid, :lookup_worker)
# whereis lookup: this step exposes process identity, mailbox flow, or failure isolation.
IO.inspect(Process.whereis(:lookup_worker) == pid)
# whereis lookup: this step exposes process identity, mailbox flow, or failure isolation.
send(pid, :stop)
```

Run: elixir main.exs.

## Example 26: Send To Named

_ex-26-send-to-named · source-matched_

This script is rendered from learning/code/ex-26-send-to-named/main.exs.

```elixir
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
parent = self()
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
pid = spawn(fn -> receive do message -> send(parent, {:received, message}) end end)
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
true = Process.register(pid, :named_receiver)
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
send(:named_receiver, :hello)
# send to named: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:received, :hello} -> IO.puts("named delivery") end
```

Run: elixir main.exs.
