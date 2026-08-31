## Workload identity decision artifact

This is deliberately not a deployment manifest. Workload identity schema differs among Kubernetes
distributions and cloud providers, and an invented generic YAML shape cannot prove that a platform
will issue temporary credentials.

| Decision            | Recorded choice                                      |
| ------------------- | ---------------------------------------------------- |
| Identity name       | `service-reader`                                     |
| Permissions         | Read objects only in the service-assets bucket       |
| Credential delivery | Platform-issued, renewable temporary credentials     |
| Static keys         | Prohibited in source, images, manifests, and CI logs |

Implement the platform-specific binding only after selecting the target provider and validating it in
that provider's documented local or non-production environment.
