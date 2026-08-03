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
