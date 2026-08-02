import "../globals.css";

interface Props {
  children: React.ReactNode;
}

export default function EntryLayout({ children }: Props) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
