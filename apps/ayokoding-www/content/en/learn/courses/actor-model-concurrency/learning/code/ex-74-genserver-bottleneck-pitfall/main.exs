# A single GenServer processes mailbox calls serially, so slow work becomes a bottleneck.
defmodule Bottleneck do
  use GenServer

  def start_link, do: GenServer.start_link(__MODULE__, 0)
  def work(pid), do: GenServer.call(pid, :work)

  @impl true
  def init(value), do: {:ok, value}

  @impl true
  def handle_call(:work, _from, value) do
    Process.sleep(50)
    {:reply, value + 1, value + 1}
  end
end

{:ok, server} = Bottleneck.start_link()
started_at = System.monotonic_time(:millisecond)
results = Task.async_stream(1..3, fn _ -> Bottleneck.work(server) end) |> Enum.to_list()
elapsed = System.monotonic_time(:millisecond) - started_at

if results != [{:ok, 1}, {:ok, 2}, {:ok, 3}] or elapsed < 140, do: raise("work was not serialized")

IO.puts("one GenServer serialized three slow requests in #{elapsed}ms")
