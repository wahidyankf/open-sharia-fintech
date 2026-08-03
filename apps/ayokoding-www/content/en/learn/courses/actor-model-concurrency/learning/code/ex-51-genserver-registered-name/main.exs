# A registered atom lets callers use a stable service name instead of a PID.
defmodule NamedServer do
  use GenServer

  def start_link(value), do: GenServer.start_link(__MODULE__, value, name: :named_server)
  def value, do: GenServer.call(:named_server, :get)

  @impl true
  def init(value), do: {:ok, value}

  @impl true
  def handle_call(:get, _from, value), do: {:reply, value, value}
end

{:ok, _pid} = NamedServer.start_link(7)
if NamedServer.value() != 7, do: raise("registered name did not resolve the server")

IO.puts("atom name routed a call to the GenServer")
