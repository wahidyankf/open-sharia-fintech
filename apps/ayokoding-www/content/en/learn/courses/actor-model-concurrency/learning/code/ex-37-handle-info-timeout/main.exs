# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
defmodule Timeout do
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
  use GenServer
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
  def init(_), do: {:ok,:waiting,1}
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
  def handle_info(:timeout,_), do: {:noreply,:fired}
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
  def handle_call(:get,_,s), do: {:reply,s,s}
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
end
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Timeout,nil)
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
Process.sleep(5)
# ex 37 handle info timeout: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid,:get))
