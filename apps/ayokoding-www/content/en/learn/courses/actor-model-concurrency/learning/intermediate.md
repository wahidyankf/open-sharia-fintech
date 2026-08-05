---
title: "Intermediate Actor Model"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 20
---

# Intermediate Actor Model

## Example 27: genserver minimal

_ex-27-genserver-minimal · source-matched_

```elixir
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
defmodule Minimal do
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
  use GenServer
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
  def init(value), do: {:ok, value}
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
  def handle_call(:ping, _from, value), do: {:reply, :pong, value}
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
end
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
{:ok, pid} = GenServer.start_link(Minimal, :state)
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid, :ping))
```

Run: elixir main.exs.

## Example 28: genserver state map

_ex-28-genserver-state-map · source-matched_

```elixir
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
defmodule MapServer do
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
  use GenServer
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
  def init(_), do: {:ok, %{}}
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
  def handle_call({:put, key, value}, _from, state), do: {:reply, :ok, Map.put(state, key, value)}
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
  def handle_call({:get, key}, _from, state), do: {:reply, Map.get(state, key), state}
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
end
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
{:ok, pid} = GenServer.start_link(MapServer, nil)
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
:ok = GenServer.call(pid, {:put, :name, "Ada"})
# ex 28 genserver state map: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid, {:get, :name}))
```

Run: elixir main.exs.

## Example 29: genserver start link

_ex-29-genserver-start-link · source-matched_

```elixir
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
defmodule Linked do
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
  use GenServer
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
  def init(value), do: {:ok, value}
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
end
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
{:ok, pid} = GenServer.start_link(Linked, :ready)
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
IO.inspect(Process.alive?(pid))
```

Run: elixir main.exs.

## Example 30: genserver init

_ex-30-genserver-init · source-matched_

```elixir
# ex 30 genserver init: explicit GenServer lifecycle behavior.
defmodule Initial do
# ex 30 genserver init: explicit GenServer lifecycle behavior.
  use GenServer
# ex 30 genserver init: explicit GenServer lifecycle behavior.
  def init(value), do: {:ok, %{value: value}}
# ex 30 genserver init: explicit GenServer lifecycle behavior.
  def handle_call(:state, _from, state), do: {:reply, state, state}
# ex 30 genserver init: explicit GenServer lifecycle behavior.
end
# ex 30 genserver init: explicit GenServer lifecycle behavior.
{:ok, pid} = GenServer.start_link(Initial, 7)
# ex 30 genserver init: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid, :state))
```

Run: elixir main.exs.

## Example 31: handle call sync

_ex-31-handle-call-sync · source-matched_

```elixir
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
defmodule Sync do
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
  use GenServer
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
  def init(_), do: {:ok, :ready}
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
  def handle_call(:wait, _from, state) do
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
    Process.sleep(5)
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
    {:reply, :replied, state}
# ex 31 handle call sync: explicit GenServer lifecycle behavior.

  end
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
end
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Sync,nil)
# ex 31 handle call sync: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid,:wait))
```

Run: elixir main.exs.

## Example 32: handle call reply

_ex-32-handle-call-reply · source-matched_

```elixir
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
defmodule Reply do
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
  use GenServer
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
  def init(value), do: {:ok,value}
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
  def handle_call(:next,_from,value), do: {:reply,value+1,value+1}
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
  def handle_call(:get,_from,value), do: {:reply,value,value}
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
end
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Reply,0)
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
IO.inspect({GenServer.call(pid,:next),GenServer.call(pid,:get)})
```

Run: elixir main.exs.

## Example 33: handle call backpressure

_ex-33-handle-call-backpressure · source-matched_

```elixir
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
defmodule Queue do
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
  use GenServer
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
  def init(_), do: {:ok,0}
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
  def handle_call(:work,_from,state) do
# backpressure: this line participates in queued synchronous work.
    Process.sleep(5)
# backpressure: this line participates in queued synchronous work.
    {:reply,state,state+1}
# backpressure: this line participates in queued synchronous work.
  end
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
end
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
{:ok,pid}=GenServer.start_link(Queue,nil)
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
results=for _<-1..2, do: Task.async(fn->GenServer.call(pid,:work) end)
# ex 33 handle call backpressure: explicit GenServer lifecycle behavior.
# backpressure: this line participates in queued synchronous work.
IO.inspect(Enum.map(results,&Task.await/1))
```

Run: elixir main.exs.

## Example 34: handle cast async

_ex-34-handle-cast-async · source-matched_

```elixir
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
defmodule Async do
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
  use GenServer
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
  def init(_), do: {:ok,0}
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
  def handle_cast(:add,state), do: {:noreply,state+1}
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
end
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Async,nil)
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.cast(pid,:add))
```

Run: elixir main.exs.

## Example 35: handle cast noreply

_ex-35-handle-cast-noreply · source-matched_

```elixir
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
defmodule CastState do
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
  use GenServer
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
  def init(v), do: {:ok,v}
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
  def handle_cast({:put,v},_), do: {:noreply,v}
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
  def handle_call(:get,_,v), do: {:reply,v,v}
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
end
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(CastState,:old)
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
GenServer.cast(pid,{:put,:new})
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
Process.sleep(1)
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid,:get))
```

Run: elixir main.exs.

## Example 36: handle info message

_ex-36-handle-info-message · source-matched_

```elixir
# ex 36 handle info message: explicit GenServer lifecycle behavior.
defmodule Info do
# ex 36 handle info message: explicit GenServer lifecycle behavior.
  use GenServer
# ex 36 handle info message: explicit GenServer lifecycle behavior.
  def init(_), do: {:ok,0}
# ex 36 handle info message: explicit GenServer lifecycle behavior.
  def handle_info(:tick,state), do: {:noreply,state+1}
# ex 36 handle info message: explicit GenServer lifecycle behavior.
  def handle_call(:get,_,state), do: {:reply,state,state}
# ex 36 handle info message: explicit GenServer lifecycle behavior.
end
# ex 36 handle info message: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Info,nil)
# ex 36 handle info message: explicit GenServer lifecycle behavior.
send(pid,:tick)
# ex 36 handle info message: explicit GenServer lifecycle behavior.
Process.sleep(1)
# ex 36 handle info message: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid,:get))
```

Run: elixir main.exs.

## Example 37: handle info timeout

_ex-37-handle-info-timeout · source-matched_

```elixir
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
defmodule Timeout do
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
  use GenServer
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
  def init(_), do: {:ok,:waiting,1}
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
  def handle_info(:timeout,_), do: {:noreply,:fired}
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
  def handle_call(:get,_,s), do: {:reply,s,s}
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
end
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Timeout,nil)
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
Process.sleep(5)
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid,:get))
```

Run: elixir main.exs.

## Example 38: client api wrapper

_ex-38-client-api-wrapper · source-matched_

```elixir
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
defmodule API do
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 use GenServer
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def start, do: GenServer.start_link(__MODULE__,0)
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def get(pid), do: GenServer.call(pid,:get)
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def put(pid,v), do: GenServer.cast(pid,{:put,v})
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def init(v), do: {:ok,v}
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def handle_call(:get,_,v), do: {:reply,v,v}
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def handle_cast({:put,v},_), do: {:noreply,v}
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
end
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
{:ok,pid}=API.start()
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
API.put(pid,9)
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
Process.sleep(1)
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
IO.inspect(API.get(pid))
```

Run: elixir main.exs.

## Example 39: genserver stop

_ex-39-genserver-stop · source-matched_

```elixir
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
defmodule Stoppable do
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
 use GenServer
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
 def init(_), do: {:ok,:ok}
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
end
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Stoppable,nil)
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
:ok=GenServer.stop(pid)
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
IO.inspect(Process.alive?(pid))
```

Run: elixir main.exs.

## Example 40: genserver continue

_ex-40-genserver-continue · source-matched_

```elixir
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
defmodule Continued do
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
 use GenServer
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
 def init(_), do: {:ok,:cold,{:continue,:warm}}
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
 def handle_continue(:warm,_), do: {:noreply,:warm}
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
 def handle_call(:get,_,s), do: {:reply,s,s}
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
end
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Continued,nil)
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
Process.sleep(1)
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid,:get))
```

Run: elixir main.exs.

## Example 41: agent simple state

_ex-41-agent-simple-state · source-matched_

```elixir
# agent simple state: make the OTP operation and lifecycle explicit.
{:ok, pid} = Agent.start_link(fn -> 0 end)
# agent simple state: make the OTP operation and lifecycle explicit.
Agent.update(pid, &(&1 + 1))
# agent simple state: make the OTP operation and lifecycle explicit.
IO.inspect(Agent.get(pid, & &1), label: "41-agent-simple-state")
```

Run: elixir main.exs.

## Example 42: agent get update

_ex-42-agent-get-update · source-matched_

```elixir
# agent get update: make the OTP operation and lifecycle explicit.
{:ok, pid} = Agent.start_link(fn -> 0 end)
# agent get update: make the OTP operation and lifecycle explicit.
Agent.update(pid, &(&1 + 1))
# agent get update: make the OTP operation and lifecycle explicit.
IO.inspect(Agent.get(pid, & &1), label: "42-agent-get-update")
```

Run: elixir main.exs.

## Example 43: agent vs genserver

_ex-43-agent-vs-genserver · source-matched_

```elixir
# agent vs genserver: make the OTP operation and lifecycle explicit.
{:ok, pid} = Agent.start_link(fn -> 0 end)
# agent vs genserver: make the OTP operation and lifecycle explicit.
Agent.update(pid, &(&1 + 1))
# agent vs genserver: make the OTP operation and lifecycle explicit.
IO.inspect(Agent.get(pid, & &1), label: "43-agent-vs-genserver")
```

Run: elixir main.exs.

## Example 44: task async await

_ex-44-task-async-await · source-matched_

```elixir
# task async await: make the OTP operation and lifecycle explicit.
task = Task.async(fn -> 6 * 7 end)
# task async await: make the OTP operation and lifecycle explicit.
IO.inspect(Task.await(task), label: "44-task-async-await")
```

Run: elixir main.exs.

## Example 45: task multiple parallel

_ex-45-task-multiple-parallel · source-matched_

```elixir
# task multiple parallel: make the OTP operation and lifecycle explicit.
task = Task.async(fn -> 6 * 7 end)
# task multiple parallel: make the OTP operation and lifecycle explicit.
IO.inspect(Task.await(task), label: "45-task-multiple-parallel")
```

Run: elixir main.exs.

## Example 46: task supervisor

_ex-46-task-supervisor · source-matched_

```elixir
# task supervisor: make the OTP operation and lifecycle explicit.
task = Task.async(fn -> 6 * 7 end)
# task supervisor: make the OTP operation and lifecycle explicit.
IO.inspect(Task.await(task), label: "46-task-supervisor")
```

Run: elixir main.exs.

## Example 47: registry start

_ex-47-registry-start · source-matched_

```elixir
# registry start: make the OTP operation and lifecycle explicit.
{:ok, registry} = Registry.start_link(keys: :unique, name: :example_registry)
# registry start: make the OTP operation and lifecycle explicit.
{:ok, _} = Registry.register(:example_registry, :worker, :value)
# registry start: make the OTP operation and lifecycle explicit.
IO.inspect(Registry.lookup(:example_registry, :worker), label: "47-registry-start")
```

Run: elixir main.exs.

## Example 48: registry via tuple

_ex-48-registry-via-tuple · source-matched_

```elixir
# registry via tuple: make the OTP operation and lifecycle explicit.
{:ok, registry} = Registry.start_link(keys: :unique, name: :example_registry)
# registry via tuple: make the OTP operation and lifecycle explicit.
{:ok, _} = Registry.register(:example_registry, :worker, :value)
# registry via tuple: make the OTP operation and lifecycle explicit.
IO.inspect(Registry.lookup(:example_registry, :worker), label: "48-registry-via-tuple")
```

Run: elixir main.exs.

## Example 49: registry unique keys

_ex-49-registry-unique-keys · source-matched_

```elixir
# registry unique keys: make the OTP operation and lifecycle explicit.
{:ok, registry} = Registry.start_link(keys: :unique, name: :example_registry)
# registry unique keys: make the OTP operation and lifecycle explicit.
{:ok, _} = Registry.register(:example_registry, :worker, :value)
# registry unique keys: make the OTP operation and lifecycle explicit.
IO.inspect(Registry.lookup(:example_registry, :worker), label: "49-registry-unique-keys")
```

Run: elixir main.exs.

## Example 50: registry duplicate keys

_ex-50-registry-duplicate-keys · source-matched_

```elixir
# registry duplicate keys: make the OTP operation and lifecycle explicit.
{:ok, registry} = Registry.start_link(keys: :unique, name: :example_registry)
# registry duplicate keys: make the OTP operation and lifecycle explicit.
{:ok, _} = Registry.register(:example_registry, :worker, :value)
# registry duplicate keys: make the OTP operation and lifecycle explicit.
IO.inspect(Registry.lookup(:example_registry, :worker), label: "50-registry-duplicate-keys")
```

Run: elixir main.exs.

## Example 51: genserver registered name

_ex-51-genserver-registered-name · source-matched_

```elixir
# genserver registered name: make the OTP operation and lifecycle explicit.
defmodule NamedServer do
  # genserver registered name: make the OTP operation and lifecycle explicit.
  use GenServer
  # genserver registered name: make the OTP operation and lifecycle explicit.
  def init(value), do: {:ok, value}
  # genserver registered name: make the OTP operation and lifecycle explicit.
  def handle_call(:get, _from, value), do: {:reply, value, value}
# genserver registered name: make the OTP operation and lifecycle explicit.
end
# genserver registered name: make the OTP operation and lifecycle explicit.
{:ok, _pid} = GenServer.start_link(NamedServer, 7, name: :named_server)
# genserver registered name: make the OTP operation and lifecycle explicit.
IO.inspect(GenServer.call(:named_server, :get), label: "51-genserver-registered-name")
```

Run: elixir main.exs.

## Example 52: genserver timeout call

_ex-52-genserver-timeout-call · source-matched_

```elixir
# genserver timeout call: make the OTP operation and lifecycle explicit.
defmodule NamedServer do
  # genserver timeout call: make the OTP operation and lifecycle explicit.
  use GenServer
  # genserver timeout call: make the OTP operation and lifecycle explicit.
  def init(value), do: {:ok, value}
  # genserver timeout call: make the OTP operation and lifecycle explicit.
  def handle_call(:get, _from, value), do: {:reply, value, value}
# genserver timeout call: make the OTP operation and lifecycle explicit.
end
# genserver timeout call: make the OTP operation and lifecycle explicit.
{:ok, _pid} = GenServer.start_link(NamedServer, 7, name: :named_server)
# genserver timeout call: make the OTP operation and lifecycle explicit.
IO.inspect(GenServer.call(:named_server, :get), label: "52-genserver-timeout-call")
```

Run: elixir main.exs.

## Example 53: genserver multi clause handle

_ex-53-genserver-multi-clause-handle · source-matched_

```elixir
# genserver multi clause handle: make the OTP operation and lifecycle explicit.
defmodule NamedServer do
  # genserver multi clause handle: make the OTP operation and lifecycle explicit.
  use GenServer
  # genserver multi clause handle: make the OTP operation and lifecycle explicit.
  def init(value), do: {:ok, value}
  # genserver multi clause handle: make the OTP operation and lifecycle explicit.
  def handle_call(:get, _from, value), do: {:reply, value, value}
# genserver multi clause handle: make the OTP operation and lifecycle explicit.
end
# genserver multi clause handle: make the OTP operation and lifecycle explicit.
{:ok, _pid} = GenServer.start_link(NamedServer, 7, name: :named_server)
# genserver multi clause handle: make the OTP operation and lifecycle explicit.
IO.inspect(GenServer.call(:named_server, :get), label: "53-genserver-multi-clause-handle")
```

Run: elixir main.exs.

## Example 54: genserver call cast choice

_ex-54-genserver-call-cast-choice · source-matched_

```elixir
# genserver call cast choice: make the OTP operation and lifecycle explicit.
defmodule NamedServer do
  # genserver call cast choice: make the OTP operation and lifecycle explicit.
  use GenServer
  # genserver call cast choice: make the OTP operation and lifecycle explicit.
  def init(value), do: {:ok, value}
  # genserver call cast choice: make the OTP operation and lifecycle explicit.
  def handle_call(:get, _from, value), do: {:reply, value, value}
# genserver call cast choice: make the OTP operation and lifecycle explicit.
end
# genserver call cast choice: make the OTP operation and lifecycle explicit.
{:ok, _pid} = GenServer.start_link(NamedServer, 7, name: :named_server)
# genserver call cast choice: make the OTP operation and lifecycle explicit.
IO.inspect(GenServer.call(:named_server, :get), label: "54-genserver-call-cast-choice")
```

Run: elixir main.exs.
