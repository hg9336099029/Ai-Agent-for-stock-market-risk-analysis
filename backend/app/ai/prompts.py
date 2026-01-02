"""
Prompt templates for GenAI risk explanation
"""

def get_stock_risk_prompt(symbol: str, risk_metrics: dict, news_context: list) -> str:
    """
    Generate prompt for stock risk explanation
    
    Args:
        symbol: Stock ticker symbol
        risk_metrics: Dictionary with all risk metrics
        news_context: List of verified news items
        
    Returns:
        Formatted prompt string
    """
    market_risk = risk_metrics.get("market_risk", {})
    financial_risk = risk_metrics.get("financial_risk", {})
    overall_score = risk_metrics.get("overall_score", 5.0)
    
    news_summary = "\n".join([
        f"- {news.get('title', '')} (Confidence: {news.get('confidence', 0):.0%})"
        for news in news_context[:3]  # Top 3 news items
    ])
    
    partial_data_note = ""
    if risk_metrics.get("partial_data"):
        partial_data_note = "\n**NOTE: Some risk metrics are based on default values or estimates due to data availability issues. Please note this uncertainty in your explanation and rely more on the news context and general knowledge of the company.**"

    prompt = f"""You are a financial risk analyst. Explain the risk profile for {symbol} in a clear, professional manner.

**Risk Score:** {overall_score:.1f}/10
{partial_data_note}

**Market Risk Metrics:**
- Beta: {market_risk.get('beta', 1.0):.2f}
- Volatility: {market_risk.get('volatility', 0.2):.2%}
- Market Correlation: {market_risk.get('correlation', 0.5):.2f}

**Financial Risk Metrics:**
- Debt-to-Equity: {financial_risk.get('debt_to_equity', 1.0):.2f}
- Interest Coverage: {financial_risk.get('interest_coverage', 5.0):.2f}
- Earnings Variability: {financial_risk.get('earnings_variability', 0.2):.2f}

Provide a structured explanation using the EXACT format below. You MUST use the dot character '•' for list items.

• ANALYSIS OF RISK SCORE: [Explain what the risk score indicates]
• MARKET RISK ANALYSIS: [Analyze Beta, Volatility, and Correlation. CITE THE SPECIFIC VALUES in your text.]
• FINANCIAL RISK ANALYSIS: [Analyze Debt/Equity and earnings stability. CITE THE SPECIFIC VALUES in your text.]
• KEY RISK FACTORS: [List other key operational or industry risks]
• NEWS IMPACT: [How recent news impacts the outlook]
• LIMITATIONS: [Important assumptions]

Use clear, professional language. Use the Unicode bullet (•) for lists. Do NOT use Markdown formatting (asterisks or hashes)."""
    
    return prompt

def get_portfolio_risk_prompt(holdings: list, risk_metrics: dict) -> str:
    """
    Generate prompt for portfolio risk explanation
    
    Args:
        holdings: List of portfolio holdings
        risk_metrics: Dictionary with portfolio metrics
        
    Returns:
        Formatted prompt string
    """
    overall_score = risk_metrics.get("overall_score", 5.0)
    portfolio_risk = risk_metrics.get("portfolio_risk", {})
    
    holdings_str = ", ".join([f"{h['symbol']} ({h['weight']:.0%})" for h in holdings])
    
    prompt = f"""You are a portfolio risk analyst. Explain the risk profile for this portfolio in a clear, professional manner.

**Portfolio Holdings:** {holdings_str}

**Overall Risk Score:** {overall_score:.1f}/10

**Portfolio Metrics:**
- Number of Holdings: {portfolio_risk.get('num_holdings', len(holdings))}
- Concentration Index (HHI): {portfolio_risk.get('concentration_index', 0.5):.3f}
- Diversification Score: {portfolio_risk.get('diversification_score', 2.0):.2f}

Provide a 2-3 paragraph explanation of:
1. Overall portfolio risk level
2. Diversification assessment
3. Concentration risks
4. Recommendations for risk management

Use clear, professional language."""
    
    return prompt
