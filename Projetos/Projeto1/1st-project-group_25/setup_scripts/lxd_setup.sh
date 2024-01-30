#!/bin/bash

# This is a file to setup LXD on the machine in order to support Linux Container execution

# Execute the container_setup.sh shell script to create and launch the container

sudo apt-get update

sudo apt install lxd

# Hit ENTER on all configurations (accept default configurations)

sudo lxd init

# Add user to the lxd group to avoid constant usage of the 'sudo' command

sudo usermod -aG lxd $USER

# Force changes

newgrp lxd 
