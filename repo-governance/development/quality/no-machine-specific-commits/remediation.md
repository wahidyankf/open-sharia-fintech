---
title: "Remediation"
description: "The steps to fix an already-committed machine-specific value, including credential rotation for sensitive leaks."
category: explanation
subcategory: development
tags:
  - git
  - commits
  - security
  - portability
  - environment
  - quality
created: 2026-03-24
when_to_use: "Use when machine-specific information has already been committed and needs remediation."
---

# Remediation

If machine-specific information has already been committed:

1. Remove the value from the current working tree and replace it with an environment variable reference or relative path.
2. Commit the corrected version.
3. If the value was sensitive (a credential or API key), rotate the credential immediately — git
   history is permanent and the value is considered exposed even after removal from HEAD. See the
   [No Secrets in Git Convention](../../../conventions/security/no-secrets-in-committed-files.md) for the complete
   remediation procedure and the full definition of what counts as a system secret.

For non-sensitive path leaks (e.g., a developer's home directory appeared in a test), a simple corrective commit is sufficient.
