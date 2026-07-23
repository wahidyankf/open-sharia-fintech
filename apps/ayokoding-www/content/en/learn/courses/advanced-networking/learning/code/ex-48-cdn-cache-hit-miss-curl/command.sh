#!/bin/sh
# ex-48: cf-cache-status is Cloudflare's own cache-state header (HIT/MISS/
# EXPIRED/STALE/BYPASS); age (RFC 9111) reports how many seconds a cached
# response has sat in the edge cache since it was fetched from the origin --
# a cache-busting query string forces a fresh MISS to contrast against (co-20)
echo "=== plain request (likely a cache HIT) ==="
curl -sI https://example.com

echo
echo "=== cache-busting query string (forces a cache MISS) ==="
curl -sI "https://example.com/?cachebust=<unique-value>"
