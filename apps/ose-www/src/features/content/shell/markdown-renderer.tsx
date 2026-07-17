"use client";

import parse, {
  type HTMLReactParserOptions,
  Element,
  domToReact,
  attributesToProps,
  type DOMNode,
} from "html-react-parser";
import Link from "next/link";
import { CodeBlock } from "@open-sharia-enterprise/web-ui/primitives";
import { MermaidDiagram } from "./mermaid";

interface MarkdownRendererProps {
  html: string;
}

export function MarkdownRenderer({ html }: MarkdownRendererProps) {
  const options: HTMLReactParserOptions = {
    replace: (domNode) => {
      if (!(domNode instanceof Element)) return;

      // Replace internal links with Next.js Link
      if (domNode.name === "a" && domNode.attribs.href) {
        const href = domNode.attribs.href;
        if (href.startsWith("/about") || href.startsWith("/updates")) {
          return (
            <Link href={href} className={domNode.attribs.class}>
              {domToReact(domNode.children as DOMNode[], options)}
            </Link>
          );
        }
      }

      // Replace mermaid code blocks (rehype-pretty-code wraps in <figure>)
      if (domNode.name === "figure" && domNode.attribs["data-rehype-pretty-code-figure"] !== undefined) {
        const pre = domNode.children.find((c): c is Element => c instanceof Element && c.name === "pre");
        if (pre?.attribs["data-language"] === "mermaid") {
          const code = pre.children.find((c): c is Element => c instanceof Element && c.name === "code");
          if (code) {
            const text = getTextContent(code);
            return <MermaidDiagram chart={text} />;
          }
        } else if (pre) {
          // Latent wiring: ose-www ships no non-mermaid fenced content today, but any that appears gets
          // a copy-to-clipboard affordance layered around the already-highlighted Shiki subtree. CodeBlock
          // never re-highlights (getTextContent(pre) is the verbatim clipboard value) and the figure is
          // reconstructed unchanged via attributesToProps (NOT domToReact([domNode]), which would re-enter
          // this branch and recurse forever). ose-www is English-only, so the Copy/Copied defaults apply.
          return (
            <CodeBlock code={getTextContent(pre)}>
              <figure {...attributesToProps(domNode.attribs, domNode.name)}>
                {domToReact(domNode.children as DOMNode[], options)}
              </figure>
            </CodeBlock>
          );
        }
      }

      // Fallback: mermaid without rehype-pretty-code wrapper
      if (
        domNode.name === "code" &&
        domNode.parent &&
        (domNode.parent as Element).name === "pre" &&
        (domNode.attribs.class?.includes("language-mermaid") || domNode.attribs["data-language"] === "mermaid")
      ) {
        const text = getTextContent(domNode);
        return <MermaidDiagram chart={text} />;
      }
    },
  };

  return (
    <div className="prose prose-neutral dark:prose-invert prose-headings:scroll-mt-20 prose-a:text-primary max-w-none">
      {parse(html, options)}
    </div>
  );
}

function getTextContent(node: Element): string {
  let text = "";
  for (const child of node.children) {
    if ("data" in child) {
      text += (child as unknown as { data: string }).data;
    }
    if ("children" in child) {
      text += getTextContent(child as Element);
    }
  }
  return text;
}
