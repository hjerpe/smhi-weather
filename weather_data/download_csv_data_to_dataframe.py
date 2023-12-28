from io import StringIO
from typing import Optional

import pandas as pd
import requests
from parameters import parameters

# Get parameter for lufttemperatur measured once per hour
TEMPERATURE = parameters["1"]


def download_csv_data_to_dataframe(
    parameter: str, station: str
) -> Optional[pd.DataFrame]:
    """Downloads meteorological data as CSV for a specific station with corrected-archive period.

    Args:
        parameter (str): The parameter value.
        station (str): The station ID.

    Returns:
        Optional[pd.DataFrame]: DataFrame containing all columns of the data or None if an error occurs.
    """
    base_url = "https://opendata-download-metobs.smhi.se/api/version/1.0"
    period = "corrected-archive"  # Targeting the corrected-archive period
    url = f"{base_url}/parameter/{parameter}/station/{station}/period/{period}/data.csv"

    try:
        response = requests.get(url)
        response.raise_for_status()

        if response.ok and response.text:
            # Convert the CSV text response to a DataFrame
            df = pd.read_csv(StringIO(response.text), sep=";", skiprows=11, header=None)
            df.columns = [
                "Datum",
                "Tid (UTC)",
                "Lufttemperatur",
                "Kvalitet",
                "missing",
                "Tidsutsnitt",
            ]
            return df
        else:
            print("No data received from the API.")
            return None

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


if __name__ == "__main__":
    parameter = TEMPERATURE.id
    stations = pd.read_csv("weather_data/data/stations.csv", sep=";")
    cols = ["key", "name"]
    # Loop over each name and key
    stations = stations[cols].drop_duplicates().head(10)
    dfs = []
    for index, row in stations.iterrows():
        station = row["key"]
        name = row["name"]
        df = download_csv_data_to_dataframe(parameter, station)
        if df is not None:
            dfs.append(df)
            # df.to_csv(f'weather_data/data/{name}.csv', index=False, sep=";")
    combined_df = pd.concat(dfs)
    # Write temperature to csv
    combined_df.to_csv("weather_data/data/temperature.csv", index=False, sep=",")
