import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "deskpilot",
  description: "Your personal workspace assistant",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
