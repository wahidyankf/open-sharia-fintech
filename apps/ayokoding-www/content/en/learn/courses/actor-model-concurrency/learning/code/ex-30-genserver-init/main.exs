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
