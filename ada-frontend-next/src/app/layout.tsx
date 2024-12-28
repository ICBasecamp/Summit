"use client";

import React from 'react';
import { usePathname, useSearchParams } from 'next/navigation';
import { Geist, Geist_Mono } from "next/font/google";
import TickerForm from './pages/TickerForm';
import AnalysisResults from './pages/AnalysisResults';
import { AnalysisProvider } from './context/AnalysisContext';
import "./globals.css";

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
  const searchParams = useSearchParams();
  const ticker = searchParams.get('ticker');

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
            {pathname === '/' && <TickerForm />}
            {pathname.startsWith('/analyze') && <AnalysisResults ticker={ticker ?? ''} />}
            {children}
          </main>
        </AnalysisProvider>
      </body>
    </html>
  );
}