import AnalysisResults from '../../pages/AnalysisResults';

export default function TickerPage({ params }: { params: { ticker: string } }) {
  return <AnalysisResults ticker={params.ticker} />;
}