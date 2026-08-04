defmodule Service do
  use GenServer

  def via, do: {:via, Registry, {ActorRegistry, :service}}
  def start_link(_), do: GenServer.start_link(__MODULE__, 0, name: via())
  def get, do: GenServer.call(via(), :get)
  def add(value), do: GenServer.call(via(), {:add, value})
  def crash, do: GenServer.call(via(), :crash)

  def init(value), do: {:ok, value}
  def handle_call(:get, _from, value), do: {:reply, value, value}
  def handle_call({:add, n}, _from, value), do: {:reply, value + n, value + n}
  def handle_call(:crash, _from, _value), do: exit(:boom)
end
