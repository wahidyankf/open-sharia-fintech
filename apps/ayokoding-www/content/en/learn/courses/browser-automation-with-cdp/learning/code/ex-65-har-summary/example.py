"""Example 65: summarize HAR-like fixture metadata without response bodies."""

# => The trace includes only status and duration from an authorized local load.
entries = [{"status": 200, "duration_ms": 10}, {"status": 304, "duration_ms": 2}]
# => Summaries keep diagnostic signal while minimizing retained data.
summary = {
    "count": len(entries),
    "max_duration_ms": max(item["duration_ms"] for item in entries),
}
# => The assertion verifies the summary reflects both trace entries and their slowest timing.
assert summary == {"count": 2, "max_duration_ms": 10}
# => Output is the bounded HAR-style observation.
print(summary)
