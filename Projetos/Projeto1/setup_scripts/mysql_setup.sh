#!/bin/bash

# This script installs and setups a MySQL instance in the context of the deti_shop Linux Container.
# It SHOULD NOT be executed outside this context!

source ../.env

sudo apt update && sudo apt upgrade

sudo apt install mysql-server

sudo apt install mysql-client

sudo apt-get install libmysqlclient-dev

mysql --version

# Configure instance security

# This step is done manually and must follow these instructions:
# Hit Enter on all options :)

sudo mysql_secure_installation

# Setup database, its tables and insert sample data

mysql -u root < ../app_sec/mysql_db/table_creation.sql

mysql -u root < ../app_sec/mysql_db/table_insertion.sql

