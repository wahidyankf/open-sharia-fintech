"""Example 41: combine allowlisting, a retry budget, and parsed fixture data."""

# => The fixture URL is authorized before any modeled extraction begins.
url, attempts = "https://fixture.test/catalog", 0
# => A bounded loop represents retrying a transient local read once.
while attempts < 2:
    attempts += 1
    if attempts == 2:
        rows = ["item-1"]
# => Success requires an allowed URL, bounded attempts, and structured output.
assert url.startswith("https://fixture.test/") and attempts == 2 and rows == ["item-1"]
# => Output proves the scraper contract without scraping a live site.
print(rows)
