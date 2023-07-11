from typing import Any

import requests

API_KEY = "0123456789"

class CityNotFoundError(Exception):
    pass

class WeatherService:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.full_weather_forecast: dict[str, Any] = {}

    def retrieve_forecast(self, city: str) -> None:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = requests.get(url, timeout=5).json()
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )

        self.full_weather_forecast = response

    @property
    def temperature(self) -> float:
        return self.full_weather_forecast["main"]["temp"] - 273.15

def main() -> None:
    city = "Laramie"
    client = WeatherService(api_key=API_KEY)
    client.retrieve_forecast(city)
    print(f"The current temperature in {city} is {client.temperature:.1f} °C.")

if __name__ == "__main__":
    main()