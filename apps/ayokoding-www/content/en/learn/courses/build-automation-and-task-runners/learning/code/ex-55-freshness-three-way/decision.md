# Three execution policies

| Tool family     | Policy                                               |
| --------------- | ---------------------------------------------------- |
| GNU Make        | compare declared input and output modification times |
| Bazel or Gradle | fingerprint declared action inputs and cache results |
| just            | execute each requested recipe                        |

The tools can be composed, but no composition changes the policy owned by the called tool.
