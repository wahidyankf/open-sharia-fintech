# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), :first)
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
send(self(), :second)
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
first = receive do message -> message end
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
second = receive do message -> message end
# mailbox fifo: this step exposes process identity, mailbox flow, or failure isolation.
IO.inspect({first, second})
