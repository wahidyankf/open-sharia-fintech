# mix new project: allocate an isolated temporary target before scaffolding.
project = Path.join(System.tmp_dir!(), "greeter-#{System.unique_integer([:positive])}")
# mix new project: mix creates the actual project rather than a printed imitation.
{_output, 0} = System.cmd("mix", ["new", project])
# mix new project: assert the structural artifacts promised by mix new.
true = File.exists?(Path.join(project, "mix.exs"))
true = File.exists?(Path.join(project, "lib/greeter.ex"))
# mix new project: remove only the temporary project this script created.
File.rm_rf!(project)
IO.puts("mix new created mix.exs and lib/greeter.ex")
