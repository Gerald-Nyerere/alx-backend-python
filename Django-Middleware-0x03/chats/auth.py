import os

file_path = "chats/auth.py"

if os.path.exists(file_path):
    if os.path.getsize(file_path) > 0:
        print(f"{file_path} exists and is not empty.")
    else:
        print(f"{file_path} exists but is empty.")
else:
    print(f"{file_path} does not exist.")
