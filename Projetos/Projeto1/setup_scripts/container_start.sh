#!/bin/bash

# LXD is required to be setup before execution, alongside some additional configuration
# Make sure to execute lxd_setup.sh at least once, beforehand.

# This script doesn't configure the Linux Container with the required services and dependencies
# To do that, execute container_config.sh 

source ../.env

lxc launch images:ubuntu/20.04 $CONT_NAME