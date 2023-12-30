from dotenv import find_dotenv, load_dotenv
from parameters import parameters
from weather_data_downloader import WeatherDataDownloader

_ = load_dotenv(find_dotenv())


if __name__ == "__main__":
    # Get parameter for lufttemperatur measured once per hour
    TEMPERATURE = parameters["1"]
    weather_data_downloader = WeatherDataDownloader(parameter_id=TEMPERATURE.id)
    parameter = TEMPERATURE.id
    weather_data_downloader.run()
