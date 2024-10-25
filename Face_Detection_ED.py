import os
import cv2
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from PIL import Image, ImageTk
from cryptography.fernet import Fernet
import base64
import hashlib

# Function to generate a key based on a passkey
def generate_key(passkey):
    hashed_passkey = hashlib.sha256(passkey.encode()).digest()
    return base64.urlsafe_b64encode(hashed_passkey)

# Function to encrypt a file
def encrypt_file(file_path, passkey):
    key = generate_key(passkey)
    cipher = Fernet(key)
    
    with open(file_path, 'rb') as file:
        original = file.read()
    encrypted = cipher.encrypt(original)
    
    with open(file_path, 'wb') as file:
        file.write(encrypted)

# Function to decrypt a file
def decrypt_file(file_path, passkey):
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

class FaceFileApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face File Encryption App")

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()

        self.btn_encrypt = tk.Button(master, text="Encrypt Files", command=self.encrypt_files)
        self.btn_encrypt.pack()

        self.btn_decrypt = tk.Button(master, text="Decrypt File", command=self.decrypt_file)
        self.btn_decrypt.config(state=tk.DISABLED)  # Initially disabled
        self.btn_decrypt.pack()

        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        self.update()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, 1.1, 4)

            # If faces are detected, enable the decrypt button
            if len(faces) > 0:
                self.btn_decrypt.config(state=tk.NORMAL)
            else:
                self.btn_decrypt.config(state=tk.DISABLED)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=imgtk, anchor=tk.NW)
            self.master.imgtk = imgtk

        self.master.after(10, self.update)

    def encrypt_files(self):
        file_paths = filedialog.askopenfilenames(title="Select Files to Encrypt")
        if not file_paths:
            return

        passkey = simpledialog.askstring("Passkey", "Enter a passkey for encryption:")
        if not passkey:
            return

        for file_path in file_paths:
            encrypt_file(file_path, passkey)
        messagebox.showinfo("Info", "Selected files have been encrypted.")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select Encrypted File")
        if not file_path:
            return

        passkey = simpledialog.askstring("Passkey", "Enter passkey to decrypt:")
        if not passkey:
            return

        decrypted_file_path = decrypt_file(file_path, passkey)
        if decrypted_file_path:
            messagebox.showinfo("Info", f"File decrypted successfully: {decrypted_file_path}")
        else:
            messagebox.showerror("Error", "Invalid passkey. Unable to decrypt the file.")

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceFileApp(root)
    root.mainloop()
