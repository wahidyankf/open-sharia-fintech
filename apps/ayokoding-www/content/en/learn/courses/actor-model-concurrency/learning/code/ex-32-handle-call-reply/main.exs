# ex 32 handle call reply: explicit GenServer lifecycle behavior.
defmodule Reply do
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
  use GenServer
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
  def init(value), do: {:ok,value}
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
  def handle_call(:next,_from,value), do: {:reply,value+1,value+1}
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
  def handle_call(:get,_from,value), do: {:reply,value,value}
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
end
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Reply,0)
# ex 32 handle call reply: explicit GenServer lifecycle behavior.
IO.inspect({GenServer.call(pid,:next),GenServer.call(pid,:get)})
