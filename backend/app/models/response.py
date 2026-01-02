"""
Pydantic models for API responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional

class MarketRiskMetrics(BaseModel):
    """Market risk metrics"""
    beta: float = Field(..., description="Stock beta")
    volatility: float = Field(..., description="Stock volatility")
    correlation: float = Field(..., description="Market correlation")

class FinancialRiskMetrics(BaseModel):
    """Financial risk metrics"""
    debt_to_equity: float = Field(..., description="Debt-to-equity ratio")
    interest_coverage: float = Field(..., description="Interest coverage ratio")
    earnings_variability: float = Field(..., description="Earnings variability coefficient")

class PortfolioRiskMetrics(BaseModel):
    """Portfolio-specific risk metrics"""
    correlation_matrix: List[List[float]] = Field(..., description="Correlation matrix")
    concentration_index: float = Field(..., description="HHI concentration index")
    diversification_score: float = Field(..., description="Diversification score")
    num_holdings: int = Field(..., description="Number of holdings")

class NewsItem(BaseModel):
    """Individual news item"""
    title: str
    summary: str
    source: str
    confidence: float = Field(..., ge=0, le=1)
    published_at: str
    url: Optional[str] = None

class StockAnalysisResponse(BaseModel):
    """Response model for stock analysis"""
    symbol: str
    risk_score: float = Field(..., ge=0, le=10)
    risk_breakdown: Dict[str, Any]
    news_impact: Optional[List[NewsItem]] = None
    explanation: Optional[str] = None
    timestamp: str

class PortfolioAnalysisResponse(BaseModel):
    """Response model for portfolio analysis"""
    holdings: List[Dict[str, Any]]
    overall_risk_score: float = Field(..., ge=0, le=10)
    metrics: Dict[str, Any]
    explanation: Optional[str] = None
    timestamp: str
