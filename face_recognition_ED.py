import os
import cv2
import face_recognition
import numpy as np
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

# Load known faces
known_face_encodings = []
known_face_names = []

def load_known_faces():
    image = cv2.imread("known_person.jpg")  # Replace with your known face image
    encoding = face_recognition.face_encodings(face_recognition.load_image_file("known_person.jpg"))[0]
    known_face_encodings.append(encoding)
    known_face_names.append("Known Person")

load_known_faces()

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
        self.btn_decrypt.pack()

        self.update()

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                if True in matches:
                    name = known_face_names[matches.index(True)]
                    # If face matches, enable decrypt button
                    self.btn_decrypt.config(state=tk.NORMAL)
                else:
                    self.btn_decrypt.config(state=tk.DISABLED)

                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

            img = Image.fromarray(frame)
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
