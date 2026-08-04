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
