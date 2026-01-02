"""
Pydantic models for API requests
"""

from pydantic import BaseModel, Field, field_validator
from typing import List

class StockAnalysisRequest(BaseModel):
    """Request model for single stock analysis"""
    symbol: str = Field(..., description="Stock ticker symbol", min_length=1, max_length=20)
    
    @field_validator('symbol')
    @classmethod
    def symbol_must_be_uppercase(cls, v: str) -> str:
        return v.upper().strip()

class PortfolioHolding(BaseModel):
    """Individual portfolio holding"""
    symbol: str = Field(..., description="Stock ticker symbol")
    weight: float = Field(..., description="Portfolio weight", ge=0, le=1)
    
    @field_validator('symbol')
    @classmethod
    def symbol_must_be_uppercase(cls, v: str) -> str:
        return v.upper().strip()

class PortfolioAnalysisRequest(BaseModel):
    """Request model for portfolio analysis"""
    holdings: List[PortfolioHolding] = Field(..., description="List of portfolio holdings", min_length=1)
    
    @field_validator('holdings')
    @classmethod
    def validate_weights_sum(cls, v: List[PortfolioHolding]) -> List[PortfolioHolding]:
        total_weight = sum(h.weight for h in v)
        if not (0.99 <= total_weight <= 1.01):  # Allow small floating point errors
            raise ValueError(f"Portfolio weights must sum to 1.0, got {total_weight}")
        return v
