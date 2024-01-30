#!/bin/bash

source ../.env

# Push all project contents - may be altered to just push what is strictly necessary

lxc file push -r .. $CONT_NAME/home/ubuntu

lxc shell $CONT_NAME

sudo apt-get update

# Key storage application necessary for secure symmetric encryption key storage using the Secret Service API
sudo apt-get -y install gnome-keyring

