import { Suspense } from "react";
import { HomeContent } from "@/features/home/shell/HomeContent";

export default function Home() {
  return (
    <Suspense>
      <HomeContent />
    </Suspense>
  );
}
