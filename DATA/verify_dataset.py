import pandas as pd

df = pd.read_csv('delhi_flood_data.csv')

print("=" * 60)
print("DATASET VERIFICATION")
print("=" * 60)
print(f"\nTotal Records: {len(df)}")
print(f"Unique Wards: {df['ward_name'].nunique()}")
print(f"Unique Zones: {df['zone'].nunique()}")

print(f"\nRisk Level Distribution:")
risk_dist = df['flood_risk_level'].value_counts().sort_index()
for risk, count in risk_dist.items():
    label = ['Safe', 'Warning', 'Danger'][int(risk)]
    print(f"  {label} ({int(risk)}): {count} ({count/len(df)*100:.1f}%)")

print(f"\nZone Distribution:")
zone_dist = df['zone'].value_counts()
for zone, count in zone_dist.items():
    print(f"  {zone}: {count} records")

print(f"\nColumn Count: {len(df.columns)}")
print(f"Columns: {', '.join(df.columns.tolist()[:5])}... (+{len(df.columns)-5} more)")

print(f"\nData Range Check:")
print(f"  Rain (24h): {df['rain_24h_mm'].min():.1f} - {df['rain_24h_mm'].max():.1f} mm")
print(f"  Yamuna Level: {df['yamuna_level_m'].min():.2f} - {df['yamuna_level_m'].max():.2f} m")
print(f"  Elevation: {df['elevation_m'].min():.1f} - {df['elevation_m'].max():.1f} m")

print("\n" + "=" * 60)
print("[SUCCESS] Dataset verification complete!")
print("=" * 60)
