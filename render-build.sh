#!/bin/bash
echo "Checking available locales..."
locale -a

echo "Setting locales..."
export LC_ALL="en_US.UTF-8"
export LANG="en_US.UTF-8"
export LANGUAGE="en_US:en"

# Proceed with other build steps
pip install -r requirements.txt
python app.py