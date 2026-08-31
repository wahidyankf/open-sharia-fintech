import { PersonalProjectsContent } from "@/features/personal-projects/shell/PersonalProjectsContent";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Independent Projects | Wahidyan Kresna Fridayoka",
  description:
    "Open-source and independent projects by Wahidyan Kresna Fridayoka, including OSE, AyoKoding, OrganicLever, and more.",
};

export default function Projects() {
  return <PersonalProjectsContent />;
}
