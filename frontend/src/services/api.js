/**
 * API Service Layer for AI Stock Risk Analysis Platform
 * Handles all backend communication
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Analyze risk for a single stock
 * @param {string} symbol - Stock ticker symbol
 * @returns {Promise<object>} Risk analysis result
 */
export const analyzeStock = async (symbol) => {
    const response = await fetch(`${API_BASE_URL}/analyze/stock`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ symbol }),
    });

    if (!response.ok) {
        throw new Error(`Failed to analyze stock: ${response.statusText}`);
    }

    return response.json();
};

/**
 * Analyze risk for a portfolio
 * @param {Array} holdings - Array of {symbol, weight} objects
 * @returns {Promise<object>} Portfolio risk analysis result
 */
export const analyzePortfolio = async (holdings) => {
    const response = await fetch(`${API_BASE_URL}/analyze/portfolio`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ holdings }),
    });

    if (!response.ok) {
        throw new Error(`Failed to analyze portfolio: ${response.statusText}`);
    }

    return response.json();
};

/**
 * Check API health status
 * @returns {Promise<object>} Health status
 */
export const checkHealth = async () => {
    const response = await fetch(`${API_BASE_URL}/health`);

    if (!response.ok) {
        throw new Error(`Health check failed: ${response.statusText}`);
    }

    return response.json();
};
