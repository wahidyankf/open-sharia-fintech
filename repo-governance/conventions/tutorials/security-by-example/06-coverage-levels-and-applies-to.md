---
title: Coverage Levels and Applies To
description: The Beginner/Intermediate/Advanced coverage-level definitions for security by-example content and which ayokoding-www tracks this convention governs.
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - security
  - tool-output
created: 2026-05-21
when_to_use: Use when assigning an example to a coverage level or checking whether a security content track falls under this convention.
---

# Coverage Levels and Applies To

## Coverage Levels

### Beginner (Examples 1–28, 0–40%)

**Focus**: Security fundamentals every engineer should know.

- Built-in OS tools only (zero specialized installs)
- Network basics: reading packet captures, firewall rules, port states
- Cryptography basics: symmetric/asymmetric encryption, hashing, TLS handshake
- System hardening: file permissions, SSH config, PAM, log reading
- Foundational concepts: CVE/CVSS, vulnerability classes, log formats

**Self-containment**: Runnable on any Ubuntu 22.04 LTS install with no additional packages.

### Intermediate (Examples 29–57, 40–75%)

**Focus**: Production-grade controls and specialized tool usage.

- Introduce specialized tools with explicit installation instructions
- Domain-specific patterns: SIEM queries, IDS rules, cloud IAM misconfigs, AD enumeration
- Incident response lifecycle, forensic triage, credential management
- Defender perspective: detection rules, log correlation, alert triage

### Advanced (Examples 58–85, 75–95%)

**Focus**: Expert-level techniques, frameworks, and full-chain scenarios.

- Full attack/defense lifecycle scenarios
- Framework-level tooling: Metasploit, Mimikatz, volatility3, SOAR
- Advanced detection engineering, threat hunting, purple team exercises
- Cloud-native security, container/Kubernetes hardening

## Applies To

This convention governs security by-example content in ayokoding-www:

- `information-security/foundations/by-example/` — IT security foundations track
- `information-security/roles/red-team/by-example/` — Red Team offensive track
- `information-security/roles/blue-team/by-example/` — Blue Team defensive track

The CISO track (`information-security/roles/ciso/by-example/`) is governed by the
[Scenario By-Example Tutorial Convention](../scenario-by-example.md), not this convention.
