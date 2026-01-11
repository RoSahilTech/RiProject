@echo off
echo ========================================
echo Delhi Flood Prediction - Setup Script
echo ========================================
echo.

echo [1/4] Creating backend models directory...
if not exist "backend\models" mkdir backend\models
echo Done!

echo.
echo [2/4] Backend Setup
echo Please run these commands in the backend directory:
echo   cd backend
echo   python -m venv venv
echo   venv\Scripts\activate
echo   pip install -r requirements.txt
echo   python train_model.py
echo.

echo [3/4] Frontend Setup
echo Please run these commands in the frontend directory:
echo   cd frontend
echo   npm install
echo.

echo [4/4] Starting Services
echo.
echo To start the backend:
echo   cd backend
echo   venv\Scripts\activate
echo   python app.py
echo.
echo To start the frontend (in a new terminal):
echo   cd frontend
echo   npm start
echo.
echo ========================================
echo Setup instructions complete!
echo ========================================
pause

