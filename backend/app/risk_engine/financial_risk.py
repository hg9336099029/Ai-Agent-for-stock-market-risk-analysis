"""
Financial risk calculation - Debt-to-Equity, Interest Coverage, Earnings Variability
"""

import numpy as np
from app.data_sources.fundamentals import get_balance_sheet, get_income_statement, get_earnings_history
from app.utils.logger import get_logger

logger = get_logger()

def calculate_debt_to_equity(symbol: str) -> float:
    """
    Calculate debt-to-equity ratio from balance sheet
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Debt-to-equity ratio
    """
    try:
        balance_sheet = get_balance_sheet(symbol)
        total_debt = balance_sheet.get("total_debt", 0)
        total_equity = balance_sheet.get("total_equity", 1)
        
        if total_equity == 0:
            return float('inf')
        
        ratio = total_debt / total_equity
        logger.info(f"Debt-to-Equity for {symbol}: {ratio:.2f}")
        
        return float(ratio)
    
    except Exception as e:
        logger.error(f"Error calculating debt-to-equity for {symbol}: {e}")
        return 1.0  # Default moderate leverage

def calculate_interest_coverage(symbol: str) -> float:
    """
    Calculate interest coverage ratio from income statement
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Interest coverage ratio
    """
    try:
        income_statement = get_income_statement(symbol)
        ebit = income_statement.get("ebit", 0)
        interest_expense = income_statement.get("interest_expense", 1)
        
        if interest_expense == 0:
            return float('inf')
        
        coverage = ebit / interest_expense
        logger.info(f"Interest Coverage for {symbol}: {coverage:.2f}")
        
        return float(coverage)
    
    except Exception as e:
        logger.error(f"Error calculating interest coverage for {symbol}: {e}")
        return 5.0  # Default moderate coverage

def calculate_earnings_variability(symbol: str, periods: int = 12) -> float:
    """
    Calculate coefficient of variation for earnings
    
    Args:
        symbol: Stock ticker symbol
        periods: Number of periods to analyze
        
    Returns:
        Earnings variability coefficient
    """
    try:
        earnings = get_earnings_history(symbol, periods)
        
        if len(earnings) == 0 or np.mean(earnings) == 0:
            return 0.5
        
        coefficient = np.std(earnings) / np.mean(earnings)
        logger.info(f"Earnings Variability for {symbol}: {coefficient:.4f}")
        
        return float(coefficient)
    
    except Exception as e:
        logger.error(f"Error calculating earnings variability for {symbol}: {e}")
        return 0.5  # Default moderate variability

def get_financial_risk_metrics(symbol: str) -> dict:
    """
    Aggregate all financial risk metrics
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dictionary with all financial risk metrics
    """
    return {
        "debt_to_equity": calculate_debt_to_equity(symbol),
        "interest_coverage": calculate_interest_coverage(symbol),
        "earnings_variability": calculate_earnings_variability(symbol)
    }
