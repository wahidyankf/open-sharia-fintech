# Trap the supervisor's shutdown so the demonstration process can inspect it.
Process.flag(:trap_exit, true)
child = %{id: :worker, start: {Agent, :start_link, [fn -> :ready end]}, restart: :permanent}
{:ok, supervisor} = Supervisor.start_link([child], strategy: :one_for_one, max_restarts: 2, max_seconds: 1)

# The third crash exceeds the configured restart intensity.
for _ <- 1..3 do
  [{:worker, pid, _, _}] = Supervisor.which_children(supervisor)
  Process.exit(pid, :kill)
  Process.sleep(20)
end

receive do
  {:EXIT, ^supervisor, :shutdown} -> IO.puts("supervisor stopped after its restart limit")
after
  200 -> raise("supervisor did not enforce its restart limit")
end
