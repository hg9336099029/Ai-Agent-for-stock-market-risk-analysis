/**
 * RiskBreakdown Component
 * Displays detailed risk metrics breakdown
 */

const RiskBreakdown = ({ riskMetrics }) => {
    if (!riskMetrics) return null;

    const MetricCard = ({ title, value, description }) => (
        <div className="bg-white rounded-lg p-4 shadow border border-gray-200">
            <h3 className="text-sm font-semibold text-gray-600 mb-1">{title}</h3>
            <p className="text-2xl font-bold text-gray-900 mb-2">{value}</p>
            {description && <p className="text-xs text-gray-500">{description}</p>}
        </div>
    );

    return (
        <div className="bg-gray-50 rounded-lg p-6 shadow-md">
            <h3 className="text-xl font-bold mb-4">Risk Breakdown</h3>

            {/* Partial Data Warning */}
            {riskMetrics.partial_data && (
                <div className="mb-6 bg-orange-50 border-l-4 border-orange-500 p-4">
                    <div className="flex items-center">
                        <div className="flex-shrink-0">
                            <span className="text-xl">⚠️</span>
                        </div>
                        <div className="ml-3">
                            <h3 className="text-sm font-medium text-orange-800">
                                Limited Data Availability
                            </h3>
                            <div className="mt-2 text-sm text-orange-700">
                                <p>
                                    Real-time market data is currently rate-limited. Some metrics below are estimated or default values.
                                    please rely on the <strong>AI Risk Explanation</strong> for the most accurate current assessment.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Market Risk */}
            <div className="mb-6">
                <h4 className="text-lg font-semibold text-gray-700 mb-3">Market Risk</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <MetricCard
                        title="Beta"
                        value={riskMetrics.market_risk?.beta?.toFixed(2) || 'N/A'}
                        description="Volatility vs market"
                    />
                    <MetricCard
                        title="Volatility"
                        value={riskMetrics.market_risk?.volatility ? `${(riskMetrics.market_risk.volatility * 100).toFixed(1)}%` : 'N/A'}
                        description="Price fluctuation"
                    />
                    <MetricCard
                        title="Correlation"
                        value={riskMetrics.market_risk?.correlation?.toFixed(2) || 'N/A'}
                        description="Market correlation"
                    />
                </div>
            </div>

            {/* Financial Risk */}
            <div className="mb-6">
                <h4 className="text-lg font-semibold text-gray-700 mb-3">Financial Risk</h4>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <MetricCard
                        title="Debt-to-Equity"
                        value={riskMetrics.financial_risk?.debt_to_equity?.toFixed(2) || 'N/A'}
                        description="Leverage ratio"
                    />
                    <MetricCard
                        title="Interest Coverage"
                        value={riskMetrics.financial_risk?.interest_coverage?.toFixed(2) || 'N/A'}
                        description="Debt servicing ability"
                    />
                    <MetricCard
                        title="Earnings Variability"
                        value={riskMetrics.financial_risk?.earnings_variability?.toFixed(2) || 'N/A'}
                        description="Income stability"
                    />
                </div>
            </div>

            {/* Portfolio Risk (if available) */}
            {riskMetrics.portfolio_risk && (
                <div>
                    <h4 className="text-lg font-semibold text-gray-700 mb-3">Portfolio Risk</h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <MetricCard
                            title="Concentration Index"
                            value={riskMetrics.portfolio_risk?.concentration_index?.toFixed(3) || 'N/A'}
                            description="Portfolio concentration"
                        />
                        <MetricCard
                            title="Diversification Score"
                            value={riskMetrics.portfolio_risk?.diversification_score?.toFixed(2) || 'N/A'}
                            description="Diversification level"
                        />
                    </div>
                </div>
            )}
        </div>
    );
};

export default RiskBreakdown;
