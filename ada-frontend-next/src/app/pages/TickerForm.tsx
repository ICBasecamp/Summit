"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { PlaceholdersAndVanishInput } from '../components/ticker-bar';

interface TickerFormProps {
  setTicker: (ticker: string) => void;
}

const TickerForm: React.FC<TickerFormProps> = ({ setTicker }) => {
  const [tickerInput, setTickerInput] = useState<string>('');
  const router = useRouter();

  const placeholders = [
    "Enter ticker symbol",
    "Type any stock symbol",
    "Try 'AAPL' or 'GOOGL'",
    "Or 'AMZN' or 'TSLA'",
    "Or 'MSFT' or 'NFLX'",
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTickerInput(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setTicker(tickerInput);
    router.push(`/analyze/${tickerInput}`);
  };

  return (
    <div className="h-[40rem] flex flex-col justify-center items-center px-4">
      <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl dark:text-white text-white">
        ADA Stock Analysis
      </h2>
      <PlaceholdersAndVanishInput
        placeholders={placeholders}
        onChange={handleChange}
        onSubmit={handleSubmit}
      />
    </div>
  );
};

export default TickerForm;