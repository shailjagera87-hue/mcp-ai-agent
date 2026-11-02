from datetime import date, timedelta

from mcp_servers.weather_server.schemas import (
    WeatherRequest,
    ForecastRequest
)


# Mock weather dataset
WEATHER_DATA = {
    "delhi": {
        "temperature": 32,
        "condition": "Sunny",
        "humidity": 45,
        "wind_speed": 12
    },

    "mumbai": {
        "temperature": 29,
        "condition": "Cloudy",
        "humidity": 75,
        "wind_speed": 18
    },

    "london": {
        "temperature": 16,
        "condition": "Rainy",
        "humidity": 80,
        "wind_speed": 15
    },

    "new york": {
        "temperature": 21,
        "condition": "Partly Cloudy",
        "humidity": 55,
        "wind_speed": 10
    }
}


def get_weather(city: str) -> dict:
    """Retrieve current weather for a city."""

    request = WeatherRequest(city=city)

    normalized_city = request.city.strip().lower()

    weather = WEATHER_DATA.get(normalized_city)

    if weather is None:
        return {
            "success": False,
            "error": "CITY_NOT_FOUND",
            "message": f"No mock weather data available for {city}"
        }

    return {
        "success": True,
        "city": city.strip(),
        "temperature_celsius": weather["temperature"],
        "condition": weather["condition"],
        "humidity_percent": weather["humidity"],
        "wind_speed_kmh": weather["wind_speed"]
    }


def get_forecast(city: str, days: int = 3) -> dict:
    """Retrieve a mock weather forecast."""

    request = ForecastRequest(city=city, days=days)

    normalized_city = request.city.strip().lower()

    weather = WEATHER_DATA.get(normalized_city)

    if weather is None:
        return {
            "success": False,
            "error": "CITY_NOT_FOUND",
            "message": f"No forecast data available for {city}"
        }

    forecast = []

    for day in range(request.days):

        forecast_date = date.today() + timedelta(days=day)

        forecast.append({
            "date": forecast_date.isoformat(),
            "temperature_celsius": (
                weather["temperature"] + day
            ),
            "condition": weather["condition"]
        })

    return {
        "success": True,
        "city": city.strip(),
        "forecast": forecast
    }