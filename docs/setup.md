# WiFi Human Detection Setup Guide

## Prerequisites

- **Python 3.11+**
- **Node.js 18+**
- **Docker & Docker Compose** (optional, for containerized setup)
- **Git**

## Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone the repository
git clone https://github.com/Student-Cybrarians/Human-Detection.git
cd Human-Detection

# Start all services
docker-compose up

# Access the application
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Setup

#### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp ../.env.example .env

# Run tests
python -m pytest test_api.py -v

# Start server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

#### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
echo "VITE_API_URL=http://localhost:8000" > .env.local

# Start development server
npm run dev

# Access at http://localhost:5173
```

#### 3. Train Models (Optional)

```bash
cd model

# Install dependencies
pip install numpy scikit-learn tensorflow joblib

# Train ANN and CNN models
python train_models.py

# Models will be saved in model/trained/
```

## Configuration

### Backend Environment Variables

Create `backend/.env`:

```env
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_ENV=development
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
SIGNAL_SAMPLING_RATE=1000
MODEL_PATH=./models/trained
CONFIDENCE_THRESHOLD=0.7
```

### Frontend Environment Variables

Create `frontend/.env.local`:

```env
VITE_API_URL=http://localhost:8000
```

## Project Structure

```
Human-Detection/
├── backend/                 # FastAPI backend
│   ├── main.py             # API endpoints
│   ├── requirements.txt     # Python dependencies
│   ├── test_api.py          # Unit tests
│   └── Dockerfile           # Docker config
├── frontend/               # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx          # Main component
│   │   ├── pages/           # Page components
│   │   └── index.css        # Global styles
│   ├── package.json         # NPM dependencies
│   ├── vite.config.js       # Vite config
│   └── Dockerfile           # Docker config
├── model/                  # ML models
│   ├── train_models.py      # Training script
│   └── trained/             # Saved models
├── .github/workflows/       # CI/CD workflows
├── docker-compose.yml       # Docker compose config
├── setup.sh                 # Setup script
└── README.md                # Project documentation
```

## Development Commands

### Backend

```bash
cd backend

# Run development server with auto-reload
python -m uvicorn main:app --reload

# Run tests
python -m pytest test_api.py -v

# Check API health
curl http://localhost:8000/health

# View API documentation
# http://localhost:8000/docs
```

### Frontend

```bash
cd frontend

# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Models

```bash
cd model

# Train new models
python train_models.py

# Results saved in model/trained/
```

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process using port
kill -9 <PID>

# Or change port in .env
BACKEND_PORT=8001
```

### Frontend can't connect to backend

```bash
# Check VITE_API_URL in frontend/.env.local
# Should match backend URL

# In development:
VITE_API_URL=http://localhost:8000

# On production:
VITE_API_URL=https://your-backend-url.com
```

### Docker issues

```bash
# Clean up containers
docker-compose down

# Rebuild images
docker-compose build --no-cache

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Testing

### Backend Tests

```bash
cd backend
python -m pytest test_api.py -v
```

### API Testing

```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"signal_id":"test_001","duration":1.0,"sampling_rate":1000}'

# Get signal data
curl http://localhost:8000/signal/demo_signal?duration=1.0
```

## Deployment

See `docs/deployment.md` for deployment instructions.

## Support

For issues or questions:
- Check existing GitHub Issues
- Create a new Issue with details
- Check project documentation in `/docs`

## License

MIT License - See LICENSE file for details
