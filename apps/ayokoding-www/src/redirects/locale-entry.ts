export interface LocaleEntryRedirect {
  source: string;
  destination: string;
  permanent: true;
}

export const localeEntryRedirects: readonly LocaleEntryRedirect[] = [
  { source: "/", destination: "/en", permanent: true },
  { source: "/EN", destination: "/en", permanent: true },
  { source: "/En", destination: "/en", permanent: true },
  { source: "/eN", destination: "/en", permanent: true },
  { source: "/ID", destination: "/id", permanent: true },
  { source: "/Id", destination: "/id", permanent: true },
  { source: "/iD", destination: "/id", permanent: true },
  { source: "/EN/:path*", destination: "/en/:path*", permanent: true },
  { source: "/En/:path*", destination: "/en/:path*", permanent: true },
  { source: "/eN/:path*", destination: "/en/:path*", permanent: true },
  { source: "/ID/:path*", destination: "/id/:path*", permanent: true },
  { source: "/Id/:path*", destination: "/id/:path*", permanent: true },
  { source: "/iD/:path*", destination: "/id/:path*", permanent: true },
];

export function resolveLocaleEntryRedirect(pathname: string): string | null {
  for (const redirect of localeEntryRedirects) {
    if (!redirect.source.endsWith("/:path*")) {
      if (pathname === redirect.source) return redirect.destination;
      continue;
    }
    const sourceRoot = redirect.source.slice(0, -"/:path*".length);
    if (!pathname.startsWith(`${sourceRoot}/`)) continue;
    const destinationRoot = redirect.destination.slice(0, -"/:path*".length);
    return `${destinationRoot}${pathname.slice(sourceRoot.length)}`;
  }
  return null;
}
