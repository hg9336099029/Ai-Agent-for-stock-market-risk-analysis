# Backend README

## AI Stock Risk Analysis Platform - Backend

Backend API for AI Stock & Portfolio Risk Analysis using FastAPI.

## Features

- **Deterministic Risk Calculation**: Uses proven financial models
- **Multi-Source News Verification**: Verifies news across sources
- **AI Explanations**: GenAI provides context, not decisions
- **RESTful API**: FastAPI with automatic OpenAPI documentation

## Setup

### 1. Create Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys if using OpenAI/Gemini
```

### 4. Run Server
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

- `GET /api/health` - Health check
- `POST /api/analyze/stock` - Analyze single stock
- `POST /api/analyze/portfolio` - Analyze portfolio

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── api/              # API endpoints
│   ├── risk_engine/      # Risk calculations
│   ├── news_rag/         # News retrieval & verification
│   ├── ai/               # AI explanation generation
│   ├── data_sources/     # Data fetching
│   ├── models/           # Pydantic models
│   └── utils/            # Utilities
├── requirements.txt
└── .env.example
```

## Notes

- Uses functional programming (no classes)
- All risk calculations are deterministic
- AI only generates explanations
- Includes caching for better performance
