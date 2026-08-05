# capture operator: this expression makes the Elixir dispatch, transform, or message flow observable.
double = &(&1 * 2)
# capture operator: this expression makes the Elixir dispatch, transform, or message flow observable.
upcase = &String.upcase/1
# capture operator: this expression makes the Elixir dispatch, transform, or message flow observable.
IO.inspect({double.(3), upcase.("hi")})
