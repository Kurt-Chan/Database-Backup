import os
import datetime
import subprocess

# Define the MySQL Workbench connection parameters
hostname = 'localhost'
port = '3306'
username = 'root'
password = '12345'
database = 'csucarigweb'

# Define the backup directory
backup_dir = r'D:\dbtest'

# Generate the backup file name with the current date
current_date = datetime.datetime.now().strftime("%m-%d-%Y")
backup_file = f"backup_{current_date}.sql"

# Build the mysqldump command
command = f'mysqldump -h {hostname} -P {port} -u {username} -p{password} --routines --events --triggers {database} > {os.path.join(backup_dir, backup_file)}'

# Execute the mysqldump command
return_code = subprocess.call(command, shell=True)

# Check if the command executed successfully
if return_code == 0:
    print(f"Backup created successfully at: {os.path.join(backup_dir, backup_file)}")
else:
    print("Backup creation failed.")
