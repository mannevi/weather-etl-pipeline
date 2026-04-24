import csv
import os
from datetime import datetime
from scripts.database import get_connection


def export_query_to_csv(description, query, filename):
    """
    Runs a SQL query and saves the results as a CSV file.
    Every report gets a timestamp so old reports are never overwritten.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(query)
    rows = cursor.fetchall()

    # Pull column names from the cursor
    columns = [desc[0] for desc in cursor.description]

    # Build timestamped output path
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = f"output/{filename}_{timestamp}.csv"

    with open(filepath, "w", newline="") as f:
        writer = csv.writer(f)

        # Write header row first
        writer.writerow(columns)

        # Write all data rows
        writer.writerows(rows)

    connection.close()
    print(f"'{description}' exported to: {filepath}")
    return filepath


if __name__ == "__main__":

    # ── REPORT 1 ─────────────────────────────────────
    # Full weather snapshot sorted by temperature
    export_query_to_csv(
        "Full Weather Snapshot",
        """
        SELECT city, temperature_f, windspeed_kmh,
               wind_category, weather_label
        FROM weather
        ORDER BY temperature_f DESC
        """,
        "report_full_snapshot"
    )

    # ── REPORT 2 ─────────────────────────────────────
    # Cities grouped by wind category with count
    export_query_to_csv(
        "Wind Category Summary",
        """
        SELECT wind_category,
               COUNT(*)              AS city_count,
               ROUND(AVG(temperature_f), 1) AS avg_temp_f
        FROM weather
        GROUP BY wind_category
        ORDER BY avg_temp_f DESC
        """,
        "report_wind_summary"
    )

    # ── REPORT 3 ─────────────────────────────────────
    # Full city report with heat label from CASE WHEN
    export_query_to_csv(
        "City Heat Classification Report",
        """
        SELECT city,
               temperature_f,
               windspeed_kmh,
               weather_label,
               CASE
                   WHEN temperature_f >= 75 THEN 'Hot'
                   WHEN temperature_f >= 65 THEN 'Warm'
                   WHEN temperature_f >= 50 THEN 'Mild'
                   ELSE 'Cold'
               END AS heat_label
        FROM weather
        ORDER BY temperature_f DESC
        """,
        "report_heat_classification"
    )

    print("\n All reports exported to the output/ folder.")