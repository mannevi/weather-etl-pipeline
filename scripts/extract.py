import requests

# Define the 5 cities with coordinates
CITIES = [
    {"city": "New York",   "lat": 40.71, "lon": -74.01},
    {"city": "Chicago",    "lat": 41.85, "lon": -87.65},
    {"city": "Houston",    "lat": 29.76, "lon": -95.37},
    {"city": "Phoenix",    "lat": 33.45, "lon": -112.07},
    {"city": "Cincinnati", "lat": 39.10, "lon": -84.51},
]

def fetch_weather(city_name, lat, lon):
    """
    Fetches current weather data for a given city
    using the Open-Meteo free API.
    """
    url = (
        f"https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        f"&current_weather=true"
    )

    response = requests.get(url)

    # Check if the API call was successful
    if response.status_code == 200:
        data = response.json()
        current = data["current_weather"]

        # Build a clean dictionary for this city
        result = {
            "city":        city_name,
            "temperature": current["temperature"],
            "windspeed":   current["windspeed"],
            "weathercode": current["weathercode"],
        }
        return result
    else:
        print(f"Failed to fetch data for {city_name}. Status: {response.status_code}")
        return None


def extract_all_cities():
    """
    Loops through all cities and collects weather data.
    Returns a list of dictionaries — one per city.
    """
    all_weather = []

    for city in CITIES:
        print(f"Fetching weather for {city['city']}...")
        result = fetch_weather(city["city"], city["lat"], city["lon"])

        if result is not None:
            all_weather.append(result)

    print(f"\n Successfully fetched data for {len(all_weather)} cities.")
    return all_weather


# Run it directly to test
if __name__ == "__main__":
    weather_data = extract_all_cities()
    for row in weather_data:
        print(row)