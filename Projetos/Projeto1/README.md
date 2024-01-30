# Assignment 1 SIO 2023/2024

## Description

This report documents Project 1 of SIO, in which an online shop specializing in DETI memorabilia at the University of Aveiro was developed.

Thus, for each vulnerability found, the related CWEs will be presented, with a brief explanation of them. </br> This is followed by a description of the vulnerability, accompanied by screenshots/GIFS demonstrating it. </br>
Finally, our resolution of the problem is described, presenting the changed code, as well as screenshots/GIFS showing the resolved vulnerability.

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
./mysql_setup.sh;\
./py_setup.sh;\
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

- Change to the ```app``` directory
```bash
cd app
```

- Run the Flask application
```bash
python3 app.py
```

#### Containerizing the SECURE application

- Follow the same procedure using the scripts in the setup_scripts_sec directory

- Please keep in mind that the secure application uses slightly modified tables to accomodate changes, thus needing a new, different database, which should be bundled in its container

### Sample accounts

- To use sample accounts, check the table_insertion.sql folder inside mysql_db on the app(_sec) folder
- You'll be able to see each account's username and password



## Found Weaknesses

- **CWE - 79** : Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')
- **CWE - 89** : Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')
- **CWE - 203** : Observable Discrepancy
- **CWE - 328** : Use of Weak Hash
- **CWE - 352** : Cross-Site Request Forgery (CSRF)
- **CWE - 434** : Unrestricted Upload of File with Dangerous Type
- **CWE - 488** : Exposure of Data Element to Wrong Session
- **CWE - 521** : Weak Password Requirements
- **CWE - 522** : Insufficiently Protected Credentials
- **CWE - 620** : Unverified Password Change
- **CWE - 916** : Use of Password Hash With Insufficient Computational Effort

## **Authors**

| NMEC   | Name              |                  Email  |
| ------ | ----------------- | ----------------------: |
| 107186 | Vítor Santos      | vitor.mtsantos@ua.pt    |
| 107403 | João Luís         | jnluis@ua.pt            |
| 108122 | Alexandre Ribeiro | alexandrepribeiro@ua.pt |
| 108840 | José Gameiro      | jose.mcgameiro@ua.pt    |

