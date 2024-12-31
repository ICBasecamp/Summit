"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { PlaceholdersAndVanishInput } from '../components/ticker-bar';

import { FlipWords } from "../components/flip-words";
import { poppins } from '../layout';


interface TickerFormProps {
  setTicker: (ticker: string) => void;
}


const TickerForm: React.FC<TickerFormProps> = ({ setTicker }) => {
  const [tickerInput, setTickerInput] = useState<string>('');
  const router = useRouter();

  const flipWords = [
    '$META?', '$AAPL?', '$AMZN?', '$NFLX?', '$GOOGL?', 
  ]

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
      <div className="flex flex-col gap-4 mb-10 sm:mb-20 ">
        <h1 className={`text-2xl text-left sm:text-5xl dark:text-white text-white ${poppins.className}`}>
          Thinking of investing in <span className="inline-block w-[120px]"><FlipWords className="text-white" words={flipWords} duration={3000} /></span> <br />
        </h1>
        <p className={`text-2xl text-left sm:text-5xl dark:text-white text-white ${poppins.className}`}>We'll break it down for you.</p>
      </div>

      <PlaceholdersAndVanishInput
        placeholders={placeholders}
        onChange={handleChange}
        onSubmit={handleSubmit}
      />
    </div>
  );
};

export default TickerForm;