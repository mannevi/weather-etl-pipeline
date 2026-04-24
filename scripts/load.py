import sqlite3
import csv
import os
from datetime import datetime
from scripts.database import get_connection, clear_table

DB_PATH = "data/weather.db"


def load_to_database(transformed_data):
    """
    Takes the cleaned list of city dictionaries
    and inserts each one as a row into the weather table.
    """
    # Clear old data first — fresh load every time
    clear_table()

    connection = get_connection()
    cursor = connection.cursor()

    for row in transformed_data:
        cursor.execute("""
            INSERT INTO weather (
                city,
                temperature_c,
                temperature_f,
                windspeed_kmh,
                wind_category,
                weather_label
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["city"],
            row["temperature_c"],
            row["temperature_f"],
            row["windspeed_kmh"],
            row["wind_category"],
            row["weather_label"],
        ))

    connection.commit()
    connection.close()

    print(f"{len(transformed_data)} rows loaded into database.")


def save_raw_backup(transformed_data):
    """
    Saves a CSV backup of what was loaded and when.
    This is your audit trail — standard practice at any MNC.
    Every pipeline run gets its own timestamped file.
    """
    # Create a timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"data/weather_backup_{timestamp}.csv"

    # Get the column names from the first dictionary
    columns = transformed_data[0].keys()

    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(transformed_data)

    print(f" Backup saved to: {filename}")


def verify_load():
    """
    After loading, reads back from the database and prints
    what was actually stored. Confirms load was successful.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM weather")
    rows = cursor.fetchall()

    print(f"\n Rows in database after load: {len(rows)}")
    for row in rows:
        print(row)

    connection.close()


# Run the full load step
if __name__ == "__main__":
    # Simulating transformed data — same as what transform.py outputs
    sample_data = [
        {"city": "New York",   "temperature_c": 17.0, "temperature_f": 62.6, "windspeed_kmh": 12.0, "wind_category": "Moderate", "weather_label": "Clear Sky"},
        {"city": "Chicago",    "temperature_c": 19.8, "temperature_f": 67.6, "windspeed_kmh": 11.6, "wind_category": "Moderate", "weather_label": "Clear Sky"},
        {"city": "Houston",    "temperature_c": 23.0, "temperature_f": 73.4, "windspeed_kmh": 12.0, "wind_category": "Moderate", "weather_label": "Overcast"},
        {"city": "Phoenix",    "temperature_c": 21.1, "temperature_f": 70.0, "windspeed_kmh": 4.7,  "wind_category": "Calm",     "weather_label": "Mainly Clear"},
        {"city": "Cincinnati", "temperature_c": 22.6, "temperature_f": 72.7, "windspeed_kmh": 9.1,  "wind_category": "Calm",     "weather_label": "Clear Sky"},
    ]

    load_to_database(sample_data)
    save_raw_backup(sample_data)
    verify_load()