import tkinter as tk
from tkinter import messagebox
import csv
import os

# -------------------------------------------------------
#  CSV FILE PATH (Always saves beside this Python script)
# -------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(BASE_DIR, "students.csv")


# -------------------------------------------------------
# CSV HELPERS
# -------------------------------------------------------
def load_students():
    """Load students from CSV file."""
    if not os.path.exists(FILE_PATH):
        return []
    with open(FILE_PATH, newline='', encoding='utf-8') as f:
        return list(csv.reader(f))


def save_students(students):
    """Save student list to CSV file."""
    try:
        with open(FILE_PATH, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerows(students)
        print(f"[DEBUG] Data saved: {len(students)} records to {FILE_PATH}")
        print(f"[DEBUG] Current students: {students}")
    except Exception as e:
        print(f"[ERROR] {e}")
        messagebox.showerror("Error", f"Failed to save data: {e}")


def refresh_listbox():
    """Refresh the listbox display."""
    listbox.delete(0, tk.END)
    for s in students:
        listbox.insert(tk.END, f"{s[0]} | {s[1]} | {s[2]} | {s[3]}")


# -------------------------------------------------------
# MAIN FUNCTIONS
# -------------------------------------------------------
def clear_fields():
    print("[DEBUG] New Entry clicked - clearing fields")
    name_var.set("")
    class_var.set("")
    grade_var.set("")
    marks_var.set("")


def add_student():
    name = name_var.get().strip()
    cls = class_var.get().strip()
    grade = grade_var.get().strip()
    marks = marks_var.get().strip()

    if not (name and cls and grade and marks):
        messagebox.showerror("Error", "Please fill all fields")
        return

    # Add to list
    students.append([name, cls, grade, marks])
    save_students(students)
    refresh_listbox()
    clear_fields()
    messagebox.showinfo("Success", "Student Added!")


def update_student():
    name = name_var.get().strip()
    cls = class_var.get().strip()
    grade = grade_var.get().strip()
    marks = marks_var.get().strip()

    print(f"[DEBUG] Update clicked - name: {name}, class: {cls}, grade: {grade}, marks: {marks}")

    if not name:
        messagebox.showerror("Error", "Enter student name!")
        return

    # Check if student exists
    found = False
    for s in students:
        if s[0] == name:
            print(f"[DEBUG] Found student: {s}, updating...")
            s[1] = cls
            s[2] = grade
            s[3] = marks
            found = True
            break

    if found:
        save_students(students)
        refresh_listbox()
        clear_fields()
        messagebox.showinfo("Updated", "Student Updated!")
    else:
        # Add as new student if not found
        print(f"[DEBUG] Student not found, adding as new...")
        students.append([name, cls, grade, marks])
        save_students(students)
        refresh_listbox()
        clear_fields()
        messagebox.showinfo("Added", "New Student Added!")


def delete_student():
    name = name_var.get().strip()

    for s in students:
        if s[0] == name:
            students.remove(s)
            save_students(students)
            refresh_listbox()
            clear_fields()
            messagebox.showinfo("Deleted", "Student Removed!")
            return

    messagebox.showerror("Error", "Student not found!")


def load_selected(event):
    """Load selected listbox item into entries."""
    try:
        index = listbox.curselection()[0]
        s = students[index]
        name_var.set(s[0])
        class_var.set(s[1])
        grade_var.set(s[2])
        marks_var.set(s[3])
    except:
        pass


# -------------------------------------------------------
# UI SETUP
# -------------------------------------------------------
root = tk.Tk()
root.title("Student Management System")
root.geometry("450x550")

tk.Label(root, text="Student Management System", font=("Arial", 16, "bold")).pack(pady=10)

# Variables
name_var = tk.StringVar()
class_var = tk.StringVar()
grade_var = tk.StringVar()
marks_var = tk.StringVar()

fields = [
    ("Name", name_var),
    ("Class", class_var),
    ("Grade", grade_var),
    ("Marks", marks_var)
]

# Input boxes
for label, var in fields:
    tk.Label(root, text=label).pack()
    tk.Entry(root, textvariable=var, width=35).pack(pady=3)


# Buttons
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Button(frame, text="New Entry", width=10, command=clear_fields).grid(row=0, column=0, padx=5)
tk.Button(frame, text="Update", width=10, command=update_student).grid(row=0, column=1, padx=5)
tk.Button(frame, text="Delete", width=10, command=delete_student).grid(row=0, column=2, padx=5)


# Listbox
tk.Label(root, text="Students List:", font=("Arial", 12, "bold")).pack(pady=5)
listbox = tk.Listbox(root, width=55, height=12)
listbox.pack()
listbox.bind("<<ListboxSelect>>", load_selected)

# Quit button
tk.Button(root, text="Quit", width=12, command=root.quit).pack(pady=10)

# Load CSV data
students = load_students()
refresh_listbox()

root.mainloop()
