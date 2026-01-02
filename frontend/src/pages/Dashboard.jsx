/**
 * Dashboard Page
 * Main page for stock and portfolio risk analysis with enhanced search
 */

import { useState } from 'react';
import StockSearch from '../components/StockSearch';
import PortfolioInput from '../components/PortfolioInput';
import RiskSummary from '../components/RiskSummary';
import RiskBreakdown from '../components/RiskBreakdown';
import NewsImpact from '../components/NewsImpact';


import { analyzeStock, analyzePortfolio } from '../services/api';

const Dashboard = () => {
    const [mode, setMode] = useState('stock'); // 'stock' or 'portfolio'
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [analysisResult, setAnalysisResult] = useState(null);

    const [portfolioStocks, setPortfolioStocks] = useState([]);

    const handleStockAnalysis = async (symbol) => {
        setLoading(true);
        setError(null);


        try {
            const result = await analyzeStock(symbol);
            setAnalysisResult(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleAddToPortfolio = (symbol) => {
        // Check if already in portfolio
        if (portfolioStocks.some(s => s.symbol === symbol)) {
            alert(`${symbol} is already in your portfolio!`);
            return;
        }

        // Add to portfolio with default weight
        const newStock = {
            symbol: symbol,
            name: symbol,
            weight: 0
        };

        setPortfolioStocks(prev => [...prev, newStock]);
        setMode('portfolio'); // Switch to portfolio mode

        alert(`✅ ${symbol} added to portfolio!`);
    };

    const handlePortfolioAnalysis = async (holdings) => {
        setLoading(true);
        setError(null);


        try {
            const result = await analyzePortfolio(holdings);
            setAnalysisResult(result);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
            <main className="container mx-auto px-4 py-8">
                {/* Header */}
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-gray-900 mb-2">
                        AI Stock & Portfolio Risk Analysis
                    </h1>
                    <p className="text-gray-600">
                        Deterministic risk calculation with AI-powered insights | Indian & US Markets
                    </p>
                </div>

                {/* Mode Toggle */}
                <div className="flex justify-center mb-8">
                    <div className="inline-flex rounded-lg border-2 border-gray-300 bg-white p-1">
                        <button
                            onClick={() => setMode('stock')}
                            className={`px-6 py-2 rounded-md font-semibold transition-colors ${mode === 'stock'
                                ? 'bg-blue-600 text-white'
                                : 'text-gray-600 hover:text-gray-900'
                                }`}
                        >
                            📈 Stock Analysis
                        </button>
                        <button
                            onClick={() => setMode('portfolio')}
                            className={`px-6 py-2 rounded-md font-semibold transition-colors ${mode === 'portfolio'
                                ? 'bg-purple-600 text-white'
                                : 'text-gray-600 hover:text-gray-900'
                                }`}
                        >
                            💼 Portfolio Analysis
                        </button>
                    </div>
                </div>

                {/* Search Section */}
                <div className="flex justify-center mb-8">
                    {mode === 'stock' ? (
                        <StockSearch
                            onSearch={handleStockAnalysis}
                            loading={loading}
                            onAddToPortfolio={handleAddToPortfolio}
                        />
                    ) : (
                        <PortfolioInput
                            onAnalyze={handlePortfolioAnalysis}
                            loading={loading}
                            initialStocks={portfolioStocks}
                            onStocksChange={setPortfolioStocks}
                        />
                    )}
                </div>

                {/* Error Display */}
                {error && (
                    <div className="max-w-4xl mx-auto mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                        <p className="text-red-800">
                            <strong>Error:</strong> {error}
                        </p>
                    </div>
                )}

                {/* Info Box */}
                {!analysisResult && !loading && (
                    <div className="max-w-6xl mx-auto space-y-6 mt-6">
                        <div className="flex justify-center">
                            {/* How It Works */}
                            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 max-w-2xl w-full">
                                <h3 className="text-lg font-semibold text-blue-900 mb-2">How It Works</h3>
                                <ul className="text-sm text-blue-800 space-y-2">
                                    <li>✓ <strong>Deterministic Risk Calculation:</strong> Risk scores are calculated using proven financial models</li>
                                    <li>✓ <strong>Multi-Source News Verification:</strong> News is verified across multiple trusted sources</li>
                                    <li>✓ <strong>AI Explanations Only:</strong> GenAI explains risk, but doesn't calculate it</li>
                                    <li>✓ <strong>Decision Support:</strong> Provides analysis, not trading advice</li>
                                </ul>
                            </div>
                        </div>

                    </div>
                )}

                {/* Simple Loading State */}
                {loading && (
                    <div className="flex flex-col items-center justify-center mt-12">
                        <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                        <p className="mt-4 text-lg font-semibold text-blue-900">Analyzing Market Data...</p>
                        <p className="text-sm text-blue-600">Calculating risk metrics and verifying news</p>
                    </div>
                )}

                {/* Results Display */}
                {analysisResult && !loading && (
                    <div className="max-w-6xl mx-auto space-y-6">
                        <RiskSummary
                            riskScore={analysisResult.risk_score}
                            symbol={analysisResult.symbol}
                        />

                        <RiskBreakdown
                            riskMetrics={analysisResult.risk_breakdown}
                        />

                        {analysisResult.news_impact && (
                            <NewsImpact
                                newsData={analysisResult.news_impact}
                                explanation={analysisResult.explanation}
                            />
                        )}

                    </div>
                )}
            </main>
        </div>
    );
};

export default Dashboard;
