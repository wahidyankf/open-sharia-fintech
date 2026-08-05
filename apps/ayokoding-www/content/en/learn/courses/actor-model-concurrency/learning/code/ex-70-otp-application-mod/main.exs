defmodule CourseApplication do
  use Application

  @impl true
  def start(_type, _args) do
    Supervisor.start_link([{Registry, keys: :unique, name: CourseRegistry}], strategy: :one_for_one)
  end
end

# An Application callback returns the supervision tree that OTP starts.
{:ok, supervisor} = CourseApplication.start(:normal, [])
Process.unlink(supervisor)
{:ok, _} = Registry.register(CourseRegistry, :authoring, :ready)

if Registry.lookup(CourseRegistry, :authoring) == [], do: raise("application registry is unavailable")

IO.puts("application callback started its registry")
