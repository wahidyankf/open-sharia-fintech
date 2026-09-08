---
description: "Defines the three leak categories, exclusions, and canonical rule sources."
when_to_use: "Use when deciding whether a candidate is a real leak."
---

# Scope and Exclusions

Inspect exactly three categories:

1. Real secrets, credentials, private values, or other values that grant access.
2. Production/staging properties that policy requires in environment or secret storage rather
   than tracked artifacts.
3. Real machine-specific absolute filesystem paths.

Public identifiers, documented public values, obvious examples/placeholders, portable repository-
relative paths, and intentionally synthetic fixtures are not leaks. Treat ambiguity as a finding
only when repository context and value shape establish that the value is real or protected. A name
containing `key`, `token`, `secret`, `prod`, or `stag` is not sufficient evidence.

Apply the canonical definitions:

- [No Secrets in Committed Files](../../../conventions/security/secrets-and-env-standards/hard-iron-rule-no-secrets-in-committed-files.md)
  and [Guard Env-File Access Policy](../../../conventions/security/secrets-and-env-standards/guard-env-file-access-policy.md).
- [Hardcoded Environment Configuration](../../../development/workflow/anti-patterns/hardcoded-environment-configuration.md).
- [No Machine-Specific Commits](../../../development/quality/no-machine-specific-commits.md),
  especially [What Counts as Machine-Specific Information](../../../development/quality/no-machine-specific-commits/what-counts-as-machine-specific-information.md).
