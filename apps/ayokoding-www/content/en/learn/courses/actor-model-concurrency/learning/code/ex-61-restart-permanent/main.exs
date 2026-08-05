child = %{id: :worker, start: {Agent, :start_link, [fn -> :ready end]}, restart: :permanent}

# A permanent child is restarted even when it exits with :normal.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
[{:worker, before, _, _}] = Supervisor.which_children(supervisor)
Agent.stop(before, :normal)
Process.sleep(20)
[{:worker, after_stop, _, _}] = Supervisor.which_children(supervisor)
if after_stop == before, do: raise("permanent child did not restart")
IO.puts("normal exit restarted permanent child")
Supervisor.stop(supervisor)
