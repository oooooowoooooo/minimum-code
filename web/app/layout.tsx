import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'AI Era — Learn Programming',
  description: 'Master Python + TypeScript through industrial-grade project dissection',
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
