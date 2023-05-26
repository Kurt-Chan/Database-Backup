import customtkinter
import os
import datetime
import subprocess

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("510x370")
root.resizable(False, False)
root.eval('tk::PlaceWindow . center')
root.title("Workbench Database Backup")

result = customtkinter.StringVar()
CACHE_FILE = "cache.txt"

def backup():
    result.set("Exporting ...")
    
    hostname = host_entry.get().strip()
    port = port_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    backup_dir = path_entry.get().strip()
    db = optionmenu.get().strip()

    current_date = datetime.datetime.now().strftime("%m-%d-%Y")
    backup_file = f"backupdb_{current_date}.sql"

    command = f'mysqldump -h {hostname} -P {port} -u {username} -p{password} --routines --events --triggers {db} > {os.path.join(backup_dir, backup_file)}'
    return_code = subprocess.call(command, shell=True)

    if return_code == 0:
        result.set(f"Backup created successfully at: {os.path.join(backup_dir, backup_file)}")
    else:
        result.set("Backup creation failed.")

    data = {
        "hostname": hostname,
        "port": port,
        "username": username,
        "password": password,
        "backup_dir": backup_dir,
        "db": db,
    }
    save_cache(data)


def validate_form():
    host = host_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    path = path_entry.get().strip()

    if not host or not username or not password or not path:
        submit_button.configure(state="disabled", fg_color="#042406")
    else:
        submit_button.configure(state="normal", fg_color="#265828")


# CACHE THE INPUTS
def save_cache(data):
    with open(CACHE_FILE, "w") as file:
        for key, value in data.items():
            file.write(f"{key}:{value}\n")

def load_cache():
    if not os.path.exists(CACHE_FILE):
        return {}

    try:
        with open(CACHE_FILE, "r") as file:
            lines = file.readlines()
            data = {}
            for line in lines:
                parts = line.strip().split(":")
                key = parts[0]
                value = ":".join(parts[1:])
                data[key] = value
            return data
    except FileNotFoundError:
        return {}


title = customtkinter.CTkLabel(root, text="Workbench Database Backup", font=("Roboto Bold", 24))
title.pack(padx=10, pady=12)

res_label = customtkinter.CTkLabel(root, textvariable = result)
res_label.pack(padx=10, pady=5)

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=12, fill="both", expand=True)

# HOST
host_label = customtkinter.CTkLabel(master=frame, text="Host")
host_label.grid(row=1, column=0, padx=5, pady=17, sticky="e")

host_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter Host name", fg_color="transparent")
host_entry.grid(row=1, column=1, padx=10, sticky="e")
host_entry.bind("<KeyRelease>", lambda event: validate_form())


# PORT
port_label = customtkinter.CTkLabel(master=frame, text="Port")
port_label.grid(row=1, column=2, padx=1, sticky="e")

port_entry = customtkinter.CTkEntry(master=frame, placeholder_text="8080", fg_color="transparent", width=60)
port_entry.grid(row=1, column=3, padx=1)
port_entry.bind("<KeyRelease>", lambda event: validate_form())


# USERNAME
username_label = customtkinter.CTkLabel(master=frame, text="Username")
username_label.grid(row=2, column=0, padx=10, sticky="e")

username_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter username", fg_color="transparent")
username_entry.grid(row=2, column=1, padx=5, pady=12, sticky="e")
username_entry.bind("<KeyRelease>", lambda event: validate_form())


# PASSWORD
password_label = customtkinter.CTkLabel(master=frame, text="Password")
password_label.grid(row=2, column=2, padx=5, sticky="e")

password_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter password", fg_color="transparent")
password_entry.grid(row=2, column=3, padx=5, sticky="e")
password_entry.bind("<KeyRelease>", lambda event: validate_form())


# PATH
path_label = customtkinter.CTkLabel(master=frame, text="File path")
path_label.grid(row=4, column=0, padx=5, sticky="e")

path_entry = customtkinter.CTkEntry(master=frame, placeholder_text="Enter file path", fg_color="transparent")
path_entry.grid(row=4, column=1, padx=5, pady=12)
path_entry.bind("<KeyRelease>", lambda event: validate_form())


# OPTION MENU
opt_label = customtkinter.CTkLabel(master=frame, text="Database")
opt_label.grid(row=4, column=2, padx=5, sticky="e")

optionmenu = customtkinter.CTkOptionMenu(master=frame, values=["csusisdb", "csucarigweb"])
optionmenu.grid(row=4, column=3, padx=5, sticky="e")

# BUTTON
submit_button = customtkinter.CTkButton(root, text="Export database", state="normal", command=backup, fg_color="#265828")
submit_button.pack(pady=12, padx=10)

# GET THE CACHED DATA
cached_data = load_cache()
host_entry.insert(0, cached_data.get("hostname", ""))
port_entry.insert(0, cached_data.get("port", ""))
username_entry.insert(0, cached_data.get("username", ""))
password_entry.insert(0, cached_data.get("password", ""))
path_entry.insert(0, cached_data.get("backup_dir", ""))
optionmenu.set(cached_data.get("db", ""))

root.mainloop()
