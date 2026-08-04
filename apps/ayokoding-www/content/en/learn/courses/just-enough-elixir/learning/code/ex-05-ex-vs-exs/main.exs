# ex vs exs: this expression exposes the Elixir value or match being learned.
source = "defmodule Greeting do\n  def hello, do: :hello\nend"
# ex vs exs: this expression exposes the Elixir value or match being learned.
Code.compile_string(source)
# ex vs exs: this expression exposes the Elixir value or match being learned.
IO.inspect(Greeting.hello(), label: "compiled .ex intent")
# ex vs exs: this expression exposes the Elixir value or match being learned.
{result, _binding} = Code.eval_string(":hello")
# ex vs exs: this expression exposes the Elixir value or match being learned.
IO.inspect(result, label: "evaluated .exs intent")
