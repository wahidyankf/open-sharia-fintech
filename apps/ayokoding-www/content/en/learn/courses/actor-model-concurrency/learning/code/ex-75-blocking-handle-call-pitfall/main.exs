# A synchronous handler that blocks longer than the caller timeout is a design hazard.
defmodule SlowCall do
  use GenServer

  def start_link, do: GenServer.start_link(__MODULE__, :ready)
  def slow(pid), do: GenServer.call(pid, :slow, 10)

  @impl true
  def init(state), do: {:ok, state}

  @impl true
  def handle_call(:slow, _from, state) do
    Process.sleep(50)
    {:reply, :done, state}
  end
end

{:ok, server} = SlowCall.start_link()

try do
  SlowCall.slow(server)
  raise("the call should have timed out")
catch
  :exit, {:timeout, _} -> IO.puts("blocking handle_call exceeded the caller timeout")
end
