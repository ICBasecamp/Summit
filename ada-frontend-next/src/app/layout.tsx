"use client";

import React, { useState } from 'react';
import { usePathname } from 'next/navigation';
import { AnalysisProvider } from './context/AnalysisContext';
import TickerForm from './pages/TickerForm';
import AnalysisResults from './pages/AnalysisResults';
import { metadata } from './metadata';
import "./globals.css";

import { Open_Sans } from 'next/font/google';

import { motion } from "framer-motion";
import { HeroHighlight, Highlight } from "./components/highlight";

import { Geist_Mono } from 'next/font/google';

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
  const ticker = pathname.split('/analyze/')[1] || null;
  const [tickerState, setTicker] = useState<string | null>(null);

  return (
    <html lang="en">
      <head>
        <title>Stock Analysis App</title>
        <meta name="description" content="Analyze stock data with insights from various sources" />
      </head>
      <body
        className={`${geistMono.className} antialiased bg-neutral-900`}
      >
        <HeroHighlight className='h-screen'>
          <AnalysisProvider>
            <main>
              {/* {pathname === '/' && <TickerForm setTicker={setTicker} />}
              {pathname.startsWith('/analyze') && <AnalysisResults ticker={ticker ?? ''} />} */}
              {children}
            </main>
          </AnalysisProvider>
        </HeroHighlight>
      </body>
    </html>
  );
}

function Geist({ variable, subsets }: { variable: string; subsets: string[]; }) {
  return { variable, subsets };
}

function createGeistMono({ variable, subsets }: { variable: string; subsets: string[]; }) {
  return { variable, subsets };
}