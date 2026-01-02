"""
Build verified context using LangChain RAG with DuckDuckGo
"""

from app.news_rag.langchain_rag import verify_news_with_rag
from app.news_rag.retriever import retrieve_news
from app.news_rag.verifier import verify_news
from app.news_rag.confidence import score_news_confidence
from app.utils.logger import get_logger
import os

logger = get_logger()

def build_news_context(symbol: str) -> list:
    """
    Build complete verified news context using LangChain RAG
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        List of verified and scored news items
    """
    logger.info(f"Building news context for {symbol}")
    
    # Check if we should use LangChain RAG (if GROQ_API_KEY is set)
    use_langchain = bool(os.getenv("GROQ_API_KEY"))
    
    if use_langchain:
        logger.info("Using LangChain RAG pipeline with DuckDuckGo")
        try:
            verified_news = verify_news_with_rag(symbol)
            
            if verified_news:
                logger.info(f"LangChain RAG returned {len(verified_news)} items")
                return verified_news
        except Exception as e:
            logger.error(f"LangChain RAG failed, falling back to basic retrieval: {e}")
    
    # Fallback to basic retrieval
    logger.info("Using basic news retrieval")
    news_items = retrieve_news(symbol)
    verified_news = verify_news(news_items)
    scored_news = score_news_confidence(verified_news)
    filtered_news = [n for n in scored_news if n.get("confidence", 0) >= 0.5]
    
    logger.info(f"Built context with {len(filtered_news)} news items for {symbol}")
    
    return filtered_news
