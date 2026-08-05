---
title: "Advanced Elixir"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 30
---

# Advanced Elixir

Run every source file with elixir main.exs.

## Example 55: Spawn Basic

_ex-55-spawn-basic · source-matched_

This runnable script is rendered from learning/code/ex-55-spawn-basic/main.exs.

```elixir
# spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, :ran) end)
# spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
  :ran -> IO.puts("spawned process ran")
# spawn basic: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 56: Spawn Returns Pid

_ex-56-spawn-returns-pid · source-matched_

This runnable script is rendered from learning/code/ex-56-spawn-returns-pid/main.exs.

```elixir
# spawn returns pid: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> receive do :stop -> :ok end end)
# spawn returns pid: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({is_pid(pid), Process.alive?(pid)})
# spawn returns pid: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, :stop)
```

Run: elixir main.exs.

## Example 57: Self Pid

_ex-57-self-pid · source-matched_

This runnable script is rendered from learning/code/ex-57-self-pid/main.exs.

```elixir
# self pid: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(self(), label: "current pid")
```

Run: elixir main.exs.

## Example 58: Send Message

_ex-58-send-message · source-matched_

This runnable script is rendered from learning/code/ex-58-send-message/main.exs.

```elixir
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> receive do message -> send(parent, {:delivered, message}) end end)
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:hello, self()})
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # send message: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:delivered, message} -> IO.inspect(message)
# send message: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 59: Receive Block

_ex-59-receive-block · source-matched_

This runnable script is rendered from learning/code/ex-59-receive-block/main.exs.

```elixir
# receive block: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), {:hello, "Ada"})
# receive block: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # receive block: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:hello, name} -> IO.puts("hello #{name}")
# receive block: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 60: Send Receive Roundtrip

_ex-60-send-receive-roundtrip · source-matched_

This runnable script is rendered from learning/code/ex-60-send-receive-roundtrip/main.exs.

```elixir
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn ->
  # send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  receive do
    # send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
    {:ping, from} -> send(from, {:pong, parent})
  # send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  end
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
end) |> send({:ping, self()})
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:pong, from} -> IO.inspect(from, label: "round trip from")
# send receive roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 61: Receive Pattern Match

_ex-61-receive-pattern-match · source-matched_

This runnable script is rendered from learning/code/ex-61-receive-pattern-match/main.exs.

```elixir
# receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), {:add, 2})
# receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), {:stop})
# receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
for _ <- 1..2 do
  # receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
  receive do
    # receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
    {:add, number} -> IO.puts("add #{number}")
    # receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
    :stop -> IO.puts("stop")
  # receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
  end
# receive pattern match: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 62: Mailbox Fifo

_ex-62-mailbox-fifo · source-matched_

This runnable script is rendered from learning/code/ex-62-mailbox-fifo/main.exs.

```elixir
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), :first)
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), :second)
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
first = receive do message -> message end
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
second = receive do message -> message end
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({first, second})
```

Run: elixir main.exs.

## Example 63: Process Isolation

_ex-63-process-isolation · source-matched_

This runnable script is rendered from learning/code/ex-63-process-isolation/main.exs.

```elixir
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> exit(:boom) end)
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
ref = Process.monitor(pid)
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:DOWN, ^ref, :process, ^pid, :boom} -> send(parent, :parent_survived)
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
  :parent_survived -> IO.puts("parent survived child crash")
# process isolation: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 64: Process Lightweight

_ex-64-process-lightweight · source-matched_

This runnable script is rendered from learning/code/ex-64-process-lightweight/main.exs.

```elixir
# process lightweight: this expression makes the Elixir dispatch, transform, or message flow observable.
pids = for _ <- 1..10_000, do: spawn(fn -> :ok end)
# process lightweight: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.puts("spawned #{length(pids)} processes")
```

Run: elixir main.exs.

## Example 65: Ping Pong Processes

_ex-65-ping-pong-processes · source-matched_

This runnable script is rendered from learning/code/ex-65-ping-pong-processes/main.exs.

```elixir
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
child = spawn(fn ->
  # ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
  send(parent, :ping)
  # ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
  receive do :pong -> send(parent, :done) end
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
end)
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do :ping -> send(child, :pong) end
# ping pong processes: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do :done -> IO.puts("ping pong complete") end
```

Run: elixir main.exs.

## Example 66: Spawn Closure Capture

_ex-66-spawn-closure-capture · source-matched_

This runnable script is rendered from learning/code/ex-66-spawn-closure-capture/main.exs.

```elixir
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
value = 42
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, {:captured, value}) end)
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:captured, captured} -> IO.inspect(captured)
# spawn closure capture: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 67: Receive Timeout

_ex-67-receive-timeout · source-matched_

This runnable script is rendered from learning/code/ex-67-receive-timeout/main.exs.

```elixir
# receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
  :message -> IO.puts("received")
# receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
after
  # receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
  10 -> IO.puts("timeout")
# receive timeout: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 68: Stateful Loop Process

_ex-68-stateful-loop-process · source-matched_

This runnable script is rendered from learning/code/ex-68-stateful-loop-process/main.exs.

```elixir
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Counter do
  # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
  def loop(total) do
    # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
    receive do
      # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
      {:add, number} -> loop(total + number)
      # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
      {:get, from} -> send(from, {:total, total}); loop(total)
      # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
      :stop -> :ok
    # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
    end
  # stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
  end
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> Counter.loop(0) end)
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:add, 3})
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:get, self()})
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do {:total, total} -> IO.inspect(total) end
# stateful loop process: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, :stop)
```

Run: elixir main.exs.

## Example 69: Pattern Match Messages

_ex-69-pattern-match-messages · source-matched_

This runnable script is rendered from learning/code/ex-69-pattern-match-messages/main.exs.

```elixir
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Adder do
  # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
  def loop(total) do
    # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
    receive do
      # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
      {:add, number} -> loop(total + number)
      # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
      {:get, from} -> send(from, {:total, total})
    # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
    end
  # pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
  end
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
pid = spawn(fn -> Adder.loop(0) end)
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:add, 5})
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
send(pid, {:get, self()})
# pattern match messages: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do {:total, total} -> IO.inspect(total) end
```

Run: elixir main.exs.

## Example 70: Pipe Transform Pipeline

_ex-70-pipe-transform-pipeline · source-matched_

This runnable script is rendered from learning/code/ex-70-pipe-transform-pipeline/main.exs.

```elixir
# pipe transform pipeline: this expression makes the Elixir dispatch, transform, or message flow observable.
result = [1, 2, 3] |> Enum.map(&(&1 * 2)) |> Enum.filter(&(&1 > 2)) |> Enum.sum()
# pipe transform pipeline: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(result)
```

Run: elixir main.exs.

## Example 71: Immutable Transform Chain

_ex-71-immutable-transform-chain · source-matched_

This runnable script is rendered from learning/code/ex-71-immutable-transform-chain/main.exs.

```elixir
# immutable transform chain: this expression makes the Elixir dispatch, transform, or message flow observable.
original = %{name: "ada", visits: 0}
# immutable transform chain: this expression makes the Elixir dispatch, transform, or message flow observable.
changed = original |> Map.update!(:name, &String.upcase/1) |> Map.update!(:visits, &(&1 + 1))
# immutable transform chain: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({original, changed})
```

Run: elixir main.exs.

## Example 72: Fold With Pattern

_ex-72-fold-with-pattern · source-matched_

This runnable script is rendered from learning/code/ex-72-fold-with-pattern/main.exs.

```elixir
# fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Fold do
  # fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  def sum(items), do: sum(items, 0)
  # fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp sum([], total), do: total
  # fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp sum([head | tail], total), do: sum(tail, total + head)
# fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# fold with pattern: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(Fold.sum([2, 3, 4]))
```

Run: elixir main.exs.

## Example 73: Map Reduce Pipeline

_ex-73-map-reduce-pipeline · source-matched_

This runnable script is rendered from learning/code/ex-73-map-reduce-pipeline/main.exs.

```elixir
# map reduce pipeline: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect([1, 2, 3] |> Enum.map(&(&1 * 2)) |> Enum.reduce(0, &+/2))
```

Run: elixir main.exs.

## Example 74: String Word Count

_ex-74-string-word-count · source-matched_

This runnable script is rendered from learning/code/ex-74-string-word-count/main.exs.

```elixir
# string word count: this expression makes the Elixir dispatch, transform, or message flow observable.
counts = "red blue red" |> String.split() |> Enum.reduce(%{}, fn word, acc -> Map.update(acc, word, 1, &(&1 + 1)) end)
# string word count: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect(counts)
```

Run: elixir main.exs.

## Example 75: Spawn Worker Compute

_ex-75-spawn-worker-compute · source-matched_

This runnable script is rendered from learning/code/ex-75-spawn-worker-compute/main.exs.

```elixir
# spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, {:result, 6 * 7}) end)
# spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:result, value} -> IO.inspect(value)
# spawn worker compute: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 76: Process Vs Shared State

_ex-76-process-vs-shared-state · source-matched_

This runnable script is rendered from learning/code/ex-76-process-vs-shared-state/main.exs.

```elixir
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
value = 1
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, {:copy, value + 1}) end)
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:copy, child_value} -> IO.inspect({value, child_value}, label: "parent and child values")
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.

## Example 77: Mix Module End To End

_ex-77-mix-module-end-to-end · source-matched_

This runnable script is rendered from learning/code/ex-77-mix-module-end-to-end/main.exs.

```elixir
# mix module end to end: run the colocated Mix test suite from this example directory.
{output, 0} = System.cmd("mix", ["test"], cd: __DIR__)
# mix module end to end: require the real test summary before reporting success.
true = String.contains?(output, "0 failures")
# mix module end to end: expose the verified local Mix workflow.
IO.puts("mix test passed")
```

Run: elixir main.exs.

## Example 78: Capstone Preview Roundtrip

_ex-78-capstone-preview-roundtrip · source-matched_

This runnable script is rendered from learning/code/ex-78-capstone-preview-roundtrip/main.exs.

```elixir
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
defmodule Preview do
  # capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  def total(items), do: items |> Enum.map(&(&1 * 2)) |> sum()
  # capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp sum([]), do: 0
  # capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  defp sum([head | tail]), do: head + sum(tail)
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
end
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, {:total, Preview.total([1, 2, 3])}) end)
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:total, value} -> IO.inspect(value, label: "round trip total")
# capstone preview roundtrip: this expression makes the Elixir dispatch, transform, or message flow observable.
end
```

Run: elixir main.exs.
