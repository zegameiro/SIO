## Setup Guide

### Instructions

- Initiate a terminal at the project directory;
- Change directory to ```setup_scripts```;
- Execute the scripts in the following order (execution is being done this way to allow easier troubleshooting in case of any failure).

Feel free to execute all of these in the same batch if you don't want to (simply copy all commands to the terminal like so).

```bash 
./lxd_setup.sh;\
./container_start.sh;\
./container_config.sh;\

cd ..
cd home/ubuntu/app_sec/setup_scripts

./mysql_setup.sh;\
./py_setup.sh;\
```

If the exception "Exception: Can not find valid pkg-config name." is raised during py_setup. Use the following command(s) while using the container's shell:

```bash
sudo apt-get update && sudo apt-get install python3-dev default-libmysqlclient-dev
```

If this doesn't work:

```bash
sudo apt install libssl-dev
```

NOTE: After executing these scripts, you should now be in the container's shell

- Go back to the project directory
```bash
cd ..
```

- Activate the python virtual environment
```bash
source venv/bin/activate
```

- Run the Flask application
```bash
python3 app.py
```

- Insert this password for the notification system email
```
ixkq boot nabr qyul
```

- It will ask to input a PEM passphrase and you should input the following
```
UA@201RSAo10
```

### Sample accounts

- To use sample accounts, check the table_insertion.sql folder inside mysql_db on the app_sec folder
- You'll be able to see each account's username and password

