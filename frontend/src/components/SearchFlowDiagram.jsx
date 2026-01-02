/**
 * SearchFlowDiagram Component
 * Visual representation of the analysis process
 */

const SearchFlowDiagram = ({ currentStep = 0 }) => {
    const steps = [
        { id: 1, title: 'Input Stock/Portfolio', icon: '📝', description: 'Enter ticker symbol or portfolio holdings' },
        { id: 2, title: 'Validate & Send', icon: '✅', description: 'Frontend validates and sends request to backend' },
        { id: 3, title: 'Market Risk Analysis', icon: '📊', description: 'Calculate beta, volatility, correlation' },
        { id: 4, title: 'Financial Risk Analysis', icon: '💰', description: 'Analyze debt, coverage, earnings stability' },
        { id: 5, title: 'News Verification', icon: '📰', description: 'Multi-source news retrieval and verification' },
        { id: 6, title: 'AI Explanation', icon: '🤖', description: 'Generate human-readable risk explanation' },
        { id: 7, title: 'Display Results', icon: '📈', description: 'Show risk score, breakdown, and news impact' }
    ];

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-bold mb-4 text-center">Analysis Process Flow</h3>

            <div className="space-y-3">
                {steps.map((step, index) => (
                    <div key={step.id} className="flex items-start gap-4">
                        {/* Step Number Circle */}
                        <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold ${currentStep >= step.id
                                ? 'bg-blue-600 text-white'
                                : 'bg-gray-200 text-gray-600'
                            }`}>
                            {step.id}
                        </div>

                        {/* Step Content */}
                        <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                                <span className="text-2xl">{step.icon}</span>
                                <h4 className={`font-semibold ${currentStep >= step.id ? 'text-blue-900' : 'text-gray-700'
                                    }`}>
                                    {step.title}
                                </h4>
                            </div>
                            <p className="text-sm text-gray-600">{step.description}</p>
                        </div>

                        {/* Connector Line */}
                        {index < steps.length - 1 && (
                            <div className="absolute left-5 w-0.5 h-8 bg-gray-300 ml-5 mt-10" />
                        )}
                    </div>
                ))}
            </div>

            {/* Legend */}
            <div className="mt-6 pt-4 border-t border-gray-200">
                <div className="flex items-center justify-center gap-6 text-sm">
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded-full bg-blue-600"></div>
                        <span className="text-gray-600">Processing Steps</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <div className="w-4 h-4 rounded-full bg-gray-200"></div>
                        <span className="text-gray-600">Pending Steps</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default SearchFlowDiagram;
