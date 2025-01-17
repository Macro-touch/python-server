# !/bin/bash
# render-build.sh

# Update and install required locales during the build process
apt-get update && apt-get install -y locales

# Generate en_US.UTF-8 locale
locale-gen en_US.UTF-8

# Set locale environment variables
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en

echo "Locale setup complete: $(locale)"

echo "Available Locales: \n"
locale -a