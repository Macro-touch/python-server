#!/bin/bash
apt-get update && apt-get install -y locales
locale-gen en_US.UTF-8
export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8
python app.py
