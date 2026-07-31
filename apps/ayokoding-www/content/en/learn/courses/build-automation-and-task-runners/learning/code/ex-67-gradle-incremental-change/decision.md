# Affected Gradle work

| Change                  | Consequence                                      |
| ----------------------- | ------------------------------------------------ |
| input.txt changes       | task declaring input.txt reruns                  |
| unrelated input changes | independent task remains eligible for UP-TO-DATE |

The scope follows explicit input edges, not an instruction to rebuild every task.
