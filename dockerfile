# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install locales and other required dependencies
RUN echo "Setting locale to en_US.UTF-8" && \
    apt-get update && \
    apt-get install -y locales && \
    apt-get install -y language-pack-en && \
    locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8

# Copy requirements.txt (if available) and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


# Set locale environment variables
ENV LANG=eng.UTF-8
ENV LC_ALL=eng.UTF-8

# Copy your Flask app code into the container
COPY . .

# Set the environment variables for Flask
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=5000

# Expose the port Flask will run on
EXPOSE 5000

# Start Flask application using Gunicorn (recommended for production)
CMD ["gunicorn", "-b", "0.0.0.0:5000", "app:app"]
