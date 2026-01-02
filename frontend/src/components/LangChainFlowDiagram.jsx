/**
 * LangChainFlowDiagram Component
 * Visual representation of LangChain-powered search and analysis flow
 */

const LangChainFlowDiagram = ({ isAnalyzing = false, currentChain = 0 }) => {
    const chains = [
        {
            id: 1,
            title: 'Input Processing',
            icon: '📝',
            description: 'Parse and validate stock symbol or portfolio',
            langchainComponent: 'PromptTemplate',
            status: currentChain >= 1 ? 'complete' : 'pending'
        },
        {
            id: 2,
            title: 'Data Retrieval Chain',
            icon: '🔍',
            description: 'Fetch market data via DuckDuckGo search',
            langchainComponent: 'RetrievalQA + DuckDuckGo',
            status: currentChain >= 2 ? 'complete' : 'pending'
        },
        {
            id: 3,
            title: 'Risk Calculation Agent',
            icon: '🧮',
            description: 'Calculate beta, volatility, and financial metrics',
            langchainComponent: 'Agent + Tools',
            status: currentChain >= 3 ? 'complete' : 'pending'
        },
        {
            id: 4,
            title: 'News Verification Chain',
            icon: '📰',
            description: 'RAG pipeline with Groq verification',
            langchainComponent: 'RAG Chain + Groq',
            status: currentChain >= 4 ? 'complete' : 'pending'
        },
        {
            id: 5,
            title: 'LLM Explanation',
            icon: '🤖',
            description: 'Generate context-aware risk explanation',
            langchainComponent: 'LLMChain (Groq)',
            status: currentChain >= 5 ? 'complete' : 'pending'
        },
        {
            id: 6,
            title: 'Response Formatting',
            icon: '📊',
            description: 'Structure and return analysis results',
            langchainComponent: 'OutputParser',
            status: currentChain >= 6 ? 'complete' : 'pending'
        }
    ];

    const getStatusColor = (status) => {
        if (status === 'complete') return 'bg-green-500 border-green-600';
        if (status === 'active') return 'bg-blue-500 border-blue-600 animate-pulse';
        return 'bg-gray-200 border-gray-300';
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-4">
                <h3 className="text-xl font-bold text-gray-900 flex items-center gap-2">
                    <span className="text-2xl">⛓️</span>
                    LangChain Analysis Pipeline
                </h3>
                {isAnalyzing && (
                    <span className="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-semibold animate-pulse">
                        Processing...
                    </span>
                )}
            </div>

            <div className="space-y-3">
                {chains.map((chain, index) => (
                    <div key={chain.id} className="relative">
                        {/* Chain Card */}
                        <div className={`border-2 rounded-lg p-4 transition-all duration-300 ${chain.status === 'complete'
                                ? 'border-green-500 bg-green-50'
                                : chain.status === 'active'
                                    ? 'border-blue-500 bg-blue-50'
                                    : 'border-gray-300 bg-white'
                            }`}>
                            <div className="flex items-start gap-4">
                                {/* Status Indicator */}
                                <div className={`flex-shrink-0 w-10 h-10 rounded-full flex items-center justify-center font-bold text-white ${getStatusColor(chain.status)}`}>
                                    {chain.status === 'complete' ? '✓' : chain.id}
                                </div>

                                {/* Content */}
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className="text-2xl">{chain.icon}</span>
                                        <h4 className="font-bold text-gray-900">{chain.title}</h4>
                                    </div>
                                    <p className="text-sm text-gray-600 mb-2">{chain.description}</p>

                                    {/* LangChain Component Badge */}
                                    <div className="inline-flex items-center gap-1 px-2 py-1 bg-purple-100 text-purple-800 rounded text-xs font-mono">
                                        <span className="text-purple-600">⛓️</span>
                                        {chain.langchainComponent}
                                    </div>
                                </div>

                                {/* Animation for active state */}
                                {chain.status === 'active' && (
                                    <div className="flex-shrink-0">
                                        <div className="w-6 h-6 border-4 border-blue-600 border-t-transparent rounded-full animate-spin"></div>
                                    </div>
                                )}
                            </div>
                        </div>

                        {/* Connector Arrow */}
                        {index < chains.length - 1 && (
                            <div className="flex justify-center my-1">
                                <div className={`text-2xl transition-colors ${chain.status === 'complete' ? 'text-green-500' : 'text-gray-300'
                                    }`}>
                                    ↓
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>

            {/* LangChain Architecture Info */}
            <div className="mt-6 pt-4 border-t border-gray-200">
                <details className="cursor-pointer">
                    <summary className="text-sm font-semibold text-gray-700 hover:text-blue-600">
                        📚 LangChain Architecture Details
                    </summary>
                    <div className="mt-3 space-y-2 text-xs text-gray-600 bg-gray-50 p-3 rounded">
                        <p><strong>PromptTemplate:</strong> Structures user input for downstream chains</p>
                        <p><strong>RetrievalQA + DuckDuckGo:</strong> Fetches real news using web search</p>
                        <p><strong>Agent + Tools:</strong> Executes risk calculations using deterministic tools</p>
                        <p><strong>RAG Chain + Groq:</strong> Verifies news credibility with LLM</p>
                        <p><strong>LLMChain:</strong> Groq-powered explanation generation</p>
                        <p><strong>OutputParser:</strong> Formats response into structured JSON</p>
                    </div>
                </details>
            </div>

            {/* Performance Metrics */}
            {isAnalyzing && currentChain > 0 && (
                <div className="mt-4 grid grid-cols-3 gap-2 text-center">
                    <div className="bg-blue-50 rounded p-2">
                        <div className="text-xs text-gray-600">Chains Complete</div>
                        <div className="text-lg font-bold text-blue-600">{currentChain}/6</div>
                    </div>
                    <div className="bg-purple-50 rounded p-2">
                        <div className="text-xs text-gray-600">LLM Calls</div>
                        <div className="text-lg font-bold text-purple-600">1</div>
                    </div>
                    <div className="bg-green-50 rounded p-2">
                        <div className="text-xs text-gray-600">Progress</div>
                        <div className="text-lg font-bold text-green-600">{Math.round((currentChain / 6) * 100)}%</div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default LangChainFlowDiagram;
