# Anti-Hallucination Fixes (Part 1)

Per the
[Plan Anti-Hallucination Convention](../../../../repo-governance/development/quality/plan-anti-hallucination.md):
apply a fix only AFTER running the verification recipe for that claim category. If the recipe cannot
establish the correct value, classify MEDIUM — never invent a replacement. Replacing one
hallucination with another that looks more plausible is the single most damaging fixer behaviour.

**Mandatory repo-grounding before apply** — per
[§Repo-Grounding Rule](../../../../repo-governance/development/quality/plan-anti-hallucination/repo-grounding-rule-hard.md#repo-grounding-rule-hard):

```bash
# File path replacement — confirm the target exists OR mark _New file_
test -f <new-path> && echo "HIGH apply" || echo "MEDIUM manual"

# Nx target replacement — confirm target appears in project.json
jq -r '.targets | keys[]' apps/<project>/project.json | grep -qx '<target>' && echo "HIGH apply" || echo "MEDIUM manual"

# Package version replacement — confirm value matches the manifest
jq -r '.dependencies.<pkg> // .devDependencies.<pkg>' package.json

# Symbol replacement — confirm grep evidence
rg -l "<symbol>" apps/ libs/

# Agent / skill name replacement — confirm definition exists (agents live in nested role
# subfolders, e.g. .claude/agents/swe/swe-typescript-dev.md, not flat under .claude/agents/)
find .claude/agents -name '<name>.md' | grep -q . && echo "HIGH apply" || echo "MEDIUM manual"
```

If the recipe fails: search for a correct value, re-run the recipe with it; if still no correct
value, classify MEDIUM, write into `## Manual Review Required`, do NOT apply.

**Per-Anti-Pattern fix strategy**: AP-1 (version without manifest evidence) → `jq` the manifest,
replace + `[Repo-grounded]` label. AP-2 (file path doesn't exist, not marked NEW) → `Glob` for the
intended file; replace if found, else append `_New file_` and add a creation step. AP-3 (invalid Nx
target) → read `project.json`, replace with closest real match, else MEDIUM. AP-4 (fabricated
function/method name) → delegate to `web-researcher` (or escalate MEDIUM). AP-5 (fabricated numeric
KPI) → rewrite as observable check/cited measurement/qualitative reasoning/`_Judgment call:_` (never
invent a number). AP-6 (fabricated test name) → `Grep` for the real name if pre-existing, else append
`_New test_` and ensure the checklist creates it. AP-7 (agent/skill name doesn't resolve) → list
`.claude/agents/`/`.claude/skills/`, find closest match, else MEDIUM. AP-8 (CLI flag without
evidence) → run `<cmd> --help`, append `[Repo-grounded]` if confirmed, else replace with verified
usage. AP-9 (behavior claim without source) → delegate to `web-researcher`, embed inline excerpt +
URL + access date, classify HIGH only after citation appended. AP-10 (broken cross-link) → resolve
relative path, update if moved, else MEDIUM.
