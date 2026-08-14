-- Proposed Phase 1 database migration for BeaverNest CLI Chat.
-- This plan artifact is not embedded or executed until copied to:
-- apps/beavernest-be/src/BeaverNestBe/Migrations/002-chat.sql
-- The application enables PRAGMA foreign_keys = ON for every connection.
CREATE TABLE chat_threads (
  id TEXT PRIMARY KEY,
  title TEXT NOT NULL DEFAULT '',
  revision INTEGER NOT NULL DEFAULT 0 CHECK (revision >= 0),
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL
);

CREATE TABLE chat_messages (
  id TEXT PRIMARY KEY,
  thread_id TEXT NOT NULL REFERENCES chat_threads (id) ON DELETE CASCADE,
  turn_id TEXT NOT NULL,
  ordinal INTEGER NOT NULL CHECK (ordinal >= 0),
  author TEXT NOT NULL CHECK (author IN ('user', 'assistant')),
  provider TEXT CHECK (provider IN ('codex', 'opencode')),
  model_id TEXT,
  markdown_body TEXT NOT NULL DEFAULT '',
  lifecycle TEXT NOT NULL CHECK (
    lifecycle IN (
      'pending',
      'streaming',
      'completed',
      'failed',
      'cancelled'
    )
  ),
  failure_kind TEXT CHECK (
    failure_kind IS NULL
    OR failure_kind IN (
      'unavailable',
      'unauthenticated',
      'exited',
      'cancelled'
    )
  ),
  last_event_sequence INTEGER NOT NULL DEFAULT 0 CHECK (last_event_sequence >= 0),
  created_at_utc TEXT NOT NULL,
  updated_at_utc TEXT NOT NULL,
  UNIQUE (thread_id, ordinal)
);

CREATE TABLE chat_provider_sessions (
  thread_id TEXT NOT NULL REFERENCES chat_threads (id) ON DELETE CASCADE,
  provider TEXT NOT NULL CHECK (provider IN ('codex', 'opencode')),
  native_session_id TEXT NOT NULL,
  transcript_revision INTEGER NOT NULL CHECK (transcript_revision >= 0),
  selected_model_id TEXT,
  updated_at_utc TEXT NOT NULL,
  PRIMARY KEY (thread_id, provider)
);

CREATE INDEX chat_messages_thread_ordinal_idx ON chat_messages (thread_id, ordinal);

CREATE INDEX chat_threads_updated_idx ON chat_threads (updated_at_utc DESC);

CREATE UNIQUE INDEX chat_messages_one_active_turn_idx ON chat_messages (thread_id)
WHERE
  author = 'assistant'
  AND lifecycle IN ('pending', 'streaming');
