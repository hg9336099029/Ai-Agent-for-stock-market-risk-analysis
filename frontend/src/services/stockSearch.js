/**
 * Stock Search Service - Real API Integration
 * Fetches live stock data from backend
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Search for stocks by query
 */
export const searchStocksAPI = async (query, limit = 10) => {
    try {
        const response = await fetch(
            `${API_BASE_URL}/search/stocks?q=${encodeURIComponent(query)}&limit=${limit}`
        );

        if (!response.ok) {
            throw new Error(`Search failed: ${response.statusText}`);
        }

        const data = await response.json();
        return data.results || [];
    } catch (error) {
        console.error('Stock search error:', error);
        return [];
    }
};

/**
 * Get popular stocks by market
 */
export const getPopularStocks = async (market = 'all') => {
    try {
        const response = await fetch(
            `${API_BASE_URL}/search/popular?market=${market}`
        );

        if (!response.ok) {
            throw new Error(`Failed to get popular stocks: ${response.statusText}`);
        }

        const data = await response.json();
        return data.stocks || {};
    } catch (error) {
        console.error('Error getting popular stocks:', error);
        return { indian: [], us: [] };
    }
};

/**
 * Get detailed stock information
 */
export const getStockInfo = async (symbol) => {
    try {
        const response = await fetch(
            `${API_BASE_URL}/search/info/${encodeURIComponent(symbol)}`
        );

        if (!response.ok) {
            throw new Error(`Failed to get stock info: ${response.statusText}`);
        }

        const data = await response.json();
        return data.data || null;
    } catch (error) {
        console.error('Error getting stock info:', error);
        return null;
    }
};
