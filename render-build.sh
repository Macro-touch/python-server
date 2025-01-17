# Install locales
apt-get update && apt-get install -y locales

mkdir -p ~/locales
localedef --inputfile en_US --charmap UTF-8 ~/locales/en_US.UTF-8

# Generate en_US.UTF-8 locale
sudo locale-gen en_US.UTF-8
locale-gen en_US.UTF-8

# Set locale environment variables
export LOCPATH=~/locales
export LANG=en_US.UTF-8
export LC_ALL=en_US.UTF-8
export LC_CTYPE=en_US.UTF-8
sudo dpkg-reconfigure locales

echo "Locale setup complete: $(locale)"
pip install -r requirements.txt