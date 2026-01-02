/**
 * PortfolioInput Component
 * Input form for portfolio holdings
 */

import { useState } from 'react';

const PortfolioInput = ({ onAnalyze, loading }) => {
    const [holdings, setHoldings] = useState([
        { symbol: '', weight: '' }
    ]);

    const addHolding = () => {
        setHoldings([...holdings, { symbol: '', weight: '' }]);
    };

    const removeHolding = (index) => {
        setHoldings(holdings.filter((_, i) => i !== index));
    };

    const updateHolding = (index, field, value) => {
        const updated = [...holdings];
        updated[index][field] = value;
        setHoldings(updated);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        const validHoldings = holdings
            .filter(h => h.symbol.trim() && h.weight)
            .map(h => ({
                symbol: h.symbol.toUpperCase(),
                weight: parseFloat(h.weight)
            }));

        if (validHoldings.length > 0) {
            onAnalyze(validHoldings);
        }
    };

    return (
        <form onSubmit={handleSubmit} className="w-full max-w-2xl">
            <div className="space-y-3">
                {holdings.map((holding, index) => (
                    <div key={index} className="flex gap-2">
                        <input
                            type="text"
                            value={holding.symbol}
                            onChange={(e) => updateHolding(index, 'symbol', e.target.value)}
                            placeholder="Symbol"
                            className="flex-1 px-4 py-2 border text-gray-900 border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={loading}
                        />
                        <input
                            type="number"
                            step="0.01"
                            min="0"
                            max="1"
                            value={holding.weight}
                            onChange={(e) => updateHolding(index, 'weight', e.target.value)}
                            placeholder="Weight(0-1)"
                            className="w-32 text-gray-900 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                            disabled={loading}
                        />
                        {holdings.length > 1 && (
                            <button
                                type="button"
                                onClick={() => removeHolding(index)}
                                className="px-3 py-2 bg-red-500 text-gray-200 rounded-lg hover:bg-red-600"
                                disabled={loading}
                            >
                                Remove
                            </button>
                        )}
                    </div>
                ))}
            </div>

            <div className="flex gap-2 mt-4">
                <button
                    type="button"
                    onClick={addHolding}
                    className="px-4 py-2 bg-gray-600 text-gray-200 rounded-lg hover:bg-gray-700"
                    disabled={loading}
                >
                    Add Holding
                </button>
                <button
                    type="submit"
                    disabled={loading}
                    className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 font-semibold"
                >
                    {loading ? 'Analyzing...' : 'Analyze Portfolio'}
                </button>
            </div>
        </form>
    );
};

export default PortfolioInput;
