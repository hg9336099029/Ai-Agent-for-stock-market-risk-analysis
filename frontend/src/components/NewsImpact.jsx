/**
 * NewsImpact Component
 * Displays news impact with confidence levels
 */

import ConfidenceBadge from './ConfidenceBadge';

const NewsImpact = ({ newsData, explanation }) => {
    if (!newsData || newsData.length === 0) {
        return (
            <div className="bg-white rounded-lg p-6 shadow-md">
                <h3 className="text-xl font-bold mb-4">News Impact</h3>
                <p className="text-gray-500">No recent news available</p>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-lg p-6 shadow-md">
            <h3 className="text-xl font-bold mb-4">News Impact</h3>

            {/* AI-Generated Explanation */}
            {explanation && (
                <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
                    <h4 className="text-sm font-semibold text-blue-900 mb-2">AI Risk Explanation</h4>
                    <p className="text-sm text-blue-800 whitespace-pre-wrap">{explanation}</p>
                </div>
            )}

            {/* News Items */}
            <div className="space-y-4">
                {newsData.map((news, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition">
                        <div className="flex justify-between items-start mb-2">
                            <h4 className="font-semibold text-gray-900 flex-1">{news.title}</h4>
                            <ConfidenceBadge confidence={news.confidence} />
                        </div>
                        <p className="text-sm text-gray-600 mb-2">{news.summary}</p>
                        <div className="flex justify-between items-center text-xs text-gray-500">
                            <span>Source: {news.source}</span>
                            <span>{new Date(news.published_at).toLocaleDateString()}</span>
                        </div>
                    </div>
                ))}
            </div>

            {/* Verification Note */}
            <div className="mt-4 bg-yellow-50 border border-yellow-200 rounded p-3">
                <p className="text-xs text-yellow-800">
                    <strong>Note:</strong> News confidence is based on multi-source verification.
                    Low confidence news is shown for awareness but does not significantly impact risk scores.
                </p>
            </div>
        </div>
    );
};

export default NewsImpact;
