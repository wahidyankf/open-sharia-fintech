# A Registry name survives the worker PID changing during a supervised restart.
defmodule RecoveringCounter do
  use GenServer

  def start_link(name), do: GenServer.start_link(__MODULE__, 0, name: name)
  def value(name), do: GenServer.call(name, :value)
  def crash(name), do: GenServer.call(name, :crash)

  @impl true
  def init(value), do: {:ok, value}

  @impl true
  def handle_call(:value, _from, value), do: {:reply, value, value}
  def handle_call(:crash, _from, value), do: {:stop, :simulated_failure, value}
end

name = {:via, Registry, {RecoveryRegistry, :authoring_service}}
children = [{Registry, keys: :unique, name: RecoveryRegistry}, {RecoveringCounter, name}]
{:ok, supervisor} = Supervisor.start_link(children, strategy: :one_for_one)

try do
  RecoveringCounter.crash(name)
catch
  :exit, _ -> :expected_failure
end

Process.sleep(20)
if RecoveringCounter.value(name) != 0, do: raise("recovered service is not reachable")

IO.puts("registry name reaches the service after recovery")
Supervisor.stop(supervisor)
