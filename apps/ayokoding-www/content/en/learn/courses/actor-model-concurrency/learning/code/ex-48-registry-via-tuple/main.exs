# A GenServer can be addressed through Registry instead of exposing its PID.
defmodule ViaCounter do
  use GenServer
  def init(v), do: {:ok, v}
  def handle_call(:get, _, v), do: {:reply, v, v}
end
{:ok, _} = Registry.start_link(keys: :unique, name: ViaRegistry)
via = {:via, Registry, {ViaRegistry, "worker"}}
{:ok, _} = GenServer.start_link(ViaCounter, 7, name: via)
IO.inspect(GenServer.call(via, :get))
