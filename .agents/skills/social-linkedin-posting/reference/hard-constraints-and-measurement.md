# Hard Constraints and Measurement

## LinkedIn Character Limit — 3,000

LinkedIn caps a single post at **3,000 characters**. **Only the post body counts** — everything
from the `OPEN SHARIA ENTERPRISE` line to end of file. The metadata header (`Posted:`,
`Platform:`, `Window:`) and the `---` separator are NOT posted and NOT counted; the author copies
from `OPEN SHARIA ENTERPRISE` downward into LinkedIn.

The body MUST be **≤ 3,000 characters**. Target **~2,900** to leave margin.

**Always measure before finishing.** Count from the `OPEN SHARIA ENTERPRISE` line to end of file
(codepoint count matches LinkedIn's counter):

```bash
awk '/^OPEN SHARIA ENTERPRISE/{p=1} p' <file> | python3 -c 'import sys;print(len(sys.stdin.read()))'
```

If the result is > 3,000, trim and re-measure until under. Never finish over the limit.

## No Vanity Metrics in the Body

The post **body** (everything below the `Week NN / Phase P, Week W` title line) MUST NOT cite
vanity/activity metrics — no commit counts, no lines-of-changed, no PR tallies, and similar.
Describe what changed and why it matters, not how much churn it took.

The `Window:` metadata line **above** the `---` MAY carry a commit tally for internal bookkeeping
only — it is never posted. Keep vanity numbers there, never in the body.
