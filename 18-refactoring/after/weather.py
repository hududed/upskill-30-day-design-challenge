from typing import Any, Callable
import requests

HttpGetFn = Callable[[str], dict[str, Any] | None]


def http_get(url: str) -> dict[str, Any] | None:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    return None


def get_complete_forecast(
    http_get_fn: HttpGetFn, api_key: str, city: str
) -> dict[str, Any] | None:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    full_weather_forecast = http_get_fn(url)
    if full_weather_forecast and "main" in full_weather_forecast:
        return full_weather_forecast
    print(
        f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
    )
    return None


def get_temperature(full_weather_forecast: dict[str, Any]) -> float:
    temperature = full_weather_forecast["main"]["temp"]
    return temperature - 273.15  # convert from Kelvin to Celsius


def get_humidity(full_weather_forecast: dict[str, Any]) -> int:
    return full_weather_forecast["main"]["humidity"]


def get_wind_speed(full_weather_forecast: dict[str, Any]) -> tuple[float, int]:
    return full_weather_forecast["wind"]["speed"]


def get_wind_direction(full_weather_forecast: dict[str, Any]) -> tuple[float, int]:
    return full_weather_forecast["wind"]["deg"]
