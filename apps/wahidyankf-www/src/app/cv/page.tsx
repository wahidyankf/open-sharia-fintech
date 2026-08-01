import { CvContent } from "@/features/cv/shell/CvContent";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "CV | Wahidyan Kresna Fridayoka",
  description:
    "Full curriculum vitae of Wahidyan Kresna Fridayoka — work experience, skills, education, and certifications.",
};

export default function CV() {
  return <CvContent />;
}
