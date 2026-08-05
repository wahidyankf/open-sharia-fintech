defmodule ChoiceServer do
  use GenServer
  def init(value), do: {:ok, value}
  # Calls reply immediately; casts intentionally provide no acknowledgement.
  def handle_call(:read, _from, value), do: {:reply, value, value}
  def handle_cast({:write, value}, _state), do: {:noreply, value}
end

{:ok, pid} = GenServer.start_link(ChoiceServer, 0)
:ok = GenServer.cast(pid, {:write, 9})
Process.sleep(10)
if GenServer.call(pid, :read) != 9, do: raise("cast state missing")
IO.puts("call replies; cast is asynchronous")
