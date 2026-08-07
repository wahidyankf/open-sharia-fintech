import Link from "next/link";
import { Github, Rss } from "lucide-react";
import { Button } from "@open-sharia-enterprise/web-ui";

export function SocialIcons() {
  return (
    <div className="flex items-center justify-center gap-2 py-8">
      <Button variant="ghost" size="icon" asChild>
        <a
          href="https://github.com/wahidyankf/ose-public"
          target="_blank"
          rel="noopener noreferrer"
          aria-label="GitHub repository"
        >
          <Github className="h-5 w-5" />
        </a>
      </Button>
      <Button variant="ghost" size="icon" asChild>
        <Link href="/feed.xml" aria-label="RSS feed">
          <Rss className="h-5 w-5" />
        </Link>
      </Button>
    </div>
  );
}
