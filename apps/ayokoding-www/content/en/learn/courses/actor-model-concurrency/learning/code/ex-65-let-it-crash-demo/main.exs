# Let the worker fail; its supervisor owns recovery instead of a local rescue block.
child = %{id: :worker, start: {Agent, :start_link, [fn -> :ready end]}, restart: :permanent}
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
[{:worker, old_pid, _, _}] = Supervisor.which_children(supervisor)
Process.exit(old_pid, :kill)
Process.sleep(20)
[{:worker, new_pid, _, _}] = Supervisor.which_children(supervisor)

if old_pid == new_pid, do: raise("worker was not recovered")

IO.puts("supervisor recovered the crashed worker")
Supervisor.stop(supervisor)
