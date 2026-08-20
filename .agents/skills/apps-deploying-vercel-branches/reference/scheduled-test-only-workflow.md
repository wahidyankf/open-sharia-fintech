# Pattern 3: Scheduled Test-Only Workflow

Used by agents whose Target Parameters name a `$WORKFLOW_FILE` with **no provisioned staging or
production deploy target**. The workflow runs tests only — it never force-pushes anything. This
agent's job is to trigger and monitor that pipeline, and report the terminal state; there is no
deploy step to verify afterward and `reference/04-post-deploy-verification-vercel-mcp.md` does not
apply here.

## Step 1: Trigger the Test Workflow

```bash
gh workflow run $WORKFLOW_FILE --repo wahidyankf/ose-public
```

## Step 2: Locate the Run

```bash
gh run list --repo wahidyankf/ose-public --workflow=$WORKFLOW_FILE --limit=3
```

## Step 3: Watch the Run to Completion

```bash
gh run view <run-id> --repo wahidyankf/ose-public
```

A passing run means the workflow's test jobs are green. It does **not** mean anything shipped
anywhere — do not invent or invoke a deploy workflow, force-push a `stag-*` branch, or claim a
deployment succeeded when this pattern applies. Standing up the first staging/production target for
that surface is future plan work, not something this agent does.

## Safety Checks

The workflow itself enforces the safety gate — its test jobs must all pass. There is nothing further
for this agent to validate locally, since the workflow tests `main` directly inside the GitHub
Actions runner.

## Common Issues

### Issue 1: Workflow run not found by `gh run list`

The dispatch can lag a few seconds — re-run the Step 2 command.

### Other job failures

A failure in any test job is a real regression in the surface under test — inspect that job's output
directly; it is not something this agent can fix by re-dispatching.
