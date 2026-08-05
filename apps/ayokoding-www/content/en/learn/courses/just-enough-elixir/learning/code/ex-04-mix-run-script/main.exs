# mix run script: make a disposable Mix project for a real mix run invocation.
project = Path.join(System.tmp_dir!(), "runner-#{System.unique_integer([:positive])}")
# mix run script: scaffold the project before executing its Mix task.
{_output, 0} = System.cmd("mix", ["new", project])
# mix run script: run the requested expression in the generated project.
{output, 0} = System.cmd("mix", ["run", "-e", "IO.puts(\"hi\")"], cd: project)
# mix run script: verify the task's observable output and clean only the temporary project.
true = String.contains?(output, "hi")
File.rm_rf!(project)
IO.puts("mix run printed hi")
