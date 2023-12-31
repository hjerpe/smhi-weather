import logging
import logging.config
from io import StringIO
from typing import Optional

import pandas as pd
import requests
import yaml
from parameters import parameters

# Load the logging configuration
logging.config.fileConfig(
    fname="/workspaces/smhi-weather/logging.conf", disable_existing_loggers=False
)
# Get the logger specified in the file
logger = logging.getLogger(__name__)


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
        with open("configs/config-ver.yml", "r") as ymlfile:
            cfg = yaml.safe_load(ymlfile)
        self.base_url = cfg["base_url"]
        self.period = cfg["default_period"]

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
                logger.info(
                    f"Successfully downloaded data for station ID: {station_id}"
                )
                return df
            else:
                logger.warning(
                    f"No data received from the API for station ID: {station_id}"
                )
                return None

        except requests.HTTPError as http_err:
            logger.error(f"HTTP error occurred for station ID {station_id}: {http_err}")
            return None
        except Exception as err:
            logger.error(
                f"An unexpected error occurred for station ID {station_id}: {err}"
            )
            return None

    def run(self):
        """Executes the data download for a list of stations and saves the combined results.
        Reads a predefined list of stations, downloads data for each, and saves the compiled data into a CSV file.
        """
        stations = pd.read_csv("weather_data/data/stations.csv", sep=";")
        cols = ["key", "name", "active", "from", "to", "municipality"]
        stations = stations[cols].drop_duplicates().head(3)
        dfs = []
        for index, row in stations.iterrows():
            station_id = row["key"]
            name = row["name"]
            df = self.download_weather_data(station_id)
            # TODO: Must combine the time and date columns to get the latest date
            if df is not None:
                df["station_id"] = station_id
                df["station_active"] = row["active"]
                df["station_municipality"] = row["municipality"]
                cols = [
                    "station_id",
                    "station_active",
                    "station_municipality",
                    "Datum",
                    "Tid (UTC)",
                    "Lufttemperatur",
                    "Kvalitet",
                    "Tidsutsnitt",
                ]
                df = df[cols]
                dfs.append(df)
        combined_df = pd.concat(dfs)
        return combined_df
        # combined_df.to_csv("weather_data/data/temperature.csv", index=False, sep=";")
