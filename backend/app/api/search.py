"""
Stock search API endpoints
"""

from fastapi import APIRouter, Query
from typing import Optional

from app.data_sources.stock_search import (
    search_stocks_yfinance,
    get_popular_indian_stocks,
    get_popular_us_stocks,
    get_stock_info_api
)

from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger()

@router.get("/search/stocks")
async def search_stocks(
    q: str = Query(..., description="Search query (symbol or company name)"),
    limit: int = Query(10, ge=1, le=50, description="Maximum results")
):
    """
    Search for stocks by symbol or company name
    
    Returns real-time stock data from yfinance
    """
    try:
        logger.info(f"Stock search request: {q}")
        
        results = search_stocks_yfinance(q, limit)
        
        return {
            "query": q,
            "count": len(results),
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Error in stock search: {e}")
        return {
            "query": q,
            "count": 0,
            "results": [],
            "error": str(e)
        }

@router.get("/search/popular")
async def get_popular_stocks(market: Optional[str] = Query(None, description="Market filter: indian, us, or all")):
    """
    Get popular stocks from specific markets
    
    Args:
        market: Filter by market (indian, us, or all)
    """
    try:
        logger.info(f"Popular stocks request for market: {market}")
        
        stocks = {
            "indian": [],
            "us": []
        }
        
        if market in [None, 'indian', 'all']:
            stocks["indian"] = get_popular_indian_stocks()
        
        if market in [None, 'us', 'all']:
            stocks["us"] = get_popular_us_stocks()
        
        # Flatten if specific market requested
        if market == 'indian':
            return {"market": "indian", "stocks": stocks["indian"]}
        elif market == 'us':
            return {"market": "us", "stocks": stocks["us"]}
        else:
            return {"market": "all", "stocks": stocks}
    
    except Exception as e:
        logger.error(f"Error getting popular stocks: {e}")
        return {
            "market": market,
            "stocks": [],
            "error": str(e)
        }

@router.get("/search/info/{symbol}")
async def get_stock_details(symbol: str):
    """
    Get detailed information for a specific stock
    
    Args:
        symbol: Stock ticker symbol (e.g., AAPL, RELIANCE.NS)
    """
    try:
        logger.info(f"Stock info request: {symbol}")
        
        info = get_stock_info_api(symbol)
        
        return {
            "symbol": symbol,
            "data": info
        }
    
    except Exception as e:
        logger.error(f"Error getting stock info for {symbol}: {e}")
        return {
            "symbol": symbol,
            "data": None,
            "error": str(e)
        }
