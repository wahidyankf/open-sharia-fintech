# The application root owns each long-lived service in one supervision boundary.
defmodule ServiceRoot do
  use Supervisor

  def start_link, do: Supervisor.start_link(__MODULE__, :ok)

  @impl true
  def init(:ok) do
    children = [
      {Registry, keys: :unique, name: ServiceRegistry},
      {Agent, fn -> %{requests: 0} end}
    ]

    Supervisor.init(children, strategy: :one_for_one)
  end
end

{:ok, root} = ServiceRoot.start_link()
if Supervisor.count_children(root).active != 2, do: raise("application root missed a service")

IO.puts("application root owns registry and worker services")
Supervisor.stop(root)
