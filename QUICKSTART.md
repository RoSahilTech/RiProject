# ⚡ Quick Start Guide

## 🚀 Fastest Way to Get Running

### Windows

1. **Open PowerShell in project folder**

2. **Backend Setup (one-time):**
   ```powershell
   cd backend
   python -m venv venv
   .\venv\Scripts\activate
   pip install -r requirements.txt
   python train_model.py
   python app.py
   ```

3. **Frontend Setup (new terminal):**
   ```powershell
   cd frontend
   npm install
   npm start
   ```

### Linux/Mac

1. **Backend Setup:**
   ```bash
   cd backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python train_model.py
   python app.py
   ```

2. **Frontend Setup (new terminal):**
   ```bash
   cd frontend
   npm install
   npm start
   ```

## ✅ Verify It Works

1. Backend should show: `Uvicorn running on http://0.0.0.0:8000`
2. Frontend should open: `http://localhost:3000`
3. Click "Run AI Prediction" button
4. Map should show colored markers

## 🎭 Demo Mode

1. Toggle **"Demo Mode"** checkbox
2. Watch live updates every 3 seconds
3. Risk levels change automatically

## 🐛 Common Issues

**"Model not found"**: Run `python train_model.py` first

**"Port in use"**: 
- Change port in `app.py` or kill process using port 8000/3000

**"npm install fails"**: 
- Delete `node_modules` folder and try again

**"Module not found"**: 
- Make sure virtual environment is activated
- Run `pip install -r requirements.txt` again

---

**Need more help?** See full README.md

