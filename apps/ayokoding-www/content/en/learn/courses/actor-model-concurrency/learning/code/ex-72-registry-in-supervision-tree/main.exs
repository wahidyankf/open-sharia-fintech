# The worker registers itself through the Registry child that starts first.
defmodule NamedCounter do
  use GenServer

  def start_link(name), do: GenServer.start_link(__MODULE__, 0, name: name)
  def increment(name), do: GenServer.call(name, :increment)

  @impl true
  def init(value), do: {:ok, value}

  @impl true
  def handle_call(:increment, _from, value), do: {:reply, value + 1, value + 1}
end

children = [
  {Registry, keys: :unique, name: CounterRegistry},
  {NamedCounter, {:via, Registry, {CounterRegistry, :draft_counter}}}
]

{:ok, supervisor} = Supervisor.start_link(children, strategy: :one_for_one)
name = {:via, Registry, {CounterRegistry, :draft_counter}}
if NamedCounter.increment(name) != 1, do: raise("registry name did not route to the counter")

IO.puts("supervision tree started a registry-named counter")
Supervisor.stop(supervisor)
