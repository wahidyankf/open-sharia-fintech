# mix module end to end: run the colocated Mix test suite from this example directory.
{output, 0} = System.cmd("mix", ["test"], cd: __DIR__)
# mix module end to end: require the real test summary before reporting success.
true = String.contains?(output, "0 failures")
# mix module end to end: expose the verified local Mix workflow.
IO.puts("mix test passed")
