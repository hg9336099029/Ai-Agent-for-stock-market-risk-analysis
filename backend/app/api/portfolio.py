"""
Portfolio analysis API endpoint
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models.request import PortfolioAnalysisRequest
from app.models.response import PortfolioAnalysisResponse
from app.risk_engine.portfolio_risk import calculate_portfolio_risk
from app.risk_engine.aggregation import aggregate_stock_risk
from app.ai.explanation import generate_risk_explanation
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger()

@router.post("/analyze/portfolio", response_model=PortfolioAnalysisResponse)
async def analyze_portfolio(request: PortfolioAnalysisRequest):
    """
    Analyze risk for a portfolio with correlation and diversification metrics
    
    Args:
        request: PortfolioAnalysisRequest with holdings
        
    Returns:
        PortfolioAnalysisResponse with risk metrics
    """
    try:
        logger.info(f"Portfolio analysis request with {len(request.holdings)} holdings")
        
        # Convert holdings to list of dicts
        holdings_list = [
            {"symbol": h.symbol, "weight": h.weight}
            for h in request.holdings
        ]
        
        # Calculate portfolio-specific metrics
        portfolio_metrics = calculate_portfolio_risk(holdings_list)
        
        # Calculate weighted risk score from individual stocks
        total_risk_score = 0.0
        individual_risks = {}
        
        for holding in request.holdings:
            stock_risk = aggregate_stock_risk(holding.symbol)
            individual_risks[holding.symbol] = stock_risk["overall_score"]
            total_risk_score += stock_risk["overall_score"] * holding.weight
        
        # Combine metrics
        combined_metrics = {
            "portfolio_risk": portfolio_metrics,
            "individual_risks": individual_risks,
            "weighted_average_risk": total_risk_score
        }
        
        # Generate explanation
        explanation = generate_risk_explanation(
            {"overall_score": total_risk_score, "portfolio_risk": portfolio_metrics},
            [],
            None
        )
        
        response = PortfolioAnalysisResponse(
            holdings=[{"symbol": h.symbol, "weight": h.weight} for h in request.holdings],
            overall_risk_score=total_risk_score,
            metrics=combined_metrics,
            explanation=explanation,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Successfully analyzed portfolio")
        
        return response
    
    except Exception as e:
        logger.error(f"Error analyzing portfolio: {e}")
        raise HTTPException(status_code=500, detail=f"Portfolio analysis failed: {str(e)}")
