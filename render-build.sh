# Install locales
apt-get update && apt-get install -y locales

# Generate en_US.UTF-8 locale
locale-gen en_US.UTF-8

# Set locale environment variables
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
sudo dpkg-reconfigure locales

echo "Locale setup complete: $(locale)"
pip install -r requirements.txt