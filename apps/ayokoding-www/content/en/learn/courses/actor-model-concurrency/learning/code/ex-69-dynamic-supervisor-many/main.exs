# The dynamic tree can grow without declaring a fixed child list in advance.
{:ok, supervisor} = DynamicSupervisor.start_link(strategy: :one_for_one)

workers =
  for number <- 1..3 do
    {:ok, pid} = DynamicSupervisor.start_child(supervisor, {Agent, fn -> number end})
    pid
  end

values = Enum.map(workers, &Agent.get(&1, fn value -> value end))
if values != [1, 2, 3], do: raise("dynamic supervisor lost a worker value")
if DynamicSupervisor.count_children(supervisor).active != 3, do: raise("not all dynamic children started")

IO.puts("dynamic supervisor started three independent workers")
DynamicSupervisor.stop(supervisor)
