import pandas as pd

df = pd.read_csv('delhi_flood_data.csv')
wards = sorted(df['ward_name'].unique().tolist())

print("const WARDS = [")
for ward in wards:
    print(f"  '{ward}',")
print("];")
