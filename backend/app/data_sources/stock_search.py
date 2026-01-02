"""
Stock search and lookup using real APIs with fallback
"""

import yfinance as yf
from app.utils.logger import get_logger
from app.utils.cache import get_cache, set_cache

logger = get_logger()

# Static stock database for fallback
STOCK_DATABASE = {
    # Indian Stocks (NSE)
    'RELIANCE.NS': {'name': 'Reliance Industries', 'market': 'NSE', 'sector': 'Conglomerate'},
    'TCS.NS': {'name': 'Tata Consultancy Services', 'market': 'NSE', 'sector': 'IT'},
    'HDFCBANK.NS': {'name': 'HDFC Bank', 'market': 'NSE', 'sector': 'Banking'},
    'INFY.NS': {'name': 'Infosys', 'market': 'NSE', 'sector': 'IT'},
    'ICICIBANK.NS': {'name': 'ICICI Bank', 'market': 'NSE', 'sector': 'Banking'},
    'HINDUNILVR.NS': {'name': 'Hindustan Unilever', 'market': 'NSE', 'sector': 'FMCG'},
    'ITC.NS': {'name': 'ITC Limited', 'market': 'NSE', 'sector': 'FMCG'},
    'SBIN.NS': {'name': 'State Bank of India', 'market': 'NSE', 'sector': 'Banking'},
    'BHARTIARTL.NS': {'name': 'Bharti Airtel', 'market': 'NSE', 'sector': 'Telecom'},
    'KOTAKBANK.NS': {'name': 'Kotak Mahindra Bank', 'market': 'NSE', 'sector': 'Banking'},
    'LT.NS': {'name': 'Larsen & Toubro', 'market': 'NSE', 'sector': 'Engineering'},
    'AXISBANK.NS': {'name': 'Axis Bank', 'market': 'NSE', 'sector': 'Banking'},
    'ASIANPAINT.NS': {'name': 'Asian Paints', 'market': 'NSE', 'sector': 'Paints'},
    # More Indian Tech/New Age
    'PAYTM.NS': {'name': 'One97 Communications (Paytm)', 'market': 'NSE', 'sector': 'Financial Technology'},
    'ZOMATO.NS': {'name': 'Zomato Ltd', 'market': 'NSE', 'sector': 'Technology'},
    'NAUKRI.NS': {'name': 'Info Edge (India) Ltd', 'market': 'NSE', 'sector': 'Technology'},
    'NYKAA.NS': {'name': 'FSN E-Commerce Ventures (Nykaa)', 'market': 'NSE', 'sector': 'E-commerce'},
    'DELHIVERY.NS': {'name': 'Delhivery Ltd', 'market': 'NSE', 'sector': 'Logistics'},
    'POLICYBZR.NS': {'name': 'PB Fintech (PolicyBazaar)', 'market': 'NSE', 'sector': 'Financial Technology'},
    
    # US Stocks
    'AAPL': {'name': 'Apple Inc.', 'market': 'NASDAQ', 'sector': 'Technology'},
    'MSFT': {'name': 'Microsoft Corporation', 'market': 'NASDAQ', 'sector': 'Technology'},
    'GOOGL': {'name': 'Alphabet Inc.', 'market': 'NASDAQ', 'sector': 'Technology'},
    'AMZN': {'name': 'Amazon.com Inc.', 'market': 'NASDAQ', 'sector': 'E-commerce'},
    'META': {'name': 'Meta Platforms Inc.', 'market': 'NASDAQ', 'sector': 'Social Media'},
    'TSLA': {'name': 'Tesla Inc.', 'market': 'NASDAQ', 'sector': 'Automotive'},
    'NVDA': {'name': 'NVIDIA Corporation', 'market': 'NASDAQ', 'sector': 'Semiconductors'},
    'JPM': {'name': 'JPMorgan Chase & Co.', 'market': 'NYSE', 'sector': 'Banking'},
    'V': {'name': 'Visa Inc.', 'market': 'NYSE', 'sector': 'Financial Services'},
    'JNJ': {'name': 'Johnson & Johnson', 'market': 'NYSE', 'sector': 'Healthcare'},
}

import requests

def get_request_session():
    """Create a session with custom headers to avoid bot detection"""
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    })
    return session

def fetch_yahoo_autocomplete(query: str):
    """
    Fetch autocomplete results from Yahoo Finance
    """
    try:
        session = get_request_session()
        # Use query2 which is often more reliable
        url = "https://query2.finance.yahoo.com/v1/finance/search"
        
        params = {
            'q': query,
            'quotesCount': 25, # Increased to ensure Indian stocks are found even if buried
            'newsCount': 0,
            'enableFuzzyQuery': 'true',
            'enableCb': 'true'
        }
        
        response = session.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if 'quotes' in data:
                return data['quotes']
                
        return []
    except Exception as e:
        logger.error(f"Error fetching Yahoo autocomplete: {e}")
        return []

def search_stocks_yfinance(query: str, limit: int = 10) -> list:
    """
    Search for stocks using Yahoo Autocomplete API as primary source
    """
    try:
        logger.info(f"Searching for stocks: {query}")
        
        # Check cache
        cache_key = f"search_{query}_{limit}"
        cached_result = get_cache(cache_key)
        if cached_result:
            return cached_result
        
        # 1. Fetch from Yahoo Autocomplete API (Primary Source)
        results = []
        seen_symbols = set()
        
        try:
            yahoo_results = fetch_yahoo_autocomplete(query)
            for item in yahoo_results:
                symbol = item.get('symbol')
                if not symbol or symbol in seen_symbols: continue
                
                # Filter types: only Stock/ETF
                quote_type = item.get('quoteType', 'EQUITY')
                if quote_type not in ['EQUITY', 'ETF', 'MUTUALFUND']:
                    continue
                
                market = item.get('exchange', 'Unknown')
                
                # Strict Filter: Only allow Indian Markets (NSE/BSE)
                final_market = None
                
                # Check 1: Symbol suffix (Strongest signal)
                if symbol.endswith('.NS'):
                    final_market = 'NSE'
                elif symbol.endswith('.BO'):
                    final_market = 'BSE'
                
                # Check 2: Exchange code (if suffix missing but valid exchange)
                elif market in ['NSI', 'NSE']:
                    final_market = 'NSE'
                elif market in ['BSI', 'BSE']:
                    final_market = 'BSE'

                # Skip if not identified as Indian market
                if not final_market:
                    continue
                
                # Clean up name
                name = item.get('shortname') or item.get('longname') or symbol
                
                results.append({
                    'symbol': symbol,
                    'name': name,
                    'market': final_market,
                    'sector': item.get('sector', 'N/A'),
                    'type': 'stock'
                })
                seen_symbols.add(symbol)
                
                if len(results) >= limit:
                    break
                    
        except Exception as e:
            logger.error(f"Yahoo API failed: {e}")

        # Removed Static Database Fallback as requested
        
        if results:
            set_cache(cache_key, results, ttl_seconds=3600)
        
        logger.info(f"Found {len(results)} results for {query}")
        return results[:limit]
    
    except Exception as e:
        logger.error(f"Error searching stocks: {e}")
        return []

def get_popular_indian_stocks() -> list:
    """Get list of popular Indian stocks"""
    return [
        {'symbol': symbol, 'name': data['name'], 'market': data['market'], 'sector': data['sector']}
        for symbol, data in STOCK_DATABASE.items()
        if '.NS' in symbol
    ][:15]

def get_popular_us_stocks() -> list:
    """Get list of popular US stocks"""
    # Fix: Corrected syntax for data['market']
    return [
        {'symbol': symbol, 'name': data['name'], 'market': data['market'], 'sector': data['sector']}
        for symbol, data in STOCK_DATABASE.items()
        if '.NS' not in symbol and '.BO' not in symbol
    ][:10]

def get_stock_info_api(symbol: str) -> dict:
    """Get detailed stock information"""
    try:
        # Check static database first
        if symbol in STOCK_DATABASE:
            data = STOCK_DATABASE[symbol]
            return {
                'symbol': symbol,
                'name': data['name'],
                'market': data['market'],
                'sector': data['sector'],
                'industry': data.get('industry', 'N/A'),
                'market_cap': 0,
                'currency': 'USD' if '.NS' not in symbol else 'INR',
                'current_price': 0,
                'previous_close': 0,
                'volume': 0
            }
        
        # Try yfinance
        ticker = yf.Ticker(symbol)
        info = ticker.info
        
        return {
            'symbol': symbol,
            'name': info.get('longName', info.get('shortName', symbol)),
            'market': info.get('exchange', 'Unknown'),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'currency': info.get('currency', 'USD'),
            'current_price': info.get('currentPrice', 0),
            'previous_close': info.get('previousClose', 0),
            'volume': info.get('volume', 0)
        }
    except Exception as e:
        logger.error(f"Error getting stock info for {symbol}: {e}")
        return {
            'symbol': symbol,
            'name': symbol,
            'market': 'Unknown',
            'sector': 'N/A'
        }
