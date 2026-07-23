---
title: "Overview"
weight: 10000000
date: 2026-05-21T00:00:00+07:00
draft: false
description: "Learn defensive security through annotated examples — built for software engineers who want to detect, investigate, and respond to threats in the systems they build"
tags: ["blue-team", "defensive-security", "soc", "siem", "threat-detection", "by-example"]
---

**Your application generates logs. When something goes wrong, those logs are the story.** This
by-example guide teaches threat detection, incident response, and SOC skills through annotated
log samples and queries — built for software engineers who want to understand what happens
after an attacker gets in.

## Why Software Engineers Need This

You instrument your code with metrics and traces for reliability. Security monitoring is the
same discipline applied to adversarial inputs. When you understand how to read an auth log, write
a detection rule, or triage an alert, you become an invaluable partner during incidents — not a
bystander waiting for the security team.

This track uses the same tools you already encounter in production: structured logs, query
languages (Splunk, Elastic), and scripting. No SOC experience or prior security background required.

## What Is Blue Team By-Example Learning?

Blue team by-example learning is a **detection-first approach** where you learn through annotated
log samples, SIEM queries, and response procedures rather than abstract theory. Each example shows:

- **What it detects** — the attack technique or anomaly the example identifies
- **Why it indicates compromise** — the behavioral pattern or IOC and its significance
- **How to respond** — triage steps, containment actions, and escalation criteria
- **False positive handling** — how to distinguish malicious activity from legitimate behavior

## Learning Progression

| Level            | Engineer Context                                             | What You Learn                                                                     |
| ---------------- | ------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| **Beginner**     | "I want to read security logs and write basic queries"       | Auth logs, Windows events, Apache logs, basic Splunk/Elastic queries, alert triage |
| **Intermediate** | "I want to detect specific attacks and respond to incidents" | AD attack detection, SIEM correlation, incident response, memory forensics         |
| **Advanced**     | "I want to build and run a detection program"                | Threat hunting, detection engineering, cloud detection, SOAR, detection metrics    |

Start at Beginner even if you are a senior engineer. Log reading and basic query skills are
the foundation everything else builds on.

## Coverage

### What Is Covered

- **Log analysis** — Windows Event Logs, Linux syslogs, application logs, and network logs
- **SIEM queries** — Splunk SPL, Elastic KQL/EQL, Microsoft Sentinel KQL, and Sigma rule writing
  for common attack patterns
- **Threat detection** — detecting reconnaissance, initial access, execution, and persistence
- **Incident triage** — alert prioritization, IOC extraction, timeline reconstruction
- **Incident response** — containment, eradication, and recovery procedures
- **Threat hunting** — hypothesis-driven hunting, anomaly baselines, and proactive detection
- **Detection engineering** — writing, testing, and maintaining detection rules

### What Is Not Covered

- Offensive exploitation techniques (see [Red Team by Example](/en/learn/information-security/roles/red-team/by-example/overview))
- Strategic security governance (see [CISO by Example](/en/learn/information-security/roles/ciso/by-example/overview))
- General IT infrastructure hardening (see [IT Security by Example](/en/learn/information-security/by-example/foundations/overview))

## Prerequisites

- Comfort reading structured text files (logs, JSON, CSV)
- Basic understanding of HTTP, DNS, and Linux processes
- No SIEM or SOC experience required — the first examples start from raw log files

If you have debugged a production incident using logs, you already have the instincts needed
to start this track.

## Structure of Each Example

Every example follows a consistent five-part format:

1. **What This Covers** — what the example detects or responds to (2-3 sentences)
2. **Scenario** — SOC or IR analyst context with the attack technique in scope
3. **Annotated Log Sample or Query** — raw logs, SIEM queries, or scripts with inline
   comments explaining each indicator and decision point
4. **Key Takeaway** — the core defensive insight to retain (1-2 sentences)
5. **Why It Matters** — production SOC relevance (50-100 words)

## Examples by Level

### Beginner (Examples 1–28)

- [Example 1: Reading /var/log/auth.log](/en/learn/information-security/roles/blue-team/by-example/beginner#example-1-reading-varlogauthlog)
- [Example 2: Reading Windows Security Event Log — Logon Events](/en/learn/information-security/roles/blue-team/by-example/beginner#example-2-reading-windows-security-event-log--event-id-4624-and-4625)
- [Example 3: Reading Windows Security Event Log — Process Creation](/en/learn/information-security/roles/blue-team/by-example/beginner#example-3-reading-windows-security-event-log--event-id-4688-process-creation)
- [Example 4: Reading /var/log/syslog](/en/learn/information-security/roles/blue-team/by-example/beginner#example-4-reading-varlogsyslog)
- [Example 5: Reading Apache/nginx Access Logs](/en/learn/information-security/roles/blue-team/by-example/beginner#example-5-reading-apachenginx-accesslog)
- [Example 6: Reading Apache/nginx Error Logs](/en/learn/information-security/roles/blue-team/by-example/beginner#example-6-reading-apachenginx-errorlog)
- [Example 7: Identifying a Brute-Force Attack in auth.log](/en/learn/information-security/roles/blue-team/by-example/beginner#example-7-identifying-a-brute-force-attack-in-authlog)
- [Example 8: Identifying a Port Scan in Firewall Logs](/en/learn/information-security/roles/blue-team/by-example/beginner#example-8-identifying-a-port-scan-in-firewall-logs)
- [Example 9: Identifying Directory Brute-Force in Web Logs](/en/learn/information-security/roles/blue-team/by-example/beginner#example-9-identifying-directory-brute-force-in-web-logs)
- [Example 10: Identifying SQL Injection Attempts in Web Logs](/en/learn/information-security/roles/blue-team/by-example/beginner#example-10-identifying-sql-injection-attempts-in-web-logs)
- [Example 11: Identifying XSS Attempts in Web Logs](/en/learn/information-security/roles/blue-team/by-example/beginner#example-11-identifying-xss-attempts-in-web-logs)
- [Example 12: Recognizing Anomalous User Agent Strings](/en/learn/information-security/roles/blue-team/by-example/beginner#example-12-recognizing-anomalous-user-agent-strings)
- [Example 13: Basic Splunk SPL Query](/en/learn/information-security/roles/blue-team/by-example/beginner#example-13-basic-splunk-spl-query)
- [Example 14: Filtering by Time Range in Splunk](/en/learn/information-security/roles/blue-team/by-example/beginner#example-14-filtering-by-time-range-in-splunk)
- [Example 15: Splunk stats and eval — Counting Failed Logins](/en/learn/information-security/roles/blue-team/by-example/beginner#example-15-splunk-stats-and-eval--counting-failed-logins-per-user)
- [Example 16: Basic Elastic KQL Query](/en/learn/information-security/roles/blue-team/by-example/beginner#example-16-basic-elastic-kql-query)
- [Example 17: Elastic EQL Sequence Query](/en/learn/information-security/roles/blue-team/by-example/beginner#example-17-elastic-eql-sequence-query)
- [Example 18: Writing a Basic Sigma Rule](/en/learn/information-security/roles/blue-team/by-example/beginner#example-18-writing-a-basic-sigma-rule--brute-force-detection)
- [Example 19: Alert Triage Workflow](/en/learn/information-security/roles/blue-team/by-example/beginner#example-19-alert-triage-workflow)
- [Example 20: IP Reputation Lookup](/en/learn/information-security/roles/blue-team/by-example/beginner#example-20-ip-reputation-lookup--abuseipdb-and-virustotal)
- [Example 21: Extracting IOCs from a Suspicious Email](/en/learn/information-security/roles/blue-team/by-example/beginner#example-21-extracting-iocs-from-a-suspicious-email)
- [Example 22: Checking a File Hash Against VirusTotal](/en/learn/information-security/roles/blue-team/by-example/beginner#example-22-checking-a-file-hash-against-virustotal)
- [Example 23: Basic Network Traffic Analysis with tshark](/en/learn/information-security/roles/blue-team/by-example/beginner#example-23-basic-network-traffic-analysis-with-tshark)
- [Example 24: Identifying a Reverse Shell in Network Logs](/en/learn/information-security/roles/blue-team/by-example/beginner#example-24-identifying-a-reverse-shell-in-network-logs)
- [Example 25: Detecting ICMP Tunneling](/en/learn/information-security/roles/blue-team/by-example/beginner#example-25-detecting-icmp-tunneling)
- [Example 26: Reading Windows PowerShell Event Logs](/en/learn/information-security/roles/blue-team/by-example/beginner#example-26-reading-windows-powershell-event-logs)
- [Example 27: Detecting Encoded PowerShell Commands](/en/learn/information-security/roles/blue-team/by-example/beginner#example-27-detecting-encoded-powershell-commands)
- [Example 28: Basic Incident Ticket Creation](/en/learn/information-security/roles/blue-team/by-example/beginner#example-28-basic-incident-ticket-creation)

### Intermediate (Examples 29–57)

- [Example 29: Detecting Pass-the-Hash](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-29-detecting-pass-the-hash--windows-event-id-4624-logontype-3-with-ntlmv2-from-a-workstation)
- [Example 30: Detecting Kerberoasting](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-30-detecting-kerberoasting--event-id-4769-tgs-requests-with-rc4-encryption-from-non-service-accounts)
- [Example 31: Detecting AS-REP Roasting](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-31-detecting-as-rep-roasting--event-id-4768-with-pre-authentication-disabled)
- [Example 32: Detecting DCSync](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-32-detecting-dcsync--event-id-4662-with-replication-rights-from-a-non-dc-ip)
- [Example 33: Detecting BloodHound Enumeration](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-33-detecting-bloodhound-enumeration--ldap-queries-with-large-result-sets-from-a-workstation)
- [Example 34: Detecting PsExec Lateral Movement](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-34-detecting-lateral-movement-via-psexec)
- [Example 35: Detecting WMI Lateral Movement](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-35-detecting-wmi-lateral-movement)
- [Example 36: Detecting LOLBin Abuse](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-36-detecting-lolbin-abuse)
- [Example 37: Detecting LSASS Access](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-37-detecting-lsass-access--sysmon-event-id-10)
- [Example 38: Detecting Registry Run Key Persistence](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-38-detecting-persistence-via-registry-run-key)
- [Example 39: Detecting Scheduled Task Persistence](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-39-detecting-scheduled-task-persistence)
- [Example 40: Detecting WMI Subscription Persistence](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-40-detecting-wmi-subscription-persistence)
- [Example 41: Detecting Web Shell Upload](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-41-detecting-web-shell-upload)
- [Example 42: Detecting C2 Beaconing](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-42-detecting-c2-beaconing)
- [Example 43: Detecting DNS Tunneling](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-43-detecting-dns-tunneling)
- [Example 44: Detecting Data Exfiltration](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-44-detecting-data-exfiltration)
- [Example 45: Splunk Threat Hunting — Rare Process Parent-Child](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-45-splunk-threat-hunting-query--rare-process-parent-child-relationships)
- [Example 46: Elastic Threat Hunting — Rare User Agents](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-46-elastic-threat-hunting--rare-user-agent-strings-in-web-logs)
- [Example 47: Building a Detection Hypothesis](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-47-building-a-detection-hypothesis--mitre-attck-t1003-lsass-dump-hunt)
- [Example 48: Sigma Rule for LSASS Access](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-48-writing-a-sigma-rule-for-lsass-access)
- [Example 49: Sigma Rule for Encoded PowerShell](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-49-writing-a-sigma-rule-for-encoded-powershell)
- [Example 50: Sentinel KQL — Impossible Travel](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-50-microsoft-sentinel-kql--detecting-impossible-travel)
- [Example 51: Sentinel KQL — New Admin Account](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-51-microsoft-sentinel-kql--alerting-on-new-admin-account-creation)
- [Example 52: Incident Containment](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-52-incident-containment--isolating-a-compromised-host)
- [Example 53: Incident Eradication](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-53-incident-eradication--removing-persistence-mechanisms)
- [Example 54: Memory Forensics Triage with volatility3](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-54-memory-forensics-triage--volatility3-pstree--netscan)
- [Example 55: Disk Forensics with Autopsy](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-55-disk-forensics-basics--autopsy-timeline-analysis)
- [Example 56: Malware Sandbox Analysis](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-56-malware-sandbox-analysis--reading-a-sandbox-report)
- [Example 57: Threat Intelligence Integration](/en/learn/information-security/roles/blue-team/by-example/intermediate#example-57-threat-intelligence-integration--misp-and-otx-ioc-lookup)

### Advanced (Examples 58–85)

- [Example 58: APT Detection with Multi-Stage Correlation](/en/learn/information-security/roles/blue-team/by-example/advanced#example-58-apt-detection-with-multi-stage-correlation)
- [Example 59: Detecting Golden Ticket Attack](/en/learn/information-security/roles/blue-team/by-example/advanced#example-59-detecting-golden-ticket-attack)
- [Example 60: Detecting Kerberos Delegation Abuse](/en/learn/information-security/roles/blue-team/by-example/advanced#example-60-detecting-kerberos-delegation-abuse)
- [Example 61: Detecting ADCS ESC1 Abuse](/en/learn/information-security/roles/blue-team/by-example/advanced#example-61-detecting-adcs-esc1-abuse)
- [Example 62: Detecting DKOM](/en/learn/information-security/roles/blue-team/by-example/advanced#example-62-detecting-dkom-direct-kernel-object-manipulation)
- [Example 63: Detecting Process Hollowing](/en/learn/information-security/roles/blue-team/by-example/advanced#example-63-detecting-process-hollowing)
- [Example 64: Detecting Fileless Malware](/en/learn/information-security/roles/blue-team/by-example/advanced#example-64-detecting-fileless-malware)
- [Example 65: Building a Detection Pipeline](/en/learn/information-security/roles/blue-team/by-example/advanced#example-65-building-a-detection-pipeline)
- [Example 66: SOAR Playbook Design](/en/learn/information-security/roles/blue-team/by-example/advanced#example-66-soar-playbook-design--automated-phishing-triage)
- [Example 67: Detection-as-Code Test](/en/learn/information-security/roles/blue-team/by-example/advanced#example-67-writing-a-detection-as-code-test)
- [Example 68: Detection Rule Lifecycle](/en/learn/information-security/roles/blue-team/by-example/advanced#example-68-detection-rule-lifecycle)
- [Example 69: Threat Hunt — Lateral Movement](/en/learn/information-security/roles/blue-team/by-example/advanced#example-69-threat-hunt-lateral-movement-hypothesis)
- [Example 70: Threat Hunt — LOLBin Abuse](/en/learn/information-security/roles/blue-team/by-example/advanced#example-70-threat-hunt-living-off-the-land)
- [Example 71: Threat Hunt — Beaconing Detection](/en/learn/information-security/roles/blue-team/by-example/advanced#example-71-threat-hunt-beaconing-detection--jitter-analysis)
- [Example 72: Threat Hunt — Credential Access](/en/learn/information-security/roles/blue-team/by-example/advanced#example-72-threat-hunt-credential-access--lsass-readers-not-in-baseline)
- [Example 73: User Behavior Analytics Baseline](/en/learn/information-security/roles/blue-team/by-example/advanced#example-73-user-behavior-analytics-baseline)
- [Example 74: Deception Technology Alert Triage](/en/learn/information-security/roles/blue-team/by-example/advanced#example-74-deception-technology-alert--honeypot-ssh-login)
- [Example 75: Network Traffic Analysis with Zeek and RITA](/en/learn/information-security/roles/blue-team/by-example/advanced#example-75-network-traffic-analysis--zeek-connlog-anomaly-detection-with-rita)
- [Example 76: Memory Forensics — Malware Extraction](/en/learn/information-security/roles/blue-team/by-example/advanced#example-76-memory-forensics-malware-extraction--volatility3-malfind)
- [Example 77: Disk Forensics — Timeline Analysis](/en/learn/information-security/roles/blue-team/by-example/advanced#example-77-disk-forensics-timeline-analysis--plaso-log2timeline--psort)
- [Example 78: Cloud Detection — AWS CloudTrail Login Without MFA](/en/learn/information-security/roles/blue-team/by-example/advanced#example-78-cloud-threat-detection--aws-cloudtrail-console-login-without-mfa)
- [Example 79: Cloud Detection — AWS IAM Privilege Escalation](/en/learn/information-security/roles/blue-team/by-example/advanced#example-79-cloud-threat-detection--aws-cloudtrail-iam-privilege-escalation)
- [Example 80: Kubernetes Audit Log Threat Detection](/en/learn/information-security/roles/blue-team/by-example/advanced#example-80-kubernetes-audit-log-threat-detection)
- [Example 81: Incident Post-Mortem Template](/en/learn/information-security/roles/blue-team/by-example/advanced#example-81-incident-post-mortem-template)
- [Example 82: Attack Simulation Validation](/en/learn/information-security/roles/blue-team/by-example/advanced#example-82-attack-simulation-validation--atomic-red-team)
- [Example 83: Purple Team Detection Mapping](/en/learn/information-security/roles/blue-team/by-example/advanced#example-83-purple-team-detection-mapping--attck-navigator-layer)
- [Example 84: Detection Metrics Dashboard](/en/learn/information-security/roles/blue-team/by-example/advanced#example-84-detection-metrics--mttd-mttr-false-positive-rate)
- [Example 85: Building a Threat Intelligence Program](/en/learn/information-security/roles/blue-team/by-example/advanced#example-85-building-a-threat-intelligence-program--misp--stixtaxii)
