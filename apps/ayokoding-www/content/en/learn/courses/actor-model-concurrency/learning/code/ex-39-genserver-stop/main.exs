# ex 39 genserver stop: explicit GenServer lifecycle behavior.
defmodule Stoppable do
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
 use GenServer
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
 def init(_), do: {:ok,:ok}
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
end
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
{:ok,pid}=GenServer.start_link(Stoppable,nil)
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
:ok=GenServer.stop(pid)
# ex 39 genserver stop: explicit GenServer lifecycle behavior.
IO.inspect(Process.alive?(pid))
