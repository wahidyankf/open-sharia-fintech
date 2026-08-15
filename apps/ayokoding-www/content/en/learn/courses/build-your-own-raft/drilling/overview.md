---
title: "Drilling Overview"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 1
---

## Recall Q&A

1. What must be unique per term? **Answer:** at most one leader.
2. When does a leader commit? **Answer:** after a majority stores a current-term entry.
3. What persists before RPC response? **Answer:** term, vote, and log.

## Calculation practice

1. What is the quorum of five nodes? **Answer:** three.
2. What is the quorum of seven nodes? **Answer:** four.

## Scenario judgment

1. Can a two-node minority of five commit? **Answer:** no; it lacks a quorum.
2. What does a node do on a higher term? **Answer:** step down and update its term.

## Design exercise

Draw a five-node Raft cluster with per-peer next/match indexes, randomized elections, dropped AppendEntries, a majority commit, and a healed partition. Mark all persistent state.

## Automaticity checklist

- I can calculate a quorum.
- I can state the RequestVote log freshness rule.
- I can state AppendEntries consistency and repair.
- I can distinguish safety from liveness.
- I can name snapshotting and membership change as stretch work.
