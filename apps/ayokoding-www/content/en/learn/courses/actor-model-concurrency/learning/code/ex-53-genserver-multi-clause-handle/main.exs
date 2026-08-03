defmodule DispatchServer do
  use GenServer
  def init(value), do: {:ok, value}
  # Message patterns select distinct protocol clauses.
  def handle_call(:get, _from, value), do: {:reply, value, value}
  def handle_call({:put, value}, _from, _state), do: {:reply, :ok, value}
end

{:ok, pid} = GenServer.start_link(DispatchServer, 0)
:ok = GenServer.call(pid, {:put, 7})
if GenServer.call(pid, :get) != 7, do: raise("clause dispatch failed")
IO.puts("get and put clauses dispatched")
