import logging
from utils.weather_integration.transform import Transform

CITIES = ["london", "paris", "berlin", "sylhet"]

logger = logging.getLogger(__name__)


class Run:
    @classmethod
    def run(cls):
        transform = Transform()

        for city in CITIES:
            try:
                logger.info(f"Attempting to fetch and push data for {city}")
                transform.push_to_postgres(city)
                logger.info(f"Successfully pushed data for {city}\n")
            except Exception as e:
                logger.error(f"Failed to fetch or push data for {city}: {e}\n")
