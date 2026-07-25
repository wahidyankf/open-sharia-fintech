import Link from "next/link";
import { Alert, AlertDescription } from "@open-sharia-enterprise/web-ui";

export interface EmptyPathListStateProps {
  /** Where the fallback CTA points — a populated sibling category, per prd.md Screen 1a. */
  fallbackHref: string;
  fallbackLabel: string;
}

/**
 * The shared empty state for a category/arc landing before any path manifest lands there (Cycle
 * 3.1a, R7) — a stated "being written, check back soon" message plus a `<Link>` CTA to a
 * populated sibling category, rendered in place of the card grid. Never a silent blank `<div>`:
 * `Alert` carries `role="alert"`, a real landmark, not styled text alone.
 *
 * Takes an explicit `fallbackHref`/`fallbackLabel` pair rather than hardcoding "careers" so
 * `arc-landing.tsx` can reuse this component verbatim with its own fallback target.
 */
export function EmptyPathListState({ fallbackHref, fallbackLabel }: EmptyPathListStateProps) {
  return (
    <Alert variant="default" className="mt-8">
      <AlertDescription>
        <p>New paths are being written — check back soon.</p>
        <Link href={fallbackHref} className="font-medium text-primary underline underline-offset-2">
          {fallbackLabel}
        </Link>
      </AlertDescription>
    </Alert>
  );
}
