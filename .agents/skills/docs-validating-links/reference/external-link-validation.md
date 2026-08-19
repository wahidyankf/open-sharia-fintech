# External Link Validation

## External Link Validation

## Verification Strategy

**Challenge**: External links can be slow to verify (network requests)

**Recommended approach**:

1. Cache results - Store validation results in cache file
2. Respect cache TTL - Re-verify after 7 days (configurable)
3. Batch verification - Verify multiple URLs in parallel
4. Handle failures gracefully - Network errors != broken link

## HTTP Request Pattern

**Verification steps**:

1. HEAD request first - Faster than GET, checks if URL accessible
2. Follow redirects - HTTP 301/302 are OK (but report for info)
3. Check status codes:
   - 200-299: OK
   - 300-399: REDIRECT (report but don't fail)
   - 400-499: BROKEN (client error, link is wrong)
   - 500-599: SERVER_ERROR (temporary, re-verify later)
   - Timeout: UNREACHABLE (network issue, re-verify later)

## Link Caching Strategy

**Cache file format** (JSON):

{
"https://diataxis.fr/": {
"status": "OK",
"http_code": 200,
"last_checked": "2026-01-25T13:30:00+07:00",
"ttl": 604800
}
}

**Cache TTL recommendations**:

- OK links: 7 days
- BROKEN links: 1 day
- REDIRECT links: 7 days
- SERVER_ERROR: 1 hour
- UNREACHABLE: 1 hour

## Common External Link Errors

**Error 1: Link returns 404**

**Criticality**: HIGH - Link is dead, user gets 404
**Action**: Update or remove link

**Error 2: Link redirects (301/302)**

**Criticality**: LOW - Link works but could be updated to final URL
**Action**: Consider updating to final destination (optional)

**Error 3: Link times out**

**Criticality**: MEDIUM - May be temporary network issue
**Action**: Re-verify after TTL expires, flag if persistent
