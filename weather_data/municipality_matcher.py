import csv
import os
import time
from typing import List, Optional

from dotenv import find_dotenv, load_dotenv
from opencage.geocoder import (
    InvalidInputError,
    OpenCageGeocode,
    RateLimitExceededError,
    UnknownError,
)


class MunicipalityMatcher:
    """A class to match coordinates to Swedish municipalities.

    This class provides methods to load data from a municipalities file and
    a weather station file and uses a geocoding service to match coordinates
    to the nearest municipality.

    Attributes:
        municipalities (List[str]): A list of Swedish municipalities.
        geocoder (OpenCageGeocode): An instance of the OpenCageGeocode client.
    """

    def __init__(self) -> None:
        """Initializes the MunicipalityMatcher with empty data."""
        # Load environment variables
        _ = load_dotenv(find_dotenv())
        self.municipalities: List[str] = []
        self.load_municipalities()
        self.geocoder = OpenCageGeocode(key=os.getenv("opencage_api_key"))

    def load_municipalities(self) -> None:
        """Loads municipality data from a CSV file."""
        filepath = "weather_data/data/swedish_municipalities.csv"
        with open(filepath, mode="r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)  # Skip the header row
            for row in reader:
                code, name = row
                self.municipalities.append(name)

    def find_municipality(self, lat: float, long: float) -> Optional[str]:
        """Finds the municipality for given coordinates using geocoding.

        Args:
            lat: The latitude of the location.
            long: The longitude of the location.

        Returns:
            Optional[str]: The municipality if found, otherwise None.
        """
        try:
            results = self.geocoder.reverse_geocode(lat, long)
            # sleep 1 second to prevent hitting the rate limit
            municipality = results[0]["components"]["municipality"]
            print(f"Processed {municipality}. Sleeping for 1 second...")
            time.sleep(1)
            if municipality.endswith("s kommun"):
                municipality = municipality[:-8]
            if municipality.endswith(" kommun"):
                municipality = municipality[:-7]
            if municipality in self.municipalities:
                return municipality
        except RateLimitExceededError as ex:
            print(f"Rate limit exceeded: {ex}")
        except InvalidInputError as ex:
            print(f"Invalid input: {ex}")
        except UnknownError as ex:
            print(f"An unknown error occurred: {ex}")
        except Exception as ex:
            print(f"An unexpected error occurred: {ex}")

        return None
