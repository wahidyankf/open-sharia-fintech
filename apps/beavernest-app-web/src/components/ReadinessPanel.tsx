import { Button, Icon } from "@open-sharia-enterprise/web-ui";
import type { ReadinessState } from "../lib/readiness-state";

interface ReadinessPanelProps {
  state: ReadinessState;
  onRefresh: () => void;
  refreshing: boolean;
}

export function ReadinessPanel({ state, onRefresh, refreshing }: ReadinessPanelProps) {
  if (state.kind === "loading") {
    return (
      <section aria-live="polite" aria-label="Foundation status" className="space-y-3">
        <p className="flex items-center gap-2 text-muted-foreground">
          <Icon name="clock" aria-label="Checking status" /> Checking foundation status
        </p>
      </section>
    );
  }

  const isReady = state.kind === "ready";
  return (
    <section aria-live="polite" aria-label="Foundation status" className="space-y-4">
      <div className="flex items-center gap-2 font-medium">
        <Icon name={isReady ? "check-circle" : "x-circle"} aria-label={isReady ? "Ready" : "Unavailable"} />
        <span>{isReady ? "Ready" : "Unavailable"}</span>
      </div>
      <dl className="grid gap-3 text-sm sm:grid-cols-3">
        <div>
          <dt className="text-muted-foreground">Application</dt>
          <dd>Available</dd>
        </div>
        <div>
          <dt className="text-muted-foreground">Database</dt>
          <dd>{isReady ? "Ready" : "Unavailable"}</dd>
        </div>
        <div>
          <dt className="text-muted-foreground">Schema</dt>
          <dd>{isReady ? "Current" : "Unknown"}</dd>
        </div>
      </dl>
      <Button type="button" onClick={onRefresh} disabled={refreshing}>
        <Icon name="rotate-ccw" /> Refresh status
      </Button>
    </section>
  );
}
