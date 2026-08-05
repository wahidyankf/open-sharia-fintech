# receive match: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), {:msg, "Ada"})
# receive match: this step exposes process identity, mailbox flow, or failure isolation.
receive do {:msg, name} -> IO.puts("matched #{name}") end
