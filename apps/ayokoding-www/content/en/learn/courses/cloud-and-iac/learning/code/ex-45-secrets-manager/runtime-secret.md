## Runtime secret-reference decision artifact

This is deliberately not YAML. Secret-manager reference fields and injection mechanisms are
provider-specific; an invented generic schema would not run and could encourage unsafe copying.

| Decision             | Recorded choice                                             |
| -------------------- | ----------------------------------------------------------- |
| Stored configuration | A secret reference, never a plaintext value                 |
| Runtime identity     | `service-reader-role` with narrowly scoped read permission  |
| Rotation             | The application handles renewed values without logging them |
| State and logs       | Never contain the secret value                              |

Choose the provider's documented secret-reference mechanism only after choosing the target runtime.
