from ezpassword import newpass
from eztxt import write
from ezlog import log
import os

password = input("Please enter a password:\n")

hashed = newpass(password)

log(f"Setting up with password {password}, hash {hashed}.")

if os.name == "nt":
    write("resources\\password", hashed)
else:
    write("resources/password", hashed)