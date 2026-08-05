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
