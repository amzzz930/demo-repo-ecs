from datetime import datetime, timedelta
import logging

from helpers.weather_api import WeatherApi
from helpers.rds.driver import PostgresDriver

KELVIN_TO_CELSIUS = 273.15

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PushToPostgres:
    def __init__(self):
        self.postgres = PostgresDriver()
        self.weather_api = WeatherApi()

    def get_location_data(self, location: str):
        """Fetches weather data for a location and processes it."""
        created_at = self.get_datetime_now_rounded()
        result = self.weather_api.get_location_data(location)

        if not result or "main" not in result:
            raise ValueError(f"⚠️ Invalid response from API: {result}")

        location_name = result.get("name")
        weather = result.get("weather")[0]  # Handle missing 'weather' key
        main = weather.get("main")
        description = weather.get("description")
        temp_kelvin = result.get("main").get("temp")

        if temp_kelvin is None:
            raise ValueError("⚠️ Temperature data missing in API response.")

        celsius = round(temp_kelvin - KELVIN_TO_CELSIUS, 2)

        return created_at, location_name, main, description, celsius

    def push_to_postgres(self, location: str):
        """Inserts weather data into the database"""
        try:
            (
                created_at,
                location_name,
                main,
                description,
                celsius,
            ) = self.get_location_data(location)

            query = """
            INSERT INTO weather_data (created_at, location_name, main, description, temp_celsius)
            VALUES (%s, %s, %s, %s, %s)
            """

            self.postgres.put_query(
                query, (created_at, location_name, main, description, celsius)
            )
            logger.info(f"✅ Successfully inserted weather data for {location_name}")

        except Exception as e:
            logger.error(f"❌ Failed to push data for {location}: {e}")

    @staticmethod
    def get_datetime_now_rounded() -> str:
        """Returns the current timestamp rounded up to the next second in ISO format."""
        now = datetime.now()
        rounded_up = now + timedelta(seconds=1) if now.microsecond > 0 else now
        return rounded_up.replace(microsecond=0).isoformat()
