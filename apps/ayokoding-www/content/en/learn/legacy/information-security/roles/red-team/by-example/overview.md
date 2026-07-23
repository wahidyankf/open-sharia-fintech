---
title: "Overview"
weight: 10000000
date: 2026-05-21T00:00:00+07:00
draft: false
description: "Learn offensive security through annotated examples — built for software engineers who want to understand how attackers think and write more defensively"
tags: ["red-team", "offensive-security", "penetration-testing", "adversary-simulation", "by-example"]
---

**The best way to stop an attacker is to think like one.** This by-example guide teaches
offensive security techniques through annotated tool output and attack scenarios — built for
software engineers who want to understand what their code looks like from the attacker's side.

> **Ethical Use Notice:** All examples are for authorized penetration testing, CTF competitions,
> lab environments, and defensive understanding only. Never apply offensive techniques against
> systems without explicit written authorization.

## Why Software Engineers Need This

You write APIs, authentication systems, file upload handlers, and database queries. Each one
is a potential attack surface. When you understand _how_ attackers exploit these systems —
the exact commands, tool output, and thought process — you write more defensively from day one.

This track uses only legal, lab-based environments (HackTheBox, TryHackMe, local VMs). You
do not need a security certification or prior penetration testing experience. You need a
terminal, curiosity, and a legal lab environment.

## What Is Red Team By-Example Learning?

Red team by-example learning is a **technique-first approach** where you learn through annotated
tool output, scripts, and adversary playbooks rather than abstract theory. Each example shows:

- **What it does** — annotated tool output documenting each step of the attack chain
- **Why it works** — the vulnerability or misconfiguration being exploited and the underlying mechanism
- **When to use it** — which phase of an engagement this technique applies to
- **Detection surface** — what artifacts the technique leaves for defenders to catch

## Learning Progression

| Level            | Engineer Context                            | What You Learn                                                  |
| ---------------- | ------------------------------------------- | --------------------------------------------------------------- |
| **Beginner**     | "I want to understand recon and scanning"   | Passive OSINT, nmap, service enumeration, basic web scanning    |
| **Intermediate** | "I want to understand exploitation"         | SQLi, XSS, shell access, privilege escalation, lateral movement |
| **Advanced**     | "I want to understand APT-level techniques" | AV evasion, C2, AD attacks, full-chain scenarios                |

Start at Beginner even if you are an experienced engineer. The recon and enumeration examples
build mental models that the exploitation examples depend on.

## Coverage

### What Is Covered

- **Reconnaissance** — passive OSINT, active scanning, service enumeration, network mapping
- **Initial access** — exploitation of common vulnerabilities, phishing simulation, credential attacks
- **Execution and persistence** — shell payloads, scheduled tasks, startup persistence mechanisms
- **Privilege escalation** — local privilege escalation on Linux and Windows
- **Lateral movement** — credential reuse, pass-the-hash, pivoting techniques
- **Exfiltration simulation** — data staging, covert channel basics
- **Post-exploitation** — situational awareness, credential dumping, living-off-the-land binaries

### What Is Not Covered

- Defensive detection and response (see [Blue Team by Example](/en/learn/information-security/roles/blue-team/by-example/overview))
- Strategic risk management and governance (see [CISO by Example](/en/learn/information-security/roles/ciso/by-example/overview))
- General IT security hardening (see [IT Security by Example](/en/learn/information-security/by-example/foundations/overview))

## Prerequisites

- Comfort with a Linux terminal (you can run commands and read output)
- Basic understanding of HTTP, TCP ports, and DNS (you know what a web server is)
- Access to a legal lab: [HackTheBox](https://www.hackthebox.com), [TryHackMe](https://tryhackme.com), or a local VM

No security certification or prior penetration testing experience required.

## Structure of Each Example

Every example follows a consistent five-part format:

1. **What This Covers** — the technique and its place in the attack chain (2-3 sentences)
2. **Scenario** — lab environment, authorized engagement context, and assumed access level
3. **Annotated Tool Output or Script** — commands and output with inline comments explaining
   each step, what it reveals, and what a defender would see
4. **Key Takeaway** — the core offensive insight and its defensive implication (1-2 sentences)
5. **Why It Matters** — production relevance for attackers and defenders (50-100 words)

## Examples by Level

### Beginner (Examples 1–28)

- [Example 1: Passive DNS Recon — whois, dig, and host](/en/learn/information-security/roles/red-team/by-example/beginner#example-1-passive-dns-recon--whois-dig-and-host-lookups)
- [Example 2: OSINT with theHarvester](/en/learn/information-security/roles/red-team/by-example/beginner#example-2-osint-with-theharvester)
- [Example 3: Google Dorking](/en/learn/information-security/roles/red-team/by-example/beginner#example-3-google-dorking)
- [Example 4: Shodan Recon](/en/learn/information-security/roles/red-team/by-example/beginner#example-4-shodan-recon)
- [Example 5: Active Host Discovery with nmap](/en/learn/information-security/roles/red-team/by-example/beginner#example-5-active-host-discovery--nmap--sn-ping-sweep)
- [Example 6: TCP SYN Scan](/en/learn/information-security/roles/red-team/by-example/beginner#example-6-tcp-syn-scan--nmap--ss)
- [Example 7: Service Version Detection](/en/learn/information-security/roles/red-team/by-example/beginner#example-7-service-version-detection--nmap--sv)
- [Example 8: OS Fingerprinting](/en/learn/information-security/roles/red-team/by-example/beginner#example-8-os-fingerprinting--nmap--o)
- [Example 9: Aggressive Scan](/en/learn/information-security/roles/red-team/by-example/beginner#example-9-aggressive-scan--nmap--a)
- [Example 10: NSE Script Scanning](/en/learn/information-security/roles/red-team/by-example/beginner#example-10-nse-script-scanning)
- [Example 11: UDP Scan](/en/learn/information-security/roles/red-team/by-example/beginner#example-11-udp-scan--nmap--su)
- [Example 12: Banner Grabbing with netcat](/en/learn/information-security/roles/red-team/by-example/beginner#example-12-banner-grabbing-with-netcat)
- [Example 13: Web Server Enumeration with curl](/en/learn/information-security/roles/red-team/by-example/beginner#example-13-web-server-enumeration-with-curl)
- [Example 14: robots.txt and sitemap.xml Recon](/en/learn/information-security/roles/red-team/by-example/beginner#example-14-robotstxt-and-sitemapxml-recon)
- [Example 15: Directory Brute-Forcing with gobuster](/en/learn/information-security/roles/red-team/by-example/beginner#example-15-directory-brute-forcing-with-gobuster)
- [Example 16: Subdomain Enumeration with gobuster](/en/learn/information-security/roles/red-team/by-example/beginner#example-16-subdomain-enumeration-with-gobuster)
- [Example 17: Virtual Host Discovery](/en/learn/information-security/roles/red-team/by-example/beginner#example-17-virtual-host-discovery)
- [Example 18: SMB Enumeration](/en/learn/information-security/roles/red-team/by-example/beginner#example-18-smb-enumeration)
- [Example 19: FTP Anonymous Login Check](/en/learn/information-security/roles/red-team/by-example/beginner#example-19-ftp-anonymous-login-check)
- [Example 20: SSH Audit](/en/learn/information-security/roles/red-team/by-example/beginner#example-20-ssh-user-enumeration--ssh-audit)
- [Example 21: HTTP Method Enumeration](/en/learn/information-security/roles/red-team/by-example/beginner#example-21-http-method-enumeration)
- [Example 22: Nikto Web Scan](/en/learn/information-security/roles/red-team/by-example/beginner#example-22-nikto-web-scan)
- [Example 23: Searchsploit](/en/learn/information-security/roles/red-team/by-example/beginner#example-23-searchsploit)
- [Example 24: CVE Lookup for a Discovered Service Version](/en/learn/information-security/roles/red-team/by-example/beginner#example-24-cve-lookup-for-a-discovered-service-version)
- [Example 25: Metasploit Basic Usage](/en/learn/information-security/roles/red-team/by-example/beginner#example-25-metasploit-basic-usage)
- [Example 26: Hydra Brute-Force](/en/learn/information-security/roles/red-team/by-example/beginner#example-26-hydra-brute-force)
- [Example 27: Password Spraying Concept](/en/learn/information-security/roles/red-team/by-example/beginner#example-27-password-spraying-concept)
- [Example 28: Screenshot Capture with EyeWitness](/en/learn/information-security/roles/red-team/by-example/beginner#example-28-screenshot-capture-with-eyewitness)

### Intermediate (Examples 29–57)

- [Example 29: Exploiting EternalBlue with Metasploit](/en/learn/information-security/roles/red-team/by-example/intermediate#example-29-exploiting-a-vulnerable-service--metasploit-eternalblue-ms17-010)
- [Example 30: Manual SQL Injection](/en/learn/information-security/roles/red-team/by-example/intermediate#example-30-manual-sql-injection--login-bypass-and-union-select)
- [Example 31: XSS Session Cookie Theft](/en/learn/information-security/roles/red-team/by-example/intermediate#example-31-xss-exploitation--stealing-session-cookies-via-reflected-xss)
- [Example 32: Command Injection](/en/learn/information-security/roles/red-team/by-example/intermediate#example-32-command-injection--exploiting-os-command-injection-in-a-web-parameter)
- [Example 33: File Inclusion Exploitation](/en/learn/information-security/roles/red-team/by-example/intermediate#example-33-file-inclusion-exploitation--lfi-and-rfi)
- [Example 34: Unrestricted File Upload](/en/learn/information-security/roles/red-team/by-example/intermediate#example-34-unrestricted-file-upload--php-webshell)
- [Example 35: Default Credentials Exploitation](/en/learn/information-security/roles/red-team/by-example/intermediate#example-35-exploiting-default-credentials)
- [Example 36: Password Cracking with hashcat](/en/learn/information-security/roles/red-team/by-example/intermediate#example-36-password-cracking-with-hashcat--ntlm-hashes)
- [Example 37: Generating a Reverse Shell with msfvenom](/en/learn/information-security/roles/red-team/by-example/intermediate#example-37-generating-a-reverse-shell-with-msfvenom)
- [Example 38: Catching a Reverse Shell with netcat](/en/learn/information-security/roles/red-team/by-example/intermediate#example-38-catching-a-reverse-shell-with-netcat)
- [Example 39: Stabilizing a Shell](/en/learn/information-security/roles/red-team/by-example/intermediate#example-39-stabilizing-a-shell--pty-upgrade)
- [Example 40: Linux Privesc — SUID Binary Abuse](/en/learn/information-security/roles/red-team/by-example/intermediate#example-40-linux-privilege-escalation--suid-binary-abuse)
- [Example 41: Linux Privesc — sudo Misconfiguration](/en/learn/information-security/roles/red-team/by-example/intermediate#example-41-linux-privesc--sudo--l-misconfiguration)
- [Example 42: Linux Privesc — Cron Job Abuse](/en/learn/information-security/roles/red-team/by-example/intermediate#example-42-linux-privesc--cron-job-with-world-writable-script)
- [Example 43: Linux Privesc — PATH Hijacking](/en/learn/information-security/roles/red-team/by-example/intermediate#example-43-linux-privesc--path-hijacking)
- [Example 44: Linux Privesc — Kernel Exploit Identification](/en/learn/information-security/roles/red-team/by-example/intermediate#example-44-linux-privesc--kernel-exploit-identification)
- [Example 45: Windows Privesc — Unquoted Service Path](/en/learn/information-security/roles/red-team/by-example/intermediate#example-45-windows-privesc--unquoted-service-path)
- [Example 46: Windows Privesc — Weak Service Permissions](/en/learn/information-security/roles/red-team/by-example/intermediate#example-46-windows-privesc--weak-service-permissions)
- [Example 47: Credential Dumping with Mimikatz](/en/learn/information-security/roles/red-team/by-example/intermediate#example-47-credential-dumping-with-mimikatz)
- [Example 48: Pass-the-Hash Attack](/en/learn/information-security/roles/red-team/by-example/intermediate#example-48-pass-the-hash-attack)
- [Example 49: Kerberoasting](/en/learn/information-security/roles/red-team/by-example/intermediate#example-49-kerberoasting)
- [Example 50: AS-REP Roasting](/en/learn/information-security/roles/red-team/by-example/intermediate#example-50-as-rep-roasting)
- [Example 51: BloodHound Data Collection](/en/learn/information-security/roles/red-team/by-example/intermediate#example-51-bloodhound-data-collection)
- [Example 52: Pivoting with SSH Port Forwarding](/en/learn/information-security/roles/red-team/by-example/intermediate#example-52-pivoting-with-ssh-port-forwarding)
- [Example 53: Pivoting with Chisel](/en/learn/information-security/roles/red-team/by-example/intermediate#example-53-pivoting-with-chisel)
- [Example 54: SMB Lateral Movement](/en/learn/information-security/roles/red-team/by-example/intermediate#example-54-smb-lateral-movement--psexecpy)
- [Example 55: WMI Lateral Movement](/en/learn/information-security/roles/red-team/by-example/intermediate#example-55-wmi-lateral-movement--wmiexecpy)
- [Example 56: Post-Exploitation Situational Awareness](/en/learn/information-security/roles/red-team/by-example/intermediate#example-56-post-exploitation-situational-awareness)
- [Example 57: Living Off the Land](/en/learn/information-security/roles/red-team/by-example/intermediate#example-57-living-off-the-land--lolbins-for-payload-delivery)

### Advanced (Examples 58–85)

- [Example 58: Custom Shellcode Generation](/en/learn/information-security/roles/red-team/by-example/advanced#example-58-custom-shellcode-generation)
- [Example 59: AV Evasion — XOR Obfuscation](/en/learn/information-security/roles/red-team/by-example/advanced#example-59-av-evasion--xor-obfuscation-of-shellcode)
- [Example 60: Process Injection](/en/learn/information-security/roles/red-team/by-example/advanced#example-60-process-injection--createremotethread)
- [Example 61: Reflective DLL Injection](/en/learn/information-security/roles/red-team/by-example/advanced#example-61-reflective-dll-injection)
- [Example 62: AMSI Bypass](/en/learn/information-security/roles/red-team/by-example/advanced#example-62-amsi-bypass--powershell-memory-patch)
- [Example 63: ETW Patching](/en/learn/information-security/roles/red-team/by-example/advanced#example-63-etw-patching--disabling-event-tracing-for-windows)
- [Example 64: Token Impersonation](/en/learn/information-security/roles/red-team/by-example/advanced#example-64-token-impersonation)
- [Example 65: DCSync Attack](/en/learn/information-security/roles/red-team/by-example/advanced#example-65-dcsync-attack)
- [Example 66: Golden Ticket Attack](/en/learn/information-security/roles/red-team/by-example/advanced#example-66-golden-ticket-attack)
- [Example 67: Silver Ticket Attack](/en/learn/information-security/roles/red-team/by-example/advanced#example-67-silver-ticket-attack)
- [Example 68: Skeleton Key Attack](/en/learn/information-security/roles/red-team/by-example/advanced#example-68-skeleton-key-attack)
- [Example 69: LSASS Dump](/en/learn/information-security/roles/red-team/by-example/advanced#example-69-lsass-dump)
- [Example 70: Credential Access via DPAPI](/en/learn/information-security/roles/red-team/by-example/advanced#example-70-credential-access-via-dpapi)
- [Example 71: C2 Framework Basics — Sliver](/en/learn/information-security/roles/red-team/by-example/advanced#example-71-c2-framework-basics--sliver)
- [Example 72: DNS C2 Exfiltration](/en/learn/information-security/roles/red-team/by-example/advanced#example-72-dns-c2-exfiltration)
- [Example 73: HTTPS C2 Traffic Blending](/en/learn/information-security/roles/red-team/by-example/advanced#example-73-https-c2-traffic-blending)
- [Example 74: Persistence via Registry Run Key](/en/learn/information-security/roles/red-team/by-example/advanced#example-74-persistence-via-registry-run-key)
- [Example 75: Persistence via Scheduled Task](/en/learn/information-security/roles/red-team/by-example/advanced#example-75-persistence-via-scheduled-task)
- [Example 76: Persistence via WMI Subscription](/en/learn/information-security/roles/red-team/by-example/advanced#example-76-persistence-via-wmi-subscription)
- [Example 77: Data Staging and Exfiltration](/en/learn/information-security/roles/red-team/by-example/advanced#example-77-data-staging-and-exfiltration)
- [Example 78: Cloud Credential Theft — AWS IMDS](/en/learn/information-security/roles/red-team/by-example/advanced#example-78-cloud-credential-theft--aws-imds)
- [Example 79: SSRF to Metadata Service](/en/learn/information-security/roles/red-team/by-example/advanced#example-79-ssrf-to-metadata-service)
- [Example 80: OAuth 2.0 Token Theft](/en/learn/information-security/roles/red-team/by-example/advanced#example-80-oauth-20-token-theft)
- [Example 81: ADCS ESC1 Abuse](/en/learn/information-security/roles/red-team/by-example/advanced#example-81-active-directory-certificate-services-abuse--esc1)
- [Example 82: Kerberos Delegation Abuse](/en/learn/information-security/roles/red-team/by-example/advanced#example-82-kerberos-delegation-abuse--unconstrained-delegation)
- [Example 83: Full-Chain Attack Scenario](/en/learn/information-security/roles/red-team/by-example/advanced#example-83-full-chain-attack-scenario--recon-to-domain-admin)
- [Example 84: Red Team Reporting](/en/learn/information-security/roles/red-team/by-example/advanced#example-84-red-team-reporting)
- [Example 85: Purple Team Debrief](/en/learn/information-security/roles/red-team/by-example/advanced#example-85-purple-team-debrief--attck-technique-mapping)
