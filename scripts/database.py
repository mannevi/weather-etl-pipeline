import sqlite3
import os

# This is where your database file will be created
DB_PATH = "data/weather.db"


def get_connection():
    """
    Creates and returns a connection to the SQLite database.
    If the database file doesn't exist, SQLite creates it automatically.
    Think of this like logging into a database server at a company.
    """
    connection = sqlite3.connect(DB_PATH)
    return connection


def create_table():
    """
    Creates the weather table if it doesn't already exist.
    This is your SQL CREATE TABLE — written inside Python.
    """
    connection = get_connection()

    # cursor is your tool to send SQL commands to the database
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            city            TEXT,
            temperature_c   REAL,
            temperature_f   REAL,
            windspeed_kmh   REAL,
            wind_category   TEXT,
            weather_label   TEXT
        )
    """)

    # Save the change to the database file
    connection.commit()
    print(" Table created (or already exists).")

    # Always close the connection when done
    connection.close()


def clear_table():
    """
    Deletes all rows before inserting fresh data.
    This prevents duplicate rows every time you run the pipeline.
    At MNCs this is called an 'upsert' or 'truncate and reload' pattern.
    """
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM weather")

    connection.commit()
    print("Old data cleared. Ready for fresh load.")
    connection.close()


# Test the connection directly
if __name__ == "__main__":
    print("Testing database connection...")
    create_table()

    # Verify the file was created
    if os.path.exists(DB_PATH):
        print(f"Database file created at: {DB_PATH}")
    else:
        print(" Something went wrong. File not found.")