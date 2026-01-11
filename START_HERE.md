# 🚀 Quick Start Guide

## The Error You're Seeing

```
Proxy error: Could not proxy request ... to http://localhost:8000
ECONNREFUSED
```

**This means the backend server is not running!**

## ✅ Fix: Start the Backend Server

### Option 1: Windows (Double-click)
- Double-click `start_backend.bat` in the project root

### Option 2: Manual Start (Windows)
```bash
cd backend
venv\Scripts\activate
python app.py
```

### Option 3: Manual Start (Linux/Mac)
```bash
cd backend
source venv/bin/activate
python app.py
```

## 🎯 Complete Setup (First Time)

### 1. Backend Setup
```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate

pip install -r requirements.txt
python train_model.py  # Train ML models
python app.py           # Start server
```

### 2. Frontend Setup (New Terminal)
```bash
cd frontend
npm install
npm start
```

## ✅ Verify It's Working

Once backend starts, you should see:
```
Uvicorn running on http://0.0.0.0:8000
```

Then refresh your frontend at `http://localhost:3000`

## 🔧 Troubleshooting

**"Module not found" errors:**
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

**"Model not found" errors:**
- Run `python train_model.py` first

**Port 8000 already in use:**
- Kill the process using port 8000
- Or change port in `backend/app.py`: `uvicorn.run(app, port=8001)`
- Update `frontend/src/App.js`: `const API_BASE = 'http://localhost:8001'`

## 💡 Pro Tip

For competition demo, run BOTH servers:
- **Terminal 1**: Backend (`python app.py`)
- **Terminal 2**: Frontend (`npm start`)

---

**The frontend will now work with fallback data if backend is offline!**
