@echo off
echo ========================================
echo Starting Delhi Flood Prediction Backend
echo ========================================
echo.

cd backend

if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found!
    echo Please run setup first:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

if not exist "models\random_forest_model.pkl" (
    echo Models not found! Training models first...
    python train_model.py
    echo.
)

echo Starting FastAPI server on http://localhost:8000
echo Press Ctrl+C to stop
echo.
python app.py

pause
