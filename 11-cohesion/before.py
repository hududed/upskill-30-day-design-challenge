import pandas as pd


def main() -> None:
    option = "All"  # choose between "All", "Temperature", "Humidity", "CO2"

    data = pd.read_csv("sensor_data.csv")
    assert option in (
        "All",
        "Temperature",
        "Humidity",
        "CO2",
    ), f'Option not valid, should be ("All", "Temperature", "Humidity", "CO2") {option} given!'

    if option in ("Temperature", "Humidity", "CO2"):
        data = data.loc[data["Sensor"] == option]

    processed_data = []
    for _, row in data.iterrows():
        sensor = row["Sensor"]
        if sensor == "Temperature":
            row["Value"] += 273.15  # Convert to Kelvin
            processed_data.append(row)
        elif sensor == "Humidity":
            row["Value"] /= 100  # Convert to scale 0-1
            processed_data.append(row)
        elif sensor == "CO2":
            row["Value"] += 23  # Compensating for sensor bias
            processed_data.append(row)

    processed_data_single = pd.DataFrame(data=processed_data)
    print(processed_data_single)


if __name__ == "__main__":
    main()
