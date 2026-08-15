---
title: "Overview"
date: 2026-08-16T00:00:00+07:00
draft: false
weight: 1
---

## Why this exists

A ledger architecture needs framework selection, immutable evidence, idempotency, period controls, and traceable contract events. AAOIFI, PSAK Syariah, and MFRS with the Bank Negara Malaysia Shariah Governance Policy are coexisting models; AAOIFI is not the single Sharia accounting standard. Malaysia is not on AAOIFI's mandatory-adoption list, and Indonesia uses AAOIFI as a basis rather than adopting it.

## Silent-failure check

### What still balances while being wrong

Double-entry can balance while a contract event is attributed to the wrong model or version. The observable signal is an audit query that cannot reproduce the policy, jurisdiction, event evidence, and reversal chain behind a posting.
