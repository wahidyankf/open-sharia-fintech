defmodule ServiceTest do
  use ExUnit.Case

  test "registry resolves a supervised service after induced crash" do
    children = [{Registry, keys: :unique, name: ActorRegistry}, {Service, []}]
    {:ok, supervisor} = Supervisor.start_link(children, strategy: :one_for_one)
    assert [{pid, _}] = Registry.lookup(ActorRegistry, :service)
    assert Service.add(2) == 2
    catch_exit(Service.crash())
    Process.sleep(10)
    assert [{restarted, _}] = Registry.lookup(ActorRegistry, :service)
    refute restarted == pid
    assert Service.get() == 0
    Supervisor.stop(supervisor)
  end
end
