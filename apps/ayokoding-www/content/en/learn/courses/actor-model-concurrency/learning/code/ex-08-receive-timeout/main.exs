# receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
receive do
  # receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
  :message -> IO.puts("received")
# receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
after
  # receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
  10 -> IO.puts("timeout")
# receive timeout: this step exposes process identity, mailbox flow, or failure isolation.
end
