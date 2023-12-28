from io import StringIO
from typing import Optional

import pandas as pd
import requests
from parameters import parameters


class WeatherDataDownloader:
    """A downloader for fetching weather data from the SMHI API.

    Attributes:
        parameter: A dictionary entry corresponding to the desired weather parameter.
        base_url (str): Base URL of the SMHI API.
        period (str): The period for which the data will be fetched.

    Methods:
        download_weather_data(station: str): Downloads weather data for a specific station.
        run(): Runs the downloader for multiple stations and compiles the data into a single CSV.
    """

    def __init__(self, parameter_id: str = "1"):
        """Initializes the WeatherDataDownloader with a specific weather parameter.

        Args:
            parameter_id (str): The ID of the parameter to fetch weather data for. Defaults to "1".
        """
        self.parameter_id = parameters[parameter_id].id
        self.base_url = "https://opendata-download-metobs.smhi.se/api/version/1.0"
        self.period = "corrected-archive"

    def download_weather_data(self, station_id: str) -> Optional[pd.DataFrame]:
        """Downloads meteorological data as CSV for a specific station with corrected-archive period.

        Fetches the weather data from the SMHI API, processes the CSV, and returns it as a pandas DataFrame.

        Args:
            station (str): The station ID to fetch weather data for.

        Returns:
            Optional[pd.DataFrame]: A DataFrame containing the weather data, or None if an error occurs.
        """
        url = f"{self.base_url}/parameter/{self.parameter_id}/station/{station_id}/period/{self.period}/data.csv"

        try:
            response = requests.get(url)
            response.raise_for_status()

            if response.ok and response.text:
                df = pd.read_csv(
                    StringIO(response.text), sep=";", skiprows=11, header=None
                )
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
            return None
        except Exception as err:
            print(f"An error occurred: {err}")
            return None

    def run(self):
        """Executes the data download for a list of stations and saves the combined results.
        Reads a predefined list of stations, downloads data for each, and saves the compiled data into a CSV file.
        """
        stations = pd.read_csv("weather_data/data/stations.csv", sep=";")
        cols = ["key", "name"]
        stations = stations[cols].drop_duplicates().head(10)
        dfs = []
        for index, row in stations.iterrows():
            station_id = row["key"]
            name = row["name"]
            df = self.download_weather_data(station_id)
            if df is not None:
                df["station_name"] = name
                df["station_id"] = station_id
                cols = [
                    "station_id",
                    "station_name",
                    "Datum",
                    "Tid (UTC)",
                    "Lufttemperatur",
                    "Kvalitet",
                    "Tidsutsnitt",
                ]
                df = df[cols]
                dfs.append(df)
        combined_df = pd.concat(dfs)
        combined_df.to_csv("weather_data/data/temperature.csv", index=False, sep=",")
