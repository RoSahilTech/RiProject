"""
FastAPI Backend for Delhi Flood Risk Prediction
Provides /predict and /demo endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib
import pandas as pd
import numpy as np
import json
import os
from typing import Optional, Dict, Any
import random
from datetime import datetime, timedelta

app = FastAPI(title="Delhi Drainage & Waterlogging Prediction API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'random_forest_model.pkl')
FEATURE_COLS_PATH = os.path.join(BASE_DIR, 'models', 'feature_columns.json')
DATA_PATH = os.path.join(BASE_DIR, '..', 'DATA', 'delhi_flood_data.csv')

model = None
feature_cols = None
ward_data = None

def load_model():
    """Load trained model and feature columns"""
    global model, feature_cols, ward_data
    
    # Ensure models directory exists
    models_dir = os.path.dirname(MODEL_PATH)
    if not os.path.exists(models_dir):
        os.makedirs(models_dir, exist_ok=True)
    
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        print(f"Model loaded from {MODEL_PATH}")
    else:
        print(f"Warning: Model not found at {MODEL_PATH}. Using fallback predictions.")
        model = None
    
    if os.path.exists(FEATURE_COLS_PATH):
        with open(FEATURE_COLS_PATH, 'r') as f:
            feature_cols = json.load(f)
        print(f"Feature columns loaded: {len(feature_cols)} features")
    else:
        # Default feature columns (NO LEAKAGE FEATURES)
        feature_cols = [
            'distance_to_yamuna_m', 'rain_1h_mm', 'rain_3h_mm', 'rain_24h_mm',
            'rain_forecast_3h_mm', 'elevation_m', 'slope_percent', 'impervious_ratio',
            'drain_density', 'drain_capacity_score', 'drain_blockage_risk',
            'yamuna_level_m', 'flooded_before', 'flood_frequency'
        ]
    
    # Load ward data for reference
    if os.path.exists(DATA_PATH):
        try:
            ward_data = pd.read_csv(DATA_PATH)
            print(f"Ward data loaded: {len(ward_data)} records")
        except Exception as e:
            print(f"Warning: Could not load ward data: {e}")
            ward_data = None

# Load on startup
@app.on_event("startup")
async def startup_event():
    load_model()

# Request models
class PredictionRequest(BaseModel):
    ward_name: Optional[str] = None
    rain_1h_mm: float = 15.5
    rain_3h_mm: float = 42.3
    rain_24h_mm: float = 85.2
    rain_forecast_3h_mm: float = 38.5
    yamuna_level_m: float = 203.5
    # Optional fields with defaults
    distance_to_yamuna_m: Optional[float] = None
    elevation_m: Optional[float] = None
    slope_percent: Optional[float] = None
    impervious_ratio: Optional[float] = None
    drain_density: Optional[float] = None
    drain_capacity_score: Optional[float] = None
    drain_blockage_risk: Optional[float] = None
    flooded_before: Optional[int] = None
    flood_frequency: Optional[int] = None

def get_ward_defaults(ward_name: str) -> Dict[str, float]:
    """Get default values for a ward from CSV data"""
    defaults = {
        'distance_to_yamuna_m': 4000.0,
        'elevation_m': 215.0,
        'slope_percent': 2.5,
        'impervious_ratio': 0.75,
        'drain_density': 0.50,
        'drain_capacity_score': 0.70,
        'drain_blockage_risk': 0.55,
        'flooded_before': 0,
        'flood_frequency': 1
    }
    
    if ward_data is not None and ward_name:
        ward_row = ward_data[ward_data['ward_name'] == ward_name]
        if not ward_row.empty:
            row = ward_row.iloc[0]
            defaults.update({
                'distance_to_yamuna_m': float(row.get('distance_to_yamuna_m', defaults['distance_to_yamuna_m'])),
                'elevation_m': float(row.get('elevation_m', defaults['elevation_m'])),
                'slope_percent': float(row.get('slope_percent', defaults['slope_percent'])),
                'impervious_ratio': float(row.get('impervious_ratio', defaults['impervious_ratio'])),
                'drain_density': float(row.get('drain_density', defaults['drain_density'])),
                'drain_capacity_score': float(row.get('drain_capacity_score', defaults['drain_capacity_score'])),
                'drain_blockage_risk': float(row.get('drain_blockage_risk', defaults['drain_blockage_risk'])),
                'flooded_before': int(row.get('flooded_before', defaults['flooded_before'])),
                'flood_frequency': int(row.get('flood_frequency', defaults['flood_frequency']))
            })
    
    return defaults

def make_prediction(features: Dict[str, float]) -> Dict[str, Any]:
    """Make prediction using ML model or fallback logic"""
    
    if model is not None and feature_cols:
        try:
            # Prepare feature vector
            feature_vector = np.array([[features.get(col, 0.0) for col in feature_cols]])
            
            # Predict
            risk_level = int(model.predict(feature_vector)[0])
            probabilities = model.predict_proba(feature_vector)[0] if hasattr(model, 'predict_proba') else [0.33, 0.33, 0.34]
            confidence = float(max(probabilities))
        except Exception as e:
            print(f"Model prediction error: {e}. Using fallback.")
            risk_level, confidence = fallback_prediction(features)
    else:
        risk_level, confidence = fallback_prediction(features)
    
    # Calculate additional metrics
    max_depth = calculate_flood_depth(features, risk_level)
    
    return {
        'flood_risk_level': risk_level,
        'risk_label': ['Safe', 'Warning', 'Danger'][risk_level],
        'confidence': confidence,
        'max_flood_depth_cm': max_depth,
        'drain_capacity_score': features.get('drain_capacity_score', 0.7),
        'citizen_reports_count': int(features.get('citizen_reports_count', 0))
    }

def fallback_prediction(features: Dict[str, float]) -> tuple:
    """Fallback prediction logic when model is not available"""
    rain_24h = features.get('rain_24h_mm', 0)
    yamuna = features.get('yamuna_level_m', 203.5)
    blockage = features.get('drain_blockage_risk', 0.5)
    
    # Simple rule-based prediction
    if rain_24h > 80 or yamuna > 204.5 or blockage > 0.75:
        return (2, 0.85)  # Danger
    elif rain_24h > 50 or yamuna > 204.0 or blockage > 0.60:
        return (1, 0.75)  # Warning
    else:
        return (0, 0.70)  # Safe

def calculate_flood_depth(features: Dict[str, float], risk_level: int) -> float:
    """Estimate flood depth based on risk level and conditions"""
    base_depth = features.get('rain_24h_mm', 0) * 0.5
    yamuna_factor = max(0, (features.get('yamuna_level_m', 203.5) - 203.0) * 10)
    blockage_factor = features.get('drain_blockage_risk', 0.5) * 30
    
    depth = base_depth + yamuna_factor + blockage_factor
    
    # Cap based on risk level
    if risk_level == 2:
        depth = max(depth, 40.0)
    elif risk_level == 1:
        depth = min(max(depth, 10.0), 40.0)
    else:
        depth = min(depth, 10.0)
    
    return min(depth, 100.0)  # Cap at 100cm

@app.get("/")
def root():
    return {
        "message": "Delhi Drainage & Waterlogging Prediction API",
        "endpoints": ["/predict", "/demo", "/health"],
        "status": "operational"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "features_count": len(feature_cols) if feature_cols else 0
    }

@app.post("/predict")
def predict(request: PredictionRequest):
    """Predict flood risk for given conditions"""
    try:
        # Get ward defaults if ward_name provided
        defaults = get_ward_defaults(request.ward_name) if request.ward_name else {}
        
        # Build feature dictionary
        features = {
            'distance_to_yamuna_m': request.distance_to_yamuna_m or defaults.get('distance_to_yamuna_m', 4000.0),
            'rain_1h_mm': request.rain_1h_mm,
            'rain_3h_mm': request.rain_3h_mm,
            'rain_24h_mm': request.rain_24h_mm,
            'rain_forecast_3h_mm': request.rain_forecast_3h_mm,
            'elevation_m': request.elevation_m or defaults.get('elevation_m', 215.0),
            'slope_percent': request.slope_percent or defaults.get('slope_percent', 2.5),
            'impervious_ratio': request.impervious_ratio or defaults.get('impervious_ratio', 0.75),
            'drain_density': request.drain_density or defaults.get('drain_density', 0.50),
            'drain_capacity_score': request.drain_capacity_score or defaults.get('drain_capacity_score', 0.70),
            'drain_blockage_risk': request.drain_blockage_risk or defaults.get('drain_blockage_risk', 0.55),
            'yamuna_level_m': request.yamuna_level_m,
            'flooded_before': request.flooded_before if request.flooded_before is not None else defaults.get('flooded_before', 0),
            'flood_frequency': request.flood_frequency if request.flood_frequency is not None else defaults.get('flood_frequency', 1),
            'citizen_reports_count': defaults.get('citizen_reports_count', 0),
            'avg_reported_depth_cm': defaults.get('avg_reported_depth_cm', 0),
            'max_flood_depth_cm': 0  # Will be calculated
        }
        
        # Make prediction
        result = make_prediction(features)
        
        return {
            "success": True,
            "ward_name": request.ward_name or "Unknown",
            **result,
            "input_features": {
                "rain_24h_mm": request.rain_24h_mm,
                "yamuna_level_m": request.yamuna_level_m,
                "rain_forecast_3h_mm": request.rain_forecast_3h_mm
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

@app.get("/demo")
def demo():
    """Return demo data for live simulation"""
    # Simulate dynamic conditions
    base_time = datetime.now()
    
    # Simulate monsoon conditions
    time_factor = (base_time.minute % 30) / 30.0  # Cycle every 30 minutes
    
    # Vary rain based on time
    rain_24h = 60 + 40 * np.sin(time_factor * np.pi)
    rain_3h = rain_24h * 0.4 + random.uniform(-5, 10)
    rain_1h = rain_3h * 0.35 + random.uniform(-2, 5)
    
    # Yamuna level varies with rain
    yamuna_base = 203.0
    yamuna_level = yamuna_base + (rain_24h / 100) * 2 + random.uniform(-0.2, 0.5)
    
    # Generate ward-specific predictions
    ward_predictions = {}
    wards = ['Karol Bagh', 'Paharganj', 'Lajpat Nagar', 'Dwarka Sector 21', 
             'Connaught Place', 'Rohini Sector 8', 'Vasant Kunj', 'Mayur Vihar Phase 1']
    
    for ward in wards:
        defaults = get_ward_defaults(ward)
        features = {
            **defaults,
            'rain_1h_mm': rain_1h + random.uniform(-3, 3),
            'rain_3h_mm': rain_3h + random.uniform(-5, 5),
            'rain_24h_mm': rain_24h + random.uniform(-10, 10),
            'rain_forecast_3h_mm': rain_3h * 1.1,
            'yamuna_level_m': yamuna_level,
            'drain_blockage_risk': defaults.get('drain_blockage_risk', 0.5) + random.uniform(-0.1, 0.1),
            'citizen_reports_count': int(defaults.get('citizen_reports_count', 0) + random.uniform(0, 3))
        }
        
        prediction = make_prediction(features)
        ward_predictions[ward] = prediction
    
    # Calculate stats
    risk_counts = {'0': 0, '1': 0, '2': 0}
    for pred in ward_predictions.values():
        risk_counts[str(pred['flood_risk_level'])] += 1
    
    # Generate live updates
    live_updates = []
    for ward, pred in list(ward_predictions.items())[:3]:
        if pred['flood_risk_level'] >= 1:
            live_updates.append({
                'ward': ward,
                'message': f"{'Severe' if pred['flood_risk_level'] == 2 else 'Moderate'} water-logging risk detected",
                'time': f"{random.randint(1, 30)}m ago",
                'type': 'alert' if pred['flood_risk_level'] == 2 else 'warning',
                'risk': pred['flood_risk_level']
            })
    
    return {
        "timestamp": base_time.isoformat(),
        "stats": {
            "totalWards": len(wards),
            "highRisk": risk_counts['2'],
            "mediumRisk": risk_counts['1'],
            "lowRisk": risk_counts['0']
        },
        "ward_data": ward_predictions,
        "live_updates": live_updates,
        "conditions": {
            "rain_24h_mm": round(rain_24h, 1),
            "yamuna_level_m": round(yamuna_level, 1),
            "rain_forecast_3h_mm": round(rain_3h * 1.1, 1)
        },
        "predictions": {
            "next_3h_risk": "High" if rain_3h > 40 else "Medium" if rain_3h > 20 else "Low"
        }
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

