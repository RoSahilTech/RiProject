# 🔧 Proxy Error Fix - ECONNREFUSED

## Problem
```
Proxy error: Could not proxy request /favicon.ico from localhost:3000 to http://localhost:8000.
ECONNREFUSED
```

**Cause**: The FastAPI backend server is not running on port 8000.

## ✅ Solution Applied

### 1. **Improved Error Handling**
- Added timeout to API calls (3-5 seconds)
- Better error messages in console
- Graceful fallback when backend is unavailable

### 2. **Better Fallback Data**
- Frontend now works even when backend is offline
- Shows realistic sample data
- Predictions work with rule-based fallback

### 3. **Easy Startup Scripts**
- `start_backend.bat` (Windows) - Double-click to start backend
- `start_backend.sh` (Linux/Mac) - Run to start backend

## 🚀 How to Fix Right Now

### Quick Fix (Windows):
```bash
# Open a new terminal/command prompt
cd backend
venv\Scripts\activate
python app.py
```

### Quick Fix (Mac/Linux):
```bash
cd backend
source venv/bin/activate
python app.py
```

### Or Use the Script:
- **Windows**: Double-click `start_backend.bat`
- **Linux/Mac**: Run `bash start_backend.sh`

## ✅ Verify It's Working

Once the backend starts, you should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Then refresh your browser at `http://localhost:3000`

## 📝 What Changed

1. **frontend/src/App.js**:
   - Added timeout to API calls
   - Better error handling with warnings instead of errors
   - Improved fallback data generation
   - Helper message in console if backend is offline

2. **New Files**:
   - `start_backend.bat` - Easy Windows startup
   - `start_backend.sh` - Easy Linux/Mac startup
   - `START_HERE.md` - Complete setup guide
   - `PROXY_ERROR_FIX.md` - This file

## 💡 Pro Tips

### For Competition Demo:
1. **Terminal 1**: Start backend (`python app.py`)
2. **Terminal 2**: Start frontend (`npm start`)
3. Both should run simultaneously

### If Port 8000 is Busy:
Change port in `backend/app.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)
```

Then update `frontend/src/App.js`:
```javascript
const API_BASE = 'http://localhost:8001';
```

## 🎯 Current Status

✅ Frontend now handles backend unavailability gracefully  
✅ Better error messages  
✅ Easy startup scripts created  
✅ Fallback data works for demo purposes  

**The proxy error will disappear once you start the backend server!**
