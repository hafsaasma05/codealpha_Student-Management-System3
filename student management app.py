import csv
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

DATA_FILE = Path(__file__).with_name("students.csv")
FIELDS = ["Roll No", "Name", "Department"]

class StudentApp:
    def __init__(self, root):
        self.root = root
        root.title("Student Management System")
        root.geometry("700x470")
        root.resizable(False, False)
        tk.Label(root, text="STUDENT MANAGEMENT SYSTEM",
                 font=("Arial", 18, "bold")).pack(pady=12)

        form = tk.Frame(root)
        form.pack(pady=8)
        self.entries = {}
        for col, field in enumerate(FIELDS):
            tk.Label(form, text=field).grid(row=0, column=col, padx=8)
            entry = tk.Entry(form, width=22)
            entry.grid(row=1, column=col, padx=8, pady=5)
            self.entries[field] = entry

        buttons = tk.Frame(root)
        buttons.pack(pady=8)
        tk.Button(buttons, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        tk.Button(buttons, text="Update Selected", command=self.update_student).pack(side="left", padx=5)
        tk.Button(buttons, text="Delete Selected", command=self.delete_student).pack(side="left", padx=5)
        tk.Button(buttons, text="Clear", command=self.clear_fields).pack(side="left", padx=5)

        self.table = ttk.Treeview(root, columns=FIELDS, show="headings", height=12)
        for field in FIELDS:
            self.table.heading(field, text=field)
            self.table.column(field, width=210, anchor="center")
        self.table.pack(padx=15, pady=12, fill="x")
        self.table.bind("<<TreeviewSelect>>", self.select_row)
        self.load_students()

    def get_values(self):
        return [self.entries[f].get().strip() for f in FIELDS]

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.table.selection_remove(self.table.selection())

    def load_students(self):
        for item in self.table.get_children():
            self.table.delete(item)
        if DATA_FILE.exists():
            with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
                for row in csv.DictReader(file):
                    self.table.insert("", "end", values=[row.get(f, "") for f in FIELDS])

    def save_students(self):
        with DATA_FILE.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=FIELDS)
            writer.writeheader()
            for item in self.table.get_children():
                writer.writerow(dict(zip(FIELDS, self.table.item(item, "values"))))

    def add_student(self):
        values = self.get_values()
        if not all(values):
            messagebox.showwarning("Missing data", "Please fill in all fields.")
            return
        if any(self.table.item(i, "values")[0] == values[0] for i in self.table.get_children()):
            messagebox.showerror("Duplicate roll number", "This roll number already exists.")
            return
        self.table.insert("", "end", values=values)
        self.save_students()
        self.clear_fields()

    def select_row(self, _event=None):
        selected = self.table.selection()
        if selected:
            for field, value in zip(FIELDS, self.table.item(selected[0], "values")):
                self.entries[field].delete(0, tk.END)
                self.entries[field].insert(0, value)

    def update_student(self):
        selected = self.table.selection()
        values = self.get_values()
        if not selected:
            messagebox.showwarning("Select a student", "Select a row to update.")
            return
        if not all(values):
            messagebox.showwarning("Missing data", "Please fill in all fields.")
            return
        self.table.item(selected[0], values=values)
        self.save_students()
        self.clear_fields()

    def delete_student(self):
        selected = self.table.selection()
        if not selected:
            messagebox.showwarning("Select a student", "Select a row to delete.")
            return
        self.table.delete(selected[0])
        self.save_students()
        self.clear_fields()

if __name__ == "__main__":
    root = tk.Tk()
    StudentApp(root)
    root.mainloop()
