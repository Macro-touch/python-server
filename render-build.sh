#!/bin/bash
echo "Checking available locales..."
locale -a

echo "Setting locales..."
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
export LANGUAGE="en_US:en"

echo "locales after download..."
locale -a

# Proceed with other build steps
pip install -r requirements.txt
docker build -t macrotouch .
python app.py