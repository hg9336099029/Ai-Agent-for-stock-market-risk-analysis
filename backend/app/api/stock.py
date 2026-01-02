"""
Stock analysis API endpoint
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime

from app.models.request import StockAnalysisRequest
from app.models.response import StockAnalysisResponse, NewsItem
from app.risk_engine.aggregation import aggregate_stock_risk
from app.news_rag.context_builder import build_news_context
from app.ai.explanation import generate_risk_explanation
from app.utils.logger import get_logger

router = APIRouter()
logger = get_logger()

@router.post("/analyze/stock", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest):
    """
    Analyze risk for a single stock with news verification and GenAI explanation
    
    Args:
        request: StockAnalysisRequest with symbol
        
    Returns:
        StockAnalysisResponse with risk metrics and explanation
    """
    try:
        logger.info(f"Stock analysis request for {request.symbol}")
        
        # Calculate deterministic risk metrics
        risk_metrics = aggregate_stock_risk(request.symbol)
        
        # Retrieve and verify news
        news_context = build_news_context(request.symbol)
        
        # Generate AI explanation (no numeric modification)
        explanation = generate_risk_explanation(risk_metrics, news_context, request.symbol)
        
        # Format news for response
        news_items = [
            NewsItem(
                title=news.get("title", ""),
                summary=news.get("summary", ""),
                source=news.get("source", ""),
                confidence=news.get("confidence", 0.5),
                published_at=news.get("published_at", ""),
                url=news.get("url")
            )
            for news in news_context
        ]
        
        response = StockAnalysisResponse(
            symbol=request.symbol,
            risk_score=risk_metrics["overall_score"],
            risk_breakdown=risk_metrics,
            news_impact=news_items,
            explanation=explanation,
            timestamp=datetime.now().isoformat()
        )
        
        logger.info(f"Successfully analyzed {request.symbol}")
        
        return response
    
    except Exception as e:
        logger.error(f"Error analyzing stock {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
