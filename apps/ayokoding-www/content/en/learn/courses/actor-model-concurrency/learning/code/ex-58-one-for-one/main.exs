first = %{id: :first, start: {Agent, :start_link, [fn -> :first end]}}
second = %{id: :second, start: {Agent, :start_link, [fn -> :second end]}}

# one_for_one restarts only the child that crashes.
{:ok, supervisor} = Supervisor.start_link([first, second], strategy: :one_for_one)
children = Map.new(Supervisor.which_children(supervisor), fn {id, pid, _, _} -> {id, pid} end)
Process.exit(children.first, :kill)
Process.sleep(20)
after_crash = Map.new(Supervisor.which_children(supervisor), fn {id, pid, _, _} -> {id, pid} end)
if after_crash.first == children.first or after_crash.second != children.second, do: raise("wrong restart scope")
IO.puts("only crashed child restarted")
Supervisor.stop(supervisor)
