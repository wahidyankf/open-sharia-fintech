import { Alert, AlertDescription } from "@open-sharia-enterprise/web-ui";
import { AlertTriangle, Info, Lightbulb } from "lucide-react";
import type { ReactNode } from "react";

interface CalloutProps {
  type: string;
  children: ReactNode;
}

const iconMap: Record<string, ReactNode> = {
  warning: <AlertTriangle className="h-4 w-4" />,
  info: <Info className="h-4 w-4" />,
  tip: <Lightbulb className="h-4 w-4" />,
};

// Full Alert variant union (default | destructive | success | warning | info), per
// swe-ui audit b06d32 Finding 3: `warning` previously mapped to `variant="destructive"`
// (3.05:1 contrast, fails WCAG AA), instead of the dedicated `warning` variant (6.90:1).
const variantMap: Record<string, "default" | "destructive" | "success" | "warning" | "info"> = {
  warning: "warning",
  info: "info",
  tip: "default",
};

export function Callout({ type, children }: CalloutProps) {
  return (
    <Alert variant={variantMap[type] ?? "default"} className="my-4">
      {iconMap[type]}
      <AlertDescription>{children}</AlertDescription>
    </Alert>
  );
}
