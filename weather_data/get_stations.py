from typing import List, Optional

import requests


def get_stations() -> Optional[List[str]]:
    """Fetches and returns a list of station names from the API.

    Returns:
        Optional[List[str]]: A list of station names or None if an error occurs.
    """
    url: str = (
        "https://opendata-download-metobs.smhi.se/api/version/latest/parameter/1.json"
    )

    try:
        response: requests.Response = requests.get(url)
        response.raise_for_status()

        data: dict = response.json()
        stations: list = data.get("station", [])
        station_names: List[str] = ["; ".join(station) for station in stations]

        return station_names

    except requests.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"An error occurred: {err}")
    return None


if __name__ == "__main__":
    station_names: Optional[List[str]] = get_stations()
    if station_names:
        print("Stations: ")
        for name in station_names:
            print(name)
