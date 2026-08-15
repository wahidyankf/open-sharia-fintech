---
title: "Overview"
date: 2026-08-14T00:00:00+07:00
draft: false
weight: 1
---

The by-example track will build a deterministic Python tool boundary in small, runnable slices. It
starts with names, descriptions, typed arguments, structured results, and local dispatch; continues
through MCP tools, resources, prompts, transports, discovery, composition, and validation; and closes
with bounded server surfaces, compatibility, and context-aware result design.

The examples use a fake model and local protocol-shaped simulations where a live provider or MCP SDK
would make learning non-deterministic. A future adapter may use an MCP implementation, but a package
or `remotebrowser` is never a prerequisite for the course.

## Intended progression

- **Beginner** establishes a single typed tool and the host-client-server roles.
- **Intermediate** composes servers, validates calls at the boundary, and handles resources, prompts,
  transports, errors, and compatibility.
- **Advanced** applies discovery filtering, capability policy, small result shapes, and a browser-service
  wrapper pattern without granting an unrestricted browser or shell.

The completed route contains at least 75 contiguous examples. Each entry will keep the five-part
by-example structure: brief explanation, diagram or code, runnable artifact, key takeaway, and why it
matters.
