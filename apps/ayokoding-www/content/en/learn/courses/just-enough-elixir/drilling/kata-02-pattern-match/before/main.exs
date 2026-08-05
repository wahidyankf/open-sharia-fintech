value = {:ok, 4}
IO.inspect(elem(value, 1), label: "positional access loses the tag")
