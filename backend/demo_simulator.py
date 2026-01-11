"""
Demo Simulator for Live Monsoon Simulation
Simulates dynamic weather conditions for judge demonstrations
"""

import time
import random
import numpy as np
import requests
from datetime import datetime
import json

API_BASE = "http://localhost:8000"

class MonsoonSimulator:
    def __init__(self):
        self.phase = "pre_monsoon"  # pre_monsoon, onset, peak, decline
        self.time_step = 0
        self.rain_base = 20.0
        self.yamuna_base = 203.0
        self.drain_blockage_increase = 0.0
        
    def simulate_monsoon_phase(self):
        """Simulate different monsoon phases"""
        phases = {
            "pre_monsoon": {
                "rain_range": (5, 25),
                "yamuna_offset": -0.3,
                "blockage_rate": 0.01,
                "duration": 10
            },
            "onset": {
                "rain_range": (30, 60),
                "yamuna_offset": 0.2,
                "blockage_rate": 0.02,
                "duration": 15
            },
            "peak": {
                "rain_range": (70, 120),
                "yamuna_offset": 1.0,
                "blockage_rate": 0.05,
                "duration": 20
            },
            "decline": {
                "rain_range": (40, 70),
                "yamuna_offset": 0.5,
                "blockage_rate": -0.01,
                "duration": 10
            }
        }
        
        current_phase_config = phases[self.phase]
        
        # Calculate current values
        rain_24h = random.uniform(*current_phase_config["rain_range"])
        rain_3h = rain_24h * 0.45 + random.uniform(-5, 10)
        rain_1h = rain_3h * 0.35 + random.uniform(-2, 5)
        
        yamuna_level = self.yamuna_base + current_phase_config["yamuna_offset"] + (rain_24h / 100) * 1.5
        
        # Simulate drain blockage accumulation
        self.drain_blockage_increase += current_phase_config["blockage_rate"]
        self.drain_blockage_increase = max(0, min(0.4, self.drain_blockage_increase))
        
        return {
            "rain_1h_mm": max(0, rain_1h),
            "rain_3h_mm": max(0, rain_3h),
            "rain_24h_mm": max(0, rain_24h),
            "rain_forecast_3h_mm": max(0, rain_3h * 1.15),
            "yamuna_level_m": round(yamuna_level, 2),
            "phase": self.phase,
            "drain_blockage_adjustment": self.drain_blockage_increase
        }
    
    def advance_phase(self):
        """Move to next monsoon phase"""
        phase_sequence = ["pre_monsoon", "onset", "peak", "decline"]
        current_index = phase_sequence.index(self.phase)
        
        if current_index < len(phase_sequence) - 1:
            self.phase = phase_sequence[current_index + 1]
            print(f"\n🌧️  Monsoon phase changed to: {self.phase.upper()}")
        else:
            # Reset to beginning for continuous loop
            self.phase = "pre_monsoon"
            self.drain_blockage_increase = 0.0
            print("\n🔄 Simulator reset - Starting new cycle")
    
    def run_continuous_simulation(self, update_interval=5):
        """Run continuous simulation updating every N seconds"""
        print("="*60)
        print("🌧️  MONSOON SIMULATION STARTED")
        print("="*60)
        print("This simulates dynamic weather conditions for demo")
        print("Press Ctrl+C to stop")
        print("="*60)
        
        step_count = 0
        phase_step = 0
        
        try:
            while True:
                conditions = self.simulate_monsoon_phase()
                
                print(f"\n⏰ Step {step_count} | Phase: {conditions['phase'].upper()}")
                print(f"📊 Current Conditions:")
                print(f"   Rain (24h): {conditions['rain_24h_mm']:.1f} mm")
                print(f"   Rain (3h): {conditions['rain_3h_mm']:.1f} mm")
                print(f"   Yamuna Level: {conditions['yamuna_level_m']:.2f} m")
                print(f"   Drain Blockage: +{conditions['drain_blockage_adjustment']:.2f}")
                
                # Try to update backend (if running)
                try:
                    # The /demo endpoint already simulates this, but we can trigger it
                    response = requests.get(f"{API_BASE}/demo", timeout=2)
                    if response.status_code == 200:
                        data = response.json()
                        high_risk = data['stats']['highRisk']
                        medium_risk = data['stats']['mediumRisk']
                        print(f"   🚨 High Risk Wards: {high_risk} | Medium: {medium_risk}")
                except:
                    print("   ⚠️  Backend not available (expected if running standalone)")
                
                phase_step += 1
                step_count += 1
                
                # Change phase every 15 steps (adjust as needed)
                if phase_step >= 15:
                    self.advance_phase()
                    phase_step = 0
                
                time.sleep(update_interval)
                
        except KeyboardInterrupt:
            print("\n\n" + "="*60)
            print("🛑 SIMULATION STOPPED")
            print("="*60)

    def run_single_cycle(self):
        """Run a single simulation cycle and return conditions"""
        conditions = self.simulate_monsoon_phase()
        self.time_step += 1
        
        if self.time_step % 10 == 0:
            self.advance_phase()
        
        return conditions

def simulate_ward_scenario():
    """Simulate a dramatic scenario for a specific ward"""
    print("\n" + "="*60)
    print("🎬 DRAMATIC SCENARIO SIMULATION")
    print("="*60)
    
    scenarios = [
        {
            "name": "Sudden Heavy Downpour",
            "ward": "Karol Bagh",
            "rain_24h": 95.0,
            "rain_3h": 65.0,
            "yamuna": 204.5,
            "blockage": 0.85
        },
        {
            "name": "Yamuna Overflow Threat",
            "ward": "Mayur Vihar Phase 1",
            "rain_24h": 75.0,
            "rain_3h": 45.0,
            "yamuna": 205.2,
            "blockage": 0.70
        },
        {
            "name": "Drain Blockage Crisis",
            "ward": "Paharganj",
            "rain_24h": 85.0,
            "rain_3h": 55.0,
            "yamuna": 204.0,
            "blockage": 0.90
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📋 Scenario: {scenario['name']}")
        print(f"   Ward: {scenario['ward']}")
        print(f"   Conditions:")
        print(f"     - Rain (24h): {scenario['rain_24h']} mm")
        print(f"     - Rain (3h): {scenario['rain_3h']} mm")
        print(f"     - Yamuna: {scenario['yamuna']} m")
        print(f"     - Drain Blockage: {scenario['blockage']*100:.0f}%")
        
        # Make prediction request
        try:
            response = requests.post(
                f"{API_BASE}/predict",
                json={
                    "ward_name": scenario['ward'],
                    "rain_1h_mm": scenario['rain_3h'] * 0.35,
                    "rain_3h_mm": scenario['rain_3h'],
                    "rain_24h_mm": scenario['rain_24h'],
                    "rain_forecast_3h_mm": scenario['rain_3h'] * 1.1,
                    "yamuna_level_m": scenario['yamuna'],
                    "drain_blockage_risk": scenario['blockage']
                },
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                risk_label = result['risk_label']
                depth = result['max_flood_depth_cm']
                print(f"   🎯 Prediction: {risk_label} Risk | Depth: {depth:.1f} cm")
            else:
                print(f"   ⚠️  API Error: {response.status_code}")
        except Exception as e:
            print(f"   ⚠️  Connection Error: {e}")
        
        time.sleep(2)

if __name__ == '__main__':
    import sys
    
    simulator = MonsoonSimulator()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--scenario':
        # Run dramatic scenarios
        simulate_ward_scenario()
    else:
        # Run continuous simulation
        interval = int(sys.argv[1]) if len(sys.argv) > 1 else 5
        simulator.run_continuous_simulation(update_interval=interval)

