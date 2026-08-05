defmodule Example77.FormatterTest do
  use ExUnit.Case

  test "public API formats a title" do
    assert Example77.Formatter.title("elixir") == "ELIXIR"
  end
end
