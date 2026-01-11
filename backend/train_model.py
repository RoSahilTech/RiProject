"""
ML Training Script for Delhi Flood Risk Prediction
Trains RandomForest and XGBoost models on flood risk data
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import xgboost as xgb
import joblib
import os

import os

def load_and_prepare_data(csv_path=None):
    """Load CSV data and prepare features"""
    if csv_path is None:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(BASE_DIR, '..', 'DATA', 'delhi_flood_data.csv')
    """Load CSV data and prepare features"""
    print(f"Loading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # Feature columns (excluding target, identifier, and LEAKAGE features)
    # REMOVED: max_flood_depth_cm, avg_reported_depth_cm, citizen_reports_count
    # These are OUTCOMES, not predictors - using them causes 100% accuracy (data leakage)
    feature_cols = [
        'distance_to_yamuna_m',
        'rain_1h_mm',
        'rain_3h_mm',
        'rain_24h_mm',
        'rain_forecast_3h_mm',
        'elevation_m',
        'slope_percent',
        'impervious_ratio',
        'drain_density',
        'drain_capacity_score',
        'drain_blockage_risk',
        'yamuna_level_m',
        'flooded_before',  # Historical data - can be used
        'flood_frequency'  # Historical frequency - can be used (but should be independent)
    ]
    
    X = df[feature_cols].fillna(0)
    y = df['flood_risk_level'].astype(int)
    
    print(f"Dataset shape: {X.shape}")
    print(f"Target distribution:\n{y.value_counts().sort_index()}")
    
    return X, y, feature_cols

def train_random_forest(X, y, feature_cols):
    """Train RandomForest model"""
    print("\n" + "="*50)
    print("Training RandomForest Model...")
    print("="*50)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=10,
        min_samples_split=5,
        min_samples_leaf=2,
        random_state=42,
        n_jobs=-1
    )
    
    rf_model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = rf_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nRandomForest Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Warning', 'Danger']))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': rf_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 5 Important Features:")
    print(feature_importance.head())
    
    return rf_model, accuracy

def train_xgboost(X, y, feature_cols):
    """Train XGBoost model"""
    print("\n" + "="*50)
    print("Training XGBoost Model...")
    print("="*50)
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    xgb_model = xgb.XGBClassifier(
        n_estimators=100,
        max_depth=6,
        learning_rate=0.1,
        subsample=0.8,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric='mlogloss'
    )
    
    xgb_model.fit(
        X_train, y_train,
        eval_set=[(X_test, y_test)],
        verbose=False
    )
    
    # Evaluate
    y_pred = xgb_model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"\nXGBoost Accuracy: {accuracy:.4f}")
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=['Safe', 'Warning', 'Danger']))
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': xgb_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nTop 5 Important Features:")
    print(feature_importance.head())
    
    return xgb_model, accuracy

def save_model(model, model_path, model_type='rf'):
    """Save trained model"""
    model_dir = os.path.dirname(model_path)
    if model_dir:
        os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, model_path)
    print(f"\n{model_type.upper()} model saved to {model_path}")

def main():
    print("="*60)
    print("Delhi Flood Risk Prediction - ML Model Training")
    print("="*60)
    
    # Load data
    X, y, feature_cols = load_and_prepare_data()
    
    # Train both models
    rf_model, rf_accuracy = train_random_forest(X, y, feature_cols)
    xgb_model, xgb_accuracy = train_xgboost(X, y, feature_cols)
    
    # Choose best model (for demo, we'll use RandomForest as it's simpler)
    print("\n" + "="*50)
    print("Model Comparison:")
    print(f"RandomForest Accuracy: {rf_accuracy:.4f}")
    print(f"XGBoost Accuracy: {xgb_accuracy:.4f}")
    print("="*50)
    
    # Save models
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    rf_path = os.path.join(BASE_DIR, 'models', 'random_forest_model.pkl')
    xgb_path = os.path.join(BASE_DIR, 'models', 'xgboost_model.pkl')
    feature_path = os.path.join(BASE_DIR, 'models', 'feature_columns.json')
    
    save_model(rf_model, rf_path, 'rf')
    save_model(xgb_model, xgb_path, 'xgboost')
    
    # Save feature columns for inference
    import json
    os.makedirs(os.path.dirname(feature_path), exist_ok=True)
    with open(feature_path, 'w') as f:
        json.dump(feature_cols, f)
    
    print("\nTraining completed successfully!")
    print(f"Using RandomForest model (Accuracy: {rf_accuracy:.4f})")

if __name__ == '__main__':
    main()

