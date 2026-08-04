# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
parent = self()
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
value = 1
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
spawn(fn -> send(parent, {:copy, value + 1}) end)
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
receive do
  # process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
  {:copy, child_value} -> IO.inspect({value, child_value}, label: "parent and child values")
# process vs shared state: this expression makes the Elixir dispatch, transform, or message flow observable.
end
