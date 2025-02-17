# Start with the official Airflow image
FROM apache/airflow:latest

# Use root to install dependencies
USER root
RUN apt-get update && apt-get install -y curl unzip

# Set the working directory
WORKDIR /opt/airflow/

# Copy dags, helpers, utils, and tests folders into the container
COPY dags /opt/airflow/dags/
COPY helpers /opt/airflow/helpers/
COPY utils /opt/airflow/utils/
COPY tests /opt/airflow/tests/
COPY requirements.txt /opt/airflow/requirements.txt

# Copy the entrypoint script and set the correct permissions
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set Python path to include custom modules
ENV PYTHONPATH="/opt/airflow/:$PYTHONPATH"

# Switch to airflow user before installing dependencies
USER airflow

# Install Python dependencies (from requirements.txt)
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Install pytest to run tests
RUN pip install --no-cache-dir pytest

# Set the entrypoint to run the tests or start the webserver
ENTRYPOINT ["/entrypoint.sh"]

# Default to running the Airflow webserver
CMD ["webserver"]
