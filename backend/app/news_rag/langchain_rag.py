"""
LangChain RAG pipeline for news verification
"""

from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema import HumanMessage

from app.news_rag.duckduckgo_search import search_stock_news_ddg
from app.utils.logger import get_logger
import os

logger = get_logger()

def create_news_verification_chain():
    """
    Create LangChain chain for news verification
    
    Returns:
        LLMChain for news verification
    """
    api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        logger.warning("GROQ_API_KEY not set, news verification will use rule-based approach")
        return None
    
    try:
        model_name = os.getenv("GROQ_MODEL", "groq/compound")
        if "groq/compound" in model_name:
            model_name = "groq/compound"
            
        llm = ChatGroq(
            groq_api_key=api_key,
            model_name=model_name,
            temperature=0.1  # Low temperature for factual verification
        )
        
        prompt = PromptTemplate(
            input_variables=["news_text", "symbol"],
            template="""Analyze the following news snippet about {symbol} and determine:
1. Is this news credible? (yes/no)
2. What is the sentiment? (positive/negative/neutral)
3. Is there any indication this might be fake news? (yes/no)

News: {news_text}

Respond in JSON format:
{{"credible": true/false, "sentiment": "positive/negative/neutral", "fake_indicator": true/false}}"""
        )
        
        chain = LLMChain(llm=llm, prompt=prompt)
        return chain
    
    except Exception as e:
        logger.error(f"Error creating news verification chain: {e}")
        return None

def verify_news_with_rag(symbol: str) -> list:
    """
    Complete RAG pipeline:
    1. Retrieve news from DuckDuckGo
    2. Verify with LangChain LLM
    3. Score confidence
    
    Args:
        symbol: Stock ticker symbol
        
    Returns:
        List of verified news items with confidence scores
    """
    logger.info(f"Starting RAG pipeline for {symbol}")
    
    # Step 1: Retrieve from DuckDuckGo
    search_results = search_stock_news_ddg(symbol, max_results=5)
    
    if not search_results:
        logger.warning(f"No search results for {symbol}")
        return []
    
    # Step 2: Verify with LangChain
    verification_chain = create_news_verification_chain()
    
    verified_news = []
    
    for idx, result in enumerate(search_results):
        news_text = result.get("snippet", "")
        
        if not news_text:
            continue
        
        # Default verification (rule-based)
        verified_item = {
            "title": f"News about {symbol} #{idx+1}",
            "summary": news_text[:200],
            "source": result.get("source", "DuckDuckGo"),
            "confidence": 0.7,  # Default moderate confidence
            "published_at": "recent",
            "url": result.get("link", "#"),
            "rag_verified": False
        }
        
        # Try LLM verification if chain available
        if verification_chain:
            try:
                verification = verification_chain.run(
                    news_text=news_text,
                    symbol=symbol
                )
                
                # Parse verification result
                import json
                try:
                    ver_result = json.loads(verification)
                    if ver_result.get("credible") and not ver_result.get("fake_indicator"):
                        verified_item["confidence"] = 0.9
                        verified_item["sentiment"] = ver_result.get("sentiment", "neutral")
                        verified_item["rag_verified"] = True
                    else:
                        verified_item["confidence"] = 0.4
                except:
                    pass
                
            except Exception as e:
                logger.error(f"Error in LLM verification: {e}")
        
        verified_news.append(verified_item)
    
    logger.info(f"RAG pipeline complete: {len(verified_news)} verified news items")
    
    return verified_news
