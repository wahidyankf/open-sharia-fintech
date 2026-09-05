import { layer } from "@effect/vitest";
import { Effect, Layer, Schema } from "effect";
import { PGlite } from "@electric-sql/pglite";
import { expect } from "vitest";
import { EmptyBatch, StorageUnavailable } from "../../../../../src/contexts/journal/domain/errors";
import { EntryName, EntryPayload } from "../../../../../src/contexts/journal/domain/schema";
import { appendEntries, listEntries } from "../../../../../src/contexts/journal/infrastructure/journal-store";
import { runMigrations } from "../../../../../src/contexts/journal/infrastructure/run-migrations";
import { PgliteService } from "../../../../../src/contexts/journal/infrastructure/runtime";

const TestPgliteLayer = Layer.scoped(
  PgliteService,
  Effect.acquireRelease(
    Effect.promise(async () => {
      const db = new PGlite();
      await runMigrations(db);
      return { db };
    }),
    ({ db }) => Effect.promise(() => db.close()),
  ),
);

const makeName = (value: string) => Schema.decodeUnknownSync(EntryName)(value);
const makePayload = (value: Record<string, unknown>) => Schema.decodeUnknownSync(EntryPayload)(value);
const makeTimestamp = () =>
  new Date().toISOString() as unknown as import("../../../../../src/contexts/journal/domain/schema").IsoTimestamp;

layer(TestPgliteLayer)("journal-store - appendEntries", (it) => {
  it.effect("returns EmptyBatch error on empty input", () =>
    Effect.gen(function* () {
      const result = yield* Effect.either(appendEntries([]));
      expect(result._tag).toBe("Left");
      if (result._tag === "Left") {
        expect(result.left).toBeInstanceOf(EmptyBatch);
      }
    }),
  );

  it.effect("appends entries and returns them", () =>
    Effect.gen(function* () {
      const timestamp = makeTimestamp();
      const entries = yield* appendEntries([
        {
          name: makeName("workout"),
          payload: makePayload({ reps: 5 }),
          startedAt: timestamp,
          finishedAt: timestamp,
          labels: [] as const,
        },
        {
          name: makeName("meal"),
          payload: makePayload({ calories: 500 }),
          startedAt: timestamp,
          finishedAt: timestamp,
          labels: [] as const,
        },
      ]);

      expect(entries).toHaveLength(2);
      expect(entries[0]?.name).toBe("workout");
      expect(entries[1]?.name).toBe("meal");
      expect(entries[0]?.id).toBeTruthy();
      expect(entries[0]?.createdAt).toBeTruthy();
    }),
  );
});

layer(TestPgliteLayer)("journal-store - listEntries", (it) => {
  it.effect(
    "returns entries ordered by created_at DESC",
    () =>
      Effect.gen(function* () {
        const firstTimestamp = makeTimestamp();
        yield* appendEntries([
          {
            name: makeName("reading"),
            payload: makePayload({}),
            startedAt: firstTimestamp,
            finishedAt: firstTimestamp,
            labels: [] as const,
          },
        ]);

        yield* Effect.promise(() => new Promise((resolve) => setTimeout(resolve, 10)));

        const secondTimestamp = makeTimestamp();
        yield* appendEntries([
          {
            name: makeName("learning"),
            payload: makePayload({}),
            startedAt: secondTimestamp,
            finishedAt: secondTimestamp,
            labels: [] as const,
          },
        ]);

        const entries = yield* listEntries();
        expect(entries).toHaveLength(2);
        expect(entries[0]?.name).toBe("learning");
        expect(entries[1]?.name).toBe("reading");
      }),
    { timeout: 30000 },
  );
});

const FailingDbLayer = Layer.scoped(
  PgliteService,
  Effect.acquireRelease(
    Effect.sync(() => ({
      db: {
        query: () => Promise.reject(new Error("connection lost")),
      } as unknown as PGlite,
    })),
    () => Effect.void,
  ),
);

layer(FailingDbLayer)("journal-store - StorageUnavailable on connection failure", (it) => {
  it.effect("appendEntries surfaces StorageUnavailable", () =>
    Effect.gen(function* () {
      const timestamp = makeTimestamp();
      const result = yield* Effect.either(
        appendEntries([
          {
            name: makeName("workout"),
            payload: makePayload({}),
            startedAt: timestamp,
            finishedAt: timestamp,
            labels: [] as const,
          },
        ]),
      );
      expect(result._tag).toBe("Left");
      if (result._tag === "Left") {
        expect(result.left).toBeInstanceOf(StorageUnavailable);
      }
    }),
  );
});
