#!/bin/bash

echo "========================================"
echo "Delhi Flood Prediction - Setup Script"
echo "========================================"
echo

echo "[1/4] Creating backend models directory..."
mkdir -p backend/models
echo "Done!"

echo
echo "[2/4] Backend Setup"
echo "Creating virtual environment..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "Training ML model..."
python train_model.py
cd ..
echo "Backend setup complete!"

echo
echo "[3/4] Frontend Setup"
cd frontend
npm install
cd ..
echo "Frontend setup complete!"

echo
echo "[4/4] Setup Complete!"
echo
echo "To start the system:"
echo "  Terminal 1 (Backend):"
echo "    cd backend"
echo "    source venv/bin/activate"
echo "    python app.py"
echo
echo "  Terminal 2 (Frontend):"
echo "    cd frontend"
echo "    npm start"
echo
echo "========================================"
echo "Setup complete! Ready to run."
echo "========================================"

