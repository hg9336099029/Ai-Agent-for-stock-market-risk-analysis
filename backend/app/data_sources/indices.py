"""
Index data retrieval
"""

import yfinance as yf
import numpy as np
from app.utils.cache import get_cache, set_cache
from app.utils.logger import get_logger

logger = get_logger()

def get_index_prices(index_symbol: str = "^GSPC", period_days: int = 252) -> np.ndarray:
    """
    Get historical index prices (default: S&P 500)
    
    Args:
        index_symbol: Index ticker (^GSPC for S&P 500)
        period_days: Number of trading days
        
    Returns:
        numpy array of closing prices
    """
    cache_key = f"index_{index_symbol}_{period_days}"
    cached = get_cache(cache_key)
    
    if cached is not None:
        return cached
    
    try:
        logger.info(f"Fetching index prices for {index_symbol}")
        # Try importing the session/raw fetcher
        from app.data_sources.market_data import get_session, fetch_prices_raw
        
        index = yf.Ticker(index_symbol, session=get_session())
        hist = index.history(period=f"{period_days}d")
        
        if not hist.empty:
            prices = hist['Close'].values
            set_cache(cache_key, prices, ttl_seconds=3600)
            return prices
            
    except Exception as e:
        logger.warning(f"yfinance failed for index {index_symbol}, trying raw fallback: {e}")

    # Fallback to raw fetch
    try:
        from app.data_sources.market_data import fetch_prices_raw, generate_fallback_prices
        raw_prices = fetch_prices_raw(index_symbol, period_days)
        if raw_prices is not None and len(raw_prices) > 0:
            logger.info(f"Raw fallback successful for {index_symbol}")
            set_cache(cache_key, raw_prices, ttl_seconds=3600)
            return raw_prices
            
        # If raw fetch also fails, return generated random walk
        logger.warning(f"Generating fallback index history for {index_symbol}")
        return generate_fallback_prices(index_symbol, period_days)
        
    except Exception as e:
        logger.error(f"Error in index fallback: {e}")
        # Absolute last resort
        return np.array([4000.0] * period_days)
