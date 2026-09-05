import assert from "node:assert/strict";
import test from "node:test";

import {
  collectorArguments,
  meetsLineThreshold,
  parseLineCoverage,
  workspaceResultsDirectory,
} from "./dotnet-unit-coverage.mjs";

test("accepts exact 99 percent line coverage", () => {
  const coverage = parseLineCoverage('<coverage line-rate="0.99" lines-covered="99" lines-valid="100">', "fixture");

  assert.deepEqual(coverage, { covered: 99, valid: 100 });
  assert.equal(meetsLineThreshold(coverage, 99), true);
});

test("rejects a rounded line rate whose exact coverage is below 99 percent", () => {
  const coverage = parseLineCoverage('<coverage line-rate="0.99" lines-covered="9899" lines-valid="10000">', "fixture");

  assert.equal(meetsLineThreshold(coverage, 99), false);
});

test("rejects coverage without exact line counts", () => {
  assert.throws(
    () => parseLineCoverage('<coverage line-rate="0.99">', "fixture"),
    /must declare lines-covered and lines-valid/u,
  );
});

test("rejects a zero line denominator", () => {
  assert.throws(
    () => parseLineCoverage('<coverage lines-covered="0" lines-valid="0">', "fixture"),
    /zero valid lines/u,
  );
});

test("rejects an impossible covered line count", () => {
  assert.throws(
    () => parseLineCoverage('<coverage lines-covered="101" lines-valid="100">', "fixture"),
    /covers more lines than it declares valid/u,
  );
});

test("accepts only a results directory nested inside the workspace", () => {
  assert.equal(workspaceResultsDirectory("/workspace", "coverage"), "/workspace/coverage");
  assert.throws(() => workspaceResultsDirectory("/workspace", "."), /inside the workspace/u);
  assert.throws(() => workspaceResultsDirectory("/workspace", "../outside"), /inside the workspace/u);
});

test("passes explicit whole-boundary source exclusions to the XPlat collector", () => {
  assert.deepEqual(collectorArguments("unit.fsproj", "coverage/collector", ["**/Parity.fs", "**/GitRoot.fs"]), [
    "test",
    "unit.fsproj",
    "--collect:XPlat Code Coverage",
    "--results-directory",
    "coverage/collector",
    "--",
    "DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=cobertura",
    "DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.ExcludeByFile=**/Parity.fs,**/GitRoot.fs",
  ]);
});
