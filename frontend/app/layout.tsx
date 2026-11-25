import './globals.css';
import type { Metadata } from 'next';

export const metadata: Metadata = {
  title: 'Siyantech Gym OS - All-in-One Fitness Business Platform',
  description: 'Operating System for Gyms, Fitness Studios & Wellness Clubs',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-[#0b0f19] text-slate-100 antialiased">
        {children}
      </body>
    </html>
  );
}
