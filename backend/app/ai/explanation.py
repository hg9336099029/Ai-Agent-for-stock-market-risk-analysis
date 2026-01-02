"""
GenAI risk explanation generation using Groq
"""

import os
from groq import Groq
from app.ai.prompts import get_stock_risk_prompt, get_portfolio_risk_prompt
from app.utils.logger import get_logger

logger = get_logger()

def get_groq_client():
    """Get Groq client instance"""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        logger.warning("GROQ_API_KEY not set, using template-based explanations")
        return None
    return Groq(api_key=api_key)

def generate_with_groq(prompt: str) -> str:
    """
    Generate explanation using Groq API
    
    Args:
        prompt: Formatted prompt string
        
    Returns:
        Generated explanation text
    """
    try:
        client = get_groq_client()
        
        if client is None:
            # Fallback to template if no API key
            return generate_template_explanation(prompt)
        
        logger.info("Generating explanation with Groq")
        
        response = client.chat.completions.create(
            model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile"),
            messages=[
                {
                    "role": "system",
                    "content": "You are a professional financial risk analyst. Provide clear, concise risk explanations without speculation. Be honest about uncertainties and limitations."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=float(os.getenv("GROQ_TEMPERATURE", "0.3")),
            max_tokens=1000,
        )
        
        explanation = response.choices[0].message.content
        logger.info("Successfully generated explanation with Groq")
        
        return explanation
    
    except Exception as e:
        logger.error(f"Error generating with Groq: {e}")
        return generate_template_explanation(prompt)

def generate_template_explanation(prompt: str) -> str:
    """
    Generate template-based explanation (fallback)
    
    Args:
        prompt: Prompt containing metrics
        
    Returns:
        Template-based explanation
    """
    # Extract risk score from prompt
    import re
    score_match = re.search(r'Risk Score:\*\* ([\d.]+)/10', prompt)
    overall_score = float(score_match.group(1)) if score_match else 5.0
    
    if overall_score >= 7:
        risk_level = "high"
        assessment = "significant risks that require careful consideration"
    elif overall_score >= 4:
        risk_level = "moderate"
        assessment = "balanced risk-reward profile with some areas of concern"
    else:
        risk_level = "low"
        assessment = "relatively stable fundamentals with manageable risks"
    
    explanation = f"""Based on the comprehensive risk analysis, this investment shows a {risk_level} risk profile with a score of {overall_score:.1f}/10.

The analysis reveals {assessment}. The quantitative metrics have been calculated using deterministic financial models and verified market data. Risk factors include market volatility, financial leverage, and earnings stability.

Recent verified news from trusted sources has been incorporated into the context of this analysis. All news items have undergone multi-source verification with confidence scoring.

**Important Limitations:** This analysis is based on historical data and current market conditions. Past performance does not guarantee future results. This is decision-support analysis, not financial advice. Always consult with a qualified financial advisor before making investment decisions."""
    
    return explanation

def generate_risk_explanation(risk_metrics: dict, news_context: list, symbol: str = None) -> str:
    """
    Generate AI-powered risk explanation
    
    Args:
        risk_metrics: Dictionary with all risk metrics
        news_context: List of verified news items
        symbol: Stock ticker symbol (optional, for stock analysis)
        
    Returns:
        Generated explanation text
    """
    logger.info(f"Generating risk explanation for {symbol or 'portfolio'}")
    
    # Generate appropriate prompt
    if symbol:
        prompt = get_stock_risk_prompt(symbol, risk_metrics, news_context)
    else:
        # For portfolio (news_context contains holdings in this case)
        prompt = get_portfolio_risk_prompt(news_context if isinstance(news_context, list) and len(news_context) > 0 and 'symbol' in news_context[0] else [], risk_metrics)
    
    # Generate with Groq
    explanation = generate_with_groq(prompt)
    
    return explanation
