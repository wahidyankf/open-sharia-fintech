# ex 29 genserver start link: explicit GenServer lifecycle behavior.
defmodule Linked do
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
  use GenServer
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
  def init(value), do: {:ok, value}
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
end
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
{:ok, pid} = GenServer.start_link(Linked, :ready)
# ex 29 genserver start link: explicit GenServer lifecycle behavior.
IO.inspect(Process.alive?(pid))
