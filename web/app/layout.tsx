import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'minimum-code — Source Code Reading Training',
  description: 'Read mainstream Python and TypeScript source code to build architecture judgment in the AI era.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#0a0a0a] text-white">
        {children}
      </body>
    </html>
  );
}
