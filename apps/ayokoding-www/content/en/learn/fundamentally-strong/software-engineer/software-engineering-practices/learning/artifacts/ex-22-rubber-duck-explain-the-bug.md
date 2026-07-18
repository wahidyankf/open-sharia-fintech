---
title: "Artifact: Rubber-Duck Narration Surfaces the Wrong Assumption"
date: 2026-07-18T00:00:00+07:00
draft: false
weight: 62
---

> ex-22 &middot; exercises co-13 &middot; narrating a bug sentence by sentence, before touching code.

**Bug report**: "gift-card balance shows $0 immediately after redemption, even for a partial
redemption that should leave a remaining balance."

**Narration, written out sentence by sentence, before opening a debugger**:

```text
1. I call redeem(card, amount) with amount less than the card's full balance.
2. redeem() should compute remaining = card.balance - amount and return it.
3. I'm SEEING remaining == 0 every time, regardless of amount.
4. That means either (a) card.balance is already 0 when redeem() runs, or (b) amount always
   equals card.balance, or (c) the subtraction itself is wrong.
5. ...wait. I'm assuming card.balance is read BEFORE the subtraction. Let me check the actual
   line order in redeem() -- does it save the balance first, or does something update
   card.balance to 0 as a "mark redeemed" step BEFORE the remaining-balance line runs?
6. That's it -- there's a `card.balance = 0` line (a "mark this card used" flag, added for a
   DIFFERENT feature) sitting ABOVE the remaining-balance calculation, not below it.
```

**Verify**: the wrong assumption ("the subtraction itself must be wrong") surfaces at step 5, purely
from re-reading the narration -- before any debugger, print statement, or code edit -- satisfying
co-13's rule that systematic debugging finds the real cause through disciplined narration first.

**Key takeaway**: saying the expected behavior out loud, one sentence at a time, forces you to
notice a silently wrong assumption (line order) that skimming the code visually let slide by twice
already.

**Why It Matters**: the "rubber duck" habit costs nothing but two minutes of writing, and it
regularly finds the bug before a single breakpoint is set -- because most bugs are a wrong mental
model of what the code does, not a mystery that requires instrumentation to see.
