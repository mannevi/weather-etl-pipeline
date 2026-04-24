from scripts.database import get_connection


def run_query(description, query):
    """
    Reusable function to run any SQL query and print results.
    One function handles all queries — clean and professional.
    """
    connection = get_connection()
    cursor = connection.cursor()

    print(f"\n{'='*50}")
    print(f" {description}")
    print(f"{'='*50}")

    cursor.execute(query)
    rows = cursor.fetchall()

    # Print column names first
    columns = [description[0] for description in cursor.description]
    print(" | ".join(columns))
    print("-" * 50)

    # Print each row
    for row in rows:
        print(" | ".join(str(value) for value in row))

    connection.close()
    return rows


if __name__ == "__main__":

    # ── QUERY 1 ──────────────────────────────────────
    # Business Question: What is the full weather snapshot?
    # SQL concepts: SELECT, ORDER BY DESC
    run_query(
        "Full Weather Snapshot — All Cities",
        """
        SELECT city, temperature_f, windspeed_kmh, 
               wind_category, weather_label
        FROM weather
        ORDER BY temperature_f DESC
        """
    )

    # ── QUERY 2 ──────────────────────────────────────
    # Business Question: Which city is hottest and coldest?
    # SQL concepts: MAX, MIN aggregations
    run_query(
        "Hottest and Coldest City",
        """
        SELECT 
            MAX(temperature_f) AS hottest_temp_f,
            MIN(temperature_f) AS coldest_temp_f
        FROM weather
        """
    )

    # ── QUERY 3 ──────────────────────────────────────
    # Business Question: What is the average temperature 
    # and wind speed across all cities?
    # SQL concepts: AVG, ROUND
    run_query(
        "Average Temperature and Wind Speed",
        """
        SELECT 
            ROUND(AVG(temperature_f), 1) AS avg_temp_f,
            ROUND(AVG(windspeed_kmh), 1) AS avg_windspeed
        FROM weather
        """
    )

    # ── QUERY 4 ──────────────────────────────────────
    # Business Question: How many cities fall into each 
    # wind category?
    # SQL concepts: GROUP BY, COUNT, ORDER BY
    run_query(
        "Cities Count by Wind Category",
        """
        SELECT wind_category, COUNT(*) AS city_count
        FROM weather
        GROUP BY wind_category
        ORDER BY city_count DESC
        """
    )

    # ── QUERY 5 ──────────────────────────────────────
    # Business Question: Which cities are warmer than 
    # the average temperature?
    # SQL concepts: Subquery, WHERE, ORDER BY
    run_query(
        "Cities Warmer Than Average",
        """
        SELECT city, temperature_f
        FROM weather
        WHERE temperature_f > (SELECT AVG(temperature_f) FROM weather)
        ORDER BY temperature_f DESC
        """
    )

    # ── QUERY 6 ──────────────────────────────────────
    # Business Question: Give each city a heat label
    # SQL concepts: CASE WHEN — exactly like your SQL notes
    run_query(
        "City Heat Classification",
        """
        SELECT city, temperature_f,
            CASE
                WHEN temperature_f >= 75 THEN 'Hot'
                WHEN temperature_f >= 65 THEN 'Warm'
                WHEN temperature_f >= 50 THEN 'Mild'
                ELSE 'Cold'
            END AS heat_label
        FROM weather
        ORDER BY temperature_f DESC
        """
    )