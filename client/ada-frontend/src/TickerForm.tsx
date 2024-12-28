import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { PlaceholdersAndVanishInput } from 'aceternity-ui';

const TickerForm: React.FC = () => {
  const [ticker, setTicker] = useState<string>('');
  const navigate = useNavigate();

  const placeholders = [
    "Enter stock symbol...",
  ];

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setTicker(e.target.value);
  };

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    navigate(`/results/${ticker}`);
  };

  return (
    <div className="h-[40rem] flex flex-col justify-center items-center px-4">
      <h2 className="mb-10 sm:mb-20 text-xl text-center sm:text-5xl dark:text-white text-black">
        Enter Ticker Symbol
      </h2>
      <PlaceholdersAndVanishInput
        placeholders={placeholders}
        onChange={handleChange}
        onSubmit={handleSubmit}
      />
      <p>Debug: TickerForm component is rendering</p>
    </div>
  );
};

export default TickerForm;