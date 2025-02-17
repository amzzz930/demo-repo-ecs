#!/bin/bash

echo "Running tests..."
pytest /opt/airflow/tests/
TEST_EXIT_CODE=$?

if [ $TEST_EXIT_CODE -ne 0 ]; then
  echo "Tests failed! Exiting..."
  exit 1
fi

echo "Tests passed! Initializing Airflow database..."
airflow db init

echo "Starting Airflow..."
exec airflow webserver
