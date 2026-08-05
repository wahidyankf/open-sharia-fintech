# ex 34 handle cast async: explicit GenServer lifecycle behavior.
defmodule Async do
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
  use GenServer
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
  def init(_), do: {:ok,0}
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
  def handle_cast(:add,state), do: {:noreply,state+1}
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
end
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Async,nil)
# ex 34 handle cast async: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.cast(pid,:add))
