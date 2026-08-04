child = %{
  id: :worker,
  start: {Task, :start_link, [fn -> Process.sleep(1_000) end]},
  restart: :temporary
}

# The explicit id and start tuple become the supervisor's child contract.
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one)
[{:worker, _pid, :worker, [Task]}] = Supervisor.which_children(supervisor)
if Supervisor.count_children(supervisor).active != 1, do: raise("child spec was ignored")
IO.puts("explicit child spec started :worker")
Supervisor.stop(supervisor)
