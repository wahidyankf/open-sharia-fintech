# A supervisor starts and owns children according to its restart strategy.
{:ok, supervisor} = Supervisor.start_link([{Agent, fn -> :ready end}], strategy: :one_for_one)

# which_children proves the declared child was actually started.
[{_id, child, :worker, _modules}] = Supervisor.which_children(supervisor)
if Agent.get(child, & &1) != :ready, do: raise("supervised child did not start")
IO.puts("supervisor started its child")
