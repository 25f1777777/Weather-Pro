import requests


BASE_URL = "https://api.openweathermap.org/data/2.5"
GEOCODE_URL = "https://api.openweathermap.org/geo/1.0/direct"


def get_coordinates(city, api_key):
    """
    Get latitude and longitude from city name.
    """

    params = {
        "q": city,
        "limit": 1,
        "appid": api_key
    }

    response = requests.get(
        GEOCODE_URL,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if not data:
        raise Exception(
            f"City '{city}' not found."
        )

    return {
        "lat": data[0]["lat"],
        "lon": data[0]["lon"]
    }


def get_current_weather(
    city,
    api_key
):
    """
    Get current weather by city.
    """

    endpoint = f"{BASE_URL}/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        endpoint,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_forecast(
    city,
    api_key
):
    """
    Get 5-day forecast.
    """

    endpoint = f"{BASE_URL}/forecast"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }

    response = requests.get(
        endpoint,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_air_quality(
    lat,
    lon,
    api_key
):
    """
    Get AQI data.
    """

    endpoint = (
        f"{BASE_URL}/air_pollution"
    )

    params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key
    }

    response = requests.get(
        endpoint,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()


def get_aqi_label(aqi):
    """
    Convert AQI number to text.
    """

    labels = {
        1: "Good",
        2: "Fair",
        3: "Moderate",
        4: "Poor",
        5: "Very Poor"
    }

    return labels.get(
        aqi,
        "Unknown"
    )