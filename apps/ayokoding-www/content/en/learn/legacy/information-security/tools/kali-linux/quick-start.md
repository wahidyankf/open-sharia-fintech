---
title: "Quick Start"
date: 2026-06-24T00:00:00+07:00
draft: false
weight: 100002
description: "Install Kali Linux in a virtual machine and run your first network scan"
tags: ["infosec", "tools", "kali-linux", "quick-start", "nmap", "penetration-testing", "linux"]
---

## What You'll Learn

By the end of this tutorial, you'll be able to:

- Download and verify the official Kali Linux VM image
- Import the image into VirtualBox or VMware
- Log in, update the system, and change the default password
- Navigate the pre-installed tool categories
- Run a basic nmap network scan against a safe local target
- Interpret the scan output

## Prerequisites

Before starting, ensure you have:

- A host machine with at least 8 GB RAM and 40 GB free disk space
- VirtualBox 7+ or VMware Workstation/Fusion installed
- A stable internet connection for image download and system update
- Basic command-line familiarity (cd, ls, sudo)

{{< callout type="warning" >}}
**Legal and Ethical Notice**: Only scan networks and systems you own or have explicit written
permission to test. Unauthorized scanning violates computer fraud laws in most jurisdictions.
All examples in this tutorial target your own local virtual machine or explicitly authorized
practice environments.
{{< /callout >}}

## What is Kali Linux?

Kali Linux is a Debian-based penetration testing distribution maintained by Offensive Security.
It ships with 600+ pre-installed security tools organized by category — reconnaissance, web
application analysis, exploitation, password attacks, wireless attacks, and more.

### Why Use a VM?

Running Kali in a virtual machine (VM) is the recommended starting point because:

- **Isolation** - Kali is sandboxed from your host OS; mistakes don't damage your main system
- **Snapshots** - Roll back instantly if you break something during practice
- **Portability** - Copy the `.ova` file to another machine and resume work immediately
- **Safe defaults** - You can freely experiment without touching host network interfaces

## Step 1: Download the Official Image

Navigate to the official Kali Linux downloads page and select the **Pre-built Virtual Machines**
section.

```text
URL: https://www.kali.org/get-kali/#kali-virtual-machines
```

- Choose **VirtualBox** (`.ova`) or **VMware** (`.7z`) depending on your hypervisor
- The `.ova` file is approximately 3.2 GB compressed
- SHA-256 checksum is listed next to each download link

### Verify the Download

Always verify integrity before importing — a corrupted or tampered image can cause subtle issues.

```bash
# Linux / macOS
sha256sum kali-linux-2024.4-virtualbox-amd64.ova
```

- `sha256sum` — computes the SHA-256 hash of the file
- Compare the output hash against the value shown on the official download page
- Any mismatch means the file is corrupt or was tampered with — re-download it

```bash
# Windows PowerShell
Get-FileHash kali-linux-2024.4-virtualbox-amd64.ova -Algorithm SHA256
```

- `Get-FileHash` — PowerShell built-in; no extra tools required
- `-Algorithm SHA256` — selects the SHA-256 algorithm to match the official checksum

{{< callout type="tip" >}}
Bookmark the [official Kali integrity page](https://www.kali.org/docs/introduction/download-official-kali-linux-images/) — it explains all checksum and GPG verification methods in detail.
{{< /callout >}}

## Step 2: Import into VirtualBox

```bash
# Import via CLI (optional — GUI works equally well)
VBoxManage import kali-linux-2024.4-virtualbox-amd64.ova \
  --vsys 0 \
  --memory 4096 \
  --cpus 2
```

- `VBoxManage import` — VirtualBox CLI import command
- `--vsys 0` — targets the first virtual system in the `.ova` manifest
- `--memory 4096` — allocates 4 GB RAM (minimum 2 GB; 4 GB recommended)
- `--cpus 2` — assigns 2 virtual CPU cores for acceptable performance

Via the GUI: **File → Import Appliance → select the `.ova` → set RAM/CPU → Finish**.

### Recommended VM Settings

| Setting      | Minimum | Recommended |
| ------------ | ------- | ----------- |
| RAM          | 2 GB    | 4 GB        |
| CPU cores    | 1       | 2           |
| Video memory | 16 MB   | 128 MB      |
| Disk         | 20 GB   | 80 GB       |
| Network mode | NAT     | NAT         |

Keep the network adapter in **NAT** mode during initial setup — Kali reaches the internet for
updates but the host machine is not directly visible to Kali, limiting attack surface during
learning.

## Step 3: First Boot and Credential Setup

Default credentials for the pre-built image:

```text
Username: kali
Password: kali
```

{{< callout type="warning" >}}
Change the default password immediately after first login. The `kali:kali` default is publicly
known and leaving it unchanged on a networked VM is a security risk.
{{< /callout >}}

```bash
# Change password for the current user
passwd
```

- `passwd` — invokes the password change utility for the currently logged-in user
- You will be prompted: current password → new password → confirm new password
- Minimum length enforced by PAM; avoid dictionary words

## Step 4: Update the System

Kali is a rolling release. The VM image may be weeks old — update before using any tools.

```bash
sudo apt update && sudo apt full-upgrade -y
```

- `sudo` — runs the following command with root privileges
- `apt update` — refreshes the local package index from Kali repositories
- `&&` — chains the next command; only runs if `apt update` succeeds
- `apt full-upgrade -y` — upgrades all installed packages; `-y` auto-confirms prompts
- `full-upgrade` (not `upgrade`) — also handles dependency changes, package removals, and
  kernel upgrades; important for Kali's rolling release model

This step may take 5-20 minutes depending on your internet speed.

## Step 5: Navigate Pre-installed Tools

Kali organizes its 600+ tools into categories accessible from the application menu.

```bash
# List all Kali-specific meta-packages
apt-cache show kali-linux-default | grep -E "^(Package|Depends|Recommends)" | head -20
```

- `apt-cache show` — displays package metadata without installing anything
- `kali-linux-default` — the meta-package that pulls in the default tool set
- `grep -E "^(Package|Depends|Recommends)"` — filters output to show only dependency lines
- `head -20` — limits output to 20 lines to avoid flooding the terminal

Key tool categories from the application menu:

| Category                 | Example Tools                      |
| ------------------------ | ---------------------------------- |
| Information Gathering    | nmap, recon-ng, maltego            |
| Vulnerability Analysis   | nikto, OpenVAS, lynis              |
| Web Application Analysis | Burp Suite, gobuster, sqlmap       |
| Password Attacks         | Hydra, John the Ripper, hashcat    |
| Wireless Attacks         | aircrack-ng, wifite, kismet        |
| Exploitation Tools       | Metasploit Framework, searchsploit |
| Post Exploitation        | Empire, mimikatz, BeEF             |
| Forensics                | Autopsy, binwalk, foremost         |

## Step 6: Your First nmap Scan

nmap (Network Mapper) is the most widely used network discovery and security auditing tool. Let's
scan the Kali VM's own loopback address as a safe, authorized target.

```bash
# Scan localhost — always authorized, zero legal risk
nmap -sV -sC 127.0.0.1
```

- `nmap` — invokes the Network Mapper scanner
- `-sV` — **version detection**: probes open ports to identify service name and version
- `-sC` — **default scripts**: runs nmap's built-in Lua NSE scripts for common checks
  (banner grabbing, HTTP title enumeration, SSL certificate inspection, etc.)
- `127.0.0.1` — loopback address; only hits your own machine, never a remote host

**Sample Output**:

```text
Starting Nmap 7.94 ( https://nmap.org )
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000026s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Debian (protocol 2.0)
| ssh-hostkey:
|   3072 ab:cd:ef:12:34:56:78:90:ab:cd:ef:12:34:56:78:90 (RSA)
```

- `PORT` column — TCP/UDP port number
- `STATE` column — `open` means accepting connections; `closed` means no service; `filtered`
  means a firewall is blocking probes
- `SERVICE` column — best-guess service name based on port number
- `VERSION` column — actual service banner returned by `-sV` probing

{{< callout type="tip" >}}
The `-sC` flag runs scripts like `ssh-hostkey` that reveal the server's SSH host keys. In real
engagements, host keys help confirm you're connecting to the intended machine and detect
potential MitM attacks.
{{< /callout >}}

### Scan a Specific Port Range

```bash
nmap -p 1-1024 127.0.0.1
```

- `-p 1-1024` — scans only the well-known port range (1 through 1024) instead of the
  default top-1000 ports
- Useful when you want faster results focused on standard service ports

### Output to a File

```bash
nmap -sV -sC -oN scan_results.txt 127.0.0.1
```

- `-oN scan_results.txt` — **normal output**: writes human-readable results to a file
- The file persists across terminal sessions — useful for documenting findings
- Alternative output formats: `-oX` (XML for tool imports), `-oG` (grep-friendly)

## What's Next?

You now have a working Kali Linux VM and can run basic nmap scans. Continue with:

- **[Beginner](/en/learn/information-security/tools/kali-linux/beginner)** — deep-dive into
  reconnaissance, web application testing, and password auditing workflows with 20+ annotated
  examples across Kali's most-used tool categories
