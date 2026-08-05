children = [
  %{id: :first, start: {Agent, :start_link, [fn -> :first end]}},
  %{id: :second, start: {Agent, :start_link, [fn -> :second end]}}
]

# A supervisor starts every declared child before start_link returns.
{:ok, supervisor} = Supervisor.start_link(children, strategy: :one_for_one)
ids = Supervisor.which_children(supervisor) |> Enum.map(&elem(&1, 0)) |> Enum.sort()
if ids != [:first, :second], do: raise("not every child started")
IO.puts("both children started")
Supervisor.stop(supervisor)
