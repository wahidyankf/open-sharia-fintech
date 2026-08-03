first = %{id: :first, start: {Agent, :start_link, [fn -> :first end]}}
second = %{id: :second, start: {Agent, :start_link, [fn -> :second end]}}

# one_for_all restarts every sibling when one child crashes.
{:ok, supervisor} = Supervisor.start_link([first, second], strategy: :one_for_all)
before = Map.new(Supervisor.which_children(supervisor), fn {id, pid, _, _} -> {id, pid} end)
Process.exit(before.first, :kill)
Process.sleep(20)
after_crash = Map.new(Supervisor.which_children(supervisor), fn {id, pid, _, _} -> {id, pid} end)
if after_crash.first == before.first or after_crash.second == before.second, do: raise("siblings not restarted")
IO.puts("all children restarted")
Supervisor.stop(supervisor)
