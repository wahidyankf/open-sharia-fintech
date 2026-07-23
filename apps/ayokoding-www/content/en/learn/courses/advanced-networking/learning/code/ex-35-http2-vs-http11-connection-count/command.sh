#!/bin/sh
# ex-35: --parallel fetches all 3 URLs concurrently instead of sequentially
# reusing one keep-alive connection -- this is what makes HTTP/1.1's
# multiple-connections behavior visible instead of hidden by keep-alive reuse.
# Compare the number of "Trying"/"Connected to" lines each protocol prints
# for the SAME 3 requests (co-15).
echo "=== HTTP/1.1, 3 resources, --parallel ==="
curl -s -v --http1.1 --parallel --parallel-max 3 \
	https://example.com/a https://example.com/b https://example.com/c \
	2>&1 >/dev/null | grep -iE "Trying|Connected to|^< HTTP"

echo
echo "=== HTTP/2, 3 resources, --parallel ==="
curl -s -v --http2 --parallel --parallel-max 3 \
	https://example.com/a https://example.com/b https://example.com/c \
	2>&1 >/dev/null | grep -iE "Trying|Connected to|using HTTP|^< HTTP"
