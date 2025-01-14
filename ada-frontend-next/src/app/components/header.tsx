"use client";

import { useState } from 'react';
import { Tabs } from './tabs';
import { PlaceholdersAndVanishInputHeader } from './ticker-bar-header';
import { Braces } from 'lucide-react';
import { ArrowDownToLine } from 'lucide-react';
import { useRouter } from 'next/navigation';

const Header = () => {
    const [tickerInput, setTickerInput] = useState('');
    const [ticker, setTicker] = useState('');
    const router = useRouter();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setTickerInput(e.target.value);
    };

    const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setTicker(tickerInput);
        router.push(`/analyze/${tickerInput}`);
    };

    const tabs = [
        {
            title: "News",
            value: "news",
            content: <></>
        },
        {
            title: "Social Media",
            value: "social-media",
            content: <></>
        },
        {
            title: "Economic Indicators",
            value: "economic-indicators/retail-sales",
            content: <></>
        },
        {
            title: "Earning Reports",
            value: "earnings-reports/earnings",
            content: <></>
        },
    ];

    return (
        <div className="w-screen py-4 px-8 gap-2 flex flex-col">
            <div className="flex h-20 w-full items-center gap-2">
                <p className="font-semibold text-lg --font-geist-mono">Ice Climbers</p>
                <div className="flex w-1/2 items-center">
                    <PlaceholdersAndVanishInputHeader 
                        placeholders={['Search for a new ticker']}
                        onChange={handleChange}
                        onSubmit={handleSubmit}
                    />
                </div>
                <div className="flex gap-1.5 ml-auto items-center">
                    <ArrowDownToLine size={18}/>
                    <p className="hover:underline cursor-pointer">Raw Data</p>
                </div>
            </div>
            <Tabs tabs={tabs} />
        </div>
    );
};

export default Header;
