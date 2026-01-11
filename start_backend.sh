#!/bin/bash

echo "========================================"
echo "Starting Delhi Flood Prediction Backend"
echo "========================================"
echo

cd backend

if [ ! -d "venv" ]; then
    echo "Virtual environment not found!"
    echo "Please run setup first:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    exit 1
fi

echo "Activating virtual environment..."
source venv/bin/activate

if [ ! -f "models/random_forest_model.pkl" ]; then
    echo "Models not found! Training models first..."
    python train_model.py
    echo
fi

echo "Starting FastAPI server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo
python app.py
