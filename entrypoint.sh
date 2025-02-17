#!/bin/bash

# Check if we are running tests
if [ "$1" == "test" ]; then
    # Run tests
    echo "Running tests..."
    pytest /opt/airflow/tests/
    TEST_EXIT_CODE=$?

    # If tests fail, exit
    if [ $TEST_EXIT_CODE -ne 0 ]; then
        echo "Tests failed! Exiting..."
        exit 1
    fi

    # If tests pass, exit without initializing Airflow DB
    echo "Tests passed! Exiting without initializing Airflow DB."
    exit 0  # Exit without running Airflow DB initialization or webserver
fi

# Default behavior: start the Airflow webserver and initialize the database
echo "Starting Airflow webserver..."
airflow db init  # Initialize the Airflow DB if not already done
exec "$@"  # This will start the Airflow webserver (CMD in Dockerfile)
