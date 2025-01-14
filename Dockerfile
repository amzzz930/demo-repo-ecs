# Use a base image with Python installed
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files to the container
COPY . /app

# Install required dependencies
# If you have a requirements.txt file, you can use it to install dependencies
RUN pip install -r requirements.txt

# Set the PYTHONPATH so the utils module can be found
ENV PYTHONPATH=/app

# Default command to run pytest
CMD ["pytest"]