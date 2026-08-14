---
title: "Security Documentation"
description: "Required SECURITY.md sections and security best practices for enterprise/financial-services platforms"
category: explanation
subcategory: conventions
tags:
  - conventions
  - documentation
  - open-source
  - repository-standards
created: 2026-04-04
when_to_use: "Read this when creating or reviewing a repository's SECURITY.md file."
---

# Security Documentation

## SECURITY.md

The SECURITY.md file provides a clear channel for security researchers to responsibly disclose vulnerabilities.

**Location:** `SECURITY.md` at repository root

**Essential Sections:**

1. **Supported Versions**
   - Which versions receive security updates
   - End-of-life policy

2. **Reporting a Vulnerability**
   - Contact method (email, security platform)
   - Expected response time
   - What information to include

3. **Security Response Process**
   - How reports are handled
   - Timeline for fixes
   - Disclosure policy

4. **Security Update Policy**
   - How security fixes are released
   - Notification mechanism

**Example:**

```markdown
# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability

**Please do not report security vulnerabilities through public GitHub issues.**

Instead, please report them via email to security@example.com.

Please include:

- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

You should receive a response within 48 hours. We will keep you informed of progress toward a fix.

## Security Response Process

1. **Acknowledgment:** We will acknowledge receipt within 48 hours
2. **Investigation:** We will investigate and assess the severity
3. **Fix Development:** We will develop a fix (timeline depends on severity)
4. **Release:** We will release a security update
5. **Disclosure:** We will publicly disclose after fix is available

## Security Updates

Security fixes are released as patch versions (e.g., 1.2.3 → 1.2.4).
Subscribe to GitHub releases to be notified of security updates.
```

## Security Best Practices

**For Enterprise Platforms with Financial Services:**

- Explicitly document compliance standards (PCI DSS, SOC 2, etc.)
- Describe data protection measures
- Document authentication and authorization architecture
- Provide security contact for enterprise users

**References:**

- [GitHub Security Advisories](https://docs.github.com/en/code-security/security-advisories)
- [FINOS Security Standards](https://www.finos.org/) (financial services as one enterprise domain)
