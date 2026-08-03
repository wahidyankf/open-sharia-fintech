# Registry starts a local unique-key process store under a name.
{:ok, _pid} = Registry.start_link(keys: :unique, name: ExampleRegistry)
# The named registry is alive and ready for registrations.
IO.inspect(Process.whereis(ExampleRegistry) != nil)
