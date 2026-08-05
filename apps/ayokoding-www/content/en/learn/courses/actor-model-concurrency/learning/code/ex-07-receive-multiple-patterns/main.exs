# receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), {:add, 2})
# receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), :stop)
# receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
for _ <- 1..2 do
  # receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
  receive do
    # receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
    {:add, value} -> IO.puts("add #{value}")
    # receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
    :stop -> IO.puts("stop")
  # receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
  end
# receive multiple patterns: this step exposes process identity, mailbox flow, or failure isolation.
end
