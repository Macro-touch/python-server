# Use a lightweight base image
FROM python:3.9-slim

# Install locales and generate en_US.UTF-8
RUN apt-get update && apt-get install -y locales \ 
    && apt-get install -y language-pack-en \
    && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8

# Set environment variables for locale
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en

# Set the working directory
WORKDIR /app

# Copy your application code
COPY . /app

RUN locale -a

# Command to run your app
CMD ["python", "app.py"]
