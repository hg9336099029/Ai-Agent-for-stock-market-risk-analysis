"""
LangChain-powered search using DuckDuckGo
"""

from langchain_community.tools import DuckDuckGoSearchResults
from langchain.agents import Tool
from app.utils.logger import get_logger

logger = get_logger()

def create_duckduckgo_search_tool():
    """
    Create DuckDuckGo search tool for LangChain
    
    Returns:
        LangChain Tool for DuckDuckGo search
    """
    search = DuckDuckGoSearchResults(num_results=5)
    
    tool = Tool(
        name="DuckDuckGo Search",
        func=search.run,
        description="Search the web for recent news and information about stocks using DuckDuckGo. Use this to find current market sentiment, news articles, and public information."
    )
    
    return tool

def search_stock_news_ddg(symbol: str, max_results: int = 5) -> list:
    """
    Search for stock news using DuckDuckGo via LangChain
    
    Args:
        symbol: Stock ticker symbol
        max_results: Maximum number of results
        
    Returns:
        List of search results
    """
    try:
        logger.info(f"Searching DuckDuckGo for {symbol} news")
        
        search = DuckDuckGoSearchResults(num_results=max_results)
        query = f"{symbol} stock news latest"
        
        results = search.run(query)
        
        logger.info(f"Found {len(results) if isinstance(results, list) else 'text'} results from DuckDuckGo")
        
        # Parse results
        if isinstance(results, str):
            # Results are in string format, parse them
            import re
            parsed_results = []
            
            # Simple parsing - in production, use proper parser
            lines = results.split('\n')
            for line in lines[:max_results]:
                if line.strip():
                    parsed_results.append({
                        "snippet": line.strip(),
                        "source": "DuckDuckGo Search"
                    })
            
            return parsed_results
        
        return results if isinstance(results, list) else []
    
    except Exception as e:
        logger.error(f"Error searching DuckDuckGo for {symbol}: {e}")
        return []
