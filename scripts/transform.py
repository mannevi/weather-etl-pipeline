# This is the Python equivalent of SQL CASE WHEN
# You are mapping a number to a human-readable label

def get_weather_label(code):
    """
    Converts a numeric weathercode from the API
    into a human-readable description.
    """
    if code == 0:
        return "Clear Sky"
    elif code == 1:
        return "Mainly Clear"
    elif code == 2:
        return "Partly Cloudy"
    elif code == 3:
        return "Overcast"
    elif code in [61, 63, 65]:
        return "Rainy"
    elif code in [71, 73, 75]:
        return "Snowy"
    elif code in [95, 96, 99]:
        return "Thunderstorm"
    else:
        return "Unknown"


def get_wind_category(windspeed):
    """
    Converts numeric windspeed into a category.
    Think of this as a CASE WHEN on a number range.
    """
    if windspeed < 10:
        return "Calm"
    elif windspeed < 20:
        return "Moderate"
    elif windspeed < 35:
        return "High Wind"
    else:
        return "Storm"


def celsius_to_fahrenheit(celsius):
    """
    Converts temperature from Celsius to Fahrenheit.
    The API always returns Celsius.
    """
    return round((celsius * 9/5) + 32, 1)


def transform(raw_data):
    """
    Takes the raw list of city dictionaries from extract.py
    and returns a cleaned, enriched version.
    One dictionary in → one richer dictionary out.
    """
    transformed = []

    for row in raw_data:
        clean_row = {
            "city":             row["city"],
            "temperature_c":    row["temperature"],
            "temperature_f":    celsius_to_fahrenheit(row["temperature"]),
            "windspeed_kmh":    row["windspeed"],
            "wind_category":    get_wind_category(row["windspeed"]),
            "weather_label":    get_weather_label(row["weathercode"]),
        }
        transformed.append(clean_row)

    print(f" Transformed {len(transformed)} records.")
    return transformed


# Test it directly
if __name__ == "__main__":
    # Simulating what extract.py returns — so you can test independently
    sample_data = [
        {"city": "New York",   "temperature": 17.0, "windspeed": 12.0, "weathercode": 0},
        {"city": "Chicago",    "temperature": 19.8, "windspeed": 11.6, "weathercode": 0},
        {"city": "Houston",    "temperature": 23.0, "windspeed": 12.0, "weathercode": 3},
        {"city": "Phoenix",    "temperature": 21.1, "windspeed": 4.7,  "weathercode": 1},
        {"city": "Cincinnati", "temperature": 22.6, "windspeed": 9.1,  "weathercode": 0},
    ]

    result = transform(sample_data)
    for row in result:
        print(row)