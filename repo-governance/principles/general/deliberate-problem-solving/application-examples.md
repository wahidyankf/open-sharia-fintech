---
description: Walks through three worked examples (API integration, database choice, feature implementation) contrasting hidden-assumption failures with deliberate approaches.
when_to_use: Use when you need a worked example of applying deliberate problem-solving to a realistic task.
---

# Application Examples

## Example 1: API Integration

**Situation**: Asked to integrate a third-party payment API

**❌ FAIL - Hidden Assumptions**:

- Assumes API uses JSON
- Assumes synchronous responses
- Proceeds to implement
- Discovers later it's XML and asynchronous
- Must rewrite everything

**✅ PASS - Deliberate Approach**:

1. "I'm assuming this API uses JSON with synchronous responses. Let me verify the documentation."
2. Reads actual API docs with WebFetch
3. Discovers it's XML with webhooks
4. "The API uses XML with webhook callbacks, not JSON synchronous responses. Should I proceed with XML parsing and webhook endpoint setup?"
5. Gets confirmation before implementing

## Example 2: Database Choice

**Situation**: Asked to add data persistence

**❌ FAIL - Silent Complex Choice**:

- Immediately chooses PostgreSQL with replication
- Implements complex setup
- User only needed simple file storage

**✅ PASS - Surface Tradeoffs**:

1. "For data persistence, I see three options:"
   - File-based storage (simplest, suitable for < 1000 records)
   - SQLite (good for single-server, ACID compliance)
   - PostgreSQL (scalable, complex setup)
2. "What's your expected scale and deployment model?"
3. Gets clarification: single server, < 100 records
4. "Given that, SQLite would be simpler than PostgreSQL. Shall I use SQLite?"
5. Implements after agreement

## Example 3: Feature Implementation

**Situation**: Asked to add "user settings"

**❌ FAIL - Hidden Confusion**:

- Unclear if settings are per-user or global
- Unclear if settings need persistence
- Implements one interpretation
- User wanted different behaviour

**✅ PASS - Name Confusion**:

1. "I'm unclear on the scope of 'user settings'. Questions:"
   - Per-user or global defaults?
   - Persisted in database or session-only?
   - Which settings should be configurable?
2. User clarifies: per-user, persisted, theme + language only
3. Now has clear requirements
4. Implements correctly on first try
