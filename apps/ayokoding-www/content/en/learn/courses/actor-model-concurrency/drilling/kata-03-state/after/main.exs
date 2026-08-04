IO.inspect(Enum.reduce([1, 2], 0, &+/2), label: "threaded state")
