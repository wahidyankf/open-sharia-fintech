import { redirect } from "next/navigation";
import { DEFAULT_LOCALE_HREF } from "@/features/i18n/core/config";

export default function RootPage() {
  redirect(DEFAULT_LOCALE_HREF);
}
