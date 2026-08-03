# A transient child is left stopped after a normal exit.
child = %{id: :worker, start: {Agent, :start_link, [fn -> :ready end]}, restart: :transient}
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
[{:worker, pid, _, _}] = Supervisor.which_children(supervisor)
Agent.stop(pid, :normal)
Process.sleep(20)

if Supervisor.which_children(supervisor) != [{:worker, :undefined, :worker, [Agent]}], do:
  raise("normal exit restarted a transient child")

IO.puts("transient child stayed stopped after a normal exit")
Supervisor.stop(supervisor)
