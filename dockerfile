# Use a lightweight base image
FROM python:3.9-slim

# Set environment variables for locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

# Install locales and generate en_US.UTF-8
RUN apt-get update && apt-get install -y locales \
    && locale-gen en_US.UTF-8 \
    && apt-get clean

# Install other dependencies for your app
RUN pip install -r requirements.txt

# Set the working directory
WORKDIR /app

# Copy your application code
COPY . /app

# Command to run your app
CMD ["python", "app.py"]
