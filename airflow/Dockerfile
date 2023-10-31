# Use the specified version of Apache Airflow as the base image
ARG AIRFLOW_VERSION=2.7.0
FROM apache/airflow:${AIRFLOW_VERSION}

# Copy the requirements file into the container
COPY requirements.txt /requirements.txt

# Upgrade pip
RUN pip install --user --upgrade pip

# Install the Python dependencies listed in requirements.txt
RUN pip install --no-cache-dir --user -r /requirements.txt

# Install a specific version of Apache Airflow to match the base image
RUN pip install apache-airflow==${AIRFLOW_VERSION}