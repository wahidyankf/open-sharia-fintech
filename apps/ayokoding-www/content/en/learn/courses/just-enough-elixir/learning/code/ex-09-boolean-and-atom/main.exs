# boolean and atom: this expression exposes the Elixir value or match being learned.
IO.inspect({true, :ok, is_boolean(true), is_atom(true), is_atom(:ok)})
