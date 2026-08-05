---
title: "Swift Availability CLI"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Build a short command-line program that reports whether requested product IDs are available. The
goal is consolidation, not an application framework: each language decision should remain visible
enough to explain from the source.

## Goal and acceptance criteria

The finished program safely removes absent requests, models success and absence with an enum carrying
associated values, dispatches through an `Inventory` protocol, transforms requests with closures, and
awaits one asynchronous request source. It builds with `swiftc`, prints one line per present request,
and never force-unwraps a value.

## Build it

1. From `code/`, run `swiftc Main.swift -o availability && ./availability`. Confirm the `nil` request
   is ignored rather than crashing, and `coffee` prints as unavailable.
2. Add an `EmptyInventory` conforming to `Inventory`; run again after substituting it. The reporting
   pipeline should remain unchanged because it depends on the protocol contract.
3. Change `fetchRequests` to return another optional SKU. Confirm `compactMap` makes the nil policy
   explicit, `map` preserves the remaining order, and the awaited function completes before output.

## Why this is the right-sized capstone

An iOS app would introduce lifecycle ownership, UI state, SDK APIs, and actor isolation before the
language itself settles. This CLI proves the primer boundary: absence is safely handled, domain state
is expressive, behavior is abstracted through a protocol, transformations are local closures, and an
`async` call has an explicit await point.
