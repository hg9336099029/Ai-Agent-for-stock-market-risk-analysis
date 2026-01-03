
import sys
import os

# Add backend to path
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), 'backend')))

from app.risk_engine.market_risk import get_market_risk_metrics
import logging

# Configure logger
logging.basicConfig(level=logging.INFO)

symbols = ["AAPL", "MSFT", "TSLA"]

print("--- Testing Market Risk Metrics (Beta, Volatility, Correlation) ---\n")

for symbol in symbols:
    print(f"Fetching market risk metrics for {symbol}...")
    metrics = get_market_risk_metrics(symbol)
    print(f"Metrics: {metrics}\n")
