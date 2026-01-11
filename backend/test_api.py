"""
Simple script to test the API endpoints
Run this after starting the backend server to verify everything works
"""

import requests
import json

API_BASE = "http://localhost:8000"

def test_health():
    print("Testing /health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed!")
            print(f"   Status: {data.get('status')}")
            print(f"   Model loaded: {data.get('model_loaded')}")
            print(f"   Features: {data.get('features_count')}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        print("   Make sure the backend is running: python app.py")
        return False

def test_predict():
    print("\nTesting /predict endpoint...")
    try:
        payload = {
            "ward_name": "Karol Bagh",
            "rain_1h_mm": 20.0,
            "rain_3h_mm": 55.0,
            "rain_24h_mm": 95.0,
            "rain_forecast_3h_mm": 60.0,
            "yamuna_level_m": 204.5
        }
        
        response = requests.post(
            f"{API_BASE}/predict",
            json=payload,
            timeout=5
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Prediction successful!")
            print(f"   Ward: {data.get('ward_name')}")
            print(f"   Risk Level: {data.get('risk_label')} ({data.get('flood_risk_level')})")
            print(f"   Confidence: {data.get('confidence', 0):.2%}")
            print(f"   Max Depth: {data.get('max_flood_depth_cm', 0):.1f} cm")
            return True
        else:
            print(f"❌ Prediction failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Prediction error: {e}")
        return False

def test_demo():
    print("\nTesting /demo endpoint...")
    try:
        response = requests.get(f"{API_BASE}/demo", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Demo data retrieved!")
            print(f"   Timestamp: {data.get('timestamp')}")
            stats = data.get('stats', {})
            print(f"   Stats: {stats.get('highRisk')} high, {stats.get('mediumRisk')} medium, {stats.get('lowRisk')} low risk")
            print(f"   Wards with data: {len(data.get('ward_data', {}))}")
            print(f"   Live updates: {len(data.get('live_updates', []))}")
            return True
        else:
            print(f"❌ Demo endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Demo endpoint error: {e}")
        return False

def main():
    print("="*60)
    print("API Test Suite - Delhi Flood Prediction")
    print("="*60)
    print(f"Testing API at: {API_BASE}")
    print()
    
    results = []
    results.append(("Health Check", test_health()))
    results.append(("Prediction", test_predict()))
    results.append(("Demo Data", test_demo()))
    
    print("\n" + "="*60)
    print("Test Results Summary")
    print("="*60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("1. Make sure backend is running: python app.py")
        print("2. Check if port 8000 is available")
        print("3. Verify model files exist: backend/models/random_forest_model.pkl")
        print("4. Run training: python train_model.py")
    
    print("="*60)

if __name__ == '__main__':
    main()

