import { Effect, Schema } from "effect";
import { PgliteService } from "./runtime";
import { JournalEntry, NewEntryInput } from "../domain/schema";
import { EmptyBatch, StorageUnavailable, StoreError } from "../domain/errors";

type RawRow = {
  id: string;
  name: string;
  payload: unknown;
  created_at: Date;
  updated_at: Date;
  storage_seq: bigint;
  started_at: Date;
  finished_at: Date;
  labels: string[];
};

function decodeRow(rawRow: unknown): JournalEntry {
  const row = rawRow as RawRow;
  return Schema.decodeUnknownSync(JournalEntry)({
    id: row.id,
    name: row.name,
    payload: row.payload,
    createdAt: row.created_at instanceof Date ? row.created_at.toISOString() : row.created_at,
    updatedAt: row.updated_at instanceof Date ? row.updated_at.toISOString() : row.updated_at,
    startedAt: row.started_at instanceof Date ? row.started_at.toISOString() : row.started_at,
    finishedAt: row.finished_at instanceof Date ? row.finished_at.toISOString() : row.finished_at,
    labels: Array.isArray(row.labels) ? row.labels : [],
  });
}

export function appendEntries(
  inputs: ReadonlyArray<NewEntryInput>,
): Effect.Effect<ReadonlyArray<JournalEntry>, StoreError, PgliteService> {
  return Effect.gen(function* () {
    if (inputs.length === 0) {
      return yield* Effect.fail(new EmptyBatch());
    }

    const { db } = yield* PgliteService;

    const now = new Date().toISOString();
    const values = inputs.map((input) => ({
      id: crypto.randomUUID(),
      name: input.name,
      payload: input.payload,
      createdAt: now,
      updatedAt: now,
      startedAt: input.startedAt,
      finishedAt: input.finishedAt,
      labels: input.labels ?? [],
    }));

    // Build parameterized multi-VALUES INSERT (8 params per row)
    const placeholders = values
      .map(
        (_, i) =>
          `($${i * 8 + 1}, $${i * 8 + 2}, $${i * 8 + 3}::jsonb, $${i * 8 + 4}::timestamptz, $${i * 8 + 5}::timestamptz, $${i * 8 + 6}::timestamptz, $${i * 8 + 7}::timestamptz, $${i * 8 + 8}::text[])`,
      )
      .join(", ");

    const params: unknown[] = values.flatMap((v) => [
      v.id,
      v.name,
      JSON.stringify(v.payload),
      v.createdAt,
      v.updatedAt,
      v.startedAt,
      v.finishedAt,
      v.labels,
    ]);

    const result = yield* Effect.tryPromise({
      try: () =>
        db.query<RawRow>(
          `INSERT INTO journal_entries (id, name, payload, created_at, updated_at, started_at, finished_at, labels)
           VALUES ${placeholders}
           RETURNING id, name, payload, created_at, updated_at, started_at, finished_at, labels, storage_seq`,
          params,
        ),
      catch: (cause) => new StorageUnavailable({ cause }),
    });

    return result.rows.map(decodeRow);
  });
}

export function listEntries(): Effect.Effect<ReadonlyArray<JournalEntry>, StoreError, PgliteService> {
  return Effect.gen(function* () {
    const { db } = yield* PgliteService;

    const result = yield* Effect.tryPromise({
      try: () =>
        db.query<RawRow>(
          `SELECT id, name, payload, created_at, updated_at, started_at, finished_at, labels, storage_seq
           FROM journal_entries
           ORDER BY created_at DESC, storage_seq ASC`,
        ),
      catch: (cause) => new StorageUnavailable({ cause }),
    });

    return result.rows.map(decodeRow);
  });
}
