"""
News confidence scoring based on source reputation and verification
"""

from app.utils.logger import get_logger

logger = get_logger()

def calculate_confidence_score(news_item: dict) -> float:
    """
    Calculate confidence score for a news item
    
    Args:
        news_item: News item dictionary
        
    Returns:
        Confidence score (0-1)
    """
    source = news_item.get("source", "").lower()
    verified = news_item.get("verified", False)
    
    # Source reputation scores
    source_scores = {
        "reuters": 0.95,
        "bloomberg": 0.95,
        "wsj": 0.9,
        "cnbc": 0.85,
        "marketwatch": 0.8,
    }
    
    base_score = source_scores.get(source, 0.6)
    
    # Boost if verified
    if verified:
        base_score = min(1.0, base_score + 0.1)
    
    return base_score

def score_news_confidence(news_items: list) -> list:
    """
    Add confidence scores to all news items
    
    Args:
        news_items: List of news items
        
    Returns:
        List of news items with confidence scores
    """
    logger.info(f"Scoring confidence for {len(news_items)} news items")
    
    scored_news = []
    for news in news_items:
        news["confidence"] = calculate_confidence_score(news)
        scored_news.append(news)
    
    return scored_news
