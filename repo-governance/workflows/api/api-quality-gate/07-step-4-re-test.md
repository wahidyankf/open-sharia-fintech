---
title: "Step 4: Re-Test"
description: Why the API quality gate re-runs the tester against a rebuilt, redeployed service rather than trusting a source-only fix.
when_to_use: Use when verifying a fix after Step 3 has been applied.
---

# Step 4: Re-Test

Rebuild and redeploy the service, then re-run step 1 against the **current** build. A fix verified
only against source, never against a live response, does not count as verified.
