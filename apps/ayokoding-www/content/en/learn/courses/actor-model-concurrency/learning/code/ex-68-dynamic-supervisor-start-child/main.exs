# DynamicSupervisor starts workers only when the application asks for them.
{:ok, supervisor} = DynamicSupervisor.start_link(strategy: :one_for_one)
{:ok, child} = DynamicSupervisor.start_child(supervisor, {Agent, fn -> :draft end})

if Agent.get(child, & &1) != :draft, do: raise("dynamic supervisor did not start the requested child")

IO.puts("dynamic supervisor started one on-demand worker")
DynamicSupervisor.stop(supervisor)
