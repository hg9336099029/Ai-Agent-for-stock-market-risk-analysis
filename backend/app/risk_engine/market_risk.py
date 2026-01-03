"""
Market risk calculation - Beta, Volatility, Correlation
"""

import numpy as np
from app.data_sources.market_data import get_stock_prices
from app.data_sources.indices import get_index_prices
from app.utils.logger import get_logger

logger = get_logger()

def calculate_beta(symbol: str, index: str = "^GSPC", period: int = 252) -> float:
    """
    Calculate stock beta relative to market index
    
    Args:
        symbol: Stock ticker symbol
        index: Market index symbol
        period: Number of trading days
        
    Returns:
        Beta value
    """
    try:
        stock_prices = get_stock_prices(symbol, period)
        index_prices = get_index_prices(index, period)
        
        # Ensure same length
        min_len = min(len(stock_prices), len(index_prices))
        stock_prices = stock_prices[-min_len:]
        index_prices = index_prices[-min_len:]
        
        # Calculate returns
        stock_returns = np.diff(stock_prices) / stock_prices[:-1]
        index_returns = np.diff(index_prices) / index_prices[:-1]
        
        # Calculate covariance and variance
        covariance = np.cov(stock_returns, index_returns)[0, 1]
        index_variance = np.var(index_returns)
        
        if index_variance == 0:
            return 1.0
        
        beta = covariance / index_variance
        logger.info(f"Beta for {symbol}: {beta:.2f}")
        
        return float(beta)
    
    except Exception as e:
        logger.error(f"Error calculating beta for {symbol}: {e}")
        return 1.0  # Market beta as default

def calculate_volatility(symbol: str, period: int = 252) -> float:
    """
    Calculate stock volatility (annualized standard deviation)
    
    Args:
        symbol: Stock ticker symbol
        period: Number of trading days
        
    Returns:
        Annualized volatility
    """
    try:
        stock_prices = get_stock_prices(symbol, period)
        stock_returns = np.diff(stock_prices) / stock_prices[:-1]
        
        # Annualized volatility (252 trading days)
        volatility = np.std(stock_returns) * np.sqrt(252)
        logger.info(f"Volatility for {symbol}: {volatility:.4f}")
        
        return float(volatility)
    
    except Exception as e:
        logger.error(f"Error calculating volatility for {symbol}: {e}")
        return 0.2  # Default moderate volatility

def calculate_correlation(symbol: str, index: str = "^GSPC", period: int = 252) -> float:
    """
    Calculate correlation coefficient with market index
    
    Args:
        symbol: Stock ticker symbol
        index: Market index symbol
        period: Number of trading days
        
    Returns:
        Correlation coefficient
    """
    try:
        stock_prices = get_stock_prices(symbol, period)
        index_prices = get_index_prices(index, period)
        
        # Ensure same length
        min_len = min(len(stock_prices), len(index_prices))
        stock_prices = stock_prices[-min_len:]
        index_prices = index_prices[-min_len:]
        
        stock_returns = np.diff(stock_prices) / stock_prices[:-1]
        index_returns = np.diff(index_prices) / index_prices[:-1]
        
        correlation = np.corrcoef(stock_returns, index_returns)[0, 1]
        logger.info(f"Correlation for {symbol}: {correlation:.4f}")
        
        return float(correlation)
    
    except Exception as e:
        logger.error(f"Error calculating correlation for {symbol}: {e}")
        return 0.5  # Default moderate correlation

def get_market_risk_metrics(symbol: str) -> dict:
    """
    Aggregate all market risk metrics
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dictionary with all market risk metrics
    """
    return {
        "beta": calculate_beta(symbol),
        "volatility": calculate_volatility(symbol),
        "correlation": calculate_correlation(symbol)
    }
