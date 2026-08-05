# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
defmodule CastState do
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
  use GenServer
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
  def init(v), do: {:ok,v}
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
  def handle_cast({:put,v},_), do: {:noreply,v}
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
  def handle_call(:get,_,v), do: {:reply,v,v}
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
end
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(CastState,:old)
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
GenServer.cast(pid,{:put,:new})
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
Process.sleep(1)
# ex 35 handle cast noreply: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid,:get))
