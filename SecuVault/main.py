import tkinter as tk
from tkinter import simpledialog, messagebox
from cryptography.fernet import Fernet
import webbrowser

# Create or load the encryption key
try:
    with open("key.key", "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

cipher_suite = Fernet(key)

def add_password():
    password = simpledialog.askstring("Add Password", "Enter the password:")
    encrypted_password = cipher_suite.encrypt(password.encode()).decode()
    with open("passwords.txt", "ab") as file:
        file.write(encrypted_password.encode() + b'\n')
    password_list.insert(tk.END, encrypted_password)

def delete_password():
    selected_item = password_list.curselection()
    if selected_item:
        index = selected_item[0]
        password_list.delete(index)
        update_passwords_file()

def decrypt_password():
    selected_item = password_list.curselection()
    if selected_item:
        index = selected_item[0]
        encrypted_password = password_list.get(index)
        decrypted_password = cipher_suite.decrypt(encrypted_password.encode()).decode()
        messagebox.showinfo("Decrypted Password", decrypted_password)

def rickroll():
    webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ")

def update_passwords_file():
    with open("passwords.txt", "wb") as file:
        for index in range(password_list.size()):
            encrypted_password = password_list.get(index)
            file.write(encrypted_password.encode() + b'\n')

# Create the main window
root = tk.Tk()
root.title("SecuVault")
root.geometry("400x300")  # Window size

# Application icon
root.iconbitmap("icon.ico")

# Buttons
add_button = tk.Button(root, text="Add Password", command=add_password)
delete_button = tk.Button(root, text="Delete Password", command=delete_password)
decrypt_button = tk.Button(root, text="Decrypt Password", command=decrypt_password)
rickroll_button = tk.Button(root, text="Not Rickroll", command=rickroll)

# Password list
password_list = tk.Listbox(root)

# Read and decrypt saved passwords
with open("passwords.txt", "rb") as file:
    for line in file:
        encrypted_password = line.decode()
        password_list.insert(tk.END, encrypted_password)

# Arrange elements on the form
add_button.pack()
delete_button.pack()
decrypt_button.pack()
rickroll_button.pack()
password_list.pack()

root.mainloop()
