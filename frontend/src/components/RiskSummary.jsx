/**
 * RiskSummary Component
 * Displays overall risk score with visual indicator
 */

const RiskSummary = ({ riskScore, symbol }) => {
    const getRiskLevel = (score) => {
        if (score >= 7) return { label: 'High Risk', color: 'text-red-600', bg: 'bg-red-100' };
        if (score >= 4) return { label: 'Medium Risk', color: 'text-yellow-600', bg: 'bg-yellow-100' };
        return { label: 'Low Risk', color: 'text-green-600', bg: 'bg-green-100' };
    };

    const risk = getRiskLevel(riskScore);

    return (
        <div className={`${risk.bg} rounded-lg p-6 shadow-md`}>
            <h2 className="text-2xl font-bold mb-2 text-yellow-600">{symbol}</h2>
            <div className="flex items-center justify-between">
                <div>
                    <p className="text-gray-600 text-sm mb-1">Overall Risk Score</p>
                    <p className={`text-5xl font-bold ${risk.color}`}>
                        {typeof riskScore === 'number' ? riskScore.toFixed(1) : 'N/A'}<span className="text-2xl">/10</span>
                    </p>
                </div>
                <div className={`px-6 py-3 rounded-full ${risk.color} font-bold text-lg`}>
                    {risk.label}
                </div>
            </div>
        </div>
    );
};

export default RiskSummary;
