import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector


# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="7777",
        database="face_detection_db"
    )


# Check if the card_id exists and return the role
def check_login(card_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT name, role FROM users WHERE card_id = %s", (card_id,))
    result = cursor.fetchone()
    db.close()

    if result:
        return result  # Return name and role if found
    else:
        return None


# Fetch attendance for a student
def fetch_student_attendance(card_id):
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT date, time FROM attendance WHERE card_id = %s", (card_id,))
    results = cursor.fetchall()
    db.close()
    return results


# Fetch all student attendance for a faculty
def fetch_all_attendance():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT card_id, name, date, time FROM attendance")
    results = cursor.fetchall()
    db.close()
    return results


# Function for student dashboard (view own attendance)
def student_dashboard(card_id, name):
    # Fetch student's attendance
    attendance = fetch_student_attendance(card_id)

    if attendance:
        # Create a new window to display attendance
        attendance_window = tk.Toplevel()
        attendance_window.title(f"{name}'s Attendance")
        attendance_window.geometry("400x300")

        tk.Label(attendance_window, text=f"Attendance for {name}", font=("Arial", 14)).pack(pady=10)

        # Create a table to display attendance
        table = ttk.Treeview(attendance_window, columns=("Date", "Time"), show="headings")
        table.heading("Date", text="Date")
        table.heading("Time", text="Time")
        table.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        for row in attendance:
            table.insert("", "end", values=row)

        attendance_window.mainloop()
    else:
        messagebox.showinfo("No Attendance", "No attendance records found.")


# Function for faculty dashboard (view all student attendance)
def faculty_dashboard(card_id, name):
    # Fetch all student attendance
    attendance = fetch_all_attendance()

    if attendance:
        # Create a new window to display all attendance records
        attendance_window = tk.Toplevel()
        attendance_window.title(f"{name}'s Faculty Dashboard")
        attendance_window.geometry("600x400")

        tk.Label(attendance_window, text=f"All Students' Attendance", font=("Arial", 14)).pack(pady=10)

        # Create a table to display all attendance
        table = ttk.Treeview(attendance_window, columns=("Card ID", "Name", "Date", "Time"), show="headings")
        table.heading("Card ID", text="Card ID")
        table.heading("Name", text="Name")
        table.heading("Date", text="Date")
        table.heading("Time", text="Time")
        table.pack(padx=20, pady=10, fill=tk.BOTH, expand=True)

        for row in attendance:
            table.insert("", "end", values=row)

        attendance_window.mainloop()
    else:
        messagebox.showinfo("No Attendance", "No attendance records found.")


# Login function
def login(card_id):
    user_info = check_login(card_id)
    if user_info:
        name, role = user_info
        if role == "student":
            student_dashboard(card_id, name)
        elif role == "faculty":
            faculty_dashboard(card_id, name)
    else:
        messagebox.showerror("Error", "Card ID not found!")


# GUI to handle login
def login_gui():
    root = tk.Tk()
    root.title("Login")
    root.geometry("350x250")

    tk.Label(root, text="Enter Card ID:", font=("Arial", 12)).pack(pady=20)
    card_entry = tk.Entry(root, font=("Arial", 12))
    card_entry.pack()

    def submit():
        card_id = card_entry.get().strip()
        if card_id:
            login(card_id)
        else:
            messagebox.showerror("Error", "Please enter a valid Card ID")

    tk.Button(root, text="Login", font=("Arial", 12), bg="blue", fg="white", command=submit).pack(pady=20)

    root.mainloop()


if __name__ == "__main__":

    login_gui()