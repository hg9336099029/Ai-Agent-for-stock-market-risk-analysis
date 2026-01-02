"""
Configuration management using environment variables
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_api_config():
    """Get API configuration"""
    return {
        "host": os.getenv("API_HOST", "0.0.0.0"),
        "port": int(os.getenv("API_PORT", "8000")),
        "reload": os.getenv("API_RELOAD", "True").lower() == "true"
    }

def get_openai_config():
    """Get OpenAI configuration"""
    return {
        "api_key": os.getenv("OPENAI_API_KEY", ""),
        "model": os.getenv("OPENAI_MODEL", "gpt-4"),
        "temperature": float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
    }

def get_gemini_config():
    """Get Google Gemini configuration"""
    return {
        "api_key": os.getenv("GEMINI_API_KEY", ""),
        "model": os.getenv("GEMINI_MODEL", "gemini-pro")
    }

def get_data_sources_config():
    """Get data sources configuration"""
    return {
        "use_cache": os.getenv("USE_CACHE", "True").lower() == "true",
        "cache_ttl": int(os.getenv("CACHE_TTL", "3600")),  # 1 hour default
        "news_lookback_hours": int(os.getenv("NEWS_LOOKBACK_HOURS", "72"))
    }

def get_risk_thresholds():
    """Get risk calculation thresholds"""
    return {
        "beta_high": float(os.getenv("BETA_HIGH", "1.5")),
        "beta_low": float(os.getenv("BETA_LOW", "0.5")),
        "volatility_high": float(os.getenv("VOLATILITY_HIGH", "0.3")),
        "debt_equity_high": float(os.getenv("DEBT_EQUITY_HIGH", "2.0")),
        "interest_coverage_low": float(os.getenv("INTEREST_COVERAGE_LOW", "2.0"))
    }
