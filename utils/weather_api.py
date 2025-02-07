import requests
from helpers.ssm.parameter_store import SSMParameterStore


class WeatherApi:
    def __init__(self):
        self.api_key = SSMParameterStore.get_parameter("WeatherApiKey")

    def get_location_data(self, location: str):
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": location, "appid": self.api_key}
        r = requests.get(url, params=params)

        return r.json()
