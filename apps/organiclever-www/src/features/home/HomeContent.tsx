import { LandingPage } from "./components/landing-page";

/**
 * HomeContent is the public marketing landing experience for organiclever-www.
 *
 * It renders the OrganicLever landing page (hero, features, rhythm demo,
 * principles, footer) carried over from the former organiclever-app-web
 * landing context. This site is greenfield-simple: no local-first database
 * and no client-side state-machine library — just static marketing content
 * built on the `features/` module-root shape the sibling www apps share.
 */
export function HomeContent() {
  return <LandingPage />;
}
