import tkinter as tk
import os
from ezpassword import check, newpass
from eztxt import read, readlines, appendn, append, write, delete
from ezlog import log
from ezcrypt import encrypt, decrypt
from pyperclip import copy

def get_pass_names():
    try:
        passwords = readlines(os.path.join("resources", "passwords"))
    except FileNotFoundError:
        log("Password file not found.")
        unlock_label.config(text="Error: Password file not found.")
        frame.after(1000, lambda: unlock_label.config(text="Enter your master password to unlock:"))
        passwords = []
    return passwords

def unlock():
    global user_master_password
    user_master_password = password_entry_box.get()
    known_correct_hash = read(os.path.join("resources", "password"))

    all_password_names = get_pass_names()

    if check(user_master_password, known_correct_hash):
        log("User has entered the correct password. Enabling widgets...")

        password_entry_button.config(text="Lock", command=lock)

        password_display_box.place(x=295, y=50)
        password_display_box.insert('1.0', "\n".join(password.split(": ")[0] for password in all_password_names))

        password_list_label.place(x=295, y=30)
        which_pass_box.place(x=10, y=74)
        which_pass_label.place(x=5, y=50)
        view_pass_button.place(x=10, y=100)
        new_pass_button.place(x=75, y=100)
        unlock_label.config(text="Press 'lock' to lock.")
        log("Widgets have all been enabled.")
    else:
        log("User entered an incorrect password.")
        unlock_label.config(text="Incorrect password.")
        frame.after(1000, lambda: unlock_label.config(text="Enter your master password to unlock:"))

def lock():
    log("Lock button pressed. Disabling widgets...")
    reset()
    password_entry_button.config(text="Unlock", command=unlock)
    password_display_box.delete('1.0', tk.END)
    password_display_box.place_forget()
    password_list_label.place_forget()
    which_pass_box.place_forget()
    which_pass_label.place_forget()
    view_pass_button.place_forget()
    new_pass_button.place_forget()
    show_label.place_forget()
    copy_button.place_forget()
    unlock_label.config(text="Enter your master password to unlock.")
    log("All widgets have been disabled.")

def view_pass():
    log("View password button pressed. Finding and decrypting password...")
    global decrypted_pass
    current_password = which_pass_box.get()
    all_password_name_list = [password.split(": ")[0] for password in get_pass_names()]
    if current_password in all_password_name_list:
        log("Password found. Decrypting...")
        try:
            decrypted_pass = decrypt(get_pass_names()[all_password_name_list.index(current_password)].split(": ")[1], user_master_password)
            log("Password decrypted. Updating label...")
            decrypted_pass_short = decrypted_pass[:12] + "..." if len(decrypted_pass) > 12 else decrypted_pass
            show_label.config(text=decrypted_pass_short)
            show_label.place(x=5, y=134)
            log("Label updated.")
            copy_button.place(x=96, y=130)
        except Exception as e:
            log(f"Error while decrypting password: {e}")
            unlock_label.config(text="Error: Failed to decrypt password.")
            frame.after(1000, lambda: unlock_label.config(text="Press 'lock' to lock."))
    else:
        log("Password not found.")
        unlock_label.config(text="Error: Password not found.")
        frame.after(1000, lambda: unlock_label.config(text="Press 'lock' to lock."))

def new_pass():
    log("Edit or create password button pressed. Asking for new password...")
    new_pass_label.place(x=3, y=128)
    new_pass_entry.place(x=8, y=150)
    new_pass_button2.place(x=8, y=170)

def create_pass(current_password):
    try:
        new_password = new_pass_entry.get()
        appendn(current_dir + "\\resources\\passwords", f"{current_password}: {encrypt(new_password, user_master_password)}")
        log(f"New password {current_password} created.")
        new_pass_label.config(text="Password Created!")
        frame.after(2000, reset())
    except Exception as e:
        log(f"Error while encrypting password: {e}")
        unlock_label.config(text="Error: Failed to encrypt password.")
        frame.after(1000, lambda: unlock_label.config(text="Press 'lock' to lock."))

def pass_chooser():
    log("Password Creating...")
    current_password = which_pass_box.get()
    all_password_name_list = [password.split(": ")[0] for password in get_pass_names()]
    if current_password not in all_password_name_list:
        create_pass(current_password)
    else:
        log("Password already exists. Updating instead...")
        file_path = os.path.join('resources', 'passwords')
        lines = readlines(file_path)
        open(file_path, "w").close()
        for line in lines:
            if current_password not in line.strip("\n"):
                append(file_path, line)
        create_pass(current_password)

def reset():
    log("Resetting...")
    show_label.place_forget()
    copy_button.place_forget()
    which_pass_box.delete('0', 'end')
    new_pass_entry.delete('0', 'end')
    new_pass_entry.place_forget()
    new_pass_label.config(text="Enter the password for that:")
    new_pass_label.place_forget()
    new_pass_button2.place_forget()
    frame.update()
    log("Window reset.")

def copy_password():
    log("Copy button pressed. Copying to clipboard...")
    try:
        copy(decrypted_pass)
        log("Copied.")
        unlock_label.config(text="Password copied to clipboard.")
    except Exception as e:
        log(f"Error while copying password: {e}")
        unlock_label.config(text="Error: Failed to copy password. Please try again.")
        frame.after(1000, lambda: unlock_label.config(text="Press 'lock' to lock."))

#Setup on top
def setupontop():
    setup_window.attributes('-topmost', True)
    setup_window.update()
    setup_window.attributes('-topmost', False)

#Sets up the program
def setup():
    log("No/New password detected. Running setup...")
    global setup_window, password_setup_old
    setup_window = tk.Toplevel(frame)
    setup_window.title("Password Manager - Setup")
    setup_window.geometry('400x100')
    setupontop()
    log("Setup window placed.")

    password_setup_label = tk.Label(setup_window, text = "Please enter a new master password.")
    password_setup_label.pack()

    global password_setup_entry
    password_setup_entry = tk.Entry(setup_window)
    password_setup_entry.pack()

    if read(os.path.join("resources", "passwords")) == "NotSetup":
        log("No password detected. Showing setup_submit button.")
        password_setup_button = tk.Button(setup_window, text = "Submit", command = setup_submit)
    else:
        log("Password change detected. Showing change_submit button and field for old password.")
        password_setup_old = tk.Entry(setup_window)
        password_setup_button = tk.Button(setup_window, text = "Submit", command = change_submit)
        password_setup_old.pack()
    password_setup_button.pack()

def new_password_create():
    log("User confirmed new password. Writing...")
    write(os.path.join("resources", "password"), newpass(password_setup_entry.get()))
    setup_confirm.destroy()
    setup_window.destroy()


def setup_no():
    log("User cancelled password change.")
    frame.lift(setup_window)
    setup_confirm.destroy()
    setupontop()


def common_submit():
    global setup_confirm
    setup_confirm=tk.Toplevel(frame)
    setup_confirm.title("Password Manager - confirm")
    setup_confirm.geometry('300x60')
    setup_confirm.attributes('-topmost', True)
    setup_confirm.update()
    setup_confirm.attributes('-topmost', False)

    password_confirm_label = tk.Label(setup_confirm, text = f"Do you want to set your password to {password_setup_entry.get()}?")
    password_confirm_label.pack()

def setup_submit():
    log("New password submitted. Opening confirmation box...")
    common_submit()
    password_confirm_yes = tk.Button(setup_confirm, text = "Confirm", command = new_password_create)
    password_confirm_yes.place(x=60, y=30)
    password_confirm_no = tk.Button(setup_confirm, text = "Go Back", command = setup_no)
    password_confirm_no.place(x=170, y=30)

def change_submit():
    log("New password sumbitted. Opening change confirmation box...")
    if check(password_setup_old.get(), read(os.path.join("resources", "password"))):
        common_submit()
        password_confirm_yes = tk.Button(setup_confirm, text = "Confirm", command = password_change)
        password_confirm_yes.place(x=60, y=30)
        password_confirm_no = tk.Button(setup_confirm, text = "Go Back", command = setup_no)
        password_confirm_no.place(x=170, y=30)
    else:
        print("Password is no. ")

def password_change():
    log("User changed their password. De and re-encrypting passwords...")
    write(os.path.join("resources", "password"), newpass(password_setup_entry.get()))
    encrypted_list = []
    all_password_name_list = [password.split(": ")[0] for password in get_pass_names()]
    write(os.path.join("resources", "passwords"), "")
    for current_password in all_password_name_list:
        try:
            appendn(os.path.join("resources", "passwords"), current_password + ": " + encrypt(decrypt(get_pass_names()[all_password_name_list.index(current_password)].split(": ")[1].removesuffix("\n"), password_setup_old.get()).translate(str.maketrans('', '', '\x0f\x08')), password_setup_entry.get()))
        except IndexError:
            pass


def main():
    global frame, current_dir, password_entry_box, password_entry_button, password_display_box, password_list_label, which_pass_box, which_pass_label, view_pass_button, new_pass_button, unlock_label, show_label, copy_button, new_pass_entry, new_pass_button2, new_pass_label

    log("Program has been started.")
    log(f"System type is {os.name}.")
    current_dir = os.getcwd()
    log(f"current_dir is {current_dir}.")

    frame = tk.Tk()
    frame.title("Password Manager")
    frame.geometry('420x200')
    log("Tkinter initialised.")

    if read(os.path.join("resources", "password")) == "NotSetup":
        setup()


    unlock_label = tk.Label(frame, text="Enter your master password to unlock:")
    unlock_label.place(x=5, y=0)

    password_entry_box = tk.Entry(frame, show="*")
    password_entry_box.place(x=10, y=24)

    password_entry_button = tk.Button(frame, text="Unlock", command=unlock)
    password_entry_button.place(x=100, y=20)

    password_display_box = tk.Text(frame, width=14, height=8)
    password_list_label = tk.Label(frame, text="Passwords Available:")

    which_pass_box = tk.Entry(frame)
    which_pass_label = tk.Label(frame, text="Enter a password's name:")

    show_label = tk.Label(frame, text="")

    copy_button = tk.Button(frame, text="Copy", command=copy_password)
    view_pass_button = tk.Button(frame, text="View", command=view_pass)
    new_pass_button = tk.Button(frame, text="New/Edit", command=new_pass)
    new_pass_entry = tk.Entry(frame)
    new_pass_button2 = tk.Button(frame, text="Create", command=pass_chooser)
    new_pass_label = tk.Label(frame, text="Enter the password for that:")

    frame.mainloop()

if __name__ == "__main__":
    main()