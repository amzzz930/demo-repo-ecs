# Always pulls the latest stable version (may introduce breaking changes)
FROM apache/airflow:latest

USER root
RUN apt-get update && apt-get install -y curl unzip

USER airflow
WORKDIR /opt/airflow/

# Copy all DAG-related files
COPY dags /opt/airflow/dags/
COPY utils /opt/airflow/utils/
COPY helpers /opt/airflow/helpers/
COPY requirements.txt /opt/airflow/requirements.txt
COPY tests /opt/airflow/tests/

# Set Python path so Airflow recognizes custom modules
ENV PYTHONPATH="/opt/airflow/:$PYTHONPATH"

# Install Python dependencies
RUN pip install --no-cache-dir -r /opt/airflow/requirements.txt

# Default command to run pytest
CMD ["pytest"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["webserver"]
