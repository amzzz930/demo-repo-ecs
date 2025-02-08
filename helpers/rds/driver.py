import psycopg2
import pandas as pd
import logging
from helpers.ssm.parameter_store import SSMParameterStore

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostgresDriver:
    @classmethod
    def connect_to_db(cls):
        """Connect to the PostgreSQL database"""
        ssm = SSMParameterStore(region="eu-west-1")
        try:
            connection = psycopg2.connect(
                host=ssm.get_parameter(parameter_name="/rds/staging/endpoint"),
                port="5432",
                database="postgres",
                user=ssm.get_parameter(parameter_name="/rds/staging/username"),
                password=ssm.get_parameter(parameter_name="/rds/staging/password"),
            )
            connection.autocommit = True  # Ensures changes are committed automatically
            logger.info("✅ Connection to the database successful")
            return connection
        except Exception as e:
            logger.error(f"❌ Failed to connect to the database: {e}")
            raise

    @classmethod
    def get_query(cls, query: str):
        """Fetch data from the database and return as a Pandas DataFrame"""
        connection = None
        try:
            connection = cls.connect_to_db()
            df = pd.read_sql(query, connection)

            if not df.empty:
                logger.info(f"✅ Query executed successfully. Rows fetched: {len(df)}")
                logger.debug(df.head(5))  # Logs first 5 rows (optional)
            else:
                logger.info("⚠️ Query returned no results.")

            return df
        except Exception as e:
            logger.error(f"❌ Error executing query: {e}")
            return None
        finally:
            if connection:
                connection.close()
                logger.info("🔌 Connection closed.")

    @classmethod
    def put_query(cls, query: str, values=None):
        """Execute an insert/update/delete query"""
        connection = None
        try:
            connection = cls.connect_to_db()
            with connection.cursor() as cursor:
                if values:
                    cursor.execute(query, values)  # Using parameterized query
                else:
                    cursor.execute(query)

                logger.info(f"✅ Query executed successfully: {query}")
        except Exception as e:
            logger.error(f"❌ Error executing query: {e}")
            return None
        finally:
            if connection:
                connection.close()
                logger.info("🔌 Connection closed.")
