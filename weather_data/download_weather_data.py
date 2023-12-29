import os
from pprint import pprint

import pandas as pd
from dotenv import find_dotenv, load_dotenv
from opencage.geocoder import OpenCageGeocode
from parameters import parameters
from weather_data_downloader import WeatherDataDownloader

_ = load_dotenv(find_dotenv())

# Get parameter for lufttemperatur measured once per hour
TEMPERATURE = parameters["1"]


if __name__ == "__main__":
    # weather_data_downloader = WeatherDataDownloader(parameter_id=TEMPERATURE.id)
    # parameter = TEMPERATURE.id
    # weather_data_downloader.run()
    stations = pd.read_csv("weather_data/data/stations.csv", sep=";")
    municipalities = pd.read_csv(
        "weather_data/data/swedish_municipalities.csv", sep=";"
    )
    stations.name = stations.name.str.lower().str.replace("-", " ")
    municipalities.name = municipalities.name.str.lower()
    # Check if the station name is in the list of municipalities
    stations["municipality"] = municipalities.name.isin(stations.name)
    # print(stations[stations.municipality == False].name)
    key = os.getenv("opencage_api_key")
    lat, long = stations[["latitude", "longitude"]].iloc[8]
    print(stations.loc[8])
    geocoder = OpenCageGeocode(key)

    results = geocoder.reverse_geocode(lat, long)
    print(type(results))
    print(results)
    pprint(results[0]["components"]["municipality"])
    municipality = results[0]["components"]["municipality"]
    if municipality.endswith("s kommun"):
        municipality = municipality[:-8]
    print(municipality)
