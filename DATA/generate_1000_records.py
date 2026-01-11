"""
Generate comprehensive dataset with ~1000 records for better ML training
Creates multiple scenarios per ward with varying conditions
"""

import random
import csv
import os

# Base ward list with coordinates (can be repeated with variations)
BASE_WARDS = [
    # Central Zone
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
    ("Nabi Karim", "Central", 28.6589, 77.2245, 3200),
    ("Ballimaran", "Central", 28.6534, 77.2189, 3050),
    
    # East Zone (20 wards)
    ("Mayur Vihar Phase 1", "East", 28.6083, 77.2908, 1500),
    ("Mayur Vihar Phase 2", "East", 28.6056, 77.2956, 1600),
    ("Mayur Vihar Phase 3", "East", 28.6023, 77.3012, 1700),
    ("Patparganj", "East", 28.5789, 77.2712, 2200),
    ("Seelampur", "East", 28.6489, 77.2478, 2600),
    ("Shahdara", "East", 28.6718, 77.2871, 1800),
    ("Gandhi Nagar", "East", 28.6565, 77.2765, 2400),
    ("Preet Vihar", "East", 28.6253, 77.3056, 2000),
    ("Geeta Colony", "East", 28.6678, 77.2723, 2700),
    ("Vivek Vihar", "East", 28.6432, 77.2956, 1900),
    ("Yamuna Vihar", "East", 28.6776, 77.2845, 1600),
    ("Laxmi Nagar", "East", 28.6215, 77.2754, 2500),
    ("Anand Vihar", "East", 28.6456, 77.3132, 1400),
    ("Krishna Nagar", "East", 28.6345, 77.2891, 2300),
    ("Nirman Vihar", "East", 28.6167, 77.2812, 2100),
    ("Karkardooma", "East", 28.6289, 77.2945, 2000),
    ("Dilshad Garden", "East", 28.6623, 77.3245, 1100),
    ("IP Extension", "East", 28.6198, 77.2989, 1900),
    ("Shakarpur", "East", 28.6545, 77.2789, 2600),
    ("Mansarovar Park", "East", 28.6723, 77.2912, 1750),
    ("Seemapuri", "East", 28.6856, 77.3023, 1200),
    
    # South Zone (25 wards)
    ("Vasant Kunj", "South", 28.5245, 77.1492, 10500),
    ("Saket", "South", 28.5576, 77.1789, 5500),
    ("Malviya Nagar", "South", 28.5623, 77.1567, 5400),
    ("Green Park", "South", 28.5432, 77.1923, 5800),
    ("Safdarjung Enclave", "South", 28.5678, 77.2034, 5200),
    ("Greater Kailash Part 1", "South", 28.5667, 77.2156, 5300),
    ("Greater Kailash Part 2", "South", 28.5612, 77.2234, 5400),
    ("Vasant Vihar", "South", 28.4867, 77.1324, 9800),
    ("Lodhi Colony", "South", 28.5812, 77.2212, 5100),
    ("Nehru Place", "South", 28.5489, 77.2189, 5600),
    ("Kalkaji", "South", 28.5376, 77.2523, 4800),
    ("Govindpuri", "South", 28.5298, 77.2634, 4700),
    ("Jasola", "South", 28.5432, 77.2891, 4200),
    ("Sarita Vihar", "South", 28.5212, 77.2745, 4500),
    ("Mehrauli", "South", 28.5234, 77.1845, 6200),
    ("Tuglakabad", "South", 28.5123, 77.2634, 4400),
    ("Sangam Vihar", "South", 28.5089, 77.2456, 4600),
    ("Deoli", "South", 28.5156, 77.2312, 5000),
    ("Ambedkar Nagar", "South", 28.5223, 77.2189, 5200),
    ("Chittaranjan Park", "South", 28.5345, 77.2356, 4900),
    ("Alaknanda", "South", 28.5412, 77.2212, 5100),
    ("Saket Block A", "South", 28.5598, 77.1823, 5600),
    ("Saket Block B", "South", 28.5576, 77.1789, 5500),
    ("Saket Block C", "South", 28.5554, 77.1756, 5450),
    ("South Extension Part 1", "South", 28.5898, 77.2112, 4800),
    ("South Extension Part 2", "South", 28.5876, 77.1989, 5100),
    
    # West Zone (30 wards)
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
    ("Subhash Nagar", "West", 28.6298, 77.1523, 6400),
    ("Karampura", "West", 28.6376, 77.1489, 6200),
    ("Ramesh Nagar", "West", 28.6312, 77.1423, 6300),
    ("Tilak Nagar", "West", 28.6156, 77.0923, 6800),
    ("Janakpuri A Block", "West", 28.5934, 77.0912, 6550),
    ("Janakpuri B Block", "West", 28.5918, 77.0892, 6500),
    ("Janakpuri C Block", "West", 28.5902, 77.0876, 6450),
    ("Rajouri Garden Extension", "West", 28.6356, 77.0934, 6250),
    ("Raja Garden", "West", 28.6445, 77.1212, 6050),
    ("Mayapuri", "West", 28.6234, 77.1123, 6400),
    ("Naraina", "West", 28.6345, 77.1345, 6100),
    ("Kirti Nagar Extension", "West", 28.6434, 77.1589, 6150),
    ("Paschim Puri", "West", 28.6756, 77.1512, 6900),
    ("Punjabi Bagh", "West", 28.6645, 77.1389, 6500),
    ("Shadipur", "West", 28.6456, 77.1298, 6300),
    
    # North Zone (20 wards)
    ("Model Town", "North", 28.6892, 77.2124, 5800),
    ("Civil Lines", "North", 28.6623, 77.2298, 4500),
    ("Burari", "North", 28.7312, 77.2123, 5600),
    ("Kamla Nagar", "North", 28.6734, 77.2212, 4200),
    ("Timarpur", "North", 28.6845, 77.2034, 4800),
    ("Kingsway Camp", "North", 28.6756, 77.1923, 5000),
    ("Azadpur", "North", 28.7123, 77.1812, 5200),
    ("Wazirabad", "North", 28.7234, 77.2345, 3800),
    ("Badli", "North", 28.7345, 77.1634, 6000),
    ("Rohini Sector 1", "North", 28.7512, 77.0823, 7400),
    ("Rohini Sector 2", "North", 28.7489, 77.0789, 7300),
    ("Rohini Sector 4", "North", 28.7467, 77.0756, 7200),
    ("Rohini Sector 7", "North", 28.7445, 77.0723, 7100),
    ("Rohini Sector 8", "North", 28.7495, 77.0565, 7200),
    ("Rohini Sector 9", "North", 28.7523, 77.0512, 7300),
    ("Adarsh Nagar", "North", 28.7012, 77.1923, 5200),
    ("Malka Ganj", "North", 28.6945, 77.2034, 5000),
    ("Roshanara Road", "North", 28.6876, 77.2145, 4800),
    ("Bara Hindu Rao", "North", 28.6789, 77.2256, 4600),
    ("Subzi Mandi", "North", 28.6823, 77.2189, 4700),
    
    # North West Zone (35 wards)
    ("Pitampura", "North West", 28.6987, 77.1687, 5900),
    ("Ashok Vihar", "North West", 28.7215, 77.1456, 6100),
    ("Shalimar Bagh", "North West", 28.7098, 77.1025, 6400),
    ("Rohini Sector 3", "North West", 28.7567, 77.0823, 7800),
    ("Rohini Sector 5", "North West", 28.7634, 77.0912, 8000),
    ("Rohini Sector 15", "North West", 28.7545, 77.0634, 8200),
    ("Rohini Sector 16", "North West", 28.7512, 77.0456, 8700),
    ("Rohini Sector 22", "North West", 28.7467, 77.0245, 9000),
    ("Rohini Sector 24", "North West", 28.7423, 77.0123, 9200),
    ("Bawana", "North West", 28.7812, 77.0356, 9500),
    ("Narela", "North West", 28.7923, 77.0245, 11000),
    ("Sultanpur", "North West", 28.7123, 77.1123, 6500),
    ("Rithala", "North West", 28.7345, 77.0734, 8500),
    ("Pehladpur", "North West", 28.6987, 77.0812, 7000),
    ("Nangloi", "North West", 28.6789, 77.0634, 8800),
    ("Hari Nagar", "North West", 28.6434, 77.0923, 7200),
    ("Raj Park", "North West", 28.6723, 77.1089, 6800),
    ("Saraswati Vihar", "North West", 28.7123, 77.1345, 6200),
    ("Wazirpur", "North West", 28.6956, 77.1512, 6000),
    ("Rohini Sector 11", "North West", 28.7589, 77.0689, 8300),
    ("Rohini Sector 12", "North West", 28.7612, 77.0645, 8400),
    ("Rohini Sector 13", "North West", 28.7634, 77.0601, 8500),
    ("Rohini Sector 14", "North West", 28.7523, 77.0589, 8600),
    ("Rohini Sector 17", "North West", 28.7489, 77.0434, 8800),
    ("Rohini Sector 18", "North West", 28.7456, 77.0389, 8900),
    ("Rohini Sector 19", "North West", 28.7423, 77.0345, 9000),
    ("Rohini Sector 20", "North West", 28.7398, 77.0301, 9100),
    ("Rohini Sector 21", "North West", 28.7376, 77.0256, 9200),
    ("Rohini Sector 23", "North West", 28.7401, 77.0189, 9300),
    ("Rohini Sector 25", "North West", 28.7434, 77.0156, 9400),
    ("Mangolpuri", "North West", 28.7234, 77.0989, 7800),
    ("Sultanpuri", "North West", 28.7145, 77.0823, 8200),
    ("Kirari", "North West", 28.7023, 77.0756, 8400),
    ("Kanjhawala", "North West", 28.6898, 77.0689, 8600),
    ("Bijwasan", "North West", 28.5312, 77.1156, 9200),
    
    # South West Zone (25 wards)
    ("Dwarka Sector 1", "South West", 28.5789, 77.0912, 8700),
    ("Dwarka Sector 2", "South West", 28.5767, 77.0878, 8800),
    ("Dwarka Sector 3", "South West", 28.5745, 77.0845, 8900),
    ("Dwarka Sector 4", "South West", 28.5723, 77.0812, 9000),
    ("Dwarka Sector 5", "South West", 28.5701, 77.0778, 9100),
    ("Dwarka Sector 6", "South West", 28.5634, 77.0734, 8800),
    ("Dwarka Sector 7", "South West", 28.5612, 77.0701, 8900),
    ("Dwarka Sector 8", "South West", 28.5598, 77.0667, 9000),
    ("Dwarka Sector 9", "South West", 28.5576, 77.0634, 9100),
    ("Dwarka Sector 10", "South West", 28.5545, 77.0912, 9000),
    ("Dwarka Sector 11", "South West", 28.5523, 77.0589, 9200),
    ("Dwarka Sector 12", "South West", 28.5501, 77.0556, 9300),
    ("Dwarka Sector 13", "South West", 28.5478, 77.0523, 9400),
    ("Dwarka Sector 14", "South West", 28.5456, 77.0823, 9200),
    ("Dwarka Sector 21", "South West", 28.5822, 77.0500, 8500),
    ("Dwarka Sector 22", "South West", 28.5367, 77.0456, 9500),
    ("Dwarka Sector 23", "South West", 28.5345, 77.0423, 9600),
    ("Dwarka Sector 24", "South West", 28.5323, 77.0389, 9700),
    ("Dwarka Sector 25", "South West", 28.5301, 77.0356, 9800),
    ("Kapashera", "South West", 28.5234, 77.1023, 9800),
    ("Dabri", "South West", 28.6123, 77.1023, 8200),
    ("Mahavir Enclave", "South West", 28.6012, 77.0912, 8400),
    ("Dashrath Puri", "South West", 28.5891, 77.0812, 8600),
    ("Chhawla", "South West", 28.5767, 77.0634, 8900),
    ("Najafgarh Extension", "South West", 28.6123, 77.0356, 8100),
    
    # South East Zone (20 wards)
    ("Lajpat Nagar", "South East", 28.5677, 77.2433, 4200),
    ("Okhla Phase 1", "South East", 28.5355, 77.2656, 3800),
    ("Okhla Phase 2", "South East", 28.5334, 77.2689, 3900),
    ("Okhla Phase 3", "South East", 28.5312, 77.2723, 4000),
    ("Defence Colony", "South East", 28.5543, 77.2345, 4100),
    ("Hauz Khas", "South East", 28.5434, 77.2056, 4800),
    ("Jangpura", "South East", 28.5978, 77.2245, 3900),
    ("New Friends Colony", "South East", 28.5456, 77.2789, 4000),
    ("Jasola Vihar", "South East", 28.5323, 77.2891, 4300),
    ("Shaheen Bagh", "South East", 28.5234, 77.3012, 4100),
    ("Kalindi Kunj", "South East", 28.5345, 77.3123, 3900),
    ("Abul Fazal Enclave", "South East", 28.5212, 77.3234, 4200),
    ("Batla House", "South East", 28.5289, 77.3189, 4150),
    ("Zakir Nagar", "South East", 28.5312, 77.3145, 4100),
    ("Johori Farm", "South East", 28.5245, 77.3089, 4050),
    ("Jamia Nagar", "South East", 28.5467, 77.2956, 4400),
    ("Okhla Industrial Area", "South East", 28.5389, 77.2823, 4000),
    ("Madanpur Khadar", "South East", 28.5156, 77.2912, 4500),
    ("Noonka", "South East", 28.5123, 77.2989, 4600),
    ("Haji Colony", "South East", 28.5089, 77.3045, 4700),
]

def generate_record(ward_info, scenario_type='normal', cell_id=1000):
    """Generate one record with specified scenario"""
    ward_name, zone, base_lat, base_lng, base_dist = ward_info
    
    # Add small variations to coordinates for same ward
    lat = base_lat + random.uniform(-0.01, 0.01)
    lng = base_lng + random.uniform(-0.01, 0.01)
    dist_yamuna = base_dist + random.uniform(-200, 200)
    
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
    
    # Generate scenario-based conditions (but don't set risk_level yet)
    if scenario_type == 'extreme_rain':
        rain_24h = random.uniform(110, 150)
        rain_3h = rain_24h * random.uniform(0.50, 0.65)
        yamuna = random.uniform(204.5, 206.0)
        blockage_risk = random.uniform(0.75, 0.95)
        drain_capacity = random.uniform(0.45, 0.60)
    elif scenario_type == 'heavy_rain':
        rain_24h = random.uniform(85, 110)
        rain_3h = rain_24h * random.uniform(0.45, 0.60)
        yamuna = random.uniform(204.2, 204.8)
        blockage_risk = random.uniform(0.65, 0.80)
        drain_capacity = random.uniform(0.50, 0.68)
    elif scenario_type == 'moderate_rain':
        rain_24h = random.uniform(50, 85)
        rain_3h = rain_24h * random.uniform(0.40, 0.55)
        yamuna = random.uniform(203.8, 204.5)
        blockage_risk = random.uniform(0.50, 0.70)
        drain_capacity = random.uniform(0.60, 0.75)
    elif scenario_type == 'light_rain':
        rain_24h = random.uniform(25, 50)
        rain_3h = rain_24h * random.uniform(0.35, 0.50)
        yamuna = random.uniform(203.2, 203.8)
        blockage_risk = random.uniform(0.40, 0.60)
        drain_capacity = random.uniform(0.65, 0.82)
    else:  # normal/dry
        rain_24h = random.uniform(5, 25)
        rain_3h = rain_24h * random.uniform(0.30, 0.45)
        yamuna = random.uniform(203.0, 203.5)
        blockage_risk = random.uniform(0.30, 0.50)
        drain_capacity = random.uniform(0.72, 0.88)
    
    rain_1h = rain_3h * random.uniform(0.28, 0.42)
    rain_forecast_3h = rain_3h * random.uniform(1.05, 1.25)
    
    # Historical data - INDEPENDENT of current risk (based on ward characteristics)
    # Wards with poor drainage/elevation are more likely to have flooded before
    historical_risk_factor = (1 - drain_capacity) * 0.5 + (210 - elevation) / 50 if elevation < 210 else 0
    historical_risk_factor = max(0, min(1, historical_risk_factor))
    
    flooded_before = random.choices([0, 1], weights=[1 - historical_risk_factor, historical_risk_factor])[0]
    if flooded_before:
        flood_frequency = random.randint(1, 6)  # Independent of current risk
    else:
        flood_frequency = random.randint(0, 1)  # Some wards never flooded
    
    # Calculate risk_level based on ACTUAL CONDITIONS, not from outcomes
    # Risk should be determined by weather + infrastructure, not by observed outcomes
    risk_score = 0
    
    # Rain contribution
    if rain_24h > 100:
        risk_score += 2
    elif rain_24h > 70:
        risk_score += 1.5
    elif rain_24h > 50:
        risk_score += 1
    
    # Yamuna level contribution
    if yamuna > 204.8:
        risk_score += 1.5
    elif yamuna > 204.3:
        risk_score += 1
    elif yamuna > 204.0:
        risk_score += 0.5
    
    # Drainage issues
    if blockage_risk > 0.80:
        risk_score += 1.5
    elif blockage_risk > 0.65:
        risk_score += 1
    
    if drain_capacity < 0.55:
        risk_score += 1
    elif drain_capacity < 0.65:
        risk_score += 0.5
    
    # Elevation (lower = higher risk)
    if elevation < 210:
        risk_score += 0.5
    elif elevation < 212:
        risk_score += 0.3
    
    # Historical context (minor contribution, but can be used)
    if flooded_before and flood_frequency > 3:
        risk_score += 0.3
    
    # Determine final risk level
    if risk_score >= 4.5:
        risk_level = 2  # Danger
    elif risk_score >= 2.5:
        risk_level = 1  # Warning
    else:
        risk_level = 0  # Safe
    
    # Add some randomness to avoid perfect correlation (5% noise)
    if random.random() < 0.05:
        if risk_level == 2:
            risk_level = random.choice([1, 2])
        elif risk_level == 0:
            risk_level = random.choice([0, 1])
        else:
            risk_level = random.choice([0, 1, 2])
    
    # Citizen reports - based on ACTUAL CONDITIONS, not risk_level (to avoid leakage)
    # Reports come from actual water depth which depends on rain, drainage, elevation
    estimated_depth = (rain_24h * 0.4) + ((yamuna - 203.0) * 15) - (drain_capacity * 30) - ((elevation - 205) * 2)
    estimated_depth = max(0, estimated_depth)
    
    if estimated_depth > 40:
        reports = random.randint(8, 20)
        avg_depth = random.uniform(30, 60)
        max_depth = random.uniform(50, 100)
    elif estimated_depth > 20:
        reports = random.randint(3, 12)
        avg_depth = random.uniform(15, 35)
        max_depth = random.uniform(25, 55)
    elif estimated_depth > 5:
        reports = random.randint(0, 5)
        avg_depth = random.uniform(5, 18) if reports > 0 else 0
        max_depth = random.uniform(10, 25) if reports > 0 else 0
    else:
        reports = random.randint(0, 2)
        avg_depth = random.uniform(0, 8) if reports > 0 else 0
        max_depth = random.uniform(0, 12) if reports > 0 else 0
    
    # Add realistic noise - not everything is deterministic
    reports = max(0, reports + random.randint(-2, 2))
    avg_depth = max(0, avg_depth + random.uniform(-3, 3))
    max_depth = max(0, max_depth + random.uniform(-5, 5))
    
    return {
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

def generate_1000_records():
    """Generate ~1000 records with balanced distribution"""
    records = []
    scenarios = ['normal', 'light_rain', 'moderate_rain', 'heavy_rain', 'extreme_rain']
    scenario_weights = [0.25, 0.25, 0.25, 0.15, 0.10]  # More normal/light, fewer extreme
    
    cell_id = 1000
    
    # Generate multiple records per ward with different scenarios
    records_per_ward = 1000 // len(BASE_WARDS)  # ~6-7 per ward
    extra_records = 1000 % len(BASE_WARDS)
    
    for ward_info in BASE_WARDS:
        num_records = records_per_ward + (1 if extra_records > 0 else 0)
        extra_records -= 1
        
        for i in range(num_records):
            scenario = random.choices(scenarios, weights=scenario_weights)[0]
            record = generate_record(ward_info, scenario, cell_id)
            records.append(record)
            cell_id += 1
    
    # Ensure exactly 1000 records
    while len(records) < 1000:
        ward_info = random.choice(BASE_WARDS)
        scenario = random.choices(scenarios, weights=scenario_weights)[0]
        record = generate_record(ward_info, scenario, cell_id)
        records.append(record)
        cell_id += 1
    
    # Shuffle for randomness
    random.shuffle(records)
    
    # Re-number cell_ids sequentially
    for i, record in enumerate(records, start=1000):
        record['cell_id'] = i
    
    return records[:1000]  # Ensure exactly 1000

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
    print("Generating 1000 flood data records...")
    print("=" * 60)
    
    # Set seed for reproducibility (optional)
    random.seed(42)
    
    records = generate_1000_records()
    
    # Get CSV path
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'delhi_flood_data.csv')
    
    write_csv(records, csv_path)
    
    print(f"[SUCCESS] Generated {len(records)} records")
    print(f"[INFO] File: {csv_path}")
    
    # Print distribution
    risk_counts = {}
    zone_counts = {}
    for record in records:
        risk = record['flood_risk_level']
        zone = record['zone']
        risk_counts[risk] = risk_counts.get(risk, 0) + 1
        zone_counts[zone] = zone_counts.get(zone, 0) + 1
    
    print(f"\n[STATS] Risk Level Distribution:")
    for risk in sorted(risk_counts.keys()):
        count = risk_counts[risk]
        label = ['Safe', 'Warning', 'Danger'][risk]
        print(f"   {label} ({risk}): {count} ({count/10:.1f}%)")
    
    print(f"\n[STATS] Zone Distribution:")
    for zone in sorted(zone_counts.keys()):
        count = zone_counts[zone]
        print(f"   {zone}: {count} records")
    
    print(f"\n[SUCCESS] Dataset ready for training!")
    print(f"Run: python ../backend/train_model.py")
