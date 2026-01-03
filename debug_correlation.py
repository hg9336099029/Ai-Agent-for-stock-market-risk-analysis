
import sys
import os
import numpy as np

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'backend')))

from app.data_sources.market_data import get_stock_prices
from app.data_sources.indices import get_index_prices
import logging

logging.basicConfig(level=logging.ERROR)

def test_correlation_logic(symbol, index):
    print(f"--- Testing logic for {symbol} vs {index} ---")
    try:
        stock_prices = get_stock_prices(symbol, 252)
        index_prices = get_index_prices(index, 252)
        
        print(f"Stock Prices Length: {len(stock_prices)}")
        print(f"Index Prices Length: {len(index_prices)}")
        
        stock_returns = np.diff(stock_prices) / stock_prices[:-1]
        index_returns = np.diff(index_prices) / index_prices[:-1]
        
        print(f"Stock Returns Length: {len(stock_returns)}")
        print(f"Index Returns Length: {len(index_returns)}")
        
        # This is where it likely fails if lengths differ
        correlation = np.corrcoef(stock_returns, index_returns)[0, 1]
        print(f"Calculated Correlation: {correlation}")
        
    except Exception as e:
        print(f"ERROR: {e}")

test_correlation_logic("AAPL", "^GSPC")
test_correlation_logic("MSFT", "^GSPC")
