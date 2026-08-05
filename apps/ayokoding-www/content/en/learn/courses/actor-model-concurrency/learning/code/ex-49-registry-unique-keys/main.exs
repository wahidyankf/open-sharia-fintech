# A unique Registry key rejects a second owner.
{:ok, _} = Registry.start_link(keys: :unique, name: UniqueRegistry)
{:ok, _} = Registry.register(UniqueRegistry, :key, :first)
# The collision result identifies the existing owner.
IO.inspect(Registry.register(UniqueRegistry, :key, :second))
