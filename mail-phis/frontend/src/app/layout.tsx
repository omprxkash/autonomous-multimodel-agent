import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "mailrecon",
  description: "Email and URL forensics pipeline",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <nav>
          <div className="container inner">
            <a href="/" className="logo">mail<span>recon</span></a>
            <div className="links">
              <a href="/">Dashboard</a>
              <a href="/submit">Analyze</a>
            </div>
          </div>
        </nav>
        <main className="container">{children}</main>
      </body>
    </html>
  );
}
