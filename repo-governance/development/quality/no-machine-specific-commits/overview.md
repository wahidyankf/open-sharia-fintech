---
title: "Overview"
description: "The two classes of harm from machine-specific values entering git history: portability failures and information disclosure."
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
when_to_use: "Use when orienting to why machine-specific commits are prohibited."
---

# Overview

Every developer works on a different machine. Absolute paths, usernames, local IP addresses, and environment-specific configuration reflect one person's setup. When these values enter the git history, they cause two classes of harm:

1. **Portability failures**: Other contributors check out the code and tests or scripts reference a path that does not exist on their machine.
2. **Accidental information disclosure**: Usernames, local network addresses, or credentials committed to a shared (or public) repository become permanently visible in git history.

This practice defines what constitutes machine-specific information, where the line sits between prohibited values and acceptable test data, and how to handle runtime configuration correctly.
