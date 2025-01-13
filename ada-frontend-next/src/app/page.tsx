"use client";

import TickerForm from './pages/TickerForm';
import AnalysisResults from './pages/AnalysisResults';

import { useState } from 'react';

const LandingPage = () => {

    const [ticker, setTicker] = useState<string | null>(null);

    return (
        <div>
            <TickerForm setTicker={setTicker}  />
        </div>
    );
}

export default LandingPage;