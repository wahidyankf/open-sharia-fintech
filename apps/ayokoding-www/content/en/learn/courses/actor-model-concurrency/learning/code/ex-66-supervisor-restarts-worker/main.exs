# This worker exits on demand so its supervisor can demonstrate recovery.
defmodule CrashableWorker do
  use GenServer

  def start_link(_), do: GenServer.start_link(__MODULE__, :ready)
  def crash(pid), do: GenServer.call(pid, :crash)

  @impl true
  def init(state), do: {:ok, state}

  @impl true
  def handle_call(:crash, _from, state), do: {:stop, :simulated_failure, state}
end

{:ok, supervisor} = Supervisor.start_link([{CrashableWorker, []}], strategy: :one_for_one)
[{CrashableWorker, old_pid, _, _}] = Supervisor.which_children(supervisor)

try do
  CrashableWorker.crash(old_pid)
catch
  :exit, _ -> :expected_failure
end

Process.sleep(20)
[{CrashableWorker, new_pid, _, _}] = Supervisor.which_children(supervisor)
if old_pid == new_pid, do: raise("GenServer was not restarted")

IO.puts("supervisor restarted the failed GenServer")
Supervisor.stop(supervisor)
