# P1 Pre-Push Quality Evidence

**Recorded**: 2026-08-13

## Initial Diagnosis

`apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push` passed. The plan's original
`npm exec nx affected -t ...` command then failed before running a target because npm consumed `-t`
instead of forwarding it to Nx. The repository-compatible form is `npm exec nx -- affected -t ...`;
the delivery command was corrected before retrying.

## Passing Retry

```bash
apps/rhino-cli/scripts/rhino-bin.sh gate run --surface=pre-push
npm exec nx -- affected -t build,test:quick,lint,specs:behavior:coverage
```

Both commands pass. The affected set is `beavernest-app`, `beavernest-be`,
`beavernest-be-e2e`, and `beavernest-app-web-e2e`; its relevant build, quick-test, lint, and
behavior-spec coverage targets are green. Flutter Web production build also completes.
