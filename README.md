# AI Stock & Portfolio Risk Analysis Platform

Complete platform for analyzing stock and portfolio risk using deterministic financial models with AI-powered explanations via Groq.

## 🚀 Quick Start Guide

### Prerequisites
- Python 3.10+ (for backend)
- Node.js 18+ (for frontend)
- Groq API Key (free at https://console.groq.com)

### 1. Clone/Navigate to Project
```bash
cd ai-stock-risk-platform
```

### 2. Setup Backend

```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY

# Run backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

### 3. Setup Frontend (New Terminal)

```bash
cd frontend

# Install dependencies (if not done)
npm install

# Run frontend dev server
npm run dev
```

Frontend will be available at: http://localhost:5174

### 4. Access the Application

- **Frontend UI**: http://localhost:5174
- **Backend API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## 📋 Features

### Backend (Python + FastAPI)
- ✅ **Deterministic Risk Calculation**
  - Market Risk: Beta, Volatility, Correlation
  - Financial Risk: Debt-to-Equity, Interest Coverage, Earnings Variability
  - Portfolio Risk: Correlation Matrix, Concentration, Diversification

- ✅ **News Verification (RAG)**
  - Multi-source news retrieval
  - Cross-source verification
  - Confidence scoring

- ✅ **AI Explanations (Groq)**
  - Groq Llama 3.1 70B model
  - Context-aware risk explanations
  - No AI in risk calculations

### Frontend (React + Vite + Tailwind)
- ✅ **Stock Analysis**
  - Autocomplete stock suggestions
  - Real-time risk analysis
  - Visual risk breakdown

- ✅ **Portfolio Analysis**
  - Dynamic holdings management
  - Weighted risk scores
  - Diversification metrics

- ✅ **Rich UI**
  - Color-coded risk levels
  - Interactive flow diagrams
  - News confidence badges

## 🔧 Configuration

### Backend `.env`
```bash
# Groq API
GROQ_API_KEY=gsk_your_groq_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
GROQ_TEMPERATURE=0.3

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Risk Thresholds (customize as needed)
BETA_HIGH=1.5
VOLATILITY_HIGH=0.3
DEBT_EQUITY_HIGH=2.0
```

### Frontend `.env.local`
```bash
VITE_API_URL=http://localhost:8000/api
VITE_ENV=development
```

## 🧪 Testing

### Test Backend API
```bash
# Health check
curl http://localhost:8000/api/health

# Analyze AAPL stock
curl -X POST http://localhost:8000/api/analyze/stock \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL"}'

# Analyze portfolio
curl -X POST http://localhost:8000/api/analyze/portfolio \
  -H "Content-Type: application/json" \
  -d '{
    "holdings": [
      {"symbol": "AAPL", "weight": 0.5},
      {"symbol": "MSFT", "weight": 0.5}
    ]
  }'
```

## 📁 Project Structure

```
ai-stock-risk-platform/
├── backend/                  # FastAPI backend
│   ├── app/
│   │   ├── api/             # API endpoints
│   │   ├── risk_engine/     # Risk calculations
│   │   ├── news_rag/        # News verification
│   │   ├── ai/              # Groq integration
│   │   ├── data_sources/    # Market data
│   │   ├── models/          # Pydantic models
│   │   └── utils/           # Utilities
│   ├── requirements.txt
│   └── .env.example
│
└── frontend/                 # React frontend
    ├── src/
    │   ├── components/      # UI components
    │   ├── pages/           # Pages
    │   └── services/        # API client
    ├── package.json
    └── vite.config.js
```

## 🎯 Usage Flow

1. **User**: Opens frontend at http://localhost:5174
2. **Input**: Enters stock symbol (e.g., AAPL) or portfolio
3. **Frontend**: Sends POST to `/api/analyze/stock` or `/api/analyze/portfolio`
4. **Backend**: 
   - Fetches market data (yfinance)
   - Calculates risk metrics (deterministic)
   - Retrieves & verifies news
   - Generates explanation (Groq AI)
5. **Response**: Returns risk score + breakdown + news + explanation
6. **Display**: Frontend shows results with visualizations

## 🔐 Security Notes

- Never commit `.env` files
- Use environment variables for API keys
- In production, use proper CORS origins
- Add rate limiting for API endpoints
- Implement authentication if needed

## 🚨 Troubleshooting

### Backend Issues

**numpy install fails on Windows:**
```bash
# Use updated requirements.txt with numpy>=1.24.0
pip install --upgrade pip
pip install -r requirements.txt
```

**Groq API errors:**
- Check API key in `.env`
- Verify internet connection
- Check Groq API status

**Port 8000 already in use:**
```bash
# Change port in .env
API_PORT=8001

# Or kill the process using port 8000
```

### Frontend Issues

**Port 5174 in use:**
- Vite will automatically try next available port

**API connection refused:**
- Ensure backend is running on port 8000
- Check `VITE_API_URL` in `.env.local`

## 📚 Documentation

- **Backend API**: http://localhost:8000/docs (Swagger UI)
- **Backend ReDoc**: http://localhost:8000/redoc
- **Groq Docs**: https://console.groq.com/docs

## 🤝 Contributing

This is a production-thinking implementation with:
- Functional programming (no classes)
- Type hints throughout
- Comprehensive error handling
- Logging and caching
- Validation with Pydantic

## 📄 License

This project is for educational and demonstration purposes.

---

**Note**: This system provides decision support, not financial advice. Always consult with qualified financial advisors before making investment decisions.
