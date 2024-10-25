import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import numpy as np
from PIL import Image, ImageTk


# Load known faces
known_face_encodings = []
known_face_names = []

def load_known_faces():
    # Load your images and their corresponding names here
    # Example:
    image = face_recognition.load_image_file("known_person.jpg")
    encoding = face_recognition.face_encodings(image)[0]
    known_face_encodings.append(encoding)
    known_face_names.append("Known Person")

# Initialize known faces
load_known_faces()

class FaceRecognitionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Recognition App")
        
        self.video_source = 0  # Use 0 for the default camera
        self.vid = cv2.VideoCapture(self.video_source)
        
        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()

        self.btn_recognize = tk.Button(master, text="Start Recognition", command=self.start_recognition)
        self.btn_recognize.pack()

        self.update()
        
    def update(self):
        ret, frame = self.vid.read()
        if ret:
            # Convert the image from BGR to RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # Detect faces and encodings
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Compare to known faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
                
                # If a match was found, use the first one
                if True in matches:
                    first_match_index = matches.index(True)
                    name = known_face_names[first_match_index]
                
                # Draw rectangle around the face
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
                
            # Convert the frame to an image for Tkinter
            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=imgtk, anchor=tk.NW)
            self.master.imgtk = imgtk  # Keep a reference to avoid garbage collection
        
        self.master.after(10, self.update)  # Refresh every 10 ms

    def start_recognition(self):
        messagebox.showinfo("Info", "Face recognition started!")

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceRecognitionApp(root)
    root.mainloop()
