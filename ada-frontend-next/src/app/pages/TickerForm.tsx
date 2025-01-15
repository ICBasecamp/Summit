"use client";

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { PlaceholdersAndVanishInput } from '../components/ticker-bar';

import { FlipWords } from "../components/flip-words";
import { poppins } from '../layout';
import { openSans } from '../layout';

import Image from 'next/image';
import { div } from 'framer-motion/client';

import News from '../../../public/news.svg';

interface TickerFormProps {
  setTicker: (ticker: string) => void;
}

interface Suggestion {
  symbol: string;
  fullName: string;
  icon: string;
}


const TickerForm: React.FC<TickerFormProps> = ({ setTicker }) => {
  const [tickerInput, setTickerInput] = useState<string>('');
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const router = useRouter();

  const stockList = [
    { symbol: 'AAPL', fullName: 'Apple Inc.', icon: 'https://logo.clearbit.com/apple.com' },
    { symbol: 'GOOGL', fullName: 'Alphabet Inc.', icon: 'https://logo.clearbit.com/google.com' },
    { symbol: 'AMZN', fullName: 'Amazon.com Inc.', icon: 'https://logo.clearbit.com/amazon.com' },
    { symbol: 'TSLA', fullName: 'Tesla Inc.', icon: 'https://logo.clearbit.com/tesla.com' },
    { symbol: 'MSFT', fullName: 'Microsoft Corporation', icon: 'https://logo.clearbit.com/microsoft.com' },
    { symbol: 'NFLX', fullName: 'Netflix Inc.', icon: 'https://logo.clearbit.com/netflix.com' },
    { symbol: 'META', fullName: 'Meta Platforms Inc.', icon: 'https://logo.clearbit.com/meta.com' },
    { symbol: 'NVDA', fullName: 'Nvidia Corporation', icon: 'https://logo.clearbit.com/nvidia.com' },
    { symbol: 'AMD', fullName: 'Advanced Micro Devices Inc.', icon: 'https://logo.clearbit.com/amd.com' },
    { symbol: 'INTC', fullName: 'Intel Corporation', icon: 'https://logo.clearbit.com/intel.com' },
    { symbol: 'CSCO', fullName: 'Cisco Systems Inc.', icon: 'https://logo.clearbit.com/cisco.com' },
    { symbol: 'ORCL', fullName: 'Oracle Corporation', icon: 'https://logo.clearbit.com/oracle.com' },
    { symbol: 'IBM', fullName: 'International Business Machines Corporation', icon: 'https://logo.clearbit.com/ibm.com' },
    { symbol: 'CRM', fullName: 'Salesforce Inc.', icon: 'https://logo.clearbit.com/salesforce.com' },
    { symbol: 'ADBE', fullName: 'Adobe Inc.', icon: 'https://logo.clearbit.com/adobe.com' },
    { symbol: 'PYPL', fullName: 'PayPal Holdings Inc.', icon: 'https://logo.clearbit.com/paypal.com' },
    { symbol: 'QCOM', fullName: 'Qualcomm Incorporated', icon: 'https://logo.clearbit.com/qualcomm.com' },
    { symbol: 'AVGO', fullName: 'Broadcom Inc.', icon: 'https://logo.clearbit.com/broadcom.com' },
    { symbol: 'TXN', fullName: 'Texas Instruments Incorporated', icon: 'https://logo.clearbit.com/ti.com' },
    { symbol: 'MU', fullName: 'Micron Technology Inc.', icon: 'https://logo.clearbit.com/micron.com' },
    { symbol: 'AMAT', fullName: 'Applied Materials Inc.', icon: 'https://logo.clearbit.com/appliedmaterials.com' },
    { symbol: 'LRCX', fullName: 'Lam Research Corporation', icon: 'https://logo.clearbit.com/lamresearch.com' },
    { symbol: 'KLAC', fullName: 'KLA Corporation', icon: 'https://logo.clearbit.com/kla.com' },
    { symbol: 'ASML', fullName: 'ASML Holding N.V.', icon: 'https://logo.clearbit.com/asml.com' },
    { symbol: 'BA', fullName: 'The Boeing Company', icon: 'https://logo.clearbit.com/boeing.com' },
    { symbol: 'CAT', fullName: 'Caterpillar Inc.', icon: 'https://logo.clearbit.com/caterpillar.com' },
    { symbol: 'DIS', fullName: 'The Walt Disney Company', icon: 'https://logo.clearbit.com/disney.com' },
    { symbol: 'XOM', fullName: 'Exxon Mobil Corporation', icon: 'https://logo.clearbit.com/exxonmobil.com' },
    { symbol: 'CVX', fullName: 'Chevron Corporation', icon: 'https://logo.clearbit.com/chevron.com' },
    { symbol: 'JNJ', fullName: 'Johnson & Johnson', icon: 'https://logo.clearbit.com/jnj.com' },
    { symbol: 'PFE', fullName: 'Pfizer Inc.', icon: 'https://logo.clearbit.com/pfizer.com' },
    { symbol: 'MRK', fullName: 'Merck & Co., Inc.', icon: 'https://logo.clearbit.com/merck.com' },
    { symbol: 'PEP', fullName: 'PepsiCo Inc.', icon: 'https://logo.clearbit.com/pepsico.com' },
    { symbol: 'KO', fullName: 'The Coca-Cola Company', icon: 'https://logo.clearbit.com/coca-cola.com' },
    { symbol: 'WMT', fullName: 'Walmart Inc.', icon: 'https://logo.clearbit.com/walmart.com' },
    { symbol: 'HD', fullName: 'The Home Depot Inc.', icon: 'https://logo.clearbit.com/homedepot.com' },
    { symbol: 'COST', fullName: 'Costco Wholesale Corporation', icon: 'https://logo.clearbit.com/costco.com' },
    { symbol: 'TGT', fullName: 'Target Corporation', icon: 'https://logo.clearbit.com/target.com' },
    { symbol: 'UPS', fullName: 'United Parcel Service Inc.', icon: 'https://logo.clearbit.com/ups.com' },
    { symbol: 'FDX', fullName: 'FedEx Corporation', icon: 'https://logo.clearbit.com/fedex.com' },
    { symbol: 'V', fullName: 'Visa Inc.', icon: 'https://logo.clearbit.com/visa.com' },
    { symbol: 'MA', fullName: 'Mastercard Incorporated', icon: 'https://logo.clearbit.com/mastercard.com' },
    { symbol: 'BAC', fullName: 'Bank of America Corporation', icon: 'https://logo.clearbit.com/bankofamerica.com' },
    { symbol: 'JPM', fullName: 'JPMorgan Chase & Co.', icon: 'https://logo.clearbit.com/jpmorganchase.com' },
    { symbol: 'GS', fullName: 'The Goldman Sachs Group Inc.', icon: 'https://logo.clearbit.com/goldmansachs.com' },
    { symbol: 'C', fullName: 'Citigroup Inc.', icon: 'https://logo.clearbit.com/citigroup.com' },
    { symbol: 'AXP', fullName: 'American Express Company', icon: 'https://logo.clearbit.com/americanexpress.com' },
    { symbol: 'T', fullName: 'AT&T Inc.', icon: 'https://logo.clearbit.com/att.com' },
    { symbol: 'VZ', fullName: 'Verizon Communications Inc.', icon: 'https://logo.clearbit.com/verizon.com' },
    { symbol: 'TMUS', fullName: 'T-Mobile US Inc.', icon: 'https://logo.clearbit.com/t-mobile.com' },
  ];

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
    if (e.target.value === '') {
      setSuggestions([]);
      return;
    } 
    setSuggestions(stockList.filter(ticker => ticker.symbol.includes(e.target.value.toUpperCase())));

  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setTicker(tickerInput);
    router.push(`/analyze/${tickerInput}`);
  };

  const handleSuggestionClick = (suggestion: string) => {
    setTickerInput(suggestion);
    setSuggestions([]);
  };

  return (
    <div className="h-screen flex gap-2 w-screen">
      <div className="h-full w-2/3 flex flex-col justify-center items-center px-4 self-center">
        <div className="flex flex-col gap-4 mb-10 sm:mb-20 ">
          <h1 className={`text-2xl text-left sm:text-5xl dark:text-white text-white ${poppins.className}`}>
            Thinking of investing in <span className="inline-block w-[120px]"><FlipWords className="text-white" words={flipWords} duration={3000} /></span> <br />
          </h1>
          <p className={`text-2xl text-left sm:text-5xl dark:text-white text-white ${poppins.className}`}>We'll help you decide.</p>
        </div>

        <div className="relative w-full max-w-xl ">
          <PlaceholdersAndVanishInput
            placeholders={placeholders}
            onChange={handleChange}
            onSubmit={handleSubmit}
            currentValue={tickerInput}
          />
          {suggestions.length > 0 && (
            <ul className="py-2 flex flex-col absolute bg-neutral-800 border border-zinc-900 w-full mt-1 rounded-lg shadow-lg z-10 max-h-48 overflow-y-auto">
              {suggestions.map((suggestion, index) => (
                <li
                  key={index}
                  className="px-4 py-3 cursor-pointer hover:bg-neutral-700 flex justify-between items-center"
                  onClick={() => handleSuggestionClick(suggestion.symbol)}
                >
                  {suggestion.symbol} - {suggestion.fullName}
                    <span>
                    <Image 
                      src={suggestion.icon} 
                      alt={""} 
                      width={28} 
                      height={28} 
                      className='rounded-md' 
                      onError={(e) => { e.currentTarget.src = '/svg'; }} 
                    />
                    </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
      <div className={`h-full w-1/3 flex flex-col py-24 px-16 items-center justify-center ${openSans.className}`}>
        {/* <div className="h-[1px] w-1/2 rounded-full bg-neutral-600"></div> */}
        <div className='flex flex-col gap-12 items-start'>
          <p className="text-2xl font-medium">Research instantly...</p>

          <div className="flex flex-col gap-2 items-start">
            <div className="flex gap-2 items-center">
              {/* <img src="/news.svg" className="w-6 h-6 filter invert"/> */}
              <p className="text-white text-xl">News</p>
            </div>
            <p className="font-light">See what news outlets are saying</p>
          </div>
          <div className="flex flex-col gap-2 items-start">
            <div className="flex gap-2 items-center">
              {/* <img src="/news.svg" className="w-8 h-8 filter invert"/> */}
              <p className="text-white text-xl">Social Media</p>
            </div>
            <p className="font-light">See what everyone is saying</p>
          </div>
            <div className="flex flex-col gap-2 items-start">
            <div className="flex gap-2 items-center">
              {/* <img src="/news.svg" className="w-8 h-8 filter invert"/> */}
              <p className="text-white text-xl">Economic Indicators</p>
            </div>
            <p className="font-light">Track market-moving economic data</p>
            </div>
            <div className="flex flex-col gap-2 items-start">
            <div className="flex gap-2 items-center">
              {/* <img src="/news.svg" className="w-8 h-8 filter invert"/> */}
              <p className="text-white text-xl">Earnings Reports</p>
            </div>
            <p className="font-light">Review financial performance and forecasts</p>
          </div>
        </div>
      </div>
    </div>

    
  );
};

export default TickerForm;