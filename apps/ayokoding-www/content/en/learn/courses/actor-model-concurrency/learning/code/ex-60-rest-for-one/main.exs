children = for id <- [:first, :middle, :last], do: %{id: id, start: {Agent, :start_link, [fn -> id end]}}

# rest_for_one keeps earlier children but restarts the crashed child and later siblings.
{:ok, supervisor} = Supervisor.start_link(children, strategy: :rest_for_one)
before = Map.new(Supervisor.which_children(supervisor), fn {id, pid, _, _} -> {id, pid} end)
Process.exit(before.middle, :kill)
Process.sleep(20)
after_crash = Map.new(Supervisor.which_children(supervisor), fn {id, pid, _, _} -> {id, pid} end)
if after_crash.first != before.first or after_crash.middle == before.middle or after_crash.last == before.last, do: raise("wrong restart scope")
IO.puts("middle and later children restarted")
Supervisor.stop(supervisor)
