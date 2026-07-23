---
title: "Overview"
weight: 10000000
date: 2026-05-21T00:00:00+07:00
draft: false
description: "Learn security foundations through annotated examples — built for software engineers who write production code but have no formal security background"
tags: ["foundations", "it-security", "network-security", "hardening", "cryptography", "by-example"]
---

**You write software. Someone will try to break it.** This by-example guide teaches essential
IT security skills through hands-on code, configurations, and real-world scenarios — built
specifically for software engineers who are new to security.

## Why Software Engineers Need This

Every production system you build has a security surface: the ports it listens on, the
certificates it trusts, the users it authenticates, the logs it generates. When something goes
wrong — a breach, a misconfiguration, a compromised dependency — engineers are the ones who
must understand, fix, and harden the system.

This track starts from the code and tools you already know (bash, Python, HTTP) and builds
security intuition incrementally. No security certification or prior background is required.

## What Is IT Security By-Example Learning?

IT security by-example learning is a **scenario-first approach** where you learn through
annotated, runnable code and real-world configurations rather than abstract theory. Each example
shows:

- **What it does** — step-by-step annotations documenting system state, network traffic, or
  configuration effects
- **Why it works** — the security rationale behind each control or attack mechanic
- **When to apply it** — practical guidance on deploying each technique in production
- **Trade-offs** — security vs. usability vs. performance in context

## Learning Progression

The three levels map directly to a software engineer's growing security responsibility:

| Level            | Who It Is For                              | What You Build                                                              |
| ---------------- | ------------------------------------------ | --------------------------------------------------------------------------- |
| **Beginner**     | Any engineer writing or deploying code     | Fluency in firewalls, TLS, SSH, file permissions, basic crypto              |
| **Intermediate** | Engineers owning services in production    | Vulnerability assessment, IAM, cloud security, SIEM basics                  |
| **Advanced**     | Senior engineers and security-minded leads | Threat modeling, zero-trust design, CI/CD security gates, incident response |

Start at Beginner even if you have years of engineering experience. Security concepts build
on each other, and the first 28 examples cover the fundamentals that every production
engineer should know.

## Coverage

### What Is Covered

- **Network security** — firewall rules, packet analysis, TLS configuration, VPN setup
- **System hardening** — OS hardening, patch management, least-privilege configuration
- **Cryptography in practice** — symmetric/asymmetric encryption, hashing, PKI, certificate management
- **Vulnerability assessment** — scanning, CVE analysis, CVSS 4.0 risk scoring, remediation prioritization
- **Cloud security basics** — cloud IAM misconfigurations, CSPM concepts, shared responsibility model
- **Incident response** — detection, containment, eradication, recovery, and post-incident review
- **Identity and access management** — authentication, authorization, MFA, privilege escalation prevention
- **Security monitoring** — log analysis, SIEM queries, anomaly detection baselines

### What Is Not Covered

- Offensive exploitation techniques (see [Red Team by Example](/en/learn/information-security/roles/red-team/by-example/overview))
- Security governance and risk management (see [CISO by Example](/en/learn/information-security/roles/ciso/by-example/overview))
- Threat detection and SOC operations (see [Blue Team by Example](/en/learn/information-security/roles/blue-team/by-example/overview))

## Prerequisites

- Comfort with a Linux/Unix terminal (you can run commands and read output)
- Basic understanding of HTTP and TCP/IP (you know what a port is)
- Ability to read shell scripts or Python code

No security background required. If you have deployed a web server or written an API, you
already have the context to understand every beginner example.

## Structure of Each Example

Every example follows a consistent five-part format:

1. **What This Covers** — what the example demonstrates and why it matters (2-3 sentences)
2. **Scenario** — the system environment or threat scenario (always realistic, never abstract)
3. **Annotated Code or Configuration** — runnable scripts, configs, or tool output with inline
   comments documenting what each line does and why
4. **Key Takeaway** — the core security insight to retain (1-2 sentences)
5. **Why It Matters** — production relevance (50-100 words)

## Examples by Level

### Beginner (Examples 1–28)

- [Example 1: Analyzing Network Traffic with tcpdump](/en/learn/information-security/by-example/foundations/beginner#example-1-analyzing-network-traffic-with-tcpdump)
- [Example 2: Reading iptables Firewall Rules](/en/learn/information-security/by-example/foundations/beginner#example-2-reading-iptables-firewall-rules)
- [Example 3: Writing a Basic iptables INPUT Rule](/en/learn/information-security/by-example/foundations/beginner#example-3-writing-a-basic-iptables-input-rule)
- [Example 4: Understanding the TCP Three-Way Handshake](/en/learn/information-security/by-example/foundations/beginner#example-4-understanding-the-tcp-three-way-handshake)
- [Example 5: Scanning Open Ports with ss](/en/learn/information-security/by-example/foundations/beginner#example-5-scanning-open-ports-with-ss)
- [Example 6: Basic nmap Host Discovery and Service Scan](/en/learn/information-security/by-example/foundations/beginner#example-6-basic-nmap-host-discovery-and-service-scan)
- [Example 7: TLS Handshake Walkthrough](/en/learn/information-security/by-example/foundations/beginner#example-7-tls-handshake-walkthrough)
- [Example 8: Generating a Self-Signed Certificate](/en/learn/information-security/by-example/foundations/beginner#example-8-generating-a-self-signed-certificate)
- [Example 9: Configuring HTTPS in nginx](/en/learn/information-security/by-example/foundations/beginner#example-9-configuring-https-in-nginx)
- [Example 10: Symmetric Encryption with AES](/en/learn/information-security/by-example/foundations/beginner#example-10-symmetric-encryption-with-aes)
- [Example 11: Asymmetric Encryption with RSA](/en/learn/information-security/by-example/foundations/beginner#example-11-asymmetric-encryption-with-rsa)
- [Example 12: Hashing Files with SHA-256](/en/learn/information-security/by-example/foundations/beginner#example-12-hashing-files-with-sha-256)
- [Example 13: Password Hashing with bcrypt](/en/learn/information-security/by-example/foundations/beginner#example-13-password-hashing-with-bcrypt)
- [Example 14: SSH Key-Based Authentication](/en/learn/information-security/by-example/foundations/beginner#example-14-ssh-key-based-authentication)
- [Example 15: Hardening sshd_config](/en/learn/information-security/by-example/foundations/beginner#example-15-hardening-sshd_config)
- [Example 16: Linux File Permissions](/en/learn/information-security/by-example/foundations/beginner#example-16-linux-file-permissions)
- [Example 17: setuid and setgid Risk](/en/learn/information-security/by-example/foundations/beginner#example-17-setuid-and-setgid-risk)
- [Example 18: User and Group Management](/en/learn/information-security/by-example/foundations/beginner#example-18-user-and-group-management)
- [Example 19: sudo Configuration](/en/learn/information-security/by-example/foundations/beginner#example-19-sudo-configuration)
- [Example 20: Finding World-Writable Files](/en/learn/information-security/by-example/foundations/beginner#example-20-finding-world-writable-files)
- [Example 21: CVE Lookup and CVSS 4.0 Scoring](/en/learn/information-security/by-example/foundations/beginner#example-21-cve-lookup-and-cvss-40-scoring)
- [Example 22: Checking Packages for Known Vulnerabilities](/en/learn/information-security/by-example/foundations/beginner#example-22-checking-packages-for-known-vulnerabilities)
- [Example 23: Reading /var/log/auth.log](/en/learn/information-security/by-example/foundations/beginner#example-23-reading-varlogauthlog)
- [Example 24: Monitoring System Resources for Anomalies](/en/learn/information-security/by-example/foundations/beginner#example-24-monitoring-system-resources-for-anomalies)
- [Example 25: Basic Syslog Forwarding Config](/en/learn/information-security/by-example/foundations/beginner#example-25-basic-syslog-forwarding-config)
- [Example 26: Password Policy with PAM](/en/learn/information-security/by-example/foundations/beginner#example-26-password-policy-with-pam)
- [Example 27: Account Lockout Policy with PAM](/en/learn/information-security/by-example/foundations/beginner#example-27-account-lockout-policy-with-pam)
- [Example 28: Checking for SUID Binaries After Install](/en/learn/information-security/by-example/foundations/beginner#example-28-checking-for-suid-binaries-after-install)

### Intermediate (Examples 29–57)

- [Example 29: Network Segmentation with VLANs](/en/learn/information-security/by-example/foundations/intermediate#example-29-network-segmentation-with-vlans)
- [Example 30: WireGuard VPN Setup](/en/learn/information-security/by-example/foundations/intermediate#example-30-wireguard-vpn-setup)
- [Example 31: Stateful Firewall with nftables](/en/learn/information-security/by-example/foundations/intermediate#example-31-stateful-firewall-with-nftables)
- [Example 32: Suricata IDS Rule Writing](/en/learn/information-security/by-example/foundations/intermediate#example-32-suricata-ids-rule-writing)
- [Example 33: TLS Certificate Chain Validation](/en/learn/information-security/by-example/foundations/intermediate#example-33-tls-certificate-chain-validation)
- [Example 34: Setting Up a Simple Internal CA](/en/learn/information-security/by-example/foundations/intermediate#example-34-setting-up-a-simple-internal-ca)
- [Example 35: DNSSEC Zone Signing](/en/learn/information-security/by-example/foundations/intermediate#example-35-dnssec-zone-signing)
- [Example 36: CVSS 4.0 Score Calculation Walkthrough](/en/learn/information-security/by-example/foundations/intermediate#example-36-cvss-40-score-calculation-walkthrough)
- [Example 37: Vulnerability Scanning with OpenVAS](/en/learn/information-security/by-example/foundations/intermediate#example-37-vulnerability-scanning-with-openvas)
- [Example 38: SQL Injection Detection and Mitigation](/en/learn/information-security/by-example/foundations/intermediate#example-38-sql-injection-detection-and-mitigation)
- [Example 39: XSS Detection and Mitigation](/en/learn/information-security/by-example/foundations/intermediate#example-39-xss-detection-and-mitigation)
- [Example 40: CSRF Protection](/en/learn/information-security/by-example/foundations/intermediate#example-40-csrf-protection)
- [Example 41: RBAC Configuration](/en/learn/information-security/by-example/foundations/intermediate#example-41-rbac-configuration)
- [Example 42: TOTP MFA Setup](/en/learn/information-security/by-example/foundations/intermediate#example-42-totp-mfa-setup)
- [Example 43: Active Directory Security Basics](/en/learn/information-security/by-example/foundations/intermediate#example-43-active-directory-security-basics)
- [Example 44: LDAP Authentication Hardening](/en/learn/information-security/by-example/foundations/intermediate#example-44-ldap-authentication-hardening)
- [Example 45: API Key Rotation Workflow](/en/learn/information-security/by-example/foundations/intermediate#example-45-api-key-rotation-workflow)
- [Example 46: Secrets Management with HashiCorp Vault](/en/learn/information-security/by-example/foundations/intermediate#example-46-secrets-management-with-hashicorp-vault)
- [Example 47: Centralized Log Aggregation](/en/learn/information-security/by-example/foundations/intermediate#example-47-centralized-log-aggregation)
- [Example 48: Writing a Basic SIEM Correlation Rule](/en/learn/information-security/by-example/foundations/intermediate#example-48-writing-a-basic-siem-correlation-rule)
- [Example 49: Establishing a Log Baseline](/en/learn/information-security/by-example/foundations/intermediate#example-49-establishing-a-log-baseline)
- [Example 50: AWS S3 Public Bucket Misconfiguration](/en/learn/information-security/by-example/foundations/intermediate#example-50-aws-s3-public-bucket-misconfiguration)
- [Example 51: AWS Config Rule for IAM](/en/learn/information-security/by-example/foundations/intermediate#example-51-aws-config-rule-for-iam)
- [Example 52: Docker Container Hardening](/en/learn/information-security/by-example/foundations/intermediate#example-52-docker-container-hardening)
- [Example 53: Kubernetes NetworkPolicy](/en/learn/information-security/by-example/foundations/intermediate#example-53-kubernetes-networkpolicy)
- [Example 54: Kubernetes RBAC](/en/learn/information-security/by-example/foundations/intermediate#example-54-kubernetes-rbac)
- [Example 55: Incident Response Phases](/en/learn/information-security/by-example/foundations/intermediate#example-55-incident-response-phases)
- [Example 56: Evidence Collection and Chain of Custody](/en/learn/information-security/by-example/foundations/intermediate#example-56-evidence-collection-and-chain-of-custody)
- [Example 57: Linux Memory Forensics Basics](/en/learn/information-security/by-example/foundations/intermediate#example-57-linux-memory-forensics-basics)

### Advanced (Examples 58–85)

- [Example 58: Zero-Trust Network Architecture](/en/learn/information-security/by-example/foundations/advanced#example-58-zero-trust-network-architecture)
- [Example 59: Mutual TLS (mTLS) Configuration](/en/learn/information-security/by-example/foundations/advanced#example-59-mutual-tls-mtls-configuration)
- [Example 60: Certificate Transparency Log Monitoring](/en/learn/information-security/by-example/foundations/advanced#example-60-certificate-transparency-log-monitoring)
- [Example 61: Hardware Security Module Concepts](/en/learn/information-security/by-example/foundations/advanced#example-61-hardware-security-module-concepts)
- [Example 62: Key Derivation with Argon2](/en/learn/information-security/by-example/foundations/advanced#example-62-key-derivation-with-argon2)
- [Example 63: Full Disk Encryption with LUKS](/en/learn/information-security/by-example/foundations/advanced#example-63-full-disk-encryption-with-luks)
- [Example 64: Advanced nftables with Connection Tracking](/en/learn/information-security/by-example/foundations/advanced#example-64-advanced-nftables-with-connection-tracking)
- [Example 65: STRIDE Threat Modeling](/en/learn/information-security/by-example/foundations/advanced#example-65-stride-threat-modeling)
- [Example 66: Security Architecture Review Checklist](/en/learn/information-security/by-example/foundations/advanced#example-66-security-architecture-review-checklist)
- [Example 67: Simulating an Attack and Defense](/en/learn/information-security/by-example/foundations/advanced#example-67-simulating-an-attack-and-defense)
- [Example 68: APT Detection with SIEM Correlation](/en/learn/information-security/by-example/foundations/advanced#example-68-apt-detection-with-siem-correlation)
- [Example 69: Honeypot Deployment](/en/learn/information-security/by-example/foundations/advanced#example-69-honeypot-deployment)
- [Example 70: ModSecurity WAF Configuration](/en/learn/information-security/by-example/foundations/advanced#example-70-modsecurity-waf-configuration)
- [Example 71: DDoS Mitigation with Rate Limiting](/en/learn/information-security/by-example/foundations/advanced#example-71-ddos-mitigation-with-rate-limiting)
- [Example 72: Supply Chain Security](/en/learn/information-security/by-example/foundations/advanced#example-72-supply-chain-security)
- [Example 73: Software Composition Analysis](/en/learn/information-security/by-example/foundations/advanced#example-73-software-composition-analysis)
- [Example 74: SBOM Generation and CycloneDX Format](/en/learn/information-security/by-example/foundations/advanced#example-74-sbom-generation-and-cyclonedx-format)
- [Example 75: Cryptographic Agility](/en/learn/information-security/by-example/foundations/advanced#example-75-cryptographic-agility)
- [Example 76: Post-Quantum Cryptography Intro](/en/learn/information-security/by-example/foundations/advanced#example-76-post-quantum-cryptography-intro)
- [Example 77: Security Automation with Ansible](/en/learn/information-security/by-example/foundations/advanced#example-77-security-automation-with-ansible)
- [Example 78: Compliance as Code with InSpec](/en/learn/information-security/by-example/foundations/advanced#example-78-compliance-as-code-with-inspec)
- [Example 79: Security Chaos Engineering](/en/learn/information-security/by-example/foundations/advanced#example-79-security-chaos-engineering)
- [Example 80: Purple Team Exercise Plan](/en/learn/information-security/by-example/foundations/advanced#example-80-purple-team-exercise-plan)
- [Example 81: Incident Communication Template](/en/learn/information-security/by-example/foundations/advanced#example-81-incident-communication-template)
- [Example 82: Business Continuity Runbook](/en/learn/information-security/by-example/foundations/advanced#example-82-business-continuity-runbook)
- [Example 83: Security KPIs and Metrics Dashboard](/en/learn/information-security/by-example/foundations/advanced#example-83-security-kpis-and-metrics-dashboard)
- [Example 84: Security Testing in CI/CD](/en/learn/information-security/by-example/foundations/advanced#example-84-security-testing-in-cicd)
- [Example 85: Advanced Cloud Security Posture Management](/en/learn/information-security/by-example/foundations/advanced#example-85-advanced-cloud-security-posture-management)
