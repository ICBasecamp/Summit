"use client";

import React, { useState } from 'react';
import { usePathname } from 'next/navigation';
import { AnalysisProvider } from './context/AnalysisContext';
import TickerForm from './pages/TickerForm';
import AnalysisResults from './pages/AnalysisResults';
import { metadata } from './metadata';
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = createGeistMono({
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
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AnalysisProvider>
          <main>
            {pathname === '/' && <TickerForm setTicker={setTicker} />}
            {pathname.startsWith('/analyze') && <AnalysisResults ticker={ticker ?? ''} />}
            {children}
          </main>
        </AnalysisProvider>
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