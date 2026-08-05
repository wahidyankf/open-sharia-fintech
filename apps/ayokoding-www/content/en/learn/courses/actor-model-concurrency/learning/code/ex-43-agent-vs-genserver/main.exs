# Agents are concise for state transformations without a message protocol.
{:ok, agent} = Agent.start_link(fn -> 0 end)
Agent.update(agent, &(&1 + 1))

defmodule CounterServer do
  use GenServer
  def start_link, do: GenServer.start_link(__MODULE__, 0)
  def increment(pid), do: GenServer.call(pid, :increment)
  def init(value), do: {:ok, value}
  # GenServer fits when the state needs an explicit synchronous protocol.
  def handle_call(:increment, _from, value), do: {:reply, value + 1, value + 1}
end

{:ok, server} = CounterServer.start_link()
if Agent.get(agent, & &1) != CounterServer.increment(server), do: raise("counters differ")
IO.puts("Agent is simple state; GenServer owns a protocol")
