
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'backend')))

from app.data_sources.market_data import get_stock_info
from app.risk_engine.financial_risk import get_financial_risk_metrics
import logging

# Configure logger to see output
logging.basicConfig(level=logging.INFO)

symbols = ["AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]

print("--- Testing yfinance ---\n")
for symbol in symbols:
    print(f"Fetching info for {symbol}...")
    info = get_stock_info(symbol)
    if info:
        print(f"Info keys found: {len(info)}")
        print(f"  Total Debt: {info.get('totalDebt')}")
        print(f"  Total Equity: {info.get('totalStockholderEquity')}")
    else:
        print(f"FAILED to get info for {symbol}")

    print(f"Fetching financial risk metrics for {symbol}...")
    metrics = get_financial_risk_metrics(symbol)
    print(f"Metrics: {metrics}\n")
