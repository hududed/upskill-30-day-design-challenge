from functools import partial
from typing import Any, Callable

import requests

API_KEY = "123456789"

HttpGet = Callable[[str], Any]

class CityNotFoundError(Exception):
    pass

def get(url: str) -> Any:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()

def get_forecast(http_get: HttpGet, api_key: str, city: str) -> dict[str, Any]:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = http_get(url)
    if "main" not in response:
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response

def get_temperature(full_weather_forecast: dict[str, Any]) -> float:
    temperature = full_weather_forecast["main"]["temp"]
    return temperature - 273.15  # convert from Kelvin to Celsius

def get_humidity(full_weather_forecast: dict[str, Any]) -> int:
    return full_weather_forecast["main"]["humidity"]

def get_wind_speed(full_weather_forecast: dict[str, Any]) -> float:
    return full_weather_forecast["wind"]["speed"]

def get_wind_direction(full_weather_forecast: dict[str, Any]) -> int:
    return full_weather_forecast["wind"]["deg"]


def main() -> None:
    # here's how we build a weather forecast function
    # that only needs a city name to work using lambda

    get_weather = lambda city: get_forecast(get, API_KEY, city)

    # or using partial
    get_weather = partial(get_forecast, get, API_KEY)

    city = "Laramie"
    weather_forecast = get_weather(city)

    print(f"The current temperature in {city} is {get_temperature(weather_forecast):.1f} °C.")
    print(f"The current humidity in {city} is {get_humidity(weather_forecast)}%.")
    print(
        f"The current wind speed in {city} is {get_wind_speed(weather_forecast)} m/s from direction {get_wind_direction(weather_forecast)} degrees."
    )


if __name__ == "__main__":
    main()
