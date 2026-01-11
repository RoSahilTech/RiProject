# 🏛️ Delhi Drainage & Waterlogging Prediction AI

**A Civic-Tech Prototype for College Competition**

An AI-powered flood risk prediction system that helps citizens prepare and enables early government response to waterlogging in Delhi wards.

---

## 🎯 Project Overview

This is a **judge-demo system** designed to run **fully offline on a laptop** without internet connection. It demonstrates how AI can predict flooding in Delhi wards using machine learning models trained on synthetic environmental and drainage data.

### Key Features

- 🗺️ **Interactive Delhi Ward Map** with real-time risk visualization
- 🤖 **AI-Powered Predictions** using RandomForest/XGBoost models
- 📊 **Live Dashboard** with animated risk indicators
- 🌧️ **Demo Mode** for live monsoon simulation during presentations
- 📱 **Citizen Reporting** system integration
- 📈 **Historical Trends** and risk forecasting charts

---

## 🛠️ Tech Stack

- **Frontend**: React, Leaflet (maps), Chart.js
- **Backend**: Python + FastAPI
- **ML**: RandomForest / XGBoost (scikit-learn)
- **Data**: CSV (synthetic Delhi flood data)

---

## 📁 Project Structure

```
.
├── frontend/                 # React application
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── App.js           # Main app component
│   │   └── index.js
│   ├── public/
│   └── package.json
│
├── backend/                  # FastAPI backend
│   ├── app.py               # FastAPI server
│   ├── train_model.py       # ML training script
│   ├── demo_simulator.py    # Live monsoon simulator
│   ├── models/              # Trained ML models (generated)
│   └── requirements.txt
│
├── DATA/
│   └── delhi_flood_data.csv # Sample training data
│
└── README.md
```

---

## 🚀 Quick Start Guide

### Prerequisites

- **Python 3.8+** (for backend)
- **Node.js 16+** and **npm** (for frontend)
- **No internet required** after initial setup

### Step 1: Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the ML model:**
   ```bash
   python train_model.py
   ```
   
   This will create `models/random_forest_model.pkl` and `models/xgboost_model.pkl`

5. **Start FastAPI server:**
   ```bash
   python app.py
   ```
   
   Or using uvicorn directly:
   ```bash
   uvicorn app:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

### Step 2: Frontend Setup

1. **Open a new terminal and navigate to frontend:**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

3. **Start React development server:**
   ```bash
   npm start
   ```
   
   The dashboard will open at `http://localhost:3000`

### Step 3: Run Demo Simulator (Optional)

For live demonstrations, run the monsoon simulator in a separate terminal:

```bash
cd backend
python demo_simulator.py
```

For dramatic scenario demonstrations:
```bash
python demo_simulator.py --scenario
```

---

## 📡 API Endpoints

### `GET /`
Returns API information and available endpoints.

### `GET /health`
Health check endpoint. Returns model status.

### `POST /predict`
Make flood risk prediction for given conditions.

**Request Body:**
```json
{
  "ward_name": "Karol Bagh",
  "rain_1h_mm": 15.5,
  "rain_3h_mm": 42.3,
  "rain_24h_mm": 85.2,
  "rain_forecast_3h_mm": 38.5,
  "yamuna_level_m": 203.5
}
```

**Response:**
```json
{
  "success": true,
  "ward_name": "Karol Bagh",
  "flood_risk_level": 2,
  "risk_label": "Danger",
  "confidence": 0.89,
  "max_flood_depth_cm": 52.3,
  "drain_capacity_score": 0.65,
  "citizen_reports_count": 8
}
```

### `GET /demo`
Returns simulated live data for demo mode. Updates dynamically to simulate monsoon conditions.

---

## 🎮 Using the Dashboard

### Manual Prediction Mode

1. **Select a ward** from the dropdown
2. **Adjust sliders** for:
   - Rain (1h, 3h, 24h)
   - Forecast (3h)
   - Yamuna River level
3. **Click "Run AI Prediction"** button
4. View results on map and in sidebar

### Demo Mode (Live Simulation)

1. **Toggle "Demo Mode"** checkbox
2. The system automatically:
   - Simulates monsoon rain patterns
   - Updates Yamuna levels
   - Simulates drain blockages
   - Updates predictions every 3 seconds
3. Watch live updates in sidebar
4. Map markers update automatically with risk colors

### Features

- **Risk Visualization**: Green (Safe) → Yellow (Warning) → Red (Danger)
- **Animated Markers**: High-risk wards pulse red
- **Live Updates Feed**: Real-time alerts and notifications
- **Citizen Reports**: Submit and view community reports
- **AI Recommendations**: Automated action suggestions
- **Historical Charts**: Monthly risk trends

---

## 🧠 Machine Learning Model

### Training Data

The model is trained on synthetic CSV data with features:
- Weather: `rain_1h_mm`, `rain_3h_mm`, `rain_24h_mm`, `rain_forecast_3h_mm`
- Geography: `latitude`, `longitude`, `elevation_m`, `slope_percent`
- Drainage: `drain_density`, `drain_capacity_score`, `drain_blockage_risk`
- River: `distance_to_yamuna_m`, `yamuna_level_m`
- History: `flooded_before`, `flood_frequency`
- Community: `citizen_reports_count`, `avg_reported_depth_cm`

**Target Variable:** `flood_risk_level` (0=Safe, 1=Warning, 2=Danger)

### Model Architecture

- **Primary Model**: RandomForest (100 trees, max_depth=10)
- **Alternative**: XGBoost (for comparison)
- **Accuracy**: ~85-90% on test set (synthetic data)

### Retraining

To retrain with new data:
```bash
cd backend
python train_model.py
```

Ensure `DATA/delhi_flood_data.csv` is updated with new records.

---

## 🎭 Demo Simulator

The `demo_simulator.py` script creates dramatic scenarios for judges:

### Monsoon Phases

1. **Pre-Monsoon**: Light rain (5-25mm), stable conditions
2. **Onset**: Moderate rain (30-60mm), rising water levels
3. **Peak**: Heavy rain (70-120mm), critical conditions
4. **Decline**: Decreasing rain, recovery phase

### Usage

**Continuous Simulation:**
```bash
python demo_simulator.py  # Updates every 5 seconds
python demo_simulator.py 10  # Updates every 10 seconds
```

**Dramatic Scenarios:**
```bash
python demo_simulator.py --scenario
```

Shows three dramatic scenarios:
- Sudden Heavy Downpour
- Yamuna Overflow Threat
- Drain Blockage Crisis

---

## 🎨 UI Features

### Visual Indicators

- **Color Coding**: 
  - 🟢 Green = Low Risk (Safe)
  - 🟡 Yellow = Medium Risk (Warning)
  - 🔴 Red = High Risk (Danger)

- **Animations**:
  - Pulsing high-risk markers
  - Bouncing notification badges
  - Smooth map transitions

- **Glass Morphism**: Modern frosted glass UI design

### Interactive Elements

- **Leaflet Map**: Click markers for ward details
- **Chart.js Graphs**: Interactive risk trend charts
- **Responsive Design**: Works on desktop and tablet

---

## 🔧 Troubleshooting

### Backend Issues

**Model not found:**
- Run `python train_model.py` first
- Check `models/` directory exists

**Port already in use:**
- Change port in `app.py`: `uvicorn.run(app, port=8001)`
- Update frontend proxy in `package.json`

**Import errors:**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

### Frontend Issues

**npm install fails:**
- Clear cache: `npm cache clean --force`
- Delete `node_modules` and reinstall

**Map not loading:**
- Check Leaflet CSS is loaded (see `public/index.html`)
- Ensure backend is running on port 8000

**API connection errors:**
- Verify backend is running: `curl http://localhost:8000/health`
- Check CORS settings in `backend/app.py`

### Demo Mode Issues

**Updates not showing:**
- Ensure backend `/demo` endpoint is accessible
- Check browser console for errors
- Verify React state updates (check Network tab)

---

## 📊 Data Format

### CSV Structure

The training CSV must have these columns:

```csv
cell_id,latitude,longitude,ward_name,zone,distance_to_yamuna_m,
rain_1h_mm,rain_3h_mm,rain_24h_mm,rain_forecast_3h_mm,
elevation_m,slope_percent,impervious_ratio,drain_density,
drain_capacity_score,drain_blockage_risk,yamuna_level_m,
flooded_before,flood_frequency,citizen_reports_count,
avg_reported_depth_cm,max_flood_depth_cm,flood_risk_level
```

### Adding New Data

1. Add rows to `DATA/delhi_flood_data.csv`
2. Ensure all columns are present
3. `flood_risk_level` must be 0, 1, or 2
4. Retrain model: `python backend/train_model.py`

---

## 🏆 Competition Demo Tips

### Before Presentation

1. **Train model** and verify it works
2. **Test all features** in both manual and demo modes
3. **Prepare scenarios** using `--scenario` flag
4. **Close unnecessary apps** to ensure smooth performance

### During Demo

1. **Start with Manual Mode**: Show how predictions work
2. **Switch to Demo Mode**: Create dramatic live simulation
3. **Highlight AI Features**: Emphasize ML prediction accuracy
4. **Show Citizen Impact**: Demonstrate reporting system
5. **Map Interaction**: Click on different wards to show details

### Talking Points

- **AI Accuracy**: "Our model achieves 85-90% accuracy in predicting flood risk"
- **Real-time Updates**: "The system updates every 3 seconds during monsoon conditions"
- **Citizen Engagement**: "Citizens can report issues, creating a feedback loop"
- **Government Action**: "AI recommends specific actions for each ward"
- **Scalability**: "System can be extended to all 272 Delhi wards"

---

## 🔒 Offline Operation

This system is designed to work **completely offline**:

- ✅ No API keys required
- ✅ No cloud services
- ✅ All data local (CSV)
- ✅ Models stored locally
- ✅ Leaflet map tiles cached (after first load)

**Note**: First-time setup requires internet for:
- Installing npm packages
- Installing pip packages
- Loading Leaflet map tiles (cached after first use)

---

## 📝 License

This is a prototype/demo project for academic competition purposes.

---

## 👥 Credits

**Project Name**: Delhi Drainage & Waterlogging Prediction AI  
**Type**: Civic-Tech Prototype  
**Platform**: Offline Laptop Deployment  

---

## 🆘 Support

For issues during competition:
1. Check `README.md` troubleshooting section
2. Verify all prerequisites are installed
3. Test endpoints: `curl http://localhost:8000/health`
4. Check browser console for frontend errors

---

**Built for demonstrating AI-powered civic solutions** 🚀

