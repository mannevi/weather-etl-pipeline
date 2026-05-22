import os
os.makedirs("data", exist_ok=True)
os.makedirs("output", exist_ok=True)

from scripts.database import create_table, clear_table
from scripts.extract import extract_all_cities
from scripts.transform import transform
from scripts.load import load_to_database, save_raw_backup, verify_load
from scripts.export import export_query_to_csv

print("=== Weather ETL Pipeline Starting ===")

print("\n[1/5] Setting up database...")
create_table()

print("\n[2/5] Extracting weather data...")
raw_data = extract_all_cities()

print("\n[3/5] Transforming data...")
transformed_data = transform(raw_data)

print("\n[4/5] Loading into SQLite...")
load_to_database(transformed_data)
save_raw_backup(transformed_data)
verify_load()

print("\n[5/5] Exporting reports...")
export_query_to_csv("Full Weather Snapshot",
    "SELECT city, temperature_f, windspeed_kmh, wind_category, weather_label FROM weather ORDER BY temperature_f DESC",
    "report_full_snapshot")

export_query_to_csv("Wind Category Summary",
    "SELECT wind_category, COUNT(*) AS city_count, ROUND(AVG(temperature_f),1) AS avg_temp_f FROM weather GROUP BY wind_category ORDER BY avg_temp_f DESC",
    "report_wind_summary")

export_query_to_csv("City Heat Classification",
    "SELECT city, temperature_f, weather_label, CASE WHEN temperature_f >= 75 THEN 'Hot' WHEN temperature_f >= 65 THEN 'Warm' WHEN temperature_f >= 50 THEN 'Mild' ELSE 'Cold' END AS heat_label FROM weather ORDER BY temperature_f DESC",
    "report_heat_classification")

print("\n=== Pipeline Complete ===")