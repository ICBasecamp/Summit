"use client";

import React from 'react';
import { usePathname } from 'next/navigation';
import { Geist, Geist_Mono } from "next/font/google";
import TickerForm from './TickerForm';
import AnalysisResults from './AnalysisResults';
import "./globals.css";

import { Open_Sans } from 'next/font/google';

import { motion } from "framer-motion";
import { HeroHighlight, Highlight } from "./components/highlight";

export const openSans = Open_Sans({ subsets: ['latin'] })

export const geistSans = Geist({
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
        <HeroHighlight className='h-screen'>
          <main>
            {pathname === '/' && <TickerForm />}
            {/* {pathname.startsWith('/results') && <AnalysisResults />} */}
            {children}
          </main>
        </HeroHighlight>
      </body>
    </html>
  );
}