from typing import Dict, List, Optional

import pandas as pd
import requests
from dotenv import find_dotenv, load_dotenv
from municipality_matcher import MunicipalityMatcher

_ = load_dotenv(find_dotenv())


def get_stations(parameter_id: str) -> Optional[pd.DataFrame]:
    """Fetches and returns a DataFraggme of station details from the API based on the given parameter.

    Args:
        parameter_id (str): The ID of the parameter to fetch the stations for.

    Returns:
        Optional[pd.DataFrame]: A DataFrame of station details or None if an error occurs.
    """
    url: str = f"https://opendata-download-metobs.smhi.se/api/version/latest/parameter/{parameter_id}.json"

    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()

        data: dict = response.json()
        stations: list = data.get("station", [])

        # Initialize an empty list to hold station data
        station_data: List[Dict[str, str]] = []

        # Loop through each station and gather details
        for station in stations:
            # Extract details from each station entry
            details = {key: str(value) for key, value in station.items()}
            station_data.append(details)

        station_data = station_data
        # Create a DataFrame from the list of station data
        df: pd.DataFrame = pd.DataFrame(station_data)
        matcher = MunicipalityMatcher()
        # Add a column for the municipality
        df["municipality"] = df.apply(
            lambda row: matcher.find_municipality(
                float(row["latitude"]), float(row["longitude"])
            ),
            axis=1,
        )
        # Save the DataFrame to a CSV file called 'stations.csv'
        df.to_csv("stations.csv", index=False)

        return df

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


if __name__ == "__main__":
    parameter_id = "1"  # Example parameter ID, replace with actual parameter ID
    df: Optional[pd.DataFrame] = get_stations(parameter_id)
    if df is not None:
        df.to_csv("weather_data/data/stations.csv", index=False, sep=";")
        print("Stations Data:")
        print(df.head())  # Print the first few rows of the DataFrame
