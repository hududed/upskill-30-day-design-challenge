from typing import Any, Protocol

import requests

API_KEY = "0123456789"

class CityNotFoundError(Exception):
    pass

class HttpClient(Protocol):
    def get(self, url: str) -> dict[str, Any]:
        ...

class RequestsClient:
    def get(self, url: str) -> Any:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    
class WeatherApi:
    def __init__(self, client: HttpClient, api_key: str) -> None:
        self.client = client
        self.api_key = api_key
        self.full_weather_forecast: dict[str, Any] = {}

    def retrieve_forecast(self, city: str) -> None:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = self.client.get(url)
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )
        self.full_weather_forecast = response
    
    @property
    def temperature(self) -> float:
        return self.full_weather_forecast["main"]["temp"] - 273.15
    
    @property
    def humidity(self) -> float:
        return self.full_weather_forecast["main"]["humidity"]
    
    @property
    def wind_speed(self) -> float:
        return self.full_weather_forecast["wind"]["speed"]
    
    @property
    def wind_direction(self) -> float:
        return self.full_weather_forecast["wind"]["deg"]
    
def main() -> None:
    city = "Laramie"

    weather = WeatherApi(RequestsClient(), api_key=API_KEY)
    weather.retrieve_forecast(city=city)
    print(f"The current temperature in {city} is {weather.temperature:.1f} °C.")
    print(f"The current humidity in {city} is {weather.humidity}%.")
    print(
        f"The current wind speed in {city} is {weather.wind_speed} m/s from direction {weather.wind_direction} degrees."
    )


if __name__ == "__main__":
    main()
