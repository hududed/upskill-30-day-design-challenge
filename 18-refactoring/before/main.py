import argparse
from weather import (
    get_complete_forecast,
    http_get,
    get_temperature,
    get_humidity,
    get_wind_speed,
    get_wind_direction,
)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Get the current weather information for a city"
    )
    parser.add_argument(
        "city", help="Name of the city to get the weather information for"
    )
    parser.add_argument(
        "-c",
        "--conditions",
        dest="conditions",
        metavar="CONDITION",
        nargs="+",
        default=["temperature"],
        choices=["all", "a", "temperature", "t", "humidity", "h", "wind", "w"],
        help="Weather conditions to display. Choose between 'all' or 'a', 'temperature' or 't', "
        "'humidity' or 'h', 'wind' or 'w'.",
    )

    parser.add_argument(
        "--api-key",
        default="123456789",
        help="API key for the OpenWeatherMap API",
    )

    args = parser.parse_args()

    if not args.api_key:
        # That will not happen because of the API default value.
        print("Please provide an API key with the --api-key option.")
        return

    if args.conditions:
        # Fetch the data from the OpenMapWeather API
        weather_forecast = get_complete_forecast(
            http_get_fn=http_get, api_key=args.api_key, city=args.city
        )

        for condition in args.conditions:
            if condition in ["temperature", "t"]:
                temperature = get_temperature(weather_forecast)
                print(
                    f"The current temperature in {args.city} is {temperature:.1f} °C."
                )
            elif condition in ["humidity", "h"]:
                print(
                    f"The current humidity in {args.city} is {get_humidity(weather_forecast)}%."
                )
            elif condition in ["wind", "w"]:
                print(
                    f"The current wind speed in {args.city} is {get_wind_speed(weather_forecast)} m/s "
                    f"from direction {get_wind_direction(weather_forecast)} degrees."
                )
            else:
                temperature = get_temperature(weather_forecast)
                print(
                    f"The current temperature in {args.city} is {temperature:.1f} °C."
                )
                print(
                    f"The current humidity in {args.city} is {get_humidity(weather_forecast)}%."
                )
                print(
                    f"The current wind speed in {args.city} is {get_wind_speed(weather_forecast)} m/s "
                    f"from direction {get_wind_direction(weather_forecast)} degrees."
                )
    else:
        # This will never happen because temperature is set as the default condition.
        print(
            f"Please specify at least one weather condition to display with the --conditions option."
        )


if __name__ == "__main__":
    main()
