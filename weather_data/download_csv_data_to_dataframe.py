from io import StringIO
from typing import Optional

import pandas as pd
import requests


def download_csv_data_to_dataframe(
    parameter: str, station: str
) -> Optional[pd.DataFrame]:
    """D

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
    parameter = "1"
    station = "159880"
    df = download_csv_data_to_dataframe(parameter, station)
    if df is not None:
        print(df)  # Print the first few rows of the DataFrame
