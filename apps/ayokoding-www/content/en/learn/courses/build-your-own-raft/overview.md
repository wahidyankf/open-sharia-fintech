---
title: "Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

Build a deliberately small Raft: election, replication, persistence-shaped state, and a replicated key-value state machine under injected failure.

This course assumes Just Enough Go and Distributed Systems. It implements the established Raft mechanics without reteaching consensus theory. Snapshotting and membership changes are explicit stretch goals; this is not a production RPC service.

## Sources

- [Raft paper](https://raft.github.io/raft.pdf)
- [Raft official site](https://raft.github.io/)
- [MIT 6.5840 labs](https://pdos.csail.mit.edu/6.824/)
