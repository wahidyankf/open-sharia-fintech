# pin operator: this expression exposes the Elixir value or match being learned.
x = 1
# pin operator: this expression exposes the Elixir value or match being learned.
try do
  # pin operator: this expression exposes the Elixir value or match being learned.
  ^x = 2
# pin operator: this expression exposes the Elixir value or match being learned.
rescue
  # pin operator: this expression exposes the Elixir value or match being learned.
  MatchError -> IO.puts("pin preserved x=#{x}")
# pin operator: this expression exposes the Elixir value or match being learned.
end
