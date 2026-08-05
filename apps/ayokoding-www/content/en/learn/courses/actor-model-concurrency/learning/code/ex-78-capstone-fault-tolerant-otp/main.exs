# This compact preview mirrors the capstone's registry-addressed recovery boundary.
defmodule PreviewService do
  use GenServer

  def start_link(name), do: GenServer.start_link(__MODULE__, :ready, name: name)
  def status(name), do: GenServer.call(name, :status)
  def crash(name), do: GenServer.call(name, :crash)

  @impl true
  def init(state), do: {:ok, state}

  @impl true
  def handle_call(:status, _from, state), do: {:reply, state, state}
  def handle_call(:crash, _from, state), do: {:stop, :preview_failure, state}
end

name = {:via, Registry, {PreviewRegistry, :service}}
children = [{Registry, keys: :unique, name: PreviewRegistry}, {PreviewService, name}]
{:ok, supervisor} = Supervisor.start_link(children, strategy: :one_for_one)

try do
  PreviewService.crash(name)
catch
  :exit, _ -> :expected_failure
end

Process.sleep(20)
if PreviewService.status(name) != :ready, do: raise("supervised capstone preview did not recover")

IO.puts("registry-addressed OTP service recovered from a crash")
Supervisor.stop(supervisor)
