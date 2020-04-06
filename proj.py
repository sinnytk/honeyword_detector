import tkinter as tk
import os
import os.path
from playsound import playsound
import hashlib
import requests
import json

myHeaders = {'Content-Type': 'application/json'}

message = ""
user = ""
first = ""
last = ""
login = False

# --------------------------------------Register Function--------------------------------------


def register():
    username_reg_entered = username_reg.get()
    fname_reg_entered = fname_reg.get()
    lname_reg_entered = lname_reg.get()
    password_reg_entered = password_reg.get()

    register_obj = {'username': username_reg_entered, 'password': password_reg_entered,
                    'first_name': fname_reg_entered, 'last_name': lname_reg_entered}
    register_obj_json = json.dumps(register_obj)
    response = requests.post(
        'http://localhost:5000/register', data=register_obj_json, headers=myHeaders)

    print(response.content)

    if response.content == b'OK':
        raise_frame(f2)
    elif response.content == b'Error':
        raise_frame(f6)

# ------------------------------------Login Function----------------------------------------


def login():

    username_log_entered = username_log.get()
    password_log_entered = password_log.get()

    login_obj = {'username': username_log_entered,
                 'password': password_log_entered}
    login_obj_json = json.dumps(login_obj)
    response = requests.post(
        'http://localhost:5000/login', data=login_obj_json, headers=myHeaders)

    if response.content == b'OK':
        raise_frame(f3)
    elif response.content == b'Wrong password':
        raise_frame(f4)
    elif response.content == b'No such user':
        raise_frame(f5)
    elif response.content == b'Honeyword detected':
        playsound('sound.wav')
        raise_frame(f7)

# -------------------------------------------Logout function-------------------------


def logout():
    print("logged out")


def show_entry_fields():
    print("First Name: %s\nLast Name: %s\nUsername: %s\nPassword: %s" %
          (e1.get(), e2.get(), e3.get(), e4.get()))


def raise_frame(frame):
    frame.tkraise()


master = tk.Tk()

f1 = tk.Frame(master)
f2 = tk.Frame(master)
f3 = tk.Frame(master)
f4 = tk.Frame(master)
f5 = tk.Frame(master)
f6 = tk.Frame(master)
f7 = tk.Frame(master)

for frame in (f1, f2, f3, f4, f5, f6, f7):
    frame.grid(row=0, column=0, sticky='news')

# -----------------------------Register Screen--------------------------

tk.Label(f1, text="First Name").pack()
fname_reg = tk.Entry(f1)
fname_reg.pack()
tk.Label(f1, text="Last Name").pack()
lname_reg = tk.Entry(f1)
lname_reg.pack()
tk.Label(f1, text="Username").pack()
username_reg = tk.Entry(f1)
username_reg.pack()
tk.Label(f1, text="Password").pack()
password_reg = tk.Entry(f1)
password_reg.pack()


tk.Button(f1, text='Register', command=register).pack()
tk.Button(f1, text='Login', command=lambda: raise_frame(f2)).pack()
tk.Button(f1, text='Quit', command=master.quit).pack()

# -----------------------------Login Screen--------------------------

tk.Label(f2, text="Username").pack()
username_log = tk.Entry(f2)
username_log.pack()
tk.Label(f2, text="Password").pack()
password_log = tk.Entry(f2)
password_log.pack()


tk.Button(f2, text='Login', command=login).pack()
tk.Button(f2, text='Register', command=lambda: raise_frame(f1)).pack()

# -----------------------------Success Screen--------------------------

tk.Label(f3, text="Welcome "+user).pack()
tk.Label(f3, text="You have been successfully logged in").pack()


tk.Button(f3, text='Logout', command=lambda: raise_frame(f1)).pack()


# -----------------------------Warning Screen--------------------------

tk.Label(f4, text="Warning").pack()
tk.Label(f4, text="Wrong Password").pack()

tk.Button(f4, text='Register', command=lambda: raise_frame(f1)).pack()
tk.Button(f4, text='Quit', command=master.quit).pack()


# -------------------------Not registered screen----------------------

tk.Label(f5, text="No such user").pack()
tk.Label(f5, text="Register to continue").pack()


tk.Button(f5, text='Register', command=lambda: raise_frame(f1)).pack()
tk.Button(f5, text='Quit', command=lambda: raise_frame(f1)).pack()

# -------------------------Weak password screen-----------------------

tk.Label(f6, text="Weak password").pack()
tk.Label(f6, text="Please choose another password").pack()


tk.Button(f6, text='Register', command=lambda: raise_frame(f1)).pack()
tk.Button(f6, text='Quit', command=lambda: raise_frame(f1)).pack()

# ------------------------Attempt to break in ---------------------------

tk.Label(f7, text="Honeyword detected").pack()

tk.Button(f7, text='Quit', command=lambda: raise_frame(f1)).pack()
tk.Button(f7, text='Register', command=lambda: raise_frame(f1)).pack()


raise_frame(f1)
master.mainloop()
