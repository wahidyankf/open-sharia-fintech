# lightweight many: this step exposes process identity, mailbox flow, or failure isolation.
pids = for _ <- 1..100_000, do: spawn(fn -> :ok end)
# lightweight many: this step exposes process identity, mailbox flow, or failure isolation.
IO.puts("spawned #{length(pids)} processes")
