from typing import Any

import requests


class CityNotFoundError(Exception):
    pass


class WeatherService:
    def __init__(self, city: str, api_key: str) -> None:
        self.api_key = api_key
        self.city = city
        self.full_weather_forecast: dict[str, Any] = {}
        self.url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}"

    def retrieve_forecast(self) -> None:
        response = requests.get(self.url, timeout=5).json()
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{self.city}' if it exists and is correctly spelled.\n"
            )

        self.full_weather_forecast = response


class MyWeatherService(WeatherService):
    def __init__(self) -> None:
        super().__init__(api_key="123456789", city="Utrecht")

    def retrieve_forecast(self) -> None:
        super().retrieve_forecast()
        # print the temperature in Celsius
        temp = self.full_weather_forecast["main"]["temp"] - 273.15
        print(f"The current temperature in {self.city} is {temp:.1f} °C.")


if __name__ == "__main__":
    MyWeatherService().retrieve_forecast()
