---
description: "The reproducibility, explicit-config, and root-cause principles, and the file-naming and no-secrets conventions this practice implements."
when_to_use: "Use when tracing this practice to the principles/conventions it implements."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: A repository that embeds absolute local paths or machine usernames only works on the committing developer's machine. Keeping commits machine-neutral ensures every contributor can check out, build, and run the project identically.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Runtime configuration that differs per environment belongs in explicit environment variables or `.env` files — not implicitly baked into source code where its machine-specific origin is invisible.

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: Machine-specific paths appearing in committed files are a symptom of missing environment variable usage or missing `.env.example` templates. This practice fixes the root cause rather than patching individual leaks after the fact.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[File Naming Convention](../../../conventions/structure/file-naming.md)**: Configuration template files follow the standard naming pattern (e.g., `.env.example`) so they are discoverable and version-controlled without exposing real values.

- **[No Secrets in Git Convention](../../../conventions/security/no-secrets-in-committed-files.md)**: The credential/secret subset of machine-specific information is governed by the hard iron rule — no system secret may ever be committed; real values stay in uncommitted `.env*` files.
