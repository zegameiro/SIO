#!/bin/bash

sudo apt-get update
sudo apt-get install python3.8
sudo apt install python3.8-venv

# Create virtual environment
python3 -m venv ../venv

# Activate VEnv. Feel free to use these 2 commands outside this script when everything has been setup
source ../venv/bin/activate
source ../.env

sudo apt install python3-pip

pip install -r ../requirements.txt




