import cv2
import os
import mysql.connector
from datetime import datetime
from skimage.metrics import structural_similarity as ssim
import numpy as np
from tkinter import Tk, Label, Entry, Button, messagebox
from database import connect_db

def mark_attendance(card_id, name):
    db = connect_db()
    cursor = db.cursor()
    now = datetime.now()
    date = now.date()
    time = now.time()
    cursor.execute("INSERT INTO attendance (card_id, name, date, time) VALUES (%s, %s, %s, %s)", (card_id, name, date, time))
    db.commit()
    db.close()
    messagebox.showinfo("Attendance", f"Attendance marked for {name}")

def compare_faces(img1, img2):
    img1 = cv2.resize(img1, (100, 100))
    img2 = cv2.resize(img2, (100, 100))
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    return ssim(img1, img2)

def recognize(card_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, image_path FROM users WHERE card_id = %s", (card_id,))
    result = cursor.fetchone()
    db.close()

    if not result:
        messagebox.showerror("Error", "Card ID not found!")
        return

    name, stored_path = result
    if not os.path.exists(stored_path):
        messagebox.showerror("Error", "Stored face image not found.")
        return

    stored_face = cv2.imread(stored_path)
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            detected_face = frame[y:y+h, x:x+w]
            similarity = compare_faces(detected_face, stored_face)

            if similarity > 0.7:
                mark_attendance(card_id, name)
                cam.release()
                cv2.destroyAllWindows()
                return
            else:
                cv2.putText(frame, "Face Not Match", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow("Face Verification", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()
    messagebox.showwarning("Failed", "No matching face found!")

def attendance_gui():
    root = Tk()
    root.title("Mark Attendance")
    root.geometry("350x250")

    Label(root, text="Enter ID Card Number:", font=("Arial", 12)).pack(pady=10)
    card_entry = Entry(root, font=("Arial", 12))
    card_entry.pack()

    def submit():
        card_id = card_entry.get().strip()
        if card_id:
            recognize(card_id)
        else:
            messagebox.showerror("Error", "Please enter ID card number")

    Button(root, text="Verify Face & Mark", font=("Arial", 12), bg="blue", fg="white", command=submit).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":

    attendance_gui()