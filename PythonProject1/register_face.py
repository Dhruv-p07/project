import cv2
import os
import mysql.connector
from tkinter import Tk, Label, Entry, Button, messagebox, StringVar, OptionMenu
from database import connect_db

def user_exists(card_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE card_id = %s", (card_id,))
    exists = cursor.fetchone()[0] > 0
    db.close()
    return exists

def save_to_db(name, card_id, image_path, role):
    if user_exists(card_id):
        messagebox.showwarning("Warning", "ID card already registered.")
        return
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (name, card_id, image_path, role) VALUES (%s, %s, %s, %s)", (name, card_id, image_path, role))
    db.commit()
    db.close()

def capture_face(name, card_id, role):
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    while True:
        ret, frame = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            face_img = frame[y:y+h, x:x+w]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

            folder = "faces"
            os.makedirs(folder, exist_ok=True)
            image_path = os.path.join(folder, f"{card_id}.jpg")
            cv2.imwrite(image_path, face_img)

            save_to_db(name, card_id, image_path, role)
            messagebox.showinfo("Success", f"{role.capitalize()} Registered: {name}")
            cam.release()
            cv2.destroyAllWindows()
            return

        cv2.imshow("Register Face", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cam.release()
    cv2.destroyAllWindows()

def register_gui():
    root = Tk()
    root.title("Register Face")
    root.geometry("350x400")

    Label(root, text="Enter Name:", font=("Arial", 12)).pack(pady=5)
    name_entry = Entry(root, font=("Arial", 12))
    name_entry.pack()

    Label(root, text="Enter ID Card Number:", font=("Arial", 12)).pack(pady=5)
    card_entry = Entry(root, font=("Arial", 12))
    card_entry.pack()

    Label(root, text="Select Role:", font=("Arial", 12)).pack(pady=5)
    role_var = StringVar()
    role_var.set("student")
    OptionMenu(root, role_var, "student", "faculty").pack()

    def submit():
        name = name_entry.get().strip()
        card_id = card_entry.get().strip()
        role = role_var.get()
        if name and card_id:
            capture_face(name, card_id, role)
        else:
            messagebox.showerror("Error", "Please enter all details")

    Button(root, text="Capture Face", font=("Arial", 12), bg="green", fg="white", command=submit).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":

    register_gui()