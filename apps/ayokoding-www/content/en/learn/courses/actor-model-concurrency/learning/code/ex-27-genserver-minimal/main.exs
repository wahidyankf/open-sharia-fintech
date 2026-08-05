# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
defmodule Minimal do
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
  use GenServer
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
  def init(value), do: {:ok, value}
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
  def handle_call(:ping, _from, value), do: {:reply, :pong, value}
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
end
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
{:ok, pid} = GenServer.start_link(Minimal, :state)
# ex 27 genserver minimal: explicit GenServer lifecycle behavior.
IO.inspect(GenServer.call(pid, :ping))
