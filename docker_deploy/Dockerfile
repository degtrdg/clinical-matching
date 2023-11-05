# Use an official Python runtime as a parent image
FROM python:3.10-slim-bookworm

# Needed to build hnswlib during pip install. 
# See here https://github.com/chroma-core/chroma/issues/642
RUN apt-get update --fix-missing && apt-get install -y --fix-missing build-essential

# Set the working directory in the container to /app
WORKDIR /app

# Add the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the command to start uvicorn
CMD uvicorn main:app --port:8000 --host=0.0.0.0