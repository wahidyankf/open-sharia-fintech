#!/usr/bin/env node

import { copyFileSync, mkdirSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { resolve, sep } from "node:path";
import { spawnSync } from "node:child_process";
import { pathToFileURL } from "node:url";

function option(name) {
  const index = process.argv.indexOf(name);
  if (index < 0 || index + 1 >= process.argv.length) {
    throw new Error(`missing required ${name} value`);
  }
  return process.argv[index + 1];
}

function optionValues(name) {
  return process.argv.flatMap((value, index, values) => {
    if (value !== name) return [];
    if (index + 1 >= values.length) throw new Error(`missing required ${name} value`);
    return [values[index + 1]];
  });
}

function coverageFiles(directory) {
  return readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const path = resolve(directory, entry.name);
    if (entry.isDirectory()) return coverageFiles(path);
    return entry.name === "coverage.cobertura.xml" ? [path] : [];
  });
}

export function parseLineCoverage(xml, source) {
  const root = /<coverage\s+([^>]+)>/u.exec(xml);
  if (root === null) throw new Error(`coverage root in ${source} is missing`);

  const coveredMatch = /\blines-covered="(\d+)"/u.exec(root[1]);
  const validMatch = /\blines-valid="(\d+)"/u.exec(root[1]);
  if (coveredMatch === null || validMatch === null) {
    throw new Error(`coverage root in ${source} must declare lines-covered and lines-valid`);
  }

  const covered = Number(coveredMatch[1]);
  const valid = Number(validMatch[1]);
  if (valid === 0) throw new Error(`coverage root in ${source} has zero valid lines`);
  if (covered > valid) throw new Error(`coverage root in ${source} covers more lines than it declares valid`);

  return { covered, valid };
}

export function meetsLineThreshold(coverage, threshold) {
  return coverage.covered * 100 >= threshold * coverage.valid;
}

export function workspaceResultsDirectory(workspacePath, requestedPath) {
  const workspace = resolve(workspacePath);
  const results = resolve(workspace, requestedPath);
  if (results === workspace || !results.startsWith(workspace + sep)) {
    throw new Error("--results must resolve to a directory inside the workspace");
  }
  return results;
}

export function collectorArguments(project, results, excludeByFile) {
  const settings = ["DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.Format=cobertura"];
  if (excludeByFile.length > 0) {
    settings.push(
      `DataCollectionRunSettings.DataCollectors.DataCollector.Configuration.ExcludeByFile=${excludeByFile.join(",")}`,
    );
  }

  return ["test", project, "--collect:XPlat Code Coverage", "--results-directory", results, "--", ...settings];
}

function main() {
  const workspace = resolve(process.cwd());
  const project = resolve(workspace, option("--project"));
  const results = workspaceResultsDirectory(workspace, option("--results"));
  const collectorResults = resolve(results, "collector");
  const threshold = Number(option("--line-threshold"));
  const excludeByFile = optionValues("--exclude-by-file");

  if (!Number.isFinite(threshold) || threshold < 0 || threshold > 100) {
    throw new Error("--line-threshold must be a number from 0 through 100");
  }

  rmSync(results, { recursive: true, force: true });
  mkdirSync(results, { recursive: true });

  const testEnvironment = { ...process.env };
  delete testEnvironment.GIT_DIR;
  delete testEnvironment.GIT_WORK_TREE;
  delete testEnvironment.GIT_COMMON_DIR;

  const test = spawnSync("dotnet", collectorArguments(project, collectorResults, excludeByFile), {
    env: testEnvironment,
    stdio: "inherit",
  });

  if (test.error !== undefined) throw test.error;
  if (test.status !== 0) process.exit(test.status ?? 1);

  const reports = coverageFiles(collectorResults);
  if (reports.length === 0) throw new Error(`dotnet test produced no coverage.cobertura.xml under ${collectorResults}`);

  const coverages = reports.map((report) => parseLineCoverage(readFileSync(report, "utf8"), report));
  const summaries = [...new Set(coverages.map(({ covered, valid }) => `${covered}/${valid}`))];
  if (summaries.length !== 1) {
    throw new Error(`dotnet test produced conflicting line coverage: ${summaries.join(", ")}`);
  }

  const coverage = coverages[0];
  const percent = (coverage.covered * 100) / coverage.valid;
  const stableReport = resolve(results, "coverage.cobertura.xml");
  copyFileSync(reports.sort()[0], stableReport);
  rmSync(collectorResults, { recursive: true, force: true });

  console.log(
    `Unit line coverage: ${coverage.covered}/${coverage.valid} (${percent.toFixed(2)}%; required: ${threshold.toFixed(2)}%)`,
  );
  console.log(`Coverage report: ${stableReport}`);

  if (!meetsLineThreshold(coverage, threshold)) {
    console.error(`ERROR: Unit line coverage ${percent.toFixed(2)}% is below ${threshold.toFixed(2)}%.`);
    process.exit(1);
  }
}

const invokedPath = process.argv[1] === undefined ? undefined : pathToFileURL(resolve(process.argv[1])).href;
if (invokedPath === import.meta.url) main();
