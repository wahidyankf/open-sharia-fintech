# process lightweight: this expression makes the Elixir dispatch, transform, or message flow observable.
pids = for _ <- 1..10_000, do: spawn(fn -> :ok end)
# process lightweight: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.puts("spawned #{length(pids)} processes")
