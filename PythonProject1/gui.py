import tkinter as tk
import subprocess

def register_face():
    subprocess.run(["python", "register_face.py"])

def recognize_face():
    subprocess.run(["python", "recognize_face.py"])

def login_user():
    subprocess.run(["python", "login.py"])

root = tk.Tk()
root.title("Face Attendance System")
root.geometry("400x350")
root.configure(bg="#f0f0f0")

title = tk.Label(root, text="Face Recognition Attendance", font=("Arial", 16, "bold"), bg="#f0f0f0")
title.pack(pady=20)

tk.Button(root, text="Register Face (Student/Faculty)", font=("Arial", 12), width=30, height=2, bg="#4caf50", fg="white", command=register_face).pack(pady=10)

tk.Button(root, text="Mark Attendance (Face Verify)", font=("Arial", 12), width=30, height=2, bg="#2196f3", fg="white", command=recognize_face).pack(pady=10)

tk.Button(root, text="Login (View Attendance)", font=("Arial", 12), width=30, height=2, bg="#ff9800", fg="white", command=login_user).pack(pady=10)

root.mainloop()