child = %{id: :worker, start: {Agent, :start_link, [fn -> :ready end]}, restart: :temporary}

# Temporary children are deliberately not restarted, even after an abnormal exit.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
[{:worker, pid, _, _}] = Supervisor.which_children(supervisor)
Process.exit(pid, :kill)
Process.sleep(20)
if Supervisor.which_children(supervisor) != [], do: raise("temporary child restarted")
IO.puts("temporary child stayed stopped")
Supervisor.stop(supervisor)
