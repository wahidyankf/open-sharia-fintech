text = "  hi  "
IO.inspect(text |> String.trim() |> String.upcase(), label: "data flows left to right")
