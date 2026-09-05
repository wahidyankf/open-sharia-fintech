#!/usr/bin/env node

import { generateMessages } from "@cucumber/gherkin";
import { SourceMediaType } from "@cucumber/messages";
import { readFile, readdir, stat } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const ADAPTERS = ["unit", "integration", "e2e"];
const EXEMPTION_TAGS = new Set(["integration-exempt", "e2e-exempt"]);
const FORBIDDEN_TAGS = new Set(["unit-exempt", "wip", "unit", "integration", "e2e"]);
const EXEMPTION_COMMENT = /^# Exemption\((integration|e2e)\): (.+); alternative-proof: (.+)$/u;
const INVALID_REASON =
  /\b(?:hard|slow|runtime|flaky|cost(?:ly)?|expensive|todo|unfinished|missing[ -]implementation|not[ -]yet[ -]implemented)\b/iu;
const BOUNDARY_REASON =
  /\b(?:boundary|public|private|internal|browser|layout|network|socket|process|filesystem|file system|database|local|same-machine|operating system|os-facing|inject|observable|trigger|http|tcp|udp)\b/iu;
const ALTERNATIVE_PROOF = /^[a-z0-9][a-z0-9-]*:test(?::[a-z0-9][a-z0-9-]*)+\s+\/\s+\S(?:.*\S)?$/iu;
const GHERKIN_DECLARATION = /^(?:Feature|Rule|Background|Scenario(?: Outline| Template)?|Examples?):/iu;
const SCENARIO_DECLARATION = /^(?:Scenario(?: Outline| Template)?):/iu;
const BINDING_FILE = /\.(?:ts|tsx|fs)$/iu;

function normaliseSource(source) {
  return source.replaceAll("\r\n", "\n").replaceAll("\r", "\n");
}

function parseFeature(resourceName, source) {
  let nextId = 0;
  let envelopes;
  try {
    envelopes = generateMessages(normaliseSource(source), resourceName, SourceMediaType.TEXT_X_CUCUMBER_GHERKIN_PLAIN, {
      includeSource: false,
      includeGherkinDocument: true,
      includePickles: true,
      newId: () => `${resourceName}:${nextId++}`,
    });
  } catch (error) {
    return {
      errors: [`${resourceName}: parse error: ${error instanceof Error ? error.message : String(error)}`],
      document: undefined,
      pickles: [],
    };
  }

  const errors = envelopes
    .filter((envelope) => envelope.parseError !== undefined)
    .map(
      ({ parseError }) =>
        `${resourceName}: parse error at ${parseError.source?.location?.line ?? "unknown"}: ${parseError.message}`,
    );
  const document = envelopes.find((envelope) => envelope.gherkinDocument !== undefined)?.gherkinDocument;
  const pickles = envelopes.filter((envelope) => envelope.pickle !== undefined).map(({ pickle }) => pickle);

  return { errors, document, pickles };
}

function scenariosIn(document) {
  if (document?.feature === undefined) return [];

  const scenarios = [];
  const visitChildren = (children) => {
    for (const child of children ?? []) {
      if (child.scenario !== undefined) scenarios.push(child.scenario);
      if (child.rule !== undefined) visitChildren(child.rule.children);
    }
  };
  visitChildren(document.feature.children);
  return scenarios;
}

function validateScenarioShape(resourceName, document) {
  const errors = [];
  const scenarios = scenariosIn(document);
  if (document?.feature === undefined) {
    errors.push(`${resourceName}: missing Feature declaration.`);
    return errors;
  }
  if (scenarios.length === 0) {
    errors.push(`${resourceName}: feature must contain at least one scenario.`);
  }

  for (const scenario of scenarios) {
    const label = `${scenario.keyword}: ${scenario.name}`;
    if (scenario.name.trim() === "") {
      errors.push(`${resourceName}:${scenario.location.line}: scenario name must not be empty.`);
    }
    if (!scenario.steps.some((step) => step.keyword.trim().toLowerCase() === "when")) {
      errors.push(`${resourceName}: ${label} requires an explicit When step.`);
    }
    if (!scenario.steps.some((step) => step.keyword.trim().toLowerCase() === "then")) {
      errors.push(`${resourceName}: ${label} requires an explicit Then step.`);
    }
    if (/outline|template/iu.test(scenario.keyword)) {
      const exampleRows = scenario.examples.flatMap((example) => example.tableBody ?? []);
      if (exampleRows.length === 0) {
        errors.push(`${resourceName}:${scenario.location.line}: ${label} requires at least one Examples row.`);
      }
    }
  }
  return errors;
}

function tagsOnLine(trimmed) {
  return trimmed
    .split(/\s+/u)
    .filter((part) => part.startsWith("@"))
    .map((part) => part.slice(1));
}

function exemptionCommentErrors(resourceName, lines, lineNumber, tagName) {
  const layer = tagName.replace("-exempt", "");
  const comment = lines[lineNumber - 2]?.trim() ?? "";
  const match = EXEMPTION_COMMENT.exec(comment);
  if (match === null || match[1] !== layer) {
    return [
      `${resourceName}:${lineNumber}: @${tagName} requires its own immediately preceding comment ` +
        `'# Exemption(${layer}): <boundary reason>; alternative-proof: <project>:test... / <scenario>'.`,
    ];
  }

  const errors = [];
  const reason = match[2] ?? "";
  if (INVALID_REASON.test(reason)) {
    errors.push(
      `${resourceName}:${lineNumber}: an exemption cannot be justified by difficulty, runtime, speed, cost, flakiness, or unfinished work.`,
    );
  }
  if (!BOUNDARY_REASON.test(reason)) {
    errors.push(`${resourceName}:${lineNumber}: an exemption reason must describe a genuine boundary mismatch.`);
  }
  if (!ALTERNATIVE_PROOF.test(match[3] ?? "")) {
    errors.push(`${resourceName}:${lineNumber}: alternative-proof must use '<project>:test... / <scenario>'.`);
  }
  return errors;
}

function validateTagPolicy(resourceName, source) {
  const lines = normaliseSource(source).split("\n");
  const errors = [];
  let pending = [];
  let insideDocString = false;

  lines.forEach((line, index) => {
    const trimmed = line.trim();
    const lineNumber = index + 1;
    if (trimmed.startsWith('"""') || trimmed.startsWith("```")) {
      insideDocString = !insideDocString;
      return;
    }
    if (insideDocString) return;
    if (trimmed.startsWith("@")) {
      const names = tagsOnLine(trimmed);
      const exemptions = names.filter((name) => EXEMPTION_TAGS.has(name));
      if (exemptions.length > 0 && names.length !== 1) {
        errors.push(`${resourceName}:${lineNumber}: each exemption requires a separate tag line.`);
      }
      for (const name of names) {
        const lowerName = name.toLowerCase();
        if (
          FORBIDDEN_TAGS.has(lowerName) ||
          lowerName.startsWith("no-") ||
          (lowerName.endsWith("-exempt") && !EXEMPTION_TAGS.has(name))
        ) {
          errors.push(
            `${resourceName}:${lineNumber}: @${name} is forbidden; Unit has no exemption and positive layer-selection tags are not used.`,
          );
        }
        if (EXEMPTION_TAGS.has(name)) {
          errors.push(...exemptionCommentErrors(resourceName, lines, lineNumber, name));
        }
        pending.push({ line: lineNumber, name });
      }
      return;
    }

    if (GHERKIN_DECLARATION.test(trimmed)) {
      const exemptions = pending.filter(({ name }) => EXEMPTION_TAGS.has(name));
      if (exemptions.length > 0 && !SCENARIO_DECLARATION.test(trimmed)) {
        errors.push(`${resourceName}:${lineNumber}: exemption tags may only annotate a Scenario or Scenario Outline.`);
      }
      pending = [];
      return;
    }

    if (trimmed !== "" && !trimmed.startsWith("#") && pending.length > 0) {
      errors.push(`${resourceName}:${lineNumber}: tags must be followed by their Gherkin declaration.`);
      pending = [];
    }
  });

  if (pending.length > 0) {
    errors.push(`${resourceName}: dangling tags are not attached to a scenario.`);
  }
  return errors;
}

export function validateFeatureSource(resourceName, source) {
  const parsed = parseFeature(resourceName, source);
  const errors = [...parsed.errors, ...validateTagPolicy(resourceName, source)];
  if (parsed.errors.length === 0) {
    errors.push(...validateScenarioShape(resourceName, parsed.document));
  }
  return { errors, pickles: parsed.pickles };
}

function lineAt(source, offset) {
  return source.slice(0, offset).split("\n").length;
}

function decodeQuotedLiteral(literal) {
  const quote = literal[0];
  const body = literal.slice(1, -1);
  if (quote === '"') {
    try {
      return JSON.parse(literal);
    } catch {
      return body.replaceAll('\\"', '"').replaceAll("\\\\", "\\");
    }
  }
  return body.replaceAll(`\\${quote}`, quote).replaceAll("\\n", "\n").replaceAll("\\\\", "\\");
}

function maskJavascriptComments(source) {
  const characters = [...source];
  let state = "code";
  for (let index = 0; index < characters.length; index += 1) {
    const character = characters[index];
    const next = characters[index + 1];
    if (state === "line-comment") {
      if (character === "\n") state = "code";
      else characters[index] = " ";
      continue;
    }
    if (state === "block-comment") {
      if (character === "*" && next === "/") {
        characters[index] = " ";
        characters[index + 1] = " ";
        index += 1;
        state = "code";
      } else if (character !== "\n") {
        characters[index] = " ";
      }
      continue;
    }
    if (state !== "code") {
      if (character === "\\") index += 1;
      else if (
        (state === "single" && character === "'") ||
        (state === "double" && character === '"') ||
        (state === "template" && character === "`")
      ) {
        state = "code";
      }
      continue;
    }
    if (character === "/" && next === "/") {
      characters[index] = " ";
      characters[index + 1] = " ";
      index += 1;
      state = "line-comment";
    } else if (character === "/" && next === "*") {
      characters[index] = " ";
      characters[index + 1] = " ";
      index += 1;
      state = "block-comment";
    } else if (character === "'") state = "single";
    else if (character === '"') state = "double";
    else if (character === "`") state = "template";
  }
  return characters.join("");
}

function maskFsharpComments(source) {
  return source
    .replace(/\(\*[\s\S]*?\*\)/gu, (comment) => comment.replace(/[^\n]/gu, " "))
    .replace(/\/\/.*$/gmu, (comment) => " ".repeat(comment.length));
}

function typescriptScenarioScopes(source) {
  if (!/\bdescribeFeature\s*\(/u.test(source)) return [];
  const scopes = [];
  const pattern = /\bScenario(?:Outline)?\s*\(\s*("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)/gu;
  for (const match of source.matchAll(pattern)) {
    scopes.push({
      offset: match.index ?? 0,
      name: decodeQuotedLiteral(match[1]),
    });
  }
  return scopes;
}

function scenarioAt(scopes, offset) {
  let scenario;
  for (const scope of scopes) {
    if (scope.offset >= offset) break;
    scenario = scope.name;
  }
  return scenario;
}

function typescriptFeatureReferences(source) {
  const references = [];
  const pattern = /("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`)/gu;
  for (const match of source.matchAll(pattern)) {
    const value = decodeQuotedLiteral(match[1]).replaceAll("\\", "/");
    const specsOffset = value.lastIndexOf("specs/");
    if (specsOffset >= 0 && value.toLowerCase().endsWith(".feature")) {
      references.push(value.slice(specsOffset));
    }
  }
  return [...new Set(references)];
}

function fsharpFeatureReferences(source) {
  const references = [];
  const pattern = /"(?:\\.|[^"\\])*"/gu;
  for (const match of source.matchAll(pattern)) {
    const value = decodeQuotedLiteral(match[0]).replaceAll("\\", "/");
    const specsOffset = value.lastIndexOf("specs/");
    if (specsOffset >= 0 && value.toLowerCase().endsWith(".feature")) {
      references.push(value.slice(specsOffset));
    }
  }
  return [...new Set(references)];
}

function extractTypescriptBindings(resourceName, source) {
  const bindings = [];
  const code = maskJavascriptComments(source);
  const scopes = typescriptScenarioScopes(code);
  const featureReferences = typescriptFeatureReferences(code);
  const pattern =
    /\b(Given|When|Then|And|But)\s*\(\s*("(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`(?:\\.|[^`\\])*`|\/(?:\\.|[^/\\\n])+\/[dgimsuvy]*)/gu;
  for (const match of code.matchAll(pattern)) {
    const literal = match[2];
    const regex = literal.startsWith("/");
    const lastSlash = regex ? literal.lastIndexOf("/") : -1;
    bindings.push({
      keyword: match[1],
      pattern: regex ? literal.slice(1, lastSlash) : decodeQuotedLiteral(literal),
      flags: regex ? literal.slice(lastSlash + 1) : "",
      expression: !regex,
      resourceName,
      line: lineAt(source, match.index ?? 0),
      scenario: scenarioAt(scopes, match.index ?? 0),
      featureReferences,
      keywordSensitive: false,
    });
  }
  return bindings;
}

function extractFsharpBindings(resourceName, source) {
  const bindings = [];
  const code = maskFsharpComments(source);
  const featureReferences = fsharpFeatureReferences(code);
  const pattern =
    /\[<(Given|When|Then)>\][\s\S]*?\b(?:let(?:\s+(?:mutable|private|internal))*\s+|member(?:\s+(?:private|internal))*\s+[A-Za-z_][A-Za-z0-9_']*\.)``([\s\S]*?)``/gu;
  for (const match of code.matchAll(pattern)) {
    bindings.push({
      keyword: match[1],
      pattern: match[2],
      flags: "",
      expression: false,
      resourceName,
      line: lineAt(source, match.index ?? 0),
      scenario: undefined,
      featureReferences,
      keywordSensitive: true,
    });
  }
  return bindings;
}

export function extractBindings(resourceName, source) {
  return resourceName.toLowerCase().endsWith(".fs")
    ? extractFsharpBindings(resourceName, source)
    : extractTypescriptBindings(resourceName, source);
}

function escapeRegex(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&");
}

function cucumberExpressionRegex(expression) {
  const placeholders = [];
  let tokenised = expression.replace(/\{([^}]+)\}/gu, (_whole, name) => {
    const marker = `OSECUCUMBERPLACEHOLDER${placeholders.length}END`;
    placeholders.push(name);
    return marker;
  });
  tokenised = tokenised.replace(/<[^>\n]+>/gu, () => {
    const marker = `OSECUCUMBERPLACEHOLDER${placeholders.length}END`;
    placeholders.push("outline-example");
    return marker;
  });
  // Playwright-BDD string expressions escape Cucumber metacharacters when
  // the feature text requires the literal character. Static matching works
  // on the resulting feature text, so discard that expression-level escape
  // before escaping the whole pattern for JavaScript RegExp construction.
  tokenised = tokenised.replace(/\\([/()])/gu, "$1");
  let source = escapeRegex(tokenised);
  placeholders.forEach((name, index) => {
    let replacement;
    switch (name) {
      case "string":
        replacement = "(?:\"[^\"\\n]*\"|'[^'\\n]*')";
        break;
      case "int":
        replacement = "-?\\d+";
        break;
      case "float":
        replacement = "-?(?:\\d+(?:\\.\\d+)?|\\.\\d+)";
        break;
      case "word":
        replacement = "\\S+";
        break;
      case "outline-example":
        replacement = ".+";
        break;
      default:
        replacement = ".+";
        break;
    }
    source = source.replace(`OSECUCUMBERPLACEHOLDER${index}END`, replacement);
  });
  return new RegExp(`^(?:${source})$`, "u");
}

function bindingRegex(binding) {
  if (binding.expression) return cucumberExpressionRegex(binding.pattern);
  try {
    const flags = [...new Set(binding.flags.replace(/[gy]/gu, "").split(""))].join("").replace("v", "u");
    return new RegExp(`^(?:${binding.pattern})$`, flags.includes("u") ? flags : `${flags}u`);
  } catch {
    return undefined;
  }
}

function matchingBindings(bindings, featureFile, pickle, step) {
  const normalisedFeatureFile = featureFile.replaceAll("\\", "/");
  return bindings.filter((binding) => {
    if (
      binding.featureReferences.length > 0 &&
      !binding.featureReferences.some((reference) => normalisedFeatureFile.endsWith(reference))
    ) {
      return false;
    }
    if (binding.scenario !== undefined && binding.scenario !== pickle.name) {
      return false;
    }
    const keyword = binding.keyword.toLowerCase();
    const type = step.type?.toLowerCase();
    const compatibleKeyword =
      keyword === "and" ||
      keyword === "but" ||
      (keyword === "given" && type === "context") ||
      (keyword === "when" && type === "action") ||
      (keyword === "then" && type === "outcome");
    return (!binding.keywordSensitive || compatibleKeyword) && bindingRegex(binding)?.test(step.text);
  });
}

export async function findFiles(root, predicate) {
  let metadata;
  try {
    metadata = await stat(root);
  } catch {
    return [];
  }
  if (metadata.isFile()) return predicate(root) ? [root] : [];
  if (!metadata.isDirectory()) return [];

  const entries = await readdir(root, { withFileTypes: true });
  const descendants = await Promise.all(entries.map((entry) => findFiles(path.join(root, entry.name), predicate)));
  return descendants.flat().toSorted();
}

async function pathExists(target) {
  try {
    await stat(target);
    return true;
  } catch {
    return false;
  }
}

function commandSurface(target) {
  return JSON.stringify({
    command: target?.options?.command,
    commands: target?.options?.commands,
    dependsOn: target?.dependsOn,
  });
}

function referencesTarget(command, target) {
  const escaped = target.replace(/[.*+?^${}()|[\]\\]/gu, "\\$&");
  return new RegExp(`(?:^|[\\s:'"])(?:[a-z0-9-]+:)?${escaped}(?=$|[\\s'"])`, "iu").test(command);
}

const RUNTIME_RUNNER = /\b(?:vitest|playwright|cargo\s+test|dotnet\s+test|mix\s+test|npm\s+test)\b/iu;
const VITEST_LINE_THRESHOLD = /--coverage\.thresholds\.lines(?:=|\s+)(\d+(?:\.\d+)?)/iu;
const COVERLET_THRESHOLD = /\/p:Threshold(?:=|\s+)(\d+(?:\.\d+)?)/iu;
const COVERLET_LINE_TYPE = /\/p:ThresholdType(?:=|\s+)line\b/iu;
const COLLECTOR_LINE_THRESHOLD = /\bdotnet-unit-coverage\.mjs\b[^\n]*--line-threshold(?:=|\s+)(\d+(?:\.\d+)?)/iu;

function unitLineCoverageThreshold(target) {
  const surface = commandSurface(target);
  const vitest = VITEST_LINE_THRESHOLD.exec(surface);
  if (vitest !== null) return Number(vitest[1]);
  const coverlet = COVERLET_THRESHOLD.exec(surface);
  if (coverlet !== null && COVERLET_LINE_TYPE.test(surface)) return Number(coverlet[1]);
  const collector = COLLECTOR_LINE_THRESHOLD.exec(surface);
  if (collector !== null) return Number(collector[1]);
  return undefined;
}

export async function validateProjectTargetContract(projectFile, configuredProject, configuredAdapters) {
  if (!(await pathExists(projectFile))) return [];

  let project;
  try {
    project = JSON.parse(await readFile(projectFile, "utf8"));
  } catch (error) {
    return [`${projectFile}: invalid project.json: ${error instanceof Error ? error.message : String(error)}`];
  }

  const errors = [];
  if (project.name !== undefined && project.name !== configuredProject) {
    errors.push(`${projectFile}: behaviour coverage project '${configuredProject}' does not match '${project.name}'.`);
  }
  const targets = project.targets ?? {};
  const dedicatedE2e = configuredProject.endsWith("-e2e");
  const ownedAdapters = dedicatedE2e ? ["e2e"] : Object.keys(configuredAdapters ?? {});

  if (!dedicatedE2e) {
    if (targets["test:unit"] === undefined) {
      errors.push(`${projectFile}: behaviour owner requires test:unit.`);
    } else {
      const threshold = unitLineCoverageThreshold(targets["test:unit"]);
      if (threshold === undefined) {
        errors.push(`${projectFile}: owner test:unit must enforce at least 99% line coverage.`);
      } else if (threshold < 99) {
        errors.push(`${projectFile}: owner test:unit line coverage threshold ${threshold}% is below the 99% minimum.`);
      }
    }
  }
  for (const adapter of ownedAdapters) {
    const ownsRuntime = adapter !== "e2e" || dedicatedE2e;
    if (ownsRuntime && targets[`test:${adapter}`] === undefined) {
      errors.push(`${projectFile}: configured ${adapterLabel(adapter)} adapter requires test:${adapter}.`);
    }
    if (targets[`test:coverage:${adapter}`] === undefined) {
      errors.push(`${projectFile}: configured ${adapterLabel(adapter)} adapter requires test:coverage:${adapter}.`);
    }
  }
  if (targets["test:coverage:behaviour"] === undefined) {
    errors.push(`${projectFile}: behaviour owner requires test:coverage:behaviour.`);
  }
  if (targets["test:coverage"] === undefined) {
    errors.push(`${projectFile}: behaviour owner requires aggregate test:coverage.`);
  }

  const coverageTargets = Object.entries(targets).filter(([name]) => name.startsWith("test:coverage"));
  for (const [name, target] of coverageTargets) {
    const surface = commandSurface(target);
    if (
      RUNTIME_RUNNER.test(surface) ||
      referencesTarget(surface, "test:unit") ||
      referencesTarget(surface, "test:integration") ||
      referencesTarget(surface, "test:e2e")
    ) {
      errors.push(`${projectFile}: ${name} must be static and must not execute a runtime test target or runner.`);
    }
    if (name !== "test:coverage" && !surface.includes("behaviour-coverage.mjs")) {
      errors.push(`${projectFile}: ${name} must invoke the project-local static behaviour validator.`);
    }
  }

  const quick = targets["test:quick"];
  if (quick === undefined) {
    errors.push(`${projectFile}: behaviour project requires test:quick.`);
  } else {
    const surface = commandSurface(quick);
    if (!referencesTarget(surface, "test:coverage")) {
      errors.push(`${projectFile}: test:quick must include aggregate test:coverage.`);
    }
    if (!dedicatedE2e && !referencesTarget(surface, "test:unit")) {
      errors.push(`${projectFile}: owner test:quick must include mandatory test:unit.`);
    }
    if (referencesTarget(surface, "test:integration") || referencesTarget(surface, "test:e2e")) {
      errors.push(`${projectFile}: test:quick must not execute Integration or E2E runtime.`);
    }
    if (
      Array.isArray(quick.options?.commands) &&
      quick.options.commands.length > 1 &&
      quick.options.parallel !== false
    ) {
      errors.push(`${projectFile}: test:quick command composition must set parallel to false.`);
    }
  }

  return errors;
}

async function loadCorpus(corpusRoots) {
  const featureFiles = (
    await Promise.all(corpusRoots.map((root) => findFiles(root, (file) => file.toLowerCase().endsWith(".feature"))))
  ).flat();
  const uniqueFeatureFiles = [...new Set(featureFiles)].toSorted();
  const parsed = await Promise.all(
    uniqueFeatureFiles.map(async (file) => ({
      file,
      result: validateFeatureSource(file, await readFile(file, "utf8")),
    })),
  );
  return { featureFiles: uniqueFeatureFiles, parsed };
}

async function loadBindings(bindingRoots) {
  const discovered = await Promise.all(bindingRoots.map((root) => findFiles(root, (file) => BINDING_FILE.test(file))));
  const files = [...new Set(discovered.flat())].toSorted();
  const bindings = (
    await Promise.all(files.map(async (file) => extractBindings(file, await readFile(file, "utf8"))))
  ).flat();
  return { files, bindings };
}

function adapterLabel(adapter) {
  return adapter === "e2e" ? "E2E" : `${adapter[0].toUpperCase()}${adapter.slice(1)}`;
}

function pickleIsExempt(pickle, adapter) {
  if (adapter === "unit") return false;
  return pickle.tags.some((tag) => tag.name === `@${adapter}-exempt`);
}

async function validateAdapter(adapter, parsedCorpus, configuration) {
  const label = adapterLabel(adapter);
  const errors = [];
  if (configuration === undefined) {
    return {
      errors: [`${label} adapter configuration is missing.`],
      bindingFiles: 0,
      bindings: 0,
    };
  }
  if (!(await pathExists(configuration.driver))) {
    errors.push(`${label} driver does not exist: ${configuration.driver}`);
  }
  const loaded = await loadBindings(configuration.bindingRoots);
  const used = new Set();
  const corpusFiles = parsedCorpus.map(({ file }) => file.replaceAll("\\", "/"));

  for (const { file, result } of parsedCorpus) {
    for (const pickle of result.pickles) {
      if (pickleIsExempt(pickle, adapter)) continue;
      for (const step of pickle.steps) {
        const matches = matchingBindings(loaded.bindings, file, pickle, step);
        const coordinate = `${file}: ${pickle.name} / ${step.text}`;
        if (matches.length === 0) {
          errors.push(`${coordinate}: undefined ${label} binding.`);
        } else if (matches.length > 1) {
          errors.push(`${coordinate}: ambiguous ${label} binding (${matches.length} matches).`);
        } else {
          used.add(matches[0]);
        }
      }
    }
  }

  for (const binding of loaded.bindings) {
    const belongsToCorpus =
      binding.featureReferences.length === 0 ||
      binding.featureReferences.some((reference) => corpusFiles.some((file) => file.endsWith(reference)));
    if (!belongsToCorpus) continue;
    if (!used.has(binding)) {
      errors.push(`${binding.resourceName}:${binding.line}: unused ${label} binding '${binding.pattern}'.`);
    }
  }
  return {
    errors,
    bindingFiles: loaded.files.length,
    bindings: loaded.bindings.length,
  };
}

function directConfiguration(options) {
  return {
    bindingRoots: options.bindingRoots ?? [],
    driver: options.driver ?? "",
  };
}

export async function validateCoverage(options) {
  const errors = [];
  if (options.projectFile !== undefined) {
    errors.push(...(await validateProjectTargetContract(options.projectFile, options.project, options.adapters)));
  }
  if (!Array.isArray(options.corpusRoots) || options.corpusRoots.length === 0) {
    errors.push(`${options.project}: at least one corpus root is required.`);
  }
  const corpus = await loadCorpus(options.corpusRoots ?? []);
  if (corpus.featureFiles.length === 0) {
    errors.push(`${options.project}: no .feature files found in the configured corpus.`);
  }
  errors.push(...corpus.parsed.flatMap(({ result }) => result.errors));

  const adapters =
    options.adapter === "behaviour"
      ? ADAPTERS.filter((adapter) => options.adapters?.[adapter] !== undefined)
      : [options.adapter];
  if (options.adapter === "behaviour" && options.adapters?.unit === undefined) {
    errors.push(`${options.project}: aggregate behaviour coverage requires a Unit adapter.`);
  }
  if (![...ADAPTERS, "behaviour"].includes(options.adapter)) {
    errors.push(`${options.project}: unsupported adapter '${options.adapter}'.`);
  }

  const adapterStats = [];
  for (const adapter of adapters.filter((value) => ADAPTERS.includes(value))) {
    const configuration = options.adapter === "behaviour" ? options.adapters[adapter] : directConfiguration(options);
    const validation = await validateAdapter(adapter, corpus.parsed, configuration);
    errors.push(...validation.errors);
    adapterStats.push({ adapter, ...validation });
  }

  return {
    errors: errors.toSorted(),
    stats: {
      project: options.project,
      features: corpus.featureFiles.length,
      scenarios: corpus.parsed.reduce((count, { result }) => count + result.pickles.length, 0),
      adapters,
      adapterStats,
    },
  };
}

function collectArguments(argv) {
  const argumentsByName = new Map();
  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    if (!argument.startsWith("--")) {
      throw new Error(`unexpected argument '${argument}'`);
    }
    const name = argument.slice(2);
    const value = argv[index + 1];
    if (value === undefined || value.startsWith("--")) {
      throw new Error(`--${name} requires a value`);
    }
    argumentsByName.set(name, [...(argumentsByName.get(name) ?? []), value]);
    index += 1;
  }
  return argumentsByName;
}

function one(argumentsByName, name) {
  const values = argumentsByName.get(name) ?? [];
  if (values.length > 1) throw new Error(`--${name} may only be supplied once`);
  return values[0];
}

function resolvePaths(base, values) {
  return values.map((value) => path.resolve(base, value));
}

function normaliseConfig(config, base, selectedAdapter) {
  if (typeof config.project !== "string" || config.project === "") {
    throw new Error("config.project must be a non-empty string");
  }
  if (!Array.isArray(config.corpus) || config.corpus.length === 0) {
    throw new Error("config.corpus must be a non-empty array");
  }
  const adapters = Object.fromEntries(
    Object.entries(config.adapters ?? {}).map(([adapter, value]) => [
      adapter,
      {
        bindingRoots: resolvePaths(base, value.bindings ?? []),
        driver: path.resolve(base, value.driver ?? ""),
      },
    ]),
  );
  const common = {
    project: config.project,
    projectFile: path.join(base, "project.json"),
    corpusRoots: resolvePaths(base, config.corpus),
    adapter: selectedAdapter,
  };
  if (selectedAdapter === "behaviour") return { ...common, adapters };
  const selected = adapters[selectedAdapter];
  if (selected === undefined) {
    throw new Error(`config.adapters.${selectedAdapter} is required`);
  }
  return { ...common, ...selected };
}

export async function parseCliOptions(argv, cwd = process.cwd()) {
  const args = collectArguments(argv);
  const configPath = one(args, "config");
  const adapter = one(args, "adapter") ?? "behaviour";
  if (configPath !== undefined) {
    const absoluteConfig = path.resolve(cwd, configPath);
    const config = JSON.parse(await readFile(absoluteConfig, "utf8"));
    return normaliseConfig(config, path.dirname(absoluteConfig), adapter);
  }

  const project = one(args, "project");
  const driver = one(args, "driver");
  if (project === undefined) throw new Error("--project is required");
  if (adapter === "behaviour") {
    throw new Error("aggregate behaviour mode requires --config");
  }
  if (driver === undefined) throw new Error("--driver is required");
  return {
    project,
    adapter,
    corpusRoots: resolvePaths(cwd, args.get("corpus") ?? []),
    bindingRoots: resolvePaths(cwd, args.get("bindings") ?? []),
    driver: path.resolve(cwd, driver),
  };
}

export async function runCli(argv, io = console) {
  try {
    const options = await parseCliOptions(argv);
    const result = await validateCoverage(options);
    if (result.errors.length > 0) {
      result.errors.forEach((error) => io.error(error));
      return 1;
    }
    io.log(
      `${result.stats.project}: ${result.stats.features} features, ${result.stats.scenarios} expanded scenarios, adapters: ${result.stats.adapters.join(", ")}.`,
    );
    return 0;
  } catch (error) {
    io.error(error instanceof Error ? error.message : String(error));
    return 2;
  }
}

const isMain = process.argv[1] !== undefined && fileURLToPath(import.meta.url) === path.resolve(process.argv[1]);
if (isMain) {
  process.exitCode = await runCli(process.argv.slice(2));
}
