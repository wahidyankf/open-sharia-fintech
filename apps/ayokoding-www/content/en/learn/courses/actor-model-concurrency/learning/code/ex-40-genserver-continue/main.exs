# ex 40 genserver continue: explicit GenServer lifecycle behavior.
defmodule Continued do
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
 use GenServer
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
 def init(_), do: {:ok,:cold,{:continue,:warm}}
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
 def handle_continue(:warm,_), do: {:noreply,:warm}
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
 def handle_call(:get,_,s), do: {:reply,s,s}
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
end
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Continued,nil)
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
Process.sleep(1)
# ex 40 genserver continue: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid,:get))
