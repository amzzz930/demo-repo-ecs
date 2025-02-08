import requests
import logging
from requests.exceptions import RequestException
from helpers.ssm.parameter_store import SsmParameterStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class WeatherApi:
    """Fetch weather data using OpenWeatherMap API"""

    BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

    def __init__(self):
        self.ssm = SsmParameterStore(region="eu-west-1")
        self.api_key = self.ssm.get_parameter(parameter_name="WeatherApiKey")

        if not self.api_key:
            raise ValueError("Weather API key not found in SSM Parameter Store")

    def get_location_data(self, location: str):
        """Fetch weather data for a given location"""
        params = {"q": location, "appid": self.api_key}

        try:
            response = requests.get(self.BASE_URL, params=params, timeout=5)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

            data = response.json()

            if "weather" not in data:
                logger.warning(f"Unexpected response format: {data}")
                return {"error": "Unexpected response format"}

            logger.info(f"Weather data retrieved successfully for {location}")
            return data

        except RequestException as e:
            logger.error(f"Error fetching weather data for {location}: {e}")
            return {"error": str(e)}
