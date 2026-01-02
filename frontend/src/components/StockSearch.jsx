/**
 * Enhanced Stock Search Component with Real API
 * Supports Indian (NSE/BSE) and US markets
 */

import { useState, useEffect } from 'react';
import { searchStocksAPI, getPopularStocks } from '../services/stockSearch';

const StockSearch = ({ onSearch, loading, onAddToPortfolio }) => {
    const [symbol, setSymbol] = useState('');
    const [showSuggestions, setShowSuggestions] = useState(false);
    const [searchResults, setSearchResults] = useState([]);
    const [popularStocks, setPopularStocks] = useState({ indian: [], us: [] });
    const [selectedMarket, setSelectedMarket] = useState('all');
    const [isSearching, setIsSearching] = useState(false);

    // Load popular stocks on mount
    useEffect(() => {
        const loadPopular = async () => {
            const stocks = await getPopularStocks('all');
            setPopularStocks(stocks);
        };
        loadPopular();
    }, []);

    // Search stocks as user types
    useEffect(() => {
        const searchTimeout = setTimeout(async () => {
            if (symbol.trim().length > 1) {
                setIsSearching(true);
                const results = await searchStocksAPI(symbol, 10);
                setSearchResults(results);
                setIsSearching(false);
            } else {
                setSearchResults([]);
            }
        }, 250); // Debounce - faster for "Amazon-like" feel

        return () => clearTimeout(searchTimeout);
    }, [symbol]);

    const handleSubmit = (e) => {
        e.preventDefault();
        if (symbol.trim()) {
            onSearch(symbol.trim());
            setShowSuggestions(false);
        }
    };

    const handleSelectSuggestion = (stockSymbol) => {
        setSymbol(stockSymbol);
        setShowSuggestions(false);
        onSearch(stockSymbol);
    };

    const handleAddStock = (e, stockSymbol) => {
        e.stopPropagation();
        if (onAddToPortfolio) {
            onAddToPortfolio(stockSymbol);
        }
    };

    const displayResults = symbol ? searchResults : [
        ...(selectedMarket === 'all' || selectedMarket === 'indian' ? popularStocks.indian.slice(0, 5) : []),
        ...(selectedMarket === 'all' || selectedMarket === 'us' ? popularStocks.us.slice(0, 5) : [])
    ];

    return (
        <div className="w-full max-w-4xl">
            {/* Market Selector */}
            <div className="mb-4 flex items-center gap-2">
                <span className="px-4 py-2 rounded-lg font-bold text-sm bg-orange-600 text-white shadow-sm flex items-center gap-2">
                    🇮🇳 Indian Market Search
                </span>
                <span className="text-xs text-gray-500 italic">
                    (NSE & BSE Listed Stocks)
                </span>
            </div>

            <form onSubmit={handleSubmit} className="w-full relative">
                <div className="flex gap-2">
                    <div className="flex-1 relative">
                        <input
                            type="text"
                            value={symbol}
                            onChange={(e) => {
                                setSymbol(e.target.value);
                                setShowSuggestions(true);
                            }}
                            onFocus={() => setShowSuggestions(true)}
                            onBlur={() => setTimeout(() => setShowSuggestions(false), 200)}
                            placeholder="Search stock (e.g., AAPL, Rel for Reliance)"
                            className="w-full px-4 py-3 bg-white text-gray-900 border-2 border-gray-300 rounded-lg focus:outline-none focus:border-blue-500 placeholder-gray-500"
                            disabled={loading}
                        />

                        {/* Suggestions Dropdown */}
                        {showSuggestions && displayResults.length > 0 && (
                            <div className="absolute z-10 w-full mt-1 bg-white border-2 border-gray-200 rounded-lg shadow-lg max-h-96 overflow-y-auto">
                                <div className="px-3 py-2 bg-gray-50 border-b border-gray-200">
                                    <p className="text-xs font-semibold text-gray-600">
                                        {isSearching ? '🔍 Searching...' : (symbol ? 'Search Results' : 'Popular Stocks')}
                                    </p>
                                </div>
                                {displayResults.map((stock) => (
                                    <div
                                        key={stock.symbol}
                                        role="button"
                                        onClick={() => handleSelectSuggestion(stock.symbol)}
                                        className="w-full px-4 py-3 text-left hover:bg-blue-50 border-b border-gray-100 last:border-b-0 transition cursor-pointer"
                                    >
                                        <div className="flex justify-between items-center">
                                            <div className="flex-1">
                                                <div className="flex items-center gap-2">
                                                    <span className="font-bold text-gray-900">{stock.symbol}</span>
                                                    <span className="text-xs px-2 py-0.5 bg-gray-200 rounded">
                                                        {stock.market}
                                                    </span>
                                                </div>
                                                <p className="text-sm text-gray-600">{stock.name}</p>
                                                {stock.sector && stock.sector !== 'N/A' && (
                                                    <p className="text-xs text-gray-500">{stock.sector}</p>
                                                )}
                                            </div>
                                            {onAddToPortfolio && (
                                                <button
                                                    onClick={(e) => handleAddStock(e, stock.symbol)}
                                                    className="ml-2 px-3 py-1 bg-green-600 text-white rounded hover:bg-green-700 text-sm font-semibold"
                                                    title="Add to Portfolio"
                                                >
                                                    + Portfolio
                                                </button>
                                            )}
                                        </div>
                                    </div>
                                ))}
                            </div>
                        )}
                    </div>

                    <button
                        type="submit"
                        disabled={loading || !symbol.trim()}
                        className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed font-semibold"
                    >
                        {loading ? 'Analyzing...' : 'Analyze'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default StockSearch;
