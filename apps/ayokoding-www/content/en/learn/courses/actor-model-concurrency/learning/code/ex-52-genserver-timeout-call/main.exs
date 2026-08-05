defmodule SlowServer do
  use GenServer
  def init(state), do: {:ok, state}
  # A caller-provided timeout protects callers from a slow mailbox handler.
  def handle_call(:slow, _from, state) do
    Process.sleep(200)
    {:reply, state, state}
  end
end

{:ok, pid} = GenServer.start_link(SlowServer, :ready)
try do
  GenServer.call(pid, :slow, 10)
catch
  :exit, {:timeout, _} -> IO.puts("call timed out")
end
