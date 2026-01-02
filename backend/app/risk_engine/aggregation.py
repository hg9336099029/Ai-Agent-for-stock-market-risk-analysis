"""
Risk aggregation and overall score calculation
"""

from app.risk_engine.market_risk import get_market_risk_metrics
from app.risk_engine.financial_risk import get_financial_risk_metrics
from app.utils.config import get_risk_thresholds
from app.utils.logger import get_logger

logger = get_logger()

def calculate_market_risk_score(market_metrics: dict) -> float:
    """
    Calculate market risk score (0-10) from metrics
    
    Args:
        market_metrics: Dictionary with beta, volatility, correlation
        
    Returns:
        Market risk score
    """
    thresholds = get_risk_thresholds()
    
    beta = market_metrics.get("beta", 1.0)
    volatility = market_metrics.get("volatility", 0.2)
    
    # Beta component (0-5)
    if beta > thresholds["beta_high"]:
        beta_score = 5.0
    elif beta < thresholds["beta_low"]:
        beta_score = 1.0
    else:
        # Linear interpolation
        beta_score = 1 + 4 * (beta - thresholds["beta_low"]) / (thresholds["beta_high"] - thresholds["beta_low"])
    
    # Volatility component (0-5)
    if volatility > thresholds["volatility_high"]:
        vol_score = 5.0
    else:
        vol_score = (volatility / thresholds["volatility_high"]) * 5
    
    # Market score sum (0-10)
    total_score = beta_score + vol_score
    
    return min(10.0, max(0.0, total_score))

def calculate_financial_risk_score(financial_metrics: dict) -> float:
    """
    Calculate financial risk score (0-10) from metrics
    
    Args:
        financial_metrics: Dictionary with debt_to_equity, interest_coverage, earnings_variability
        
    Returns:
        Financial risk score
    """
    thresholds = get_risk_thresholds()
    
    debt_equity = financial_metrics.get("debt_to_equity", 1.0)
    interest_cov = financial_metrics.get("interest_coverage", 5.0)
    earnings_var = financial_metrics.get("earnings_variability", 0.2)
    
    # Debt-to-equity component (0-4)
    if debt_equity > thresholds["debt_equity_high"]:
        debt_score = 4.0
    else:
        debt_score = (debt_equity / thresholds["debt_equity_high"]) * 4
    
    # Interest coverage component (0-3, inverted - lower coverage = higher risk)
    if interest_cov < thresholds["interest_coverage_low"]:
        coverage_score = 3.0
    else:
        coverage_score = max(0, 3.0 - (interest_cov / 10) * 3)
    
    # Earnings variability component (0-3)
    earnings_score = min(3.0, earnings_var * 10)
    
    total_score = debt_score + coverage_score + earnings_score
    
    return min(10.0, max(0.0, total_score))

def aggregate_stock_risk(symbol: str) -> dict:
    """
    Aggregate all risk metrics for a stock and calculate overall score
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        Dictionary with all metrics and overall score
    """
    logger.info(f"Aggregating risk for {symbol}")
    
    try:
        # Get all metrics
        market_metrics = get_market_risk_metrics(symbol)
    except Exception as e:
        logger.error(f"Error getting market metrics: {e}")
        # Default to neutral values yielding market_score ~5.0
        # Beta 1.0 -> 3.0 score, Vol 0.12 -> 2.0 score. Total 5.0.
        market_metrics = {"beta": 1.0, "volatility": 0.12, "correlation": 0.5}
        
    try:
        financial_metrics = get_financial_risk_metrics(symbol)
    except Exception as e:
        logger.error(f"Error getting financial metrics: {e}")
        # Default to neutral values yielding financial_score ~5.0
        # D/E 1.0 -> 2.0, Cov 5.0 -> 1.5, EarnVar 0.15 -> 1.5. Total 5.0.
        financial_metrics = {
            "debt_to_equity": 1.0, 
            "interest_coverage": 5.0, 
            "earnings_variability": 0.15
        }
    
    # Calculate component scores
    market_score = calculate_market_risk_score(market_metrics)
    financial_score = calculate_financial_risk_score(financial_metrics)
    
    # Overall score (weighted average)
    overall_score = (market_score * 0.6) + (financial_score * 0.4)
    
    logger.info(f"Overall risk score for {symbol}: {overall_score:.2f}")
    
    return {
        "overall_score": overall_score,
        "market_risk": market_metrics,
        "financial_risk": financial_metrics,
        "component_scores": {
            "market": market_score,
            "financial": financial_score
        },
        "partial_data": True # Flag to indicate potential data issues
    }
