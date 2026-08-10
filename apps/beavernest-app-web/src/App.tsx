import { useCallback, useEffect, useReducer, useRef } from "react";
import { AppHeader, Card, CardContent, CardHeader, CardTitle } from "@open-sharia-enterprise/web-ui";
import { ReadinessPanel } from "./components/ReadinessPanel";
import { fetchReadiness } from "./lib/readiness-client";
import { initialReadinessState, reduceReadiness } from "./lib/readiness-state";

export function App() {
  const [state, dispatch] = useReducer(reduceReadiness, initialReadinessState);
  const inFlight = useRef(false);

  const refresh = useCallback(async () => {
    if (inFlight.current) {
      return;
    }

    inFlight.current = true;
    dispatch({ type: "request" });
    try {
      dispatch({ type: "resolved", response: await fetchReadiness() });
    } catch {
      dispatch({ type: "failed" });
    } finally {
      inFlight.current = false;
    }
  }, []);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  return (
    <div className="min-h-screen">
      <AppHeader title="BeaverNest" />
      <main className="mx-auto flex min-h-[calc(100vh-64px)] max-w-2xl items-center px-4 py-8">
        <Card className="w-full">
          <CardHeader>
            <CardTitle>Foundation status</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <p className="text-muted-foreground">No workspace features yet</p>
            <ReadinessPanel state={state} onRefresh={() => void refresh()} refreshing={state.kind === "loading"} />
          </CardContent>
        </Card>
      </main>
    </div>
  );
}
