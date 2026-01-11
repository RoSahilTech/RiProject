"""
Script to generate additional synthetic flood data for Delhi wards
Generates 70 more records to reach 100 total
"""

import random
import csv

# Delhi ward names (additional realistic names)
additional_wards = [
    ("Shahdara", "East"), ("Gandhi Nagar", "East"), ("Preet Vihar", "East"),
    ("Geeta Colony", "East"), ("Vivek Vihar", "East"), ("Yamuna Vihar", "East"),
    ("Seemapuri", "East"), ("Mansarovar Park", "East"), ("Shakarpur", "East"),
    ("Laxmi Nagar", "East"),
    
    ("Rohini Sector 3", "North West"), ("Rohini Sector 5", "North West"),
    ("Rohini Sector 15", "North West"), ("Rohini Sector 16", "North West"),
    ("Bawana", "North West"), ("Narela", "North West"), ("Burari", "North"),
    ("Kamla Nagar", "North"), ("Timarpur", "North"), ("Kingsway Camp", "North"),
    
    ("Dwarka Sector 6", "South West"), ("Dwarka Sector 10", "South West"),
    ("Dwarka Sector 14", "South West"), ("Dwarka Sector 22", "South West"),
    ("Uttam Nagar", "South West"), ("Najafgarh", "South West"), ("Bindapur", "South West"),
    ("Palam", "South West"), ("Mahipalpur", "South West"), ("Munirka", "South West"),
    
    ("Saket Block B", "South"), ("Saket Block D", "South"), ("Malviya Nagar Extension", "South"),
    ("Green Park", "South"), ("Safdarjung Enclave", "South"), ("Lodhi Colony", "South"),
    ("Jangpura Extension", "South"), ("Nehru Place", "South"), ("Kalkaji", "South"),
    ("Govindpuri", "South"),
    
    ("Chandni Chowk", "Central"), ("Daryaganj", "Central"), ("Jama Masjid", "Central"),
    ("Sadar Bazaar", "Central"), ("Paharganj Extension", "Central"), ("Nabi Karim", "Central"),
    ("Daryaganj", "Central"), ("Ballimaran", "Central"), ("Bara Hindu Rao", "Central"),
    ("Tis Hazari", "Central"),
    
    ("Patel Nagar", "West"), ("Rajendra Place", "West"), ("Karampura", "West"),
    ("Subhash Nagar", "West"), ("Kirti Nagar", "West"), ("Moti Nagar", "West"),
    ("Ramesh Nagar", "West"), ("Rajouri Garden Extension", "West"), ("Tagore Garden", "West"),
    ("Vikaspuri", "West"),
    
    ("Laxmi Nagar Extension", "East"), ("Mayur Vihar Phase 2", "East"),
    ("Mayur Vihar Phase 3", "East"), ("IP Extension", "East"), ("Anand Vihar", "East"),
    ("Krishna Nagar", "East"), ("Nirman Vihar", "East"), ("Karkardooma", "East"),
    ("Dilshad Garden", "East"), ("Gharoli", "East"),
    
    ("Sarita Vihar", "South"), ("Jasola", "South"), ("Madanpur Khadar", "South"),
    ("Tuglakabad", "South"), ("Sangam Vihar", "South"), ("Deoli", "South"),
    ("Ambedkar Nagar", "South"), ("Mehrauli", "South"), ("Vasant Kunj Extension", "South"),
    ("Munirka Extension", "South")
]

def generate_realistic_data():
    """Generate realistic flood data with proper correlations"""
    
    records = []
    cell_id = 1031
    
    for ward_name, zone in additional_wards:
        # Generate coordinates based on zone (realistic Delhi bounds)
        lat = random.uniform(28.45, 28.75)
        lng = random.uniform(77.08, 77.32)
        
        # Distance to Yamuna (varies by zone)
        if zone == "East":
            dist_yamuna = random.uniform(1000, 4000)
        elif zone == "Central":
            dist_yamuna = random.uniform(2500, 4500)
        else:
            dist_yamuna = random.uniform(5000, 11000)
        
        # Elevation (South higher, East lower)
        if zone == "South":
            elevation = random.uniform(220, 230)
        elif zone == "East":
            elevation = random.uniform(205, 212)
        elif zone == "Central":
            elevation = random.uniform(214, 222)
        else:
            elevation = random.uniform(215, 225)
        
        # Slope
        slope = random.uniform(1.0, 5.5)
        
        # Impervious ratio (urbanization level)
        impervious = random.uniform(0.55, 0.92)
        
        # Drain density and capacity (inversely related to blockage risk)
        drain_density = random.uniform(0.35, 0.72)
        drain_capacity = random.uniform(0.48, 0.88)
        blockage_risk = random.uniform(0.30, 0.85)
        
        # Historical flooding
        flooded_before = random.choices([0, 1], weights=[0.4, 0.6])[0]
        flood_frequency = random.randint(0, 5) if flooded_before else 0
        
        # Generate rain data (varies by season/scenario)
        scenario = random.choice(['light', 'moderate', 'heavy', 'extreme'])
        
        if scenario == 'light':
            rain_24h = random.uniform(10, 35)
            rain_3h = rain_24h * random.uniform(0.35, 0.50)
            rain_1h = rain_3h * random.uniform(0.30, 0.40)
            yamuna = random.uniform(203.0, 203.5)
        elif scenario == 'moderate':
            rain_24h = random.uniform(40, 70)
            rain_3h = rain_24h * random.uniform(0.40, 0.55)
            rain_1h = rain_3h * random.uniform(0.30, 0.40)
            yamuna = random.uniform(203.5, 204.2)
        elif scenario == 'heavy':
            rain_24h = random.uniform(75, 110)
            rain_3h = rain_24h * random.uniform(0.45, 0.60)
            rain_1h = rain_3h * random.uniform(0.30, 0.40)
            yamuna = random.uniform(204.0, 204.8)
        else:  # extreme
            rain_24h = random.uniform(110, 130)
            rain_3h = rain_24h * random.uniform(0.50, 0.65)
            rain_1h = rain_3h * random.uniform(0.30, 0.40)
            yamuna = random.uniform(204.5, 205.5)
        
        rain_forecast_3h = rain_3h * random.uniform(1.05, 1.20)
        
        # Calculate flood risk based on conditions
        risk_score = 0
        if rain_24h > 80 or yamuna > 204.5 or blockage_risk > 0.75:
            risk_level = 2  # Danger
        elif rain_24h > 50 or yamuna > 204.0 or blockage_risk > 0.60 or (flooded_before and rain_24h > 40):
            risk_level = 1  # Warning
        else:
            risk_level = 0  # Safe
        
        # Adjust based on drainage and elevation
        if drain_capacity < 0.55 and elevation < 210:
            risk_level = min(risk_level + 1, 2)
        if drain_capacity > 0.80 and elevation > 225:
            risk_level = max(risk_level - 1, 0)
        
        # Citizen reports based on risk
        if risk_level == 2:
            reports = random.randint(10, 20)
            avg_depth = random.uniform(30, 50)
            max_depth = random.uniform(50, 90)
        elif risk_level == 1:
            reports = random.randint(3, 10)
            avg_depth = random.uniform(10, 30)
            max_depth = random.uniform(20, 50)
        else:
            reports = random.randint(0, 3)
            avg_depth = random.uniform(0, 10) if reports > 0 else 0
            max_depth = random.uniform(0, 15) if reports > 0 else 0
        
        # Round values appropriately
        record = {
            'cell_id': cell_id,
            'latitude': round(lat, 4),
            'longitude': round(lng, 4),
            'ward_name': ward_name,
            'zone': zone,
            'distance_to_yamuna_m': round(dist_yamuna, 1),
            'rain_1h_mm': round(rain_1h, 1),
            'rain_3h_mm': round(rain_3h, 1),
            'rain_24h_mm': round(rain_24h, 1),
            'rain_forecast_3h_mm': round(rain_forecast_3h, 1),
            'elevation_m': round(elevation, 1),
            'slope_percent': round(slope, 1),
            'impervious_ratio': round(impervious, 2),
            'drain_density': round(drain_density, 2),
            'drain_capacity_score': round(drain_capacity, 2),
            'drain_blockage_risk': round(blockage_risk, 2),
            'yamuna_level_m': round(yamuna, 1),
            'flooded_before': flooded_before,
            'flood_frequency': flood_frequency,
            'citizen_reports_count': reports,
            'avg_reported_depth_cm': round(avg_depth, 1),
            'max_flood_depth_cm': round(max_depth, 1),
            'flood_risk_level': risk_level
        }
        
        records.append(record)
        cell_id += 1
    
    return records

def append_to_csv(records, csv_path='delhi_flood_data.csv'):
    """Append new records to existing CSV"""
    import os
    # Get absolute path
    if not os.path.isabs(csv_path):
        csv_path = os.path.join(os.path.dirname(__file__), csv_path)
    
    # Read existing data
    existing_records = []
    if os.path.exists(csv_path):
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            existing_records = list(reader)
    
    # Append new records
    all_records = existing_records + records
    
    # Write back to CSV
    fieldnames = [
        'cell_id', 'latitude', 'longitude', 'ward_name', 'zone',
        'distance_to_yamuna_m', 'rain_1h_mm', 'rain_3h_mm', 'rain_24h_mm',
        'rain_forecast_3h_mm', 'elevation_m', 'slope_percent', 'impervious_ratio',
        'drain_density', 'drain_capacity_score', 'drain_blockage_risk',
        'yamuna_level_m', 'flooded_before', 'flood_frequency',
        'citizen_reports_count', 'avg_reported_depth_cm', 'max_flood_depth_cm',
        'flood_risk_level'
    ]
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_records)
    
    print(f"[SUCCESS] Added {len(records)} new records to {csv_path}")
    print(f"[INFO] Total records: {len(all_records)}")
    
    # Print distribution
    risk_counts = {}
    for record in all_records:
        risk = int(record['flood_risk_level'])
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    print(f"\n[STATS] Risk Level Distribution:")
    print(f"   Safe (0): {risk_counts.get(0, 0)}")
    print(f"   Warning (1): {risk_counts.get(1, 0)}")
    print(f"   Danger (2): {risk_counts.get(2, 0)}")

if __name__ == '__main__':
    import os
    print("Generating 70 additional flood data records...")
    print("=" * 60)
    
    new_records = generate_realistic_data()
    # Get the CSV path relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'delhi_flood_data.csv')
    append_to_csv(new_records, csv_path)
    
    print("\n[SUCCESS] Data generation complete!")
    print("Ready for model training with 100 total records.")
