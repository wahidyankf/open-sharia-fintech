---
title: "Artifact: A Sandboxed Shell Command Stays Isolated from the Host"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 65
---

> A sandboxed write whose effect never reaches the host outside the sandbox boundary --
> exercises co-12.

```text
[agent, inside sandbox rooted at /sandbox] $ echo "sandbox write" > /sandbox/tmp/output.txt
[sandbox] file written: /sandbox/tmp/output.txt (14 bytes)

[host process, OUTSIDE the sandbox namespace] $ ls /tmp/output.txt
ls: /tmp/output.txt: No such file or directory

[host process, OUTSIDE the sandbox namespace] $ ls /sandbox
ls: /sandbox: No such file or directory
  -- the sandbox root itself only exists inside the sandboxed mount namespace; the host
     process has no path into it at all
```
