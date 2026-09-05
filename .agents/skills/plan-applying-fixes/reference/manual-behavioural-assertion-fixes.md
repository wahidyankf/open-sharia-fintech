# Manual Behavioural Assertion Fixes

## Manual Behavioural Assertion Fixes (Step 5c Findings)

### 1. Missing Playwright MCP Steps for UI Plans

```markdown
### Manual UI Verification (Playwright MCP)

- [ ] Start dev server: `rtk ./hippo run --class service --disk-path . -- npm exec nx -- dev [project-name]`
- [ ] Navigate to affected pages via `browser_navigate`
- [ ] Inspect DOM via `browser_snapshot` — verify correct rendering
- [ ] Test interactive flows via `browser_click` / `browser_fill_form`
- [ ] Check for JS errors via `browser_console_messages` — must be zero errors
- [ ] Verify API integration via `browser_network_requests`
- [ ] Take screenshots via `browser_take_screenshot` for visual verification
- [ ] Document verification results in this checklist
```

### 2. Missing curl Steps for API Plans

```markdown
### Manual API Verification (curl)

- [ ] Start backend server: `rtk ./hippo run --class service --disk-path . -- npm exec nx -- dev [project-name]`
- [ ] Verify health endpoint: `curl -s http://localhost:[port]/api/health | jq .`
- [ ] Verify affected endpoints return expected responses
- [ ] Test error cases with invalid payloads — verify proper error responses
- [ ] Verify response status codes, shapes, and data integrity
- [ ] Document verification results in this checklist
```

### 3. Missing End-to-End Flow for Full-Stack Plans

```markdown
### End-to-End Flow Verification

- [ ] Start both frontend and backend dev servers
- [ ] Use Playwright MCP to interact with the UI
- [ ] Verify UI actions trigger correct API calls (`browser_network_requests`)
- [ ] Verify API responses are correctly rendered in the UI
- [ ] Test complete user flows end-to-end
- [ ] Document verification results in this checklist
```

### Confidence Assessment

**HIGH**: section completely missing — add the template, or the section references the wrong
project/port — fix with correct values from plan context. **MEDIUM**: section exists but is
vague — flag for manual review.
