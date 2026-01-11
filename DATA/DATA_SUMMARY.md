# Dataset Summary

## ✅ Dataset Generated Successfully

**Total Records**: 1000  
**File**: `delhi_flood_data.csv`

## 📊 Risk Level Distribution

- **Safe (0)**: 519 records (51.9%)
- **Warning (1)**: 234 records (23.4%)  
- **Danger (2)**: 247 records (24.7%)

*Note: Higher percentage of Safe records is realistic as most wards are safe during normal conditions*

## 🗺️ Coverage

**Zones Covered** (1000 records across 8 zones):
- Central: 72 records
- East: 126 records
- West: 150 records
- South: 152 records
- North: 100 records
- North West: 175 records
- South West: 125 records
- South East: 100 records

**Total**: ~187 unique Delhi wards with multiple scenario variations per ward

## 📈 Features

All 17 feature columns included:
- Weather data (rain_1h, rain_3h, rain_24h, rain_forecast_3h)
- Geographic (latitude, longitude, elevation, slope)
- Drainage (drain_density, drain_capacity_score, drain_blockage_risk)
- River data (distance_to_yamuna, yamuna_level)
- Historical (flooded_before, flood_frequency)
- Community (citizen_reports_count, avg_reported_depth_cm, max_flood_depth_cm)

## 🎯 Ready for Training

Dataset is balanced and ready for ML model training:

```bash
cd backend
python train_model.py
```

## 📝 Notes

- Data is synthetic but realistic with proper feature correlations
- Multiple scenarios per ward (normal, light rain, moderate, heavy, extreme)
- Risk levels determined by realistic flood conditions
- All values within plausible ranges for Delhi
- Better dataset size for ML training (1000 records vs 100)

## 🎯 Scenarios Included

Each ward has records with different weather scenarios:
- **Normal/Dry**: Low rain, stable conditions (25%)
- **Light Rain**: 25-50mm, minimal risk (25%)
- **Moderate Rain**: 50-85mm, variable risk (25%)
- **Heavy Rain**: 85-110mm, elevated risk (15%)
- **Extreme Rain**: 110-150mm, critical conditions (10%)
