import os
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(passkey):
    """Generate a Fernet key based on the provided passkey."""
    # Create a SHA-256 hash of the passkey
    hashed_passkey = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed_passkey)

def encrypt_file(file_path, passkey):
    """Encrypt the file at the given path using the provided passkey."""
    key = generate_key(passkey)
    cipher = Fernet(key)
    
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = cipher.encrypt(original)
    
    with open(file_path, 'wb') as file:
        file.write(encrypted)

def decrypt_file(file_path, passkey):
    """Decrypt the file at the given path using the provided passkey."""
    key = generate_key(passkey)
    cipher = Fernet(key)
    
    with open(file_path, 'rb') as file:
        encrypted = file.read()
    
    try:
        decrypted = cipher.decrypt(encrypted)
        temp_file_path = f"{file_path}.dec"
        with open(temp_file_path, 'wb') as file:
            file.write(decrypted)
        return temp_file_path
    except Exception:
        return None

def select_files():
    """Select multiple files to encrypt."""
    file_paths = filedialog.askopenfilenames(title="Select Files to Encrypt")
    if not file_paths:
        return
    
    passkey = simpledialog.askstring("Passkey", "Enter a passkey for encryption:")
    if not passkey:
        return
    
    for file_path in file_paths:
        encrypt_file(file_path, passkey)
    messagebox.showinfo("Info", "Selected files have been encrypted.")

def open_file():
    """Open a file and decrypt it for viewing."""
    file_path = filedialog.askopenfilename(title="Select Encrypted File")
    if not file_path:
        return
    
    passkey = simpledialog.askstring("Passkey", "Enter passkey to decrypt:")
    if not passkey:
        return
    
    decrypted_file_path = decrypt_file(file_path, passkey)
    
    if decrypted_file_path:
        with open(decrypted_file_path, 'r') as file:
            content = file.read()
        
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, content)
        
        # Automatically delete the decrypted file after viewing
        os.remove(decrypted_file_path)
    else:
        messagebox.showerror("Error", "Invalid passkey. Unable to decrypt the file.")

# Create the main application window
app = tk.Tk()
app.title("File Encryption/Decryption App")

# Create a text area for displaying file content
text_area = tk.Text(app, wrap='word', height=20, width=50)
text_area.pack(padx=10, pady=10)

# Create buttons for selecting files to encrypt and for opening files
encrypt_button = tk.Button(app, text="Encrypt Files", command=select_files)
encrypt_button.pack(pady=10)

open_button = tk.Button(app, text="Open Encrypted File", command=open_file)
open_button.pack(pady=10)

# Start the Tkinter event loop
app.mainloop()
