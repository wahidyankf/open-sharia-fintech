---
title: "IaC Forward Scaffold"
description: Why Terraform and Ansible surfaces are documented as commented-out forward scaffolds in the env-contract section until IaC is added.
when_to_use: Use when adding Terraform or Ansible to the repo and you need to activate the pre-staged env-contract entries.
category: explanation
subcategory: conventions
tags:
  - security
  - secrets
  - env-files
  - guard-env-file-access
  - naming
  - reproducibility
created: 2026-06-10
---

# IaC Forward Scaffold

Terraform and Ansible surfaces are documented in the `env-contract:` section of `repo-config.yml`
as **commented forward-scaffold** entries — syntactically present but inactive. Uncomment and fill
in `root` when IaC surfaces are added
to the repository. This prevents the drift guard from producing false findings before IaC exists while
ensuring the pattern is immediately available when it does.
