import os
from tkinter import Tk, Label, Button, filedialog, StringVar
from cryptography.fernet import Fernet

# Function to generate a key and save it
def generate_key():
    key = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Function to load the key
def load_key():
    return open("secret.key", "rb").read()

# Function to encrypt a file
def encrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        original_file = file.read()

    encrypted_file = fernet.encrypt(original_file)

    encrypted_file_path = file_path + ".encrypted"
    with open(encrypted_file_path, "wb") as file:
        file.write(encrypted_file)

    # Delete the original file
    os.remove(file_path)
    return encrypted_file_path

# Function to decrypt a file
def decrypt_file(file_path):
    key = load_key()
    fernet = Fernet(key)

    with open(file_path, "rb") as file:
        encrypted_file = file.read()

    decrypted_file = fernet.decrypt(encrypted_file)

    decrypted_file_path = file_path.replace(".encrypted", "")
    with open(decrypted_file_path, "wb") as file:
        file.write(decrypted_file)

    # Delete the encrypted file
    os.remove(file_path)
    return decrypted_file_path

# Function to handle file selection and encryption
def select_file_encrypt():
    file_path = filedialog.askopenfilename()
    if file_path:
        encrypted_file_path = encrypt_file(file_path)
        result.set(f"File encrypted: {encrypted_file_path}")

# Function to handle file selection and decryption
def select_file_decrypt():
    file_path = filedialog.askopenfilename()
    if file_path:
        decrypted_file_path = decrypt_file(file_path)
        result.set(f"File decrypted: {decrypted_file_path}")

# Generate a key if it doesn't exist
if not os.path.exists("secret.key"):
    generate_key()

# Create the main Tkinter window
root = Tk()
root.title("File Encryptor/Decryptor")

result = StringVar()
result_label = Label(root, textvariable=result)
result_label.pack(pady=10)

encrypt_button = Button(root, text="Encrypt File", command=select_file_encrypt)
encrypt_button.pack(pady=10)

decrypt_button = Button(root, text="Decrypt File", command=select_file_decrypt)
decrypt_button.pack(pady=10)

# Run the application
root.mainloop()
