import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

class FaceDetectionApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Face Detection App")
        
        self.video_source = 0  # Use 0 for the default camera
        self.vid = cv2.VideoCapture(self.video_source)
        
        self.canvas = tk.Canvas(master, width=640, height=480)
        self.canvas.pack()

        self.update()
        
    def update(self):
        ret, frame = self.vid.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            faces = face_cascade.detectMultiScale(gray, 1.1, 4)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)
            self.canvas.create_image(0, 0, image=imgtk, anchor=tk.NW)
            self.master.imgtk = imgtk

        self.master.after(10, self.update)  # Refresh every 10 ms

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create the main application window
if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetectionApp(root)
    root.mainloop()
