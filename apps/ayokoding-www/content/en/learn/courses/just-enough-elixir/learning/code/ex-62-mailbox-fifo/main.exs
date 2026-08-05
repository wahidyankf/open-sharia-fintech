# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), :first)
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
send(self(), :second)
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
first = receive do message -> message end
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
second = receive do message -> message end
# mailbox fifo: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({first, second})
