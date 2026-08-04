defmodule WorkerGroup do
  use Supervisor

  def start_link(_), do: Supervisor.start_link(__MODULE__, :ok)

  @impl true
  def init(_) do
    children = [
      Supervisor.child_spec({Agent, fn -> :first end}, id: :first_worker),
      Supervisor.child_spec({Agent, fn -> :second end}, id: :second_worker)
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end

# The root supervises a supervisor, which in turn supervises two workers.
{:ok, root} = Supervisor.start_link([{WorkerGroup, []}], strategy: :one_for_one)
[{WorkerGroup, group, :supervisor, _}] = Supervisor.which_children(root)

if Supervisor.count_children(group).active != 2, do: raise("nested supervisor did not start both workers")

IO.puts("root supervisor started a nested worker group")
Supervisor.stop(root)
