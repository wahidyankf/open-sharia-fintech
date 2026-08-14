---
title: Coverage Metric, Diagram Use Cases, and Core-First Tooling
description: How security by-example tutorials measure coverage, use Mermaid diagrams, and introduce tools in core-first order across Beginner/Intermediate/Advanced levels.
category: explanation
subcategory: conventions
tags:
  - convention
  - tutorial
  - by-example
  - security
  - tool-output
created: 2026-05-21
when_to_use: Use when scoping coverage percentages, choosing which diagrams to include, or deciding when to introduce a specialized security tool.
---

# Coverage Metric, Diagram Use Cases, and Core-First Tooling

## Coverage metric

**SWE by-example**: 95% of language/framework features.

**Security by-example**: Coverage maps to the domain's primary framework:

- **Foundations (IT Security)**: Coverage of essential security controls — network, crypto,
  hardening, IAM, monitoring, incident response
- **Red Team**: Coverage of MITRE ATT&CK Enterprise tactics — Reconnaissance through Impact
- **Blue Team**: Coverage of MITRE ATT&CK detection surface — detection, triage, hunting,
  response per tactic

Coverage percentages per level follow the same pattern:

- Beginner: 0–40%
- Intermediate: 40–75%
- Advanced: 75–95%

## Mermaid diagram use cases

Security by-example diagrams visualize:

- **Attack chains**: Recon → Initial Access → Execution → Persistence → Lateral Movement
- **Kill chains**: Lockheed Martin or Unified Kill Chain phases
- **Network topologies**: Attacker, DMZ, internal segments, target hosts
- **Incident timelines**: Sequence of detected events leading to compromise
- **Detection logic**: Alert correlation flow, triage decision trees
- **TLS/PKI flows**: Certificate chain, handshake sequence

Same color-blind palette as SWE by-example applies (Blue #0173B2, Orange #DE8F05, Teal #029E73,
Purple #CC78BC, Brown #CA9161).

## Core-first principle for security tools

Apply the same "core features first" principle from [SWE By-Example](../swe-by-example.md), adapted
for security:

**Beginner level — built-in OS tools only (zero specialized tool installation)**:

- Network inspection: `ss`, `netstat`, `ip`, `ping`, `traceroute`, `dig`, `host`, `whois`
- Packet capture: `tcpdump` (ships with most Linux distros)
- Cryptography: `openssl` (standard), `sha256sum`, `gpg`
- File permissions: `ls`, `find`, `stat`, `chmod`, `chown`
- Log reading: `cat`, `grep`, `awk`, `journalctl`, `tail -f`
- SSH: `ssh`, `ssh-keygen`, `scp` (standard OpenSSH)
- Process inspection: `ps`, `top`, `lsof`, `strace`

**Intermediate level — introduce specialized tools with justification**:

- `nmap` — when `ss`/`netstat` are insufficient for remote host discovery
- `gobuster`/`ffuf` — when manual curl enumeration is too slow for coverage
- `Suricata`/`Snort` — when manual log parsing is insufficient for real-time detection
- `Splunk`/`Elastic` — when grep/awk are insufficient for correlation across log sources
- `Vault` — when environment variables are insufficient for secrets management
- Mark each introduction: "Note: This example uses [tool]. Install with: [command]"

**Advanced level — full ecosystem including frameworks**:

- `Metasploit`, `Mimikatz`, `BloodHound` — with explicit authorized-lab framing
- Cloud CLIs (`aws`, `az`, `gcloud`) for cloud security examples
- `volatility3`, `autopsy` for forensics
- SOAR platforms for detection automation
