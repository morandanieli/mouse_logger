# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# this is for opencv package
RUN apt-get update && \
    apt-get install -y gcc libffi-dev libssl-dev libgl1-mesa-glx libglib2.0-0 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Make FLASK_PORT available to the world outside this container
EXPOSE $FLASK_RUN_PORT

CMD ["sh", "-c", "flask run --host=$FLASK_RUN_HOST --port=$FLASK_RUN_PORT"]


