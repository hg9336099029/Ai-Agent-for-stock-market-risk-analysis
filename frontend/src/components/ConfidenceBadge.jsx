/**
 * ConfidenceBadge Component
 * Displays confidence level for news verification
 */

const ConfidenceBadge = ({ confidence }) => {
    const getConfidenceColor = (level) => {
        if (level >= 0.8) return 'bg-green-500 text-black';
        if (level >= 0.5) return 'bg-yellow-500 text-black';
        return 'bg-red-500 text-black';
    };

    const getConfidenceLabel = (level) => {
        if (level >= 0.8) return 'High Confidence';
        if (level >= 0.5) return 'Medium Confidence';
        return 'Low Confidence';
    };

    return (
        <span className={`px-3 py-1 rounded-full text-sm font-semibold ${getConfidenceColor(confidence)}`}>
            {getConfidenceLabel(confidence)} ({(confidence * 100).toFixed(0)}%)
        </span>
    );
};

export default ConfidenceBadge;
