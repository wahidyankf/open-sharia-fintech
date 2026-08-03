# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
defmodule API do
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 use GenServer
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def start, do: GenServer.start_link(__MODULE__,0)
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def get(pid), do: GenServer.call(pid,:get)
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def put(pid,v), do: GenServer.cast(pid,{:put,v})
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def init(v), do: {:ok,v}
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def handle_call(:get,_,v), do: {:reply,v,v}
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
 def handle_cast({:put,v},_), do: {:noreply,v}
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
end
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
{:ok,pid}=API.start()
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
API.put(pid,9)
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
Process.sleep(1)
# ex 38 client api wrapper: explicit GenServer lifecycle behavior.
IO.inspect(API.get(pid))
