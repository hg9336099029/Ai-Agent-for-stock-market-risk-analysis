"""
Portfolio risk calculation - Correlation Matrix, Concentration, Diversification
"""

import numpy as np
from app.data_sources.market_data import get_stock_prices
from app.utils.logger import get_logger

logger = get_logger()

def calculate_correlation_matrix(holdings: list) -> list:
    """
    Calculate correlation matrix for portfolio holdings
    
    Args:
        holdings: List of dicts with 'symbol' and 'weight' keys
        
    Returns:
        Correlation matrix as list of lists
    """
    try:
        symbols = [h["symbol"] for h in holdings]
        
        # Get returns for all stocks
        returns_list = []
        for symbol in symbols:
            prices = get_stock_prices(symbol, 252)
            returns = np.diff(prices) / prices[:-1]
            returns_list.append(returns)
        
        # Stack returns into matrix
        returns_matrix = np.array(returns_list)
        
        # Calculate correlation matrix
        corr_matrix = np.corrcoef(returns_matrix)
        
        logger.info(f"Calculated correlation matrix for {len(symbols)} stocks")
        
        return corr_matrix.tolist()
    
    except Exception as e:
        logger.error(f"Error calculating correlation matrix: {e}")
        n = len(holdings)
        # Return identity matrix as fallback
        return np.eye(n).tolist()

def calculate_concentration_index(holdings: list) -> float:
    """
    Calculate Herfindahl-Hirschman Index for portfolio concentration
    
    Args:
        holdings: List of dicts with 'weight' key
        
    Returns:
        HHI concentration index
    """
    try:
        weights = [h["weight"] for h in holdings]
        hhi = sum(w**2 for w in weights)
        
        logger.info(f"Portfolio concentration index (HHI): {hhi:.4f}")
        
        return float(hhi)
    
    except Exception as e:
        logger.error(f"Error calculating concentration index: {e}")
        return 1.0 / len(holdings)  # Equal weight as fallback

def calculate_diversification_score(holdings: list) -> float:
    """
    Calculate portfolio diversification score (inverse of concentration)
    
    Args:
        holdings: List of dicts with 'weight' key
        
    Returns:
        Diversification score
    """
    try:
        concentration = calculate_concentration_index(holdings)
        
        if concentration == 0:
            return len(holdings)
        
        score = 1 / concentration
        logger.info(f"Portfolio diversification score: {score:.2f}")
        
        return float(score)
    
    except Exception as e:
        logger.error(f"Error calculating diversification score: {e}")
        return float(len(holdings))

def calculate_portfolio_risk(holdings: list) -> dict:
    """
    Aggregate all portfolio risk metrics
    
    Args:
        holdings: List of dicts with 'symbol' and 'weight' keys
        
    Returns:
        Dictionary with all portfolio risk metrics
    """
    return {
        "correlation_matrix": calculate_correlation_matrix(holdings),
        "concentration_index": calculate_concentration_index(holdings),
        "diversification_score": calculate_diversification_score(holdings),
        "num_holdings": len(holdings)
    }
