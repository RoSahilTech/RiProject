"""
Regenerate complete dataset with exactly 100 records
Ensures proper risk level distribution
"""

import random
import csv
import os

# All Delhi wards (realistic names across all zones)
ALL_WARDS = [
    # Central Zone (10 wards)
    ("Karol Bagh", "Central", 28.6514, 77.1907, 3500),
    ("Connaught Place", "Central", 28.6315, 77.2167, 3200),
    ("Paharganj", "Central", 28.6453, 77.2128, 2800),
    ("Old Delhi", "Central", 28.6145, 77.1876, 3300),
    ("Chandni Chowk", "Central", 28.6557, 77.2309, 3000),
    ("Daryaganj", "Central", 28.6393, 77.2417, 3100),
    ("Jama Masjid", "Central", 28.6507, 77.2337, 2900),
    ("Sadar Bazaar", "Central", 28.6692, 77.2128, 3600),
    ("Tis Hazari", "Central", 28.6728, 77.2179, 3800),
    ("Kashmere Gate", "Central", 28.6798, 77.2076, 3100),
    
    # East Zone (15 wards)
    ("Mayur Vihar Phase 1", "East", 28.6083, 77.2908, 1500),
    ("Patparganj", "East", 28.5789, 77.2712, 2200),
    ("Seelampur", "East", 28.6489, 77.2478, 2600),
    ("Shahdara", "East", 28.6718, 77.2871, 1800),
    ("Gandhi Nagar", "East", 28.6565, 77.2765, 2400),
    ("Preet Vihar", "East", 28.6253, 27.3056, 2000),
    ("Geeta Colony", "East", 28.6678, 77.2723, 2700),
    ("Vivek Vihar", "East", 28.6432, 77.2956, 1900),
    ("Yamuna Vihar", "East", 28.6776, 77.2845, 1600),
    ("Laxmi Nagar", "East", 28.6215, 77.2754, 2500),
    ("Anand Vihar", "East", 28.6456, 77.3132, 1400),
    ("Krishna Nagar", "East", 28.6345, 77.2891, 2300),
    ("Nirman Vihar", "East", 28.6167, 77.2812, 2100),
    ("Karkardooma", "East", 28.6289, 77.2945, 2000),
    ("Dilshad Garden", "East", 28.6623, 77.3245, 1100),
    
    # South Zone (15 wards)
    ("Vasant Kunj", "South", 28.5245, 77.1492, 10500),
    ("Saket", "South", 28.5576, 77.1789, 5500),
    ("Malviya Nagar", "South", 28.5623, 77.1567, 5400),
    ("Green Park", "South", 28.5432, 77.1923, 5800),
    ("Safdarjung Enclave", "South", 28.5678, 77.2034, 5200),
    ("Greater Kailash Part 1", "South", 28.5667, 77.2156, 5300),
    ("Vasant Vihar", "South", 28.4867, 77.1324, 9800),
    ("Lodhi Colony", "South", 28.5812, 77.2212, 5100),
    ("Nehru Place", "South", 28.5489, 77.2189, 5600),
    ("Kalkaji", "South", 28.5376, 77.2523, 4800),
    ("Govindpuri", "South", 28.5298, 77.2634, 4700),
    ("Jasola", "South", 28.5432, 77.2891, 4200),
    ("Sarita Vihar", "South", 28.5212, 77.2745, 4500),
    ("Mehrauli", "South", 28.5234, 77.1845, 6200),
    ("Tuglakabad", "South", 28.5123, 77.2634, 4400),
    
    # West Zone (15 wards)
    ("Rajouri Garden", "West", 28.6334, 77.0912, 6200),
    ("Paschim Vihar", "West", 28.6734, 77.1478, 6800),
    ("Janakpuri", "West", 28.5918, 77.0892, 6500),
    ("Patel Nagar", "West", 28.6345, 77.1612, 6000),
    ("Rajendra Place", "West", 28.6289, 77.1734, 5900),
    ("Kirti Nagar", "West", 28.6412, 77.1545, 6100),
    ("Moti Nagar", "West", 28.6523, 77.1467, 6300),
    ("Tagore Garden", "West", 28.6189, 77.0823, 6600),
    ("Vikaspuri", "West", 28.5923, 77.0734, 7000),
    ("Uttam Nagar", "West", 28.6123, 77.0523, 7200),
    ("Bindapur", "West", 28.6034, 77.0645, 7100),
    ("Najafgarh", "West", 28.6123, 77.0356, 8000),
    ("Palam", "West", 28.5678, 77.1023, 7500),
    ("Mahipalpur", "West", 28.5545, 77.1234, 7300),
    ("Munirka", "West", 28.5423, 77.1456, 6900),
    
    # North Zone (10 wards)
    ("Model Town", "North", 28.6892, 77.2124, 5800),
    ("Civil Lines", "North", 28.6623, 77.2298, 4500),
    ("Burari", "North", 28.7312, 77.2123, 5600),
    ("Kamla Nagar", "North", 28.6734, 77.2212, 4200),
    ("Timarpur", "North", 28.6845, 77.2034, 4800),
    ("Kingsway Camp", "North", 28.6756, 77.1923, 5000),
    ("Azadpur", "North", 28.7123, 77.1812, 5200),
    ("Wazirabad", "North", 28.7234, 77.2345, 3800),
    ("Badli", "North", 28.7345, 77.1634, 6000),
    ("Rohini Sector 8", "North", 28.7495, 77.0565, 7200),
    
    # North West Zone (15 wards)
    ("Pitampura", "North West", 28.6987, 77.1687, 5900),
    ("Ashok Vihar", "North West", 28.7215, 77.1456, 6100),
    ("Shalimar Bagh", "North West", 28.7098, 77.1025, 6400),
    ("Rohini Sector 3", "North West", 28.7567, 77.0823, 7800),
    ("Rohini Sector 5", "North West", 28.7634, 77.0912, 8000),
    ("Rohini Sector 15", "North West", 28.7545, 77.0634, 8200),
    ("Bawana", "North West", 28.7812, 77.0356, 9500),
    ("Narela", "North West", 28.7923, 77.0245, 11000),
    ("Sultanpur", "North West", 28.7123, 77.1123, 6500),
    ("Rithala", "North West", 28.7345, 77.0734, 8500),
    ("Rohini Sector 16", "North West", 28.7512, 77.0456, 8700),
    ("Rohini Sector 22", "North West", 28.7467, 77.0245, 9000),
    ("Rohini Sector 24", "North West", 28.7423, 77.0123, 9200),
    ("Nangloi", "North West", 28.6789, 77.0634, 8800),
    ("Pehladpur", "North West", 28.6987, 77.0812, 7000),
    
    # South West Zone (10 wards)
    ("Dwarka Sector 21", "South West", 28.5822, 77.0500, 8500),
    ("Dwarka Sector 6", "South West", 28.5634, 77.0734, 8800),
    ("Dwarka Sector 10", "South West", 28.5545, 77.0912, 9000),
    ("Dwarka Sector 14", "South West", 28.5456, 77.0823, 9200),
    ("Dwarka Sector 22", "South West", 28.5367, 77.0456, 9500),
    ("Kapashera", "South West", 28.5234, 77.1023, 9800),
    ("Dabri", "South West", 28.6123, 77.1023, 8200),
    ("Mahavir Enclave", "South West", 28.6012, 77.0912, 8400),
    ("Dashrath Puri", "South West", 28.5891, 77.0812, 8600),
    ("Chhawla", "South West", 28.5767, 77.0634, 8900),
    
    # South East Zone (10 wards)
    ("Lajpat Nagar", "South East", 28.5677, 77.2433, 4200),
    ("Okhla Phase 1", "South East", 28.5355, 77.2656, 3800),
    ("Defence Colony", "South East", 28.5543, 77.2345, 4100),
    ("Hauz Khas", "South East", 28.5434, 77.2056, 4800),
    ("Jangpura", "South East", 28.5978, 77.2245, 3900),
    ("New Friends Colony", "South East", 28.5456, 77.2789, 4000),
    ("Jasola Vihar", "South East", 28.5323, 77.2891, 4300),
    ("Shaheen Bagh", "South East", 28.5234, 77.3012, 4100),
    ("Kalindi Kunj", "South East", 28.5345, 77.3123, 3900),
    ("Abul Fazal Enclave", "South East", 28.5212, 77.3234, 4200),
]

def generate_realistic_record(ward_info, target_risk_level=None):
    """Generate one realistic record"""
    ward_name, zone, lat, lng, dist_yamuna = ward_info
    
    # Elevation based on zone
    if zone == "South":
        elevation = random.uniform(220, 230)
    elif zone == "East":
        elevation = random.uniform(205, 212)
    elif zone == "Central":
        elevation = random.uniform(214, 222)
    else:
        elevation = random.uniform(215, 225)
    
    slope = random.uniform(1.0, 5.5)
    impervious = random.uniform(0.55, 0.92)
    drain_density = random.uniform(0.35, 0.72)
    drain_capacity = random.uniform(0.48, 0.88)
    
    # Determine risk level and generate matching conditions
    if target_risk_level is not None:
        risk_level = target_risk_level
    else:
        risk_level = random.choices([0, 1, 2], weights=[35, 40, 25])[0]
    
    # Generate conditions matching risk level
    if risk_level == 2:  # Danger
        rain_24h = random.uniform(85, 125)
        yamuna = random.uniform(204.3, 205.2)
        blockage_risk = random.uniform(0.70, 0.90)
        flooded_before = 1
        flood_frequency = random.randint(3, 6)
    elif risk_level == 1:  # Warning
        rain_24h = random.uniform(50, 85)
        yamuna = random.uniform(203.8, 204.5)
        blockage_risk = random.uniform(0.55, 0.75)
        flooded_before = random.choices([0, 1], weights=[0.3, 0.7])[0]
        flood_frequency = random.randint(1, 4) if flooded_before else 0
    else:  # Safe
        rain_24h = random.uniform(10, 50)
        yamuna = random.uniform(203.0, 203.8)
        blockage_risk = random.uniform(0.30, 0.60)
        flooded_before = random.choices([0, 1], weights=[0.7, 0.3])[0]
        flood_frequency = random.randint(0, 2) if flooded_before else 0
    
    # Adjust drain capacity based on risk (higher risk = worse drainage)
    if risk_level == 2:
        drain_capacity = random.uniform(0.48, 0.65)
    elif risk_level == 1:
        drain_capacity = random.uniform(0.60, 0.75)
    else:
        drain_capacity = random.uniform(0.70, 0.88)
    
    # Calculate related rain values
    rain_3h = rain_24h * random.uniform(0.40, 0.55)
    rain_1h = rain_3h * random.uniform(0.30, 0.40)
    rain_forecast_3h = rain_3h * random.uniform(1.05, 1.20)
    
    # Citizen reports
    if risk_level == 2:
        reports = random.randint(10, 20)
        avg_depth = random.uniform(30, 55)
        max_depth = random.uniform(50, 95)
    elif risk_level == 1:
        reports = random.randint(3, 12)
        avg_depth = random.uniform(12, 35)
        max_depth = random.uniform(20, 55)
    else:
        reports = random.randint(0, 3)
        avg_depth = random.uniform(0, 12) if reports > 0 else 0
        max_depth = random.uniform(0, 18) if reports > 0 else 0
    
    return {
        'cell_id': 0,  # Will be assigned
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

def generate_balanced_dataset():
    """Generate exactly 100 records with balanced distribution"""
    # Target: ~35 Safe, ~40 Warning, ~25 Danger
    risk_targets = [0] * 35 + [1] * 40 + [2] * 25
    random.shuffle(risk_targets)
    
    records = []
    used_wards = set()
    
    for i, target_risk in enumerate(risk_targets):
        # Select unused ward
        available = [w for w in ALL_WARDS if w[0] not in used_wards]
        if not available:
            # If all used, reuse randomly
            ward_info = random.choice(ALL_WARDS)
        else:
            ward_info = random.choice(available)
            used_wards.add(ward_info[0])
        
        record = generate_realistic_record(ward_info, target_risk)
        record['cell_id'] = 1000 + i + 1
        records.append(record)
    
    return records

def write_csv(records, csv_path):
    """Write records to CSV"""
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
        writer.writerows(records)

if __name__ == '__main__':
    print("Regenerating complete dataset with exactly 100 records...")
    print("=" * 60)
    
    # Set seed for reproducibility
    random.seed(42)
    
    records = generate_balanced_dataset()
    
    # Get CSV path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'delhi_flood_data.csv')
    
    write_csv(records, csv_path)
    
    print(f"[SUCCESS] Generated {len(records)} records")
    print(f"[INFO] File: {csv_path}")
    
    # Print distribution
    risk_counts = {}
    for record in records:
        risk = record['flood_risk_level']
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
    
    print(f"\n[STATS] Risk Level Distribution:")
    print(f"   Safe (0): {risk_counts.get(0, 0)} ({risk_counts.get(0, 0)}%)")
    print(f"   Warning (1): {risk_counts.get(1, 0)} ({risk_counts.get(1, 0)}%)")
    print(f"   Danger (2): {risk_counts.get(2, 0)} ({risk_counts.get(2, 0)}%)")
    
    print(f"\n[SUCCESS] Dataset ready for training!")
    print("Run: python ../backend/train_model.py")
