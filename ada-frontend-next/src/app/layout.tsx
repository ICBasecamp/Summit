"use client";

import React from 'react';
import { usePathname } from 'next/navigation';
import { Geist, Geist_Mono } from "next/font/google";
import TickerForm from './TickerForm';
import AnalysisResults from './AnalysisResults';
import "./globals.css";

import { Open_Sans } from 'next/font/google';

const openSans = Open_Sans({ subsets: ['latin'] })

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const pathname = usePathname();

  return (
    <html lang="en">
      <body
        className={`${geistSans.className} ${geistMono.className} antialiased bg-neutral-900`}
      >
        <main>
          {pathname === '/' && <TickerForm />}
          {pathname.startsWith('/results') && <AnalysisResults />}
          {children}
        </main>
      </body>
    </html>
  );
}